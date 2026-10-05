"""
validate-figma-conformance.py

Responsibility
--------------
Automates `ui-engine/visual-benchmark.md`'s Level B (Figma-spec
conformance) — previously a manual, agent-executed comparison with no
deterministic check of its own (a real gap found during a benchmark run:
every Level B check had to be done by hand, reading `capture-render.py`'s
computed-style fields and comparing them to `figma-context.json` one
value at a time). Two related, both-deterministic checks, against the
same two input files:

1. **Figma-token source traceability** (closes the same benchmark's
   traceability gap): every token in `product-builder/ui/
   design-tokens.json` whose `description` field cites a Figma source
   (contains the literal word "Figma") must have a `value` that actually
   appears somewhere in `BRD/figma/figma-context.json`'s own `tokens.*`
   section. A citation whose claimed value doesn't trace to a real
   entry is a fabricated/stale citation — `[Blocker]`, the same severity
   a fabricated assumption gets everywhere else in this engine (Rule 10's
   discipline, applied here to a Figma citation specifically).
2. **Figma-token realization** (the actual "conformance" half of Level
   B): for every Figma-cited token that DID trace correctly, check
   whether its value was ever actually observed in a real render —
   scanning every `*.json` manifest under `product-builder/qa/
   render-capture/**` (the same manifests `validate-rendered-layout.py`
   already consumes) for a matching `backgroundColor`/`color`/
   `borderColor`/`borderRadius`/`fontFamily`/`padding`/`gap` value. A
   token declared as Figma-sourced
   but never once rendered is `[Minor]` — declared-but-unused drift, not
   a Blocker, since a token can legitimately exist for a screen not yet
   implemented this pass.

Not applicable (not a failure) when `BRD/figma/figma-context.json` is
absent — not every product uses a Figma reference. Degrades to a single
disclosed `[Note]` when no render-capture manifests exist yet (e.g. before
Preview & Run has run) — the traceability check (1) still runs in full
either way, since it needs no render at all; only check (2) depends on
rendering.

What this deliberately does NOT check
--------------------------------------
Whether a non-Figma-cited token is correct (that's `validate-tokens.py`'s
job, unchanged). Whether a *component* choice is the right one for its
need (`agents/design-system-expert.md`'s judgment,
`component-registry/registry-integration.md`). Spacing/sizing conformance
with sub-pixel tolerance — color/radius/font comparisons are exact-after-
normalization (hex vs. rgb() string forms); this script does not invent a
tolerance scheme beyond that. Layout/composition conformance (that's
Level A, `compare-reference-visual.py`, and `ui-audit-framework.md`'s own
pipeline) — this script only checks token-level color/radius/typography
values, matching exactly what Level B's gap type
(`visual-benchmark.md`'s **Figma-spec deviation** row) describes.

Status: implemented.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import _common
from _common import Finding, hex_to_rgb

# Matches design-tokens/token-schema.md's precise citation marker only
# ("Figma source: ...") — NOT a bare mention of the word "Figma" anywhere
# in a description. A looser substring match was tried first and found,
# on real data, to both false-positive (a description explaining that NO
# Figma source existed for this token still contains the word "Figma")
# and false-negative (a citation phrased as "aliased to Figma X" doesn't
# start with the word) — this precise marker is the fix, not a smarter
# heuristic.
FIGMA_CITATION_RE = re.compile(r"figma\s+source\s*:", re.IGNORECASE)


def _load_json(path: Path):
    if not path.is_file():
        return None, "missing-file"
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, f"invalid JSON ({e})"


def _collect_figma_token_values(figma_context: dict) -> dict[str, set]:
    """Flatten figma-context.json's tokens.* into {category: {normalized
    value, ...}} buckets so a design-tokens.json claim can be checked
    against the real set, regardless of exactly where under tokens.* it
    lived (colors/typography/spacing/radius/elevation/sizing)."""
    buckets: dict[str, set] = {"color": set(), "radius": set(), "font": set(), "other": set()}
    tokens = figma_context.get("tokens", {})
    if not isinstance(tokens, dict):
        return buckets

    def walk(node, category_hint: str):
        if isinstance(node, dict):
            if "value" in node and not isinstance(node["value"], (dict, list)):
                _bucket_value(buckets, category_hint, node["value"])
                return
            for key, child in node.items():
                walk(child, key if key in ("colors", "radius", "typography", "spacing", "elevation", "sizing") else category_hint)
        elif isinstance(node, list):
            for child in node:
                walk(child, category_hint)

    for category, section in tokens.items():
        walk(section, category)
    return buckets


def _normalize_family(value: str) -> str:
    """CSS font-family values are commonly quoted ('"Inter", sans-serif')
    while a citation source is just as commonly a plain, unquoted string
    ('Inter, sans-serif') — strip quote characters before any comparison
    so this difference in *quoting convention* never reads as a value
    mismatch."""
    return value.replace('"', "").replace("'", "").strip().lower()


def _bucket_value(buckets: dict[str, set], category_hint: str, value) -> None:
    if not isinstance(value, str):
        return
    rgb = hex_to_rgb(value)
    if rgb is not None:
        buckets["color"].add(rgb)
        return
    if re.fullmatch(r"\d+(\.\d+)?px", value.strip()):
        buckets["radius"].add(value.strip().lower())
        return
    # typography family / anything else textual
    buckets["font"].add(_normalize_family(value))
    buckets["other"].add(_normalize_family(value))


def _rgb_from_css(value: str):
    """Parse an rgb()/rgba() string (capture-render.py's computed-style
    form) into an (r, g, b) tuple, or a #hex string via _common's own
    parser — whichever this value actually is."""
    if not isinstance(value, str):
        return None
    m = re.match(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", value)
    if m:
        return tuple(int(m.group(i)) for i in (1, 2, 3))
    return hex_to_rgb(value)


def _find_figma_cited_tokens(design_tokens, path="") -> list[tuple[str, str]]:
    """Walk design-tokens.json looking for leaf token objects whose
    description cites Figma — returns [(path, claimed_value), ...]."""
    found = []
    if isinstance(design_tokens, dict):
        if "value" in design_tokens and isinstance(design_tokens.get("description"), str):
            if FIGMA_CITATION_RE.search(design_tokens["description"]):
                found.append((path, design_tokens["value"]))
            return found
        for key, child in design_tokens.items():
            found += _find_figma_cited_tokens(child, f"{path}.{key}" if path else key)
    return found


def _value_traces(claimed_value, figma_buckets: dict[str, set]) -> bool:
    rgb = hex_to_rgb(claimed_value) if isinstance(claimed_value, str) else None
    if rgb is not None:
        return rgb in figma_buckets["color"]
    if isinstance(claimed_value, str) and re.fullmatch(r"\d+(\.\d+)?px", claimed_value.strip()):
        return claimed_value.strip().lower() in figma_buckets["radius"]
    if isinstance(claimed_value, str):
        v = _normalize_family(claimed_value)
        return any(v in other or other in v for other in figma_buckets["other"])
    return False


def _value_observed_in_renders(claimed_value, render_dir: Path) -> bool:
    if not render_dir.is_dir():
        return False
    rgb = hex_to_rgb(claimed_value) if isinstance(claimed_value, str) else None
    needle = claimed_value.strip().lower() if isinstance(claimed_value, str) else None
    family_needle = _normalize_family(claimed_value) if isinstance(claimed_value, str) else None
    for manifest_path in render_dir.glob("**/*.json"):
        manifest, err = _load_json(manifest_path)
        if err or not isinstance(manifest, dict):
            continue
        for el in manifest.get("elements", []):
            if rgb is not None:
                for field in ("backgroundColor", "color", "borderColor"):
                    if _rgb_from_css(el.get(field, "")) == rgb:
                        return True
            elif needle:
                for field in ("borderRadius", "padding", "gap"):
                    v = el.get(field)
                    if isinstance(v, str) and needle in v.lower():
                        return True
                for field in ("fontFamily",):
                    v = el.get(field)
                    if isinstance(v, str) and family_needle and family_needle in _normalize_family(v):
                        return True
    return False


def validate(product_dir: Path) -> list[Finding]:
    figma_context_path = product_dir / "BRD" / "figma" / "figma-context.json"
    if not figma_context_path.is_file():
        return [Finding("Note", "No Figma Design Context present — Level B conformance is not applicable for this product", "BRD/figma/figma-context.json", "not-applicable")]

    figma_context, err = _load_json(figma_context_path)
    if err:
        return [Finding("Blocker", f"figma-context.json {err}", "BRD/figma/figma-context.json", "load-error")]

    tokens_path = product_dir / "product-builder" / "ui" / "design-tokens.json"
    design_tokens, err = _load_json(tokens_path)
    rel_tokens = "ui/design-tokens.json"
    if err:
        severity = "Major" if err == "missing-file" else "Blocker"
        return [Finding(severity, f"design-tokens.json {err}", rel_tokens, "load-error")]

    figma_buckets = _collect_figma_token_values(figma_context)
    cited = _find_figma_cited_tokens(design_tokens)

    findings: list[Finding] = []
    render_dir = product_dir / "product-builder" / "qa" / "render-capture"
    renders_exist = render_dir.is_dir() and any(render_dir.glob("**/*.json"))
    if not renders_exist:
        findings.append(Finding("Note", "No render-capture manifests found yet — token-realization check (2) skipped; traceability check (1) still ran in full", str(render_dir), "renders-unavailable"))

    for path, claimed_value in cited:
        if not _value_traces(claimed_value, figma_buckets):
            findings.append(Finding(
                "Blocker",
                f"design-tokens.json path '{path}' cites a Figma source (its description "
                f"mentions 'Figma') with value {claimed_value!r}, but no entry in "
                f"figma-context.json's tokens.* actually holds that value — fabricated or "
                f"stale Figma citation",
                rel_tokens, "figma-traceability",
            ))
            continue
        if renders_exist and not _value_observed_in_renders(claimed_value, render_dir):
            findings.append(Finding(
                "Minor",
                f"design-tokens.json path '{path}' is a traceable Figma-sourced token "
                f"({claimed_value!r}) but was never observed in any rendered manifest — "
                f"declared but possibly unused this pass",
                rel_tokens, "figma-realization",
            ))

    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("product_dir", help="Path to a products/<slug>/ directory.")
    args = parser.parse_args(argv)

    findings = validate(Path(args.product_dir))
    if not findings:
        print("validate-figma-conformance: no findings.")
        return 0
    for f in findings:
        print(f)
    return 1 if any(f.severity in ("Blocker", "Major") for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
