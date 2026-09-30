"""
validate-visual-regression.py

Responsibility
--------------
Deterministic, structural diff between a screen's committed baseline
(`product-builder/ui/baselines/<SCREEN-NNN>.json`) and its freshly
captured current state (`product-builder/ui/baselines/<SCREEN-NNN>.current.json`),
per `visual-regression/{baseline-model,diff-detection,tolerance-thresholds,
severity-classification}.md`:

- Region order/presence changes -> Layout shifts.
- A component present in baseline but absent from current -> Missing elements.
- A component present in current but absent from baseline -> Unexpected elements.
- A shared component's registryBase/variant/alignment differing -> Component
  inconsistencies / Alignment problems.
- A shared component's token paths differing, bucketed by category ->
  Spacing changes / Typography changes / Color deviations (other token
  categories bucket into Component inconsistencies).
- Breakpoint behavior differing -> Responsive regressions.
- A resolved token path that isn't a recognized category at all -> always
  Critical (a raw-value/unauthorized-path violation, per
  `design-tokens/token-audit.md`'s same discipline applied here).

Every finding's severity is reported two ways, per `visual-regression/
severity-classification.md`: a Critical/High/Medium/Low label (shown in
the message, this system's own finer scale) and the mapped Blocker/Major/
Minor/Note value (the `Finding.severity` field itself) so this script
aggregates alongside every other `validate-*.py` using the one shared
vocabulary, never a second competing one.

What this deliberately does NOT check
--------------------------------------
Whether a diff is *actually* an intentional, approved change (that's
`visual-regression/baseline-updates.md`'s Baseline Update record, a human/
agent judgment) or whether a missing element sits on a core-workflow
scenario (which would escalate High to Critical per `severity-
classification.md` — `agents/qa-expert.md`'s job, cross-checking
`ux-scenario-testing/*`, not this script's). This script also does not
capture the "current" snapshot itself — that's produced by whichever
agent/workflow step is running the comparison, from the same structured
facts `baseline-model.md` names, the same "scripts don't reason" boundary
`create-product-builder.py`'s own docstring already states.

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

# Fixed scales, per ui-engine/design-system.md and typography.md — used
# only to measure "how many steps apart," never to invent a value outside
# them.
SPACING_SCALE = [4, 8, 12, 16, 24, 32, 48, 64, 96]
TYPE_SIZE_SCALE = ["caption", "body", "bodyLarge", "h3", "h2", "h1", "display"]

# Recognized top-level token category prefixes, per
# design-tokens/token-schema.md. A resolved path whose category isn't in
# this set is not a valid token reference at all.
KNOWN_TOKEN_CATEGORIES = {
    "color", "typography", "spacing", "grid", "radius", "border",
    "elevation", "sizing", "breakpoint", "motion", "zIndex", "product",
}

CRITICAL, HIGH, MEDIUM, LOW = "Critical", "High", "Medium", "Low"
LABEL_TO_MAPPED = {CRITICAL: "Blocker", HIGH: "Major", MEDIUM: "Minor", LOW: "Note"}


def _finding(label: str, category: str, message: str, rel: str) -> Finding:
    return Finding(LABEL_TO_MAPPED[label], f"[{label}] {category} — {message}", rel, category)


def _load_json(path: Path) -> tuple[dict | None, str | None]:
    text = read_text(path)
    if text is None:
        return None, "missing-file"
    try:
        return json.loads(text), None
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON: {exc}"


def _index_components(snapshot: dict) -> dict[str, dict]:
    """Flatten {component_id: {..., '_region': region_name}} from a
    baseline/current snapshot's 'regions' list."""
    index: dict[str, dict] = {}
    for region in snapshot.get("regions", []):
        for comp in region.get("components", []):
            comp_id = comp.get("id")
            if not comp_id:
                continue
            entry = dict(comp)
            entry["_region"] = region.get("name", "")
            index[comp_id] = entry
    return index


