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
- Contrast: every declared `{foreground, background}` semantic triplet
  pairing, plus `text.primary`/`text.muted` against `background`/`surface`,
  computed against real WCAG relative-luminance ratios (not eyeballed) in
  both light and dark mode, against `ui-engine/color-system.md`'s stated
  4.5:1/3:1 thresholds (`design-tokens/token-audit.md`'s Contrast validation
  check). Only certifies the pairings actually checked, per that rule's own
  "pairing contract, not a one-time pass" framing — a new color combination
  a later screen improvises is a fresh check, not an assumed pass.
- Contrast (B8.1, semantic/tinted-background pairing): every declared
  `{onSoft, soft}` pair — the optional, additive extension to the semantic
  triplet (`design-tokens/semantic-tokens.md`) that badges, chips, status
  pills, delta indicators, semantic icon containers, and avatar initials/
  backgrounds actually use — computed exactly like the plain triplet above,
  independently of it: a semantic key's plain foreground/background pair
  passing is never treated as certifying its `soft` background too.
- Target size: every `sizing.control*` token cleared against the WCAG 2.2
  Target Size (Minimum) 24px floor (`ux-engine/accessibility.md`) — a real
  dimensional calculation, not a visual "looks big enough" assumption.

What this deliberately does NOT check
--------------------------------------
Whether a token is used in the *semantically correct role* on a given
screen (a `warning`-toned value applied to a primary CTA), whether a
logged Token gap's proposed resolution is the right one, raw values inside
vendored/third-party code Design-Glanza didn't generate, or a color
combination outside the pairings named above (e.g. a semantic color reused
directly as a badge fill under body text) — all judgment calls,
`agents/design-system-expert.md`'s job per `design-tokens/token-audit.md`,
not this script's. This script also does not perform full JSON Schema
validation (`design-tokens.schema.json` is the canonical shape reference
for a human/agent to check against; this script implements the equivalent
structural checks directly, dependency-free, matching every other script
in this folder's stdlib-only posture).

Status: implemented.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import _common
from _common import (
    CONTRAST_MIN_LARGE,
    CONTRAST_MIN_NORMAL,
    Finding,
    contrast_ratio,
    read_text,
)

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


def _mode_value(token, mode):
    """A leaf token's resolved hex value for one theme mode — themed tokens
    store {light, dark}; an untethemed token stores a bare string used for
    both modes."""
    if not isinstance(token, dict):
        return None
    value = token.get("value")
    if isinstance(value, dict):
        return value.get(mode, value.get("light"))
    return value if isinstance(value, str) else None


# Semantic keys whose `soft`/`onSoft` pairing (Pass 3, below) is checked
# against a named, real-world component pattern — per
# ui-engine/color-system.md's Semantic mapping table extension and
# design-tokens/semantic-tokens.md's Structure section. Keyed by semantic
# name only to attach a human-readable "this is what actually breaks"
# pattern list to a finding; any other semantic key with a `soft` field
# still gets checked, just without a named pattern list (falls back to a
# generic description).
SOFT_PAIRING_COMPONENT_PATTERNS = {
    "success": "badges, chips, status pills, delta indicators (positive), semantic icon containers",
    "warning": "badges, chips, status pills, semantic icon containers",
    "error": "badges, chips, status pills, delta indicators (negative), semantic icon containers, form field error states",
    "info": "badges, chips, status pills, semantic icon containers",
    "primary": "avatar initials/backgrounds, active/selected nav or tab states",
    "secondary": "avatar initials/backgrounds, active/selected nav or tab states",
    "neutral": "avatar initials/backgrounds, disabled-adjacent chips",
}


def _check_contrast(tokens: dict, rel: str) -> list[Finding]:
    """Deterministic pass of ui-engine/color-system.md's Contrast compliance
    rule — the rule states every semantic triplet's foreground-on-background
    pairing is checked in both light and dark theme; this is that check,
    not a restatement of it. Three passes: (1) every declared {foreground,
    background} triplet pair (color-system.md's own named contract); (2)
    color.semantic.text.{primary,muted} against the two most common
    surfaces (background, surface) — the pairings almost every screen
    actually uses, per token-audit.md's 'checked pairings are an explicit,
    named contract' framing; (3) every declared {onSoft, soft} tinted-
    background pairing — the badge/chip/status-pill/delta-indicator/
    semantic-icon-container/avatar pattern, checked independently of
    whether that same semantic key's plain foreground-on-background pair
    (pass 1) already passed, since a tinted 'soft' background is not the
    same background and does not inherit pass 1's result. A color
    combination outside all three pairings above (e.g. text reused as a
    badge fill with no soft/onSoft declared at all) is explicitly NOT
    certified by this check, matching color-system.md's 'pairing contract,
    not a one-time pass' framing — it is a fresh check for whoever
    introduces it, not a gap in this function."""
    findings: list[Finding] = []
    color = tokens.get("color")
    if not isinstance(color, dict):
        return findings
    semantic = color.get("semantic")
    if not isinstance(semantic, dict):
        return findings

    modes = ("light", "dark")

    def add(path: str, mode: str, ratio: float, threshold: float, pattern: str | None = None):
        # Below even the lenient 3:1 large-text/UI-boundary bar: Major
        # regardless of role. Above 3:1 but below the role's own threshold
        # (only reachable for primary-weight text, held to 4.5:1): Minor —
        # still a real defect, just not an unreadable one.
        severity = "Major" if ratio < CONTRAST_MIN_LARGE else "Minor"
        pattern_note = f" — affects: {pattern}" if pattern else ""
        findings.append(Finding(
            severity,
            f"'{path}' ({mode} mode) has a {ratio:.2f}:1 contrast ratio, "
            f"below the {threshold}:1 minimum (ui-engine/color-system.md's "
            f"Contrast compliance rule){pattern_note}",
            rel, "contrast-failure",
        ))

    # Pass 1: every declared {foreground, background} triplet pair.
    for key, entry in semantic.items():
        if not isinstance(entry, dict):
            continue
        fg, bg = entry.get("foreground"), entry.get("background")
        if not (isinstance(fg, dict) and isinstance(bg, dict)):
            continue
        for mode in modes:
            fg_hex, bg_hex = _mode_value(fg, mode), _mode_value(bg, mode)
            ratio = contrast_ratio(fg_hex, bg_hex)
            if ratio is not None and ratio < CONTRAST_MIN_NORMAL:
                add(f"color.semantic.{key}.foreground on .background", mode,
                    ratio, CONTRAST_MIN_NORMAL)

    # Pass 2: text.primary / text.muted against background and surface.
    text = semantic.get("text")
    if isinstance(text, dict):
        for text_key in ("primary", "muted"):
            text_tok = text.get(text_key)
            if not isinstance(text_tok, dict):
                continue
            threshold = CONTRAST_MIN_NORMAL if text_key == "primary" else CONTRAST_MIN_LARGE
            for surf_name in ("background", "surface"):
                surf_entry = semantic.get(surf_name)
                if not isinstance(surf_entry, dict):
                    continue
                surf_bg = surf_entry.get("background")
                if not isinstance(surf_bg, dict):
                    continue
                for mode in modes:
                    text_hex = _mode_value(text_tok, mode)
                    surf_hex = _mode_value(surf_bg, mode)
                    ratio = contrast_ratio(text_hex, surf_hex)
                    if ratio is not None and ratio < threshold:
                        add(f"color.semantic.text.{text_key} on "
                            f".semantic.{surf_name}.background", mode,
                            ratio, threshold)

    # Pass 3 (B8.1): every declared {onSoft, soft} tinted-background pair —
    # the badge/chip/status-pill/delta-indicator/semantic-icon-container/
    # avatar pattern a benchmark run found failing in generated output even
    # though the same semantic key's plain foreground/background pair (pass
    # 1) passed cleanly. `soft` and `onSoft` are optional, additive fields
    # on the existing triplet (design-tokens/semantic-tokens.md) — a
    # semantic key with no `soft` declared is unaffected by this pass, not
    # flagged as missing one; declaring `soft` with no `onSoft` falls back
    # to checking the key's own plain `foreground` against `soft`, since
    # that is exactly the "don't assume a token passing against the main
    # surface also passes against a different, tinted one" case this pass
    # exists to catch, never silently skipped for lack of a dedicated field.
    for key, entry in semantic.items():
        if not isinstance(entry, dict):
            continue
        soft = entry.get("soft")
        if not isinstance(soft, dict):
            continue
        on_soft = entry.get("onSoft")
        fg_field_name = "onSoft" if isinstance(on_soft, dict) else "foreground"
        fg_token = on_soft if isinstance(on_soft, dict) else entry.get("foreground")
        if not isinstance(fg_token, dict):
            continue  # no foreground of any kind to pair with `soft` — nothing to check
        pattern = SOFT_PAIRING_COMPONENT_PATTERNS.get(key)
        for mode in modes:
            fg_hex, soft_hex = _mode_value(fg_token, mode), _mode_value(soft, mode)
            ratio = contrast_ratio(fg_hex, soft_hex)
            if ratio is not None and ratio < CONTRAST_MIN_NORMAL:
                add(f"color.semantic.{key}.{fg_field_name} on .soft", mode,
                    ratio, CONTRAST_MIN_NORMAL, pattern)

    return findings


# WCAG 2.2 Target Size (Minimum) — 24 CSS px is the absolute floor for any
# interactive target, per ux-engine/accessibility.md's WCAG 2.2-specific
# rules. This is the general-web minimum, not the stricter touch-specific
# 44px bar (responsive-system.md's Touch-target sizing rule) — that bar is
# breakpoint-conditional (touch-relevant breakpoints only) and a token
# value carries no breakpoint context, so it isn't checked here; 24px is
# the one threshold every control-height token must clear unconditionally.
TARGET_SIZE_MIN_PX = 24


def _px_value(raw) -> float | None:
    """Parse a '32px'-shaped token value into a float, or None if it isn't
    a parseable px value (e.g. a percentage or a var() reference)."""
    if not isinstance(raw, str):
        return None
    m = re.fullmatch(r"\s*(-?[\d.]+)\s*px\s*", raw)
    return float(m.group(1)) if m else None


def _check_target_size(tokens: dict, rel: str) -> list[Finding]:
    """Every sizing.control* token (button/input/select outer height, per
    design-system.md's Sizing scale) clears the 24px WCAG 2.2 Target Size
    minimum — a real, calculable dimensional check rather than a visual
    'looks tappable' assumption. Today's three control tokens (32/40/48px)
    already clear it; this check is the safety net against a future
    product-specific override or a master-scale edit shrinking one below
    the floor, not a currently-expected finding."""
    findings: list[Finding] = []
    sizing = tokens.get("sizing")
    if not isinstance(sizing, dict):
        return findings
    for key, token in sizing.items():
        if not key.lower().startswith("control"):
            continue  # avatar/other sizing tokens aren't interactive targets
        if not isinstance(token, dict):
            continue
        px = _px_value(token.get("value"))
        if px is not None and px < TARGET_SIZE_MIN_PX:
            findings.append(Finding(
                "Major",
                f"'sizing.{key}' is {px:.0f}px, below the {TARGET_SIZE_MIN_PX}px "
                "WCAG 2.2 Target Size (Minimum) — ux-engine/accessibility.md's "
                "WCAG 2.2-specific rules",
                rel, "target-size-failure",
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


def _is_expected_onsoft_fallback(paths: list[str]) -> bool:
    """A semantic key's `onSoft` legitimately equals its own `foreground`
    exactly when that foreground already clears the `soft`-background bar
    unaided (design-tokens/semantic-tokens.md's documented fallback,
    `_check_contrast` pass 3) — this is the intended degenerate case of a
    real, checked pairing, not an accidental duplicate name, so it's
    excluded here the same deliberate way typography's sub-axes are."""
    if len(paths) != 2:
        return False
    suffixes = {p.rsplit(".", 1)[-1] for p in paths}
    prefixes = {p.rsplit(".", 1)[0] for p in paths}
    return suffixes == {"foreground", "onSoft"} and len(prefixes) == 1


def _check_redundant_tokens(tokens: dict, rel: str) -> list[Finding]:
    """Flag two different token paths *within the same top-level category*
    that resolve to the exact same value — design-tokens/token-audit.md's
    Redundant tokens check. Scoped per-category (never cross-category, e.g.
    radius.none vs. border.width.none) since a same-value coincidence across
    unrelated categories is meaningless, not a real duplicate name; typography
    is excluded entirely (see the constant above), and a semantic key's
    `onSoft` intentionally equaling its own `foreground` (the documented
    fallback case, above) is excluded the same way."""
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
            if _is_expected_onsoft_fallback(paths):
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
    findings += _check_contrast(tokens, rel)
    findings += _check_target_size(tokens, rel)
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
