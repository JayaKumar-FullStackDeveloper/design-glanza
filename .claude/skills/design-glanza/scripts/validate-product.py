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
   `validate-requirements.py`, `validate-screens.py`, and
   `validate-states.py`.

What this deliberately does NOT check
--------------------------------------
Anything requiring reasoning or subjective judgment - see each aggregated
script's own docstring for its specific boundary. This script only combines
their structural findings into one pass/fail result; it does not itself
judge quality. `generate-report.py` renders the human-readable report from
this script's output; `agents/qa-expert.md` is where reasoning-based
judgment (the nine `methodology/test.md` dimensions, rubric scoring) lives.

Status: implemented.
"""

from __future__ import annotations

import argparse
import sys

import _common
from _common import Finding

cpb = _common.load_sibling_module("create-product-builder")
vreq = _common.load_sibling_module("validate-requirements")
vscr = _common.load_sibling_module("validate-screens")
vst = _common.load_sibling_module("validate-states")


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

    builder_dir = _common.PRODUCTS_DIR / slug / "product-builder"
    findings += vreq.validate(builder_dir)
    findings += vscr.validate(builder_dir)
    findings += vst.validate(builder_dir)

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