def _token_category(path: str) -> str | None:
    if not isinstance(path, str) or "." not in path:
        return None
    prefix = path.split(".", 1)[0]
    return prefix if prefix in KNOWN_TOKEN_CATEGORIES else None


def _scale_step_distance(scale: list, a: str, b: str) -> int | None:
    """Distance in scale steps between two token path suffixes (e.g.
    'spacing.16' -> 16, 'typography.size.h2' -> 'h2'). None if either
    value isn't found in the scale (can't measure adjacency)."""
    try:
        ia, ib = scale.index(a), scale.index(b)
    except ValueError:
        return None
    return abs(ia - ib)


def _diff_token_value(category: str, comp_id: str, region: str,
                       baseline_path: str, current_path: str, rel: str) -> Finding | None:
    if baseline_path == current_path:
        return None

    base_cat, cur_cat = _token_category(baseline_path), _token_category(current_path)
    if base_cat is None or cur_cat is None:
        return _finding(
            CRITICAL, "Invalid token reference",
            f"{comp_id} ({region})'s '{category}' resolves to '{current_path}', "
            "not a recognized design-tokens category — a raw/unauthorized value",
            rel,
        )

    if category == "spacing":
        try:
            a = int(baseline_path.rsplit(".", 1)[1])
            b = int(current_path.rsplit(".", 1)[1])
            steps = _scale_step_distance(SPACING_SCALE, a, b)
        except (IndexError, ValueError):
            steps = None
        label = MEDIUM if steps == 1 else HIGH
        return _finding(
            label, "Spacing changes",
            f"{comp_id} ({region}): '{baseline_path}' -> '{current_path}'"
            + (f" ({steps} scale step(s))" if steps is not None else ""),
            rel,
        )

    if category == "typography":
        base_role, cur_role = baseline_path.rsplit(".", 1)[-1], current_path.rsplit(".", 1)[-1]
        steps = _scale_step_distance(TYPE_SIZE_SCALE, base_role, cur_role)
        label = MEDIUM if steps == 1 else HIGH
        return _finding(
            label, "Typography changes",
            f"{comp_id} ({region}): '{baseline_path}' -> '{current_path}'"
            + (f" ({steps} scale step(s))" if steps is not None else ""),
            rel,
        )

    if category == "color":
        # Same semantic role (e.g. both color.semantic.warning.*) but a
        # different exact path is a smaller drift than switching roles
        # entirely (warning -> error).
        base_role = baseline_path.split(".")[:3]
        cur_role = current_path.split(".")[:3]
        label = MEDIUM if base_role == cur_role else HIGH
        return _finding(
            label, "Color deviations",
            f"{comp_id} ({region}): '{baseline_path}' -> '{current_path}'",
            rel,
        )

    # Any other token category (radius, elevation, motion, sizing, border,
    # zIndex) that changed is bucketed as a component-level inconsistency
    # rather than inventing a 10th category not in diff-detection.md's list.
    return _finding(
        HIGH, "Component inconsistencies",
        f"{comp_id} ({region})'s '{category}' token changed: '{baseline_path}' "
        f"-> '{current_path}', no stated reason",
        rel,
    )


