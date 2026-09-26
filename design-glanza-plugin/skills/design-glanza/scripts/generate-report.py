"""
generate-report.py

Responsibility
--------------
Aggregate validate-product.py's findings into one readable QA report,
following `templates/qa-report.md`'s shape:

- Aggregate validation results (from validate-product.py).
- Identify missing artifacts (checks the known product-builder artifact
  paths from `workflows/execute-product-builder.md`'s action table against
  what actually exists, flagged only once product.json's status implies
  work has started - an empty artifact on a freshly-scaffolded product is
  expected, not a finding).
- Identify invalid references (surfaced from the aggregated findings whose
  `check` field is a referential-integrity check, not a value this script
  computes itself).
- Generate a readable QA report (rendered Markdown, written to
  `product-builder/qa/qa-report.md` or printed to stdout).

What this deliberately does NOT do
------------------------------------
This is the most important boundary in the whole validation toolchain:
this script does **not** fabricate the report sections that require
reasoning. `methodology/test.md`'s nine evaluation dimensions,
`evals/evaluation-rubric.md`'s scored dimensions, `agents/
design-system-expert.md`'s drift judgment, and `agents/
accessibility-expert.md`'s conformance judgment are all reasoning-based -
this script renders those sections as explicitly **"Not evaluated by this
script"** with a pointer to the file/agent that must produce them, rather
than inventing a score or a verdict. A script that faked a passing test
dimension or a rubric score would be worse than no report at all. Per the
instruction: prefer deterministic validation in scripts and reasoning-based
validation in Claude instructions - this script is the deterministic half
only, and says so in its own output.

Status: implemented.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import _common
from _common import Finding

vprod = _common.load_sibling_module("validate-product")

# Known product-builder artifacts, per workflows/execute-product-builder.md's
# action table. Used only to report an inventory - not a pass/fail judgment
# beyond "does the file exist yet."
EXPECTED_ARTIFACTS = [
    "requirements/brd-analysis-notes.md",
    "requirements/requirement-matrix.md",
    "requirements/business-logic.md",
    "requirements/user-roles.md",
    "requirements/dependency-analysis.md",
    "requirements/edge-cases.md",
    "product/product-definition.md",
    "domain/domain-application-notes.md",
    "ux/user-flows.md",
    "ux/sitemap.md",
    "ux/navigation.md",
    "ux/screen-architecture.md",
    "ux/ux-rules.md",
    "ux/state-matrix.md",
    "ux/accessibility.md",
    "ui/design-system.md",
    "ui/components.md",
    "ui/ui-rules.md",
    "ui/responsive-rules.md",
    "workflows/implementation-notes.md",
]

# Once status has moved past "scaffolded", a missing artifact is worth
# flagging (softly); on a freshly-scaffolded product, everything pending is
# expected and not a finding.
STATUSES_WHERE_MISSING_IS_NOTEWORTHY = {"validated", "built", "tested", "audited"}


def _severity_counts(findings: list[Finding]) -> dict[str, int]:
    counts = {s: 0 for s in _common.SEVERITIES}
    for f in findings:
        counts[f.severity] = counts.get(f.severity, 0) + 1
    return counts


def find_missing_artifacts(slug: str) -> list[str]:
    product_dir = _common.PRODUCTS_DIR / slug
    builder_dir = product_dir / "product-builder"
    product_json_path = product_dir / "product.json"

    status = "scaffolded"
    if product_json_path.is_file():
        try:
            status = json.loads(product_json_path.read_text(encoding="utf-8")).get("status", "scaffolded")
        except json.JSONDecodeError:
            pass

    missing = [a for a in EXPECTED_ARTIFACTS if not (builder_dir / a).is_file()]
    if status not in STATUSES_WHERE_MISSING_IS_NOTEWORTHY:
        return []  # expected to be pending at this stage - not a finding
    return missing


def render_report(slug: str) -> str:
    ok, findings = vprod.validate(slug)
    missing = find_missing_artifacts(slug)
    invalid_refs = [f for f in findings if f.check in (
        "dangling-reference", "orphaned-screen", "unverifiable-reference",
    )]
    counts = _severity_counts(findings)
    generated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    lines = [
        f"# QA Report - {slug}",
        "",
        f"> Generated {generated_at} by `scripts/generate-report.py` "
        "(deterministic checks only - see below).",
        "",
        "## Findings (deterministic)",
        "",
    ]
    if not findings:
        lines.append("_No structural findings._")
    else:
        for f in findings:
            lines.append(f"- {f}")
    lines += ["", "## Missing artifacts", ""]
    if not missing:
        lines.append("_None (or not yet expected at this product's current status)._")
    else:
        for path in missing:
            lines.append(f"- `{path}` - not yet produced")
    lines += ["", "## Invalid references", ""]
    if not invalid_refs:
        lines.append("_None found._")
    else:
        for f in invalid_refs:
            lines.append(f"- {f}")
    lines += [
        "",
        "## Severity summary",
        "",
        "| Severity | Count |",
        "|---|---|",
    ]
    for sev in _common.SEVERITIES:
        lines.append(f"| {sev} | {counts.get(sev, 0)} |")
    lines += [
        "",
        "## Test dimension summary (methodology/test.md)",
        "",
        "_Not evaluated by this script._ All nine dimensions (task "
        "completion, usability, discoverability, error prevention, "
        "feedback, accessibility, responsiveness, edge cases, "
        "business-rule correctness) require reasoning-based evaluation by "
        "`agents/qa-expert.md` against `methodology/test.md` - a script "
        "cannot judge whether a flow is usable or a business rule is "
        "correctly embodied. Do not treat this report as complete until "
        "that evaluation has been run and appended here.",
        "",
        "## Rubric scores (evals/evaluation-rubric.md)",
        "",
        "_Not evaluated by this script._ `evals/evaluation-rubric.md` is "
        "still architecture shell as of this report; once implemented, "
        "scoring is a reasoning-based judgment, not a script computation.",
        "",
        "## Design-system drift notes",
        "",
        "_Not evaluated by this script._ Requires `agents/"
        "design-system-expert.md`'s reuse-vs-new-variant review, which is "
        "a judgment call this toolchain does not automate.",
        "",
        "## Accessibility conformance notes",
        "",
        "_Not evaluated by this script._ This script checks structural "
        "facts only (state-matrix references, requirement mapping); full "
        "conformance (contrast values, focus order correctness) requires "
        "`agents/accessibility-expert.md`'s review.",
        "",
        "## Overall gate status",
        "",
        f"**{'PASS' if ok else 'FAIL'}** on deterministic checks "
        f"(B1, B5, B7, B10 partial). This is **not** the same as the "
        "Audit -> Iterate gate passing overall - `config/quality-gates.md`'s "
        "B2, B3, B4, B6, B8, B9, B11, B12 all require reasoning-based "
        "review this script does not perform. Per "
        "`workflows/execute-product-builder.md`'s completion criteria: a "
        "deterministic PASS here is necessary, never sufficient, for "
        "declaring the product complete.",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("slug", help="product_slug under products/ to report on.")
    parser.add_argument("--output", default=None, help="Path to write the report to (default: print to stdout).")
    args = parser.parse_args(argv)

    report = render_report(args.slug)
    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"Wrote report to {args.output}")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
