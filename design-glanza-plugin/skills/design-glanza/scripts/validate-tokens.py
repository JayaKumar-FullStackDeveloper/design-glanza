"""
validate-tokens.py

Responsibility
--------------
Deterministic, structural checks of a product's design token set
(`product-builder/ui/design-tokens.json`, per
`design-tokens/design-tokens.schema.json`):

- The file exists and is valid JSON.
- Every master-required top-level category is present (color, typography,
  spacing, grid, radius, border, elevation, sizing, breakpoint, motion,
  zIndex) — per `design-tokens/token-schema.md`.
- Every required semantic color token is present (primary, secondary,
  surface, background, text.primary, text.muted, success, warning, error,
  info, neutral) — per `design-tokens/semantic-tokens.md`.
- Theme completeness: where any `themeable: true` token declares a `dark`
  value, every `themeable: true` token must — zero partial theme coverage
  (`design-tokens/theming.md`).
- Inheritance integrity: every top-level key is either a known master
  category, an optional known extension (`secondary`, `dataViz`), or the
  `product.*` namespace — an unrecognized top-level key is flagged as a
  possible unauthorized scale extension (`design-tokens/
  token-inheritance.md`).
- Raw-value scan: `product-builder/ui/*.md` files are scanned for
  pattern-detectable raw values (hex colors, `rgb()`/`rgba()`) with no
  adjacent "Token gap" log entry (`design-tokens/token-audit.md`'s
  justified-exception shape).
- Redundant tokens: two different paths in the same top-level category
  resolving to the exact same value, flagged for a reuse-vs-alias review
  (`design-tokens/token-audit.md`'s Redundant tokens check) — never
  auto-merged.

What this deliberately does NOT check
--------------------------------------
Whether a token is used in the *semantically correct role* on a given
screen (a `warning`-toned value applied to a primary CTA), whether a
logged Token gap's proposed resolution is the right one, or raw values
inside vendored/third-party code Design-Glanza didn't generate — all
judgment calls, `agents/design-system-expert.md`'s job per
`design-tokens/token-audit.md`, not this script's. This script also does
not perform full JSON Schema validation (`design-tokens.schema.json` is
the canonical shape reference for a human/agent to check against; this
script implements the equivalent structural checks directly, dependency-
free, matching every other script in this folder's stdlib-only posture).

Status: implemented.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import _common
from _common import Finding, read_text

# The 12 master-required top-level categories, per
# design-tokens/design-tokens.schema.json's own `required` list.
REQUIRED_CATEGORIES = [
    "color", "typography", "spacing", "grid", "radius", "border",
    "elevation", "sizing", "breakpoint", "motion", "zIndex",
]

# Recognized top-level keys beyond the required categories — extending
# this set means a genuine new master category was added to the schema,
# not a per-product decision (design-tokens/token-inheritance.md).
KNOWN_OPTIONAL_TOP_LEVEL = {"$inherits", "$comment", "product"}

# The 10 required semantic tokens, per design-tokens/semantic-tokens.md.
# 'text' is nested (primary/muted); every other entry is a top-level key
# under color.semantic.
REQUIRED_SEMANTIC_KEYS = [
    "primary", "secondary", "surface", "background", "success", "warning",
    "error", "info", "neutral",
]
REQUIRED_TEXT_SUBKEYS = ["primary", "muted"]

TRIPLET_FIELDS = ["foreground", "background", "border"]

HEX_COLOR_RE = re.compile(r"#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3}([0-9a-fA-F]{2})?)?\b")
RGB_FUNC_RE = re.compile(r"\brgba?\(\s*[\d.]+\s*,\s*[\d.]+\s*,\s*[\d.]+")
TOKEN_GAP_MARKER_RE = re.compile(r"Token gap:", re.IGNORECASE)


def _load_json(path: Path) -> tuple[dict | None, str | None]:
    text = read_text(path)
    if text is None:
        return None, "missing-file"
    try:
        return json.loads(text), None
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON: {exc}"


def _check_top_level(tokens: dict, rel: str) -> list[Finding]:
    findings: list[Finding] = []
    for cat in REQUIRED_CATEGORIES:
        if cat not in tokens:
            findings.append(Finding(
                "Blocker", f"Missing required top-level category '{cat}'",
                rel, "missing-category",
            ))
    known = set(REQUIRED_CATEGORIES) | KNOWN_OPTIONAL_TOP_LEVEL | {"secondary", "dataViz"}
    # 'secondary'/'dataViz' actually live under color.*, not top-level —
    # tolerate them here only if a product genuinely nests differently;
    # the real check is against top-level keys actually present.
    for key in tokens.keys():
        if key not in known and key not in REQUIRED_CATEGORIES:
            findings.append(Finding(
                "Major",
                f"Unrecognized top-level key '{key}' — not a master category, "
                "not a known optional extension, and not under the product.* "
                "namespace; possible unauthorized scale extension",
                rel, "unauthorized-extension",
            ))
    return findings


def _check_semantic_tokens(tokens: dict, rel: str) -> list[Finding]:
    findings: list[Finding] = []
    color = tokens.get("color")
    if not isinstance(color, dict):
        return findings  # already reported as a missing category
    semantic = color.get("semantic")
    if not isinstance(semantic, dict):
        findings.append(Finding(
            "Blocker", "color.semantic is missing or not an object",
            rel, "missing-semantic",
        ))
        return findings
    for key in REQUIRED_SEMANTIC_KEYS:
        if key not in semantic:
            findings.append(Finding(
                "Major", f"Missing required semantic token 'color.semantic.{key}'",
                rel, "missing-semantic-token",
            ))
            continue
        entry = semantic[key]
        if isinstance(entry, dict) and any(f in entry for f in TRIPLET_FIELDS):
            for field in TRIPLET_FIELDS:
                if field not in entry:
                    findings.append(Finding(
                        "Minor",
                        f"color.semantic.{key} is missing its '{field}' triplet field",
                        rel, "incomplete-triplet",
                    ))
    text = semantic.get("text")
    if not isinstance(text, dict):
        findings.append(Finding(
            "Major", "Missing required semantic token group 'color.semantic.text'",
            rel, "missing-semantic-token",
        ))
    else:
        for sub in REQUIRED_TEXT_SUBKEYS:
            if sub not in text:
                findings.append(Finding(
                    "Major", f"Missing required semantic token 'color.semantic.text.{sub}'",
                    rel, "missing-semantic-token",
                ))
    return findings


def _iter_leaf_tokens(node, path=""):
    """Yield (path, token_dict) for every dict that looks like a leaf token
    (has a 'value' key), walking the tree depth-first."""
    if isinstance(node, dict):
        if "value" in node:
            yield path, node
            return
        for k, v in node.items():
            if k.startswith("$"):
                continue
            yield from _iter_leaf_tokens(v, f"{path}.{k}" if path else k)


def _check_theme_completeness(tokens: dict, rel: str) -> list[Finding]:
    findings: list[Finding] = []
    themeable_leaves = [
        (p, t) for p, t in _iter_leaf_tokens(tokens) if t.get("themeable") is True
    ]
    any_dark_declared = any(
        isinstance(t.get("value"), dict) and "dark" in t["value"]
        for _, t in themeable_leaves
    )
    if not any_dark_declared:
        return findings  # this product hasn't opted into dark mode at all
    for path, token in themeable_leaves:
        value = token.get("value")
        if not isinstance(value, dict) or "light" not in value or "dark" not in value:
            findings.append(Finding(
                "Major",
                f"'{path}' is themeable and this product declares dark mode "
                "elsewhere, but it has no complete {light, dark} pair",
                rel, "partial-theme-coverage",
            ))
    return findings


# Categories excluded from the redundant-token check: typography's
# sub-axes (family/weight/lineHeight) are *designed* to repeat the same
# value across multiple size roles (e.g. h2/h3 intentionally sharing
# weight 600; a single-family product intentionally has family.base ==
# family.display, per typography.md's own Font pairing default) — flagging
# that as "redundant" would be noise against the scale's own design, not a
# real duplicate-naming defect. Confirmed empirically: running this check
# against design-tokens/templates/design-tokens.json's own reference
# instance before this exclusion produced 6 pure-noise findings, 0 of them
# real. Every other category (color, spacing, radius, etc.) is a single
# closed scale where each named step is meant to be a distinct value, so a
# collision there is a genuine anomaly worth flagging.
REDUNDANCY_CHECK_EXCLUDED_CATEGORIES = {"typography"}


def _check_redundant_tokens(tokens: dict, rel: str) -> list[Finding]:
    """Flag two different token paths *within the same top-level category*
    that resolve to the exact same value — design-tokens/token-audit.md's
    Redundant tokens check. Scoped per-category (never cross-category, e.g.
    radius.none vs. border.width.none) since a same-value coincidence across
    unrelated categories is meaningless, not a real duplicate name; typography
    is excluded entirely (see the constant above)."""
    findings: list[Finding] = []
    by_category: dict[str, dict] = {}
    for path, token in _iter_leaf_tokens(tokens):
        category = path.split(".", 1)[0]
        if category in REDUNDANCY_CHECK_EXCLUDED_CATEGORIES:
            continue
        value = token.get("value")
        if isinstance(value, dict):
            hashable = tuple(sorted(value.items()))
        elif isinstance(value, list):
            continue  # non-scalar, non-mode value - not comparable this way
        else:
            hashable = value
        by_category.setdefault(category, {}).setdefault(hashable, []).append(path)

    for category, groups in by_category.items():
        for value, paths in groups.items():
            if len(paths) < 2:
                continue
            findings.append(Finding(
                "Minor",
                f"{len(paths)} '{category}' token paths resolve to the same "
                f"value ({value!r}): {', '.join(sorted(paths))} — one should "
                "alias the other rather than two independent names for one value",
                rel, "redundant-token",
            ))
    return findings


def _scan_raw_values(product_builder_dir: Path) -> list[Finding]:
    findings: list[Finding] = []
    ui_dir = product_builder_dir / "ui"
    if not ui_dir.is_dir():
        return findings
    for md_path in sorted(ui_dir.glob("*.md")):
        text = read_text(md_path)
        if text is None:
            continue
        rel = f"ui/{md_path.name}"
        for lineno, line in enumerate(text.splitlines(), start=1):
            if TOKEN_GAP_MARKER_RE.search(line):
                continue  # this line (or the gap block it's part of) is a logged exception
            for match in HEX_COLOR_RE.finditer(line):
                findings.append(Finding(
                    "Minor",
                    f"Raw hex color '{match.group(0)}' with no adjacent Token gap "
                    "log entry",
                    rel, "raw-value",
                ))
            for match in RGB_FUNC_RE.finditer(line):
                findings.append(Finding(
                    "Minor",
                    f"Raw rgb()/rgba() value '{match.group(0)}...' with no adjacent "
                    "Token gap log entry",
                    rel, "raw-value",
                ))
    return findings


def validate(product_builder_dir: Path) -> list[Finding]:
    findings: list[Finding] = []
    tokens_path = product_builder_dir / "ui" / "design-tokens.json"
    rel = "ui/design-tokens.json"

    tokens, err = _load_json(tokens_path)
    if err:
        severity = "Major" if err == "missing-file" else "Blocker"
        findings.append(Finding(severity, f"design-tokens.json {err}", rel, "load-error"))
        return findings

    findings += _check_top_level(tokens, rel)
    findings += _check_semantic_tokens(tokens, rel)
    findings += _check_theme_completeness(tokens, rel)
    findings += _check_redundant_tokens(tokens, rel)
    findings += _scan_raw_values(product_builder_dir)
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("product_builder_dir", help="Path to a product-builder/ directory.")
    args = parser.parse_args(argv)

    findings = validate(Path(args.product_builder_dir))
    if not findings:
        print("validate-tokens: no findings.")
        return 0
    for f in findings:
        print(f)
    return 1 if any(f.severity in ("Blocker", "Major") for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
