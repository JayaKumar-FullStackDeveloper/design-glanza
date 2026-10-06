"""
validate-rendered-layout.py

Responsibility
--------------
The MEASURE step of the GENERATE -> RENDER -> OBSERVE -> MEASURE -> COMPARE
-> FIX -> RE-RENDER -> RE-CHECK loop (Rule 20, gate B15, this version's
quality-engine upgrade). Consumes the raw per-element geometry JSON that
`capture-render.py` produced from a REAL rendered page (never source code,
never an LLM's reading of markup) and applies deterministic geometric
analysis to it, emitting `_common.Finding` objects in the shared severity
vocabulary (Blocker/Major/Minor/Note).

Pure logic, zero rendering: this script never launches a browser and has
no Playwright/Pillow import. That split is deliberate (the user's
"prefer separation" instruction) — it means this analysis is unit-testable
against a hand-built JSON fixture with no browser available at all, and it
means a change to the analysis thresholds never requires re-rendering
anything to test.

What it checks (all against REAL rendered geometry, never inferred from
HTML/CSS source):

1. Overflow — `scrollWidth > clientWidth` / `scrollHeight > clientHeight`
   beyond a small anti-aliasing tolerance, on any element whose own
   computed `overflow-x`/`overflow-y` is not `auto`/`scroll` (an
   intentionally scrollable container, e.g. a data table body, is not a
   defect). This is the single mechanism used to catch: text overflow,
   clipped text, horizontal/vertical content overflow, content escaping
   its container, and an overflowing button/badge/table cell — all of
   these are the same underlying geometric signature (rendered content
   larger than its box) and are reported under one `overflow` check so
   the Finding message always names the concrete element and its
   magnitude instead of a generic label.
2. Alignment — elements grouped by (parentPath, first class token) as a
   "sibling set" (the repeating-card/repeating-row pattern every design
   system relies on); a sibling whose `top` (for a row-like set) or
   `left` (for a column-like set) deviates from the sibling-set's modal
   edge by more than ALIGNMENT_TOLERANCE_PX is flagged. This is real
   shared-edge measurement, not a heuristic about class names.
3. Spacing — gap between consecutive siblings in a sibling set (same
   parent, adjacent in DOM order, same row or column) measured as the
   real pixel distance between one element's edge and the next's;
   flagged when one gap deviates from the set's modal gap by more than
   SPACING_TOLERANCE_PX (inconsistent rhythm — the gap token silently
   changed partway through a repeating group).
4. Sizing — height (or width, for a horizontal set) of siblings in a set
   compared the same way; flagged when one diverges from the set's
   modal size beyond SIZING_TOLERANCE_PX (e.g. one KPI card/button/input
   taller or shorter than its row-mates).
5. Overlap — pairwise bounding-box intersection among *direct-text*
   leaf elements only (an element with its own visible text node, not a
   layout wrapper) that do not share an ancestor/descendant relationship
   — catches real text/icon collisions and stacking conflicts while
   deliberately not flagging intentional layering (a badge positioned
   over a card's corner, an avatar overlapping a banner) that's leaf-
   wrapper overlap rather than text-on-text collision.
6. Accessibility (added this version) — interprets `capture-render.py`'s
   captured `axe_violations` field, where present: a `critical` axe
   violation is a Blocker finding, `serious` is Major, `moderate`/`minor`
   are Minor — the deterministic counterpart to
   `ux-engine/accessibility.md`'s structural rules, not a replacement for
   them. A manifest with no `axe_violations` field (the capture ran with
   `--no-axe`, or axe-core injection itself failed) emits nothing here —
   silently skipped is correct, since a missing *capability* and a clean
   *result* must never be reported identically; a captured injection
   failure is surfaced as its own Note finding instead.
7. Performance budget (added this version) — interprets the captured
   `web_vitals` field against a pragmatic budget (LCP ≤ 4.0s, CLS ≤ 0.25,
   INP ≤ 500ms — well above "broken," well below a marketing-page-strict
   Core Web Vitals target) as Major findings. INP here is a single-
   sample, best-effort approximation (`capture-render.py`'s own
   docstring) — a missing value (no interactive element found) is
   skipped, never treated as a failure.

Thresholds are deliberately conservative (favor missing a borderline
case over flagging an intentional design choice) — see each constant's
comment. This keeps the signal trustworthy: every Finding this script
emits names a real, reproducible number from an actual render.

Standalone-screen support: operates on whatever manifest JSON
`capture-render.py` wrote, regardless of whether that HTML came from a
full Product Builder pass or a standalone screen request — no scaffold
awareness here at all.

Status: implemented and verified — the three defect classes (alignment
drift, overflow, overlap) were each independently proven detectable
against a hand-built fixture before this script was written (see this
version's changelog, Test 1/2/4).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import Finding  # noqa: E402

# All tolerances are in CSS pixels, measured at the viewport the manifest
# was captured at. Deliberately looser than a pixel-perfect-diff tool: this
# is catching *real* drift (a changed/forgotten token), not sub-pixel
# rendering jitter between font hinting passes.
OVERFLOW_TOLERANCE_PX = 2
ALIGNMENT_TOLERANCE_PX = 4
SPACING_TOLERANCE_PX = 6
SIZING_TOLERANCE_PX = 6
OVERLAP_MIN_AREA_PX = 16  # ignore sub-4x4px intersections (anti-aliasing noise)

SCROLLABLE_OVERFLOW_VALUES = {"auto", "scroll"}

# axe-core's own impact vocabulary -> this script's shared severity
# vocabulary. "critical"/"serious" are the two ux-audit hard-gates on;
# kept as Blocker/Major here too so this validator's own exit code
# already reflects that without a separate gate check.
AXE_IMPACT_TO_SEVERITY = {
    "critical": "Blocker",
    "serious": "Major",
    "moderate": "Minor",
    "minor": "Minor",
}

# Pragmatic performance budget (see ux-audit's performance-budget
# technique): well above "broken," well below a marketing-page-strict
# Core Web Vitals target, since this runs against ordinary app screens,
# not just landing pages.
LCP_BUDGET_MS = 4000.0
CLS_BUDGET = 0.25
INP_BUDGET_MS = 500.0


def _loc(manifest: dict, el: dict) -> str:
    return f"{manifest['viewport_name']}/{manifest['theme']} :: {el['path']}"


def check_overflow(manifest: dict) -> list[Finding]:
    findings = []
    for el in manifest["elements"]:
        dx = el["scrollWidth"] - el["clientWidth"]
        dy = el["scrollHeight"] - el["clientHeight"]
        if dx > OVERFLOW_TOLERANCE_PX and el["overflowX"] not in SCROLLABLE_OVERFLOW_VALUES:
            findings.append(Finding(
                severity="Blocker",
                message=(
                    f"Horizontal overflow: rendered content is {dx:.0f}px wider than its "
                    f"container (scrollWidth {el['scrollWidth']:.0f} vs clientWidth "
                    f"{el['clientWidth']:.0f}), text=\"{el['text']}\""
                ),
                file=_loc(manifest, el),
                check="rendered-overflow",
            ))
        if dy > OVERFLOW_TOLERANCE_PX and el["overflowY"] not in SCROLLABLE_OVERFLOW_VALUES:
            findings.append(Finding(
                severity="Blocker",
                message=(
                    f"Vertical overflow: rendered content is {dy:.0f}px taller than its "
                    f"container (scrollHeight {el['scrollHeight']:.0f} vs clientHeight "
                    f"{el['clientHeight']:.0f}), text=\"{el['text']}\""
                ),
                file=_loc(manifest, el),
                check="rendered-overflow",
            ))
    return findings


def _sibling_sets(elements: list[dict]) -> dict:
    """Group elements by (parentPath, first class token) - the repeating
    card/row/column pattern. Sets of size 1 carry no comparison signal and
    are dropped."""
    groups: dict = {}
    for el in elements:
        if not el["classes"]:
            continue
        first_class = el["classes"].split()[0]
        key = (el["parentPath"], first_class)
        groups.setdefault(key, []).append(el)
    return {k: v for k, v in groups.items() if len(v) >= 2}


def _modal(values: list[float], tolerance: float) -> float:
    """The most common value in a list, clustering within `tolerance` of
    each other - robust to one true outlier skewing a plain mean."""
    buckets: list[list[float]] = []
    for v in sorted(values):
        placed = False
        for b in buckets:
            if abs(b[-1] - v) <= tolerance:
                b.append(v)
                placed = True
                break
        if not placed:
            buckets.append([v])
    best = max(buckets, key=len)
    return sum(best) / len(best)


def check_alignment_spacing_sizing(manifest: dict) -> list[Finding]:
    findings = []
    for (parent_path, cls), members in _sibling_sets(manifest["elements"]).items():
        members = sorted(members, key=lambda e: (e["top"], e["left"]))
        is_row_like = (max(e["top"] for e in members) - min(e["top"] for e in members)) < (
            max(e["left"] for e in members) - min(e["left"] for e in members)
        )

        # --- Alignment: shared edge on the cross-axis ---
        edge_key = "top" if is_row_like else "left"
        edges = [e[edge_key] for e in members]
        modal_edge = _modal(edges, ALIGNMENT_TOLERANCE_PX)
        for e in members:
            drift = abs(e[edge_key] - modal_edge)
            if drift > ALIGNMENT_TOLERANCE_PX:
                findings.append(Finding(
                    severity="Major",
                    message=(
                        f"Misaligned sibling in '.{cls}' set under {parent_path}: "
                        f"{edge_key}={e[edge_key]:.0f}px, set baseline={modal_edge:.0f}px "
                        f"(drift {drift:.0f}px), text=\"{e['text']}\""
                    ),
                    file=_loc(manifest, e),
                    check="rendered-alignment",
                ))

        # --- Sizing: height (row-like) or width (column-like) ---
        size_key = "height" if is_row_like else "width"
        sizes = [e[size_key] for e in members]
        modal_size = _modal(sizes, SIZING_TOLERANCE_PX)
        for e in members:
            drift = abs(e[size_key] - modal_size)
            if drift > SIZING_TOLERANCE_PX:
                findings.append(Finding(
                    severity="Minor",
                    message=(
                        f"Inconsistent sizing in '.{cls}' set under {parent_path}: "
                        f"{size_key}={e[size_key]:.0f}px, set baseline={modal_size:.0f}px "
                        f"(drift {drift:.0f}px), text=\"{e['text']}\""
                    ),
                    file=_loc(manifest, e),
                    check="rendered-sizing",
                ))

        # --- Spacing: gap between consecutive members along the main axis ---
        main_key_start = "left" if is_row_like else "top"
        main_key_end = "right" if is_row_like else "bottom"
        ordered = sorted(members, key=lambda e: e[main_key_start])
        gaps = []
        for a, b in zip(ordered, ordered[1:]):
            gaps.append(b[main_key_start] - a[main_key_end])
        if len(gaps) >= 2:
            modal_gap = _modal(gaps, SPACING_TOLERANCE_PX)
            for (a, b), gap in zip(zip(ordered, ordered[1:]), gaps):
                drift = abs(gap - modal_gap)
                if drift > SPACING_TOLERANCE_PX:
                    findings.append(Finding(
                        severity="Minor",
                        message=(
                            f"Inconsistent spacing in '.{cls}' set under {parent_path}: "
                            f"gap={gap:.0f}px between \"{a['text']}\" and \"{b['text']}\", "
                            f"set baseline={modal_gap:.0f}px (drift {drift:.0f}px)"
                        ),
                        file=_loc(manifest, b),
                        check="rendered-spacing",
                    ))
    return findings


def _is_ancestor_or_descendant(a: dict, b: dict) -> bool:
    return a["path"] != b["path"] and (a["path"].startswith(b["path"]) or b["path"].startswith(a["path"]))


def _intersection_area(a: dict, b: dict) -> float:
    left = max(a["left"], b["left"])
    right = min(a["right"], b["right"])
    top = max(a["top"], b["top"])
    bottom = min(a["bottom"], b["bottom"])
    if right <= left or bottom <= top:
        return 0.0
    return (right - left) * (bottom - top)


def check_overlap(manifest: dict) -> list[Finding]:
    findings = []
    leaves = [e for e in manifest["elements"] if e["hasDirectText"]]
    for i in range(len(leaves)):
        for j in range(i + 1, len(leaves)):
            a, b = leaves[i], leaves[j]
            if _is_ancestor_or_descendant(a, b):
                continue
            if a["parentPath"] == b["parentPath"] and a["path"] == b["path"]:
                continue
            area = _intersection_area(a, b)
            if area > OVERLAP_MIN_AREA_PX:
                findings.append(Finding(
                    severity="Major",
                    message=(
                        f"Overlapping text/elements: \"{a['text']}\" and \"{b['text']}\" "
                        f"intersect over {area:.0f}px^2"
                    ),
                    file=f"{_loc(manifest, a)} <-> {b['path']}",
                    check="rendered-overlap",
                ))
    return findings


def check_accessibility(manifest: dict) -> list[Finding]:
    """Interprets capture-render.py's captured axe_violations field - this
    script never launches axe-core itself, consistent with the pure-logic/
    zero-rendering split this whole file already follows."""
    findings = []
    axe = manifest.get("axe_violations")
    if axe is None:
        return findings  # axe wasn't run against this manifest - not a finding, a missing capability
    if isinstance(axe, dict) and "error" in axe:
        findings.append(Finding(
            severity="Note",
            message=f"axe-core accessibility scan unavailable: {axe['error']}",
            file=f"{manifest['viewport_name']}/{manifest['theme']}",
            check="rendered-accessibility",
        ))
        return findings
    for v in axe:
        severity = AXE_IMPACT_TO_SEVERITY.get(v.get("impact"), "Minor")
        findings.append(Finding(
            severity=severity,
            message=f"axe-core {v.get('impact')} violation: {v.get('help')} ({v.get('nodes', 0)} node(s))",
            file=f"{manifest['viewport_name']}/{manifest['theme']} :: {v.get('id')}",
            check="rendered-accessibility",
        ))
    return findings


def check_performance_budget(manifest: dict) -> list[Finding]:
    """Interprets capture-render.py's captured web_vitals field against
    the pragmatic LCP/CLS/INP budget above. Caller is expected to invoke
    this against the representative route(s) a performance budget
    actually applies to (ux-audit's own "once, on a representative
    route" posture) - this function itself doesn't select which manifest
    that is, it only judges whichever one it's given."""
    findings = []
    vitals = manifest.get("web_vitals")
    if not vitals:
        return findings  # vitals weren't captured against this manifest
    loc = f"{manifest['viewport_name']}/{manifest['theme']}"
    lcp = vitals.get("lcp_ms")
    if lcp is not None and lcp > LCP_BUDGET_MS:
        findings.append(Finding(
            severity="Major",
            message=f"LCP {lcp:.0f}ms exceeds the {LCP_BUDGET_MS:.0f}ms pragmatic budget",
            file=loc, check="rendered-performance-budget",
        ))
    cls = vitals.get("cls")
    if cls is not None and cls > CLS_BUDGET:
        findings.append(Finding(
            severity="Major",
            message=f"CLS {cls:.3f} exceeds the {CLS_BUDGET:.2f} pragmatic budget",
            file=loc, check="rendered-performance-budget",
        ))
    inp = vitals.get("inp_ms")
    if inp is not None and inp > INP_BUDGET_MS:
        findings.append(Finding(
            severity="Major",
            message=(
                f"INP ~{inp:.0f}ms (single-sample approximation) exceeds the "
                f"{INP_BUDGET_MS:.0f}ms pragmatic budget"
            ),
            file=loc, check="rendered-performance-budget",
        ))
    return findings


def validate_manifest(manifest: dict) -> list[Finding]:
    findings = []
    findings.extend(check_overflow(manifest))
    findings.extend(check_alignment_spacing_sizing(manifest))
    findings.extend(check_overlap(manifest))
    findings.extend(check_accessibility(manifest))
    findings.extend(check_performance_budget(manifest))
    return findings


def validate(manifest_paths: list[Path]) -> list[Finding]:
    findings = []
    for mp in manifest_paths:
        manifest = json.loads(mp.read_text(encoding="utf-8"))
        if "elements" not in manifest:
            # Not a per-viewport render manifest - e.g. capture-render.py
            # --sweep's own sweep-summary.json living in the same
            # directory glob scans land on. Disclosed and skipped, never
            # a crash, matching this file's existing posture toward any
            # other missing/unavailable capability.
            findings.append(Finding(
                severity="Note",
                message="skipped: not a per-viewport render manifest (no 'elements' field - likely a sweep-summary.json or other non-manifest JSON in this directory)",
                file=str(mp), check="rendered-layout-input",
            ))
            continue
        findings.extend(validate_manifest(manifest))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("manifest_dir", nargs="?", default=None, help="Directory of *.json manifests written by capture-render.py. Omit when passing one or more --manifest instead.")
    parser.add_argument("--manifest", action="append", help="A specific manifest JSON file; may be repeated. Overrides manifest_dir scanning if given.")
    args = parser.parse_args(argv)

    if not args.manifest and not args.manifest_dir:
        parser.error("either manifest_dir or at least one --manifest is required")

    if args.manifest:
        paths = [Path(m) for m in args.manifest]
    else:
        paths = sorted(Path(args.manifest_dir).glob("*.json"))

    if not paths:
        print("error: no manifest JSON files found", file=sys.stderr)
        return 2

    findings = validate(paths)
    blockers = [f for f in findings if f.severity == "Blocker"]
    majors = [f for f in findings if f.severity == "Major"]

    for f in findings:
        print(str(f))

    print(f"\n{len(findings)} finding(s): {len(blockers)} Blocker, {len(majors)} Major, "
          f"{len(findings) - len(blockers) - len(majors)} Minor/Note")

    # Consistent with validate-generated-artifact.py's convention: both
    # Blocker and Major fail the CLI exit code, not only Blocker — a
    # misaligned/inconsistently-sized sibling (Major) is as real a defect
    # as an overflow (Blocker), just less severe.
    return 1 if any(f.severity in ("Blocker", "Major") for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
