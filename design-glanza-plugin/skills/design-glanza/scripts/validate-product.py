"""
validate-product.py

Responsibility
--------------
The top-level product validator. Two layers, both deterministic:

1. Scaffold integrity (reused, not duplicated, from
   `create-product-builder.py`'s own `validate` subcommand):
   - product.json exists and is valid (parses, has all 10 required fields,
     product_slug matches the directory, product_type is a recognized pack).
   - product-builder/ exists.
   - SKILL.md exists.
   - Required directories exist (BRD/, output/, and all 7
     product-builder/ subdirectories).
2. Content-quality structural checks, aggregating
   `validate-requirements.py`, `validate-screens.py`, `validate-states.py`
   (B1/B5/B7), `validate-tokens.py` (B6/B8, including **B8.1**'s
   onSoft/soft semantic-contrast pass), `validate-generated-artifact.py`
   (B14's structural-validation layer), and
   `validate-data-consistency.py` (B15's Cross-Artifact Data Realism
   check) — every deterministic validator in this folder feeds this
   gate's aggregate QA status, not a subset of them.
3. Rendered-layout evidence (B14/B15/B20's render-and-measure layer,
   OPTIONAL — see below): for every `.html` file directly under
   `output/`, renders it with `capture-render.py` (desktop/tablet/mobile
   x light/dark) and runs `validate-rendered-layout.py`'s geometric
   analysis against the real rendered result — real overflow,
   alignment, spacing, sizing, and overlap findings, not source-code
   inference. Screenshots and DOM manifests are written to
   `product-builder/qa/render-capture/` so they're available to a later
   benchmark/reference-comparison pass, not discarded after this run.

Why step 3 is optional, not required, at this layer
------------------------------------------------------
Playwright is a real, heavyweight (browser-binary) dependency — every
*other* validator in this folder stays stdlib-only specifically so it
always runs, in any environment, with nothing to install
(see `capture-render.py`'s own docstring for why rendering itself is the
one deliberate exception). If Playwright isn't installed in a given
environment, this script degrades to a single Note finding explaining
that and runs every other check exactly as before — it never crashes,
and it never silently skips without saying so. This mirrors B9's existing
"agent review only, not a gap" precedent: an unavailable capability is
disclosed, not papered over. Where Playwright *is* available (install it
once: `pip install playwright && playwright install chromium`), this
step runs automatically — no flag needed to opt in — because rendering
evidence is what B15/B20 now require wherever it's obtainable.

What this deliberately does NOT check
--------------------------------------
Anything requiring reasoning or subjective judgment - see each aggregated
script's own docstring for its specific boundary. This script only combines
their structural findings into one pass/fail result; it does not itself
judge quality. `generate-report.py` renders the human-readable report from
this script's output; `agents/qa-expert.md` is where reasoning-based
judgment (the nine `methodology/test.md` dimensions, rubric scoring) lives.
**B9**'s new Alternative-component accessibility contract has no
deterministic script backing it (per `config/quality-gates.md`'s B9
"Checked by" — agent review only) and so is not, and cannot be, aggregated
here; it is not a gap in this script, there is nothing of its kind to add.
Reference-image comparison (`compare-reference-visual.py`) is also not
aggregated here — it needs a specific reference image named per-screen,
which this slug-level aggregator has no way to pick automatically; it's
invoked directly in the benchmark/audit cycle (`visual-benchmark.md`)
where that mapping is already known.

Status: implemented.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import _common
from _common import Finding

cpb = _common.load_sibling_module("create-product-builder")
vreq = _common.load_sibling_module("validate-requirements")
vscr = _common.load_sibling_module("validate-screens")
vst = _common.load_sibling_module("validate-states")
vtok = _common.load_sibling_module("validate-tokens")
vart = _common.load_sibling_module("validate-generated-artifact")
vdc = _common.load_sibling_module("validate-data-consistency")
vrl = _common.load_sibling_module("validate-rendered-layout")


def _rendered_layout_findings(output_dir: Path, capture_dir: Path) -> list[Finding]:
    """Render every output/*.html and analyze the real result. Degrades to
    one explanatory Note (never a crash, never a silent skip) if
    Playwright isn't installed in this environment."""
    html_files = sorted(output_dir.glob("*.html")) if output_dir.is_dir() else []
    if not html_files:
        return []

    crend = _common.load_sibling_module("capture-render")
    if crend.sync_playwright is None:
        return [Finding(
            "Note",
            "Rendered-layout evidence skipped: Playwright is not installed "
            "in this environment (pip install playwright && playwright "
            "install chromium to enable it). Structural/token/data checks "
            "above still ran in full.",
            "", "rendered-layout",
        )]

    findings: list[Finding] = []
    for html_path in html_files:
        out_dir = capture_dir / html_path.stem
        manifests = crend.capture(str(html_path), out_dir, crend.DEFAULT_VIEWPORTS, ["light", "dark"])
        for m in manifests:
            manifest = json.loads(Path(m["manifest"]).read_text(encoding="utf-8"))
            findings += vrl.validate_manifest(manifest)
    return findings


def validate(slug: str) -> tuple[bool, list[Finding]]:
    findings: list[Finding] = []

    scaffold_ok, scaffold_report = cpb.validate_scaffold(slug)
    for line in scaffold_report.splitlines():
        if line.strip().startswith("[FAIL]"):
            findings.append(Finding("Blocker", line.strip()[7:].strip(), "", "scaffold"))
    if not scaffold_ok:
        # Scaffold is broken enough that content checks would just report
        # "file not found" everywhere - still run them (they're graceful
        # about missing files), but the scaffold findings above already
        # explain why.
        pass

    product_dir = _common.PRODUCTS_DIR / slug
    builder_dir = product_dir / "product-builder"
    findings += vreq.validate(builder_dir)
    findings += vscr.validate(builder_dir)
    findings += vst.validate(builder_dir)
    findings += vtok.validate(builder_dir)
    findings += vart.validate(product_dir / "output")
    findings += vdc.validate(builder_dir)
    findings += _rendered_layout_findings(product_dir / "output", builder_dir / "qa" / "render-capture")

    ok = not any(f.severity in ("Blocker", "Major") for f in findings)
    return ok, findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("slug", help="product_slug under products/ to validate.")
    args = parser.parse_args(argv)

    ok, findings = validate(args.slug)
    if not findings:
        print(f"validate-product ({args.slug}): no findings. PASS")
        return 0
    for f in findings:
        print(f)
    print(f"\nOverall: {'PASS' if ok else 'FAIL'} ({len(findings)} finding(s))")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