def diff_snapshots(baseline: dict, current: dict, rel: str) -> list[Finding]:
    findings: list[Finding] = []

    # Layout shifts: region presence/order.
    base_regions = [r.get("name") for r in baseline.get("regions", [])]
    cur_regions = [r.get("name") for r in current.get("regions", [])]
    if base_regions != cur_regions:
        findings.append(_finding(
            HIGH, "Layout shifts",
            f"Region order/presence changed: {base_regions} -> {cur_regions}",
            rel,
        ))

    base_idx, cur_idx = _index_components(baseline), _index_components(current)

    for comp_id, comp in base_idx.items():
        if comp_id not in cur_idx:
            findings.append(_finding(
                CRITICAL, "Missing elements",
                f"{comp_id} ({comp.get('_region', '')}) present in baseline, "
                "absent from current",
                rel,
            ))

    for comp_id, comp in cur_idx.items():
        if comp_id not in base_idx:
            findings.append(_finding(
                HIGH, "Unexpected elements",
                f"{comp_id} ({comp.get('_region', '')}) present in current, "
                "absent from baseline, no stated Design Direction change",
                rel,
            ))

    for comp_id in sorted(set(base_idx) & set(cur_idx)):
        b, c = base_idx[comp_id], cur_idx[comp_id]
        region = c.get("_region", "")

        if b.get("registryBase") != c.get("registryBase") or b.get("variant") != c.get("variant"):
            findings.append(_finding(
                HIGH, "Component inconsistencies",
                f"{comp_id} ({region}): registryBase/variant changed "
                f"('{b.get('registryBase')}'/{b.get('variant')} -> "
                f"'{c.get('registryBase')}'/{c.get('variant')})",
                rel,
            ))

        if "alignment" in b or "alignment" in c:
            if b.get("alignment") != c.get("alignment"):
                findings.append(_finding(
                    MEDIUM, "Alignment problems",
                    f"{comp_id} ({region}): alignment changed "
                    f"('{b.get('alignment')}' -> '{c.get('alignment')}')",
                    rel,
                ))

        base_tokens, cur_tokens = b.get("tokens", {}), c.get("tokens", {})
        for token_cat in sorted(set(base_tokens) | set(cur_tokens)):
            bp, cp = base_tokens.get(token_cat), cur_tokens.get(token_cat)
            if bp is None or cp is None or bp == cp:
                continue
            finding = _diff_token_value(token_cat, comp_id, region, bp, cp, rel)
            if finding:
                findings.append(finding)

    base_bp, cur_bp = baseline.get("breakpoints", {}), current.get("breakpoints", {})
    for bp_name in sorted(set(base_bp) | set(cur_bp)):
        if base_bp.get(bp_name) != cur_bp.get(bp_name):
            findings.append(_finding(
                HIGH, "Responsive regressions",
                f"Breakpoint '{bp_name}' reflow changed: '{base_bp.get(bp_name)}' "
                f"-> '{cur_bp.get(bp_name)}'",
                rel,
            ))

    return findings


def validate(product_builder_dir: Path, screen: str | None = None) -> list[Finding]:
    baselines_dir = product_builder_dir / "ui" / "baselines"
    if not baselines_dir.is_dir():
        return [Finding("Note", "No ui/baselines/ directory yet — no screen has a baseline captured.", "ui/baselines/", "no-baselines")]

    findings: list[Finding] = []
    baseline_paths = sorted(baselines_dir.glob("*.json"))
    for path in baseline_paths:
        if path.name.endswith(".current.json"):
            continue
        screen_id = path.stem
        if screen and screen_id != screen:
            continue
        current_path = baselines_dir / f"{screen_id}.current.json"
        rel = f"ui/baselines/{screen_id}.json"

        baseline, err = _load_json(path)
        if err:
            findings.append(Finding("Blocker", f"baseline {err}", rel, "load-error"))
            continue
        if not current_path.is_file():
            findings.append(Finding(
                "Note",
                f"No current capture ({current_path.name}) to diff against yet "
                "— nothing to compare this pass.",
                rel, "no-current-capture",
            ))
            continue
        current, err = _load_json(current_path)
        if err:
            findings.append(Finding("Blocker", f"current capture {err}", rel, "load-error"))
            continue

        findings.extend(diff_snapshots(baseline, current, rel))

    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("product_builder_dir", help="Path to a product-builder/ directory.")
    parser.add_argument("--screen", help="Limit to one SCREEN-NNN id (default: diff every screen with a baseline).")
    args = parser.parse_args(argv)

    findings = validate(Path(args.product_builder_dir), args.screen)
    if not findings:
        print("validate-visual-regression: no findings.")
        return 0
    for f in findings:
        print(f)
    return 1 if any(f.severity in ("Blocker", "Major") for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
