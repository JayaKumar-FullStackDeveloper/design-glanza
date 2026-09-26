"""
validate-requirements.py

Responsibility
--------------
Deterministic, structural checks of a product's requirement model
(`product-builder/requirements/requirement-matrix.md`, and its sibling
`business-logic.md` / `user-roles.md` / `dependency-analysis.md` /
`edge-cases.md` files where present):

- Requirement IDs exist (the file isn't empty of REQ-NNN definitions).
- Duplicate IDs are detected (the same REQ-NNN defined more than once).
- Required requirement fields exist (the table header names every field
  `product-intelligence/requirement-engine.md` requires, and no defined
  row is missing a cell for one).
- Traceability references are valid (every REQ-NNN/BR-NNN/DEP-NNN cited
  from a row actually has a defining row somewhere it can be checked).

What this deliberately does NOT check
--------------------------------------
Whether a requirement's *description* is well-written, whether its
*business rule* is correct, or whether its *priority* is sensible — those
are judgment calls. Per the instruction to prefer deterministic validation
in scripts and reasoning-based validation in Claude instructions, this
script only checks structural facts (existence, uniqueness, completeness of
cells, referential integrity) — never quality. Content-quality review is
`agents/brd-analyst.md`'s and `agents/qa-expert.md`'s job, reasoning against
`config/quality-gates.md`'s B1/B2 criteria, not this script's.

Status: implemented.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import _common
from _common import Finding, find_row_defined_ids, read_text, split_table_rows

# The field schema owned by product-intelligence/requirement-engine.md and
# templates/requirement-matrix.md. Checked as header-column presence, not
# exact position - authored tables vary in column order.
REQUIRED_FIELDS = [
    "id", "source", "description", "type", "actor", "action",
    "system response", "business rule", "validation", "dependency",
    "confidence", "priority", "status", "downstream",
]


def _header_row(text: str) -> list[str] | None:
    rows = split_table_rows(text)
    return rows[0] if rows else None


def validate(product_builder_dir: Path) -> list[Finding]:
    findings: list[Finding] = []
    req_path = product_builder_dir / "requirements" / "requirement-matrix.md"
    req_rel = "requirements/requirement-matrix.md"
    text = read_text(req_path)

    if text is None:
        findings.append(Finding(
            "Blocker", "requirement-matrix.md not found", req_rel, "missing-file"
        ))
        return findings

    # 1. Requirement IDs exist.
    defined_ids = find_row_defined_ids(text, "REQ")
    if not defined_ids:
        findings.append(Finding(
            "Major", "No REQ-NNN requirement rows found - matrix is empty",
            req_rel, "empty",
        ))
        return findings

    # 2. Duplicate IDs.
    seen: dict[str, int] = {}
    for rid in defined_ids:
        seen[rid] = seen.get(rid, 0) + 1
    for rid, count in seen.items():
        if count > 1:
            findings.append(Finding(
                "Blocker", f"Duplicate requirement ID {rid} defined {count} times",
                req_rel, "duplicate-id",
            ))

    # 3. Required fields present (header-level check) and no blank cells in
    #    defined rows (row-level check).
    header = _header_row(text)
    if header is None:
        findings.append(Finding(
            "Major", "No markdown table header found in requirement-matrix.md",
            req_rel, "missing-header",
        ))
    else:
        header_lower = " | ".join(header).lower()
        for field in REQUIRED_FIELDS:
            if field not in header_lower:
                findings.append(Finding(
                    "Major", f"Requirement matrix header is missing a '{field}' column",
                    req_rel, "missing-field",
                ))

    for row in split_table_rows(text):
        if not row or not row[0].startswith("REQ-"):
            continue
        blanks = [i for i, cell in enumerate(row) if not cell]
        if blanks:
            findings.append(Finding(
                "Minor",
                f"{row[0]}: {len(blanks)} blank cell(s) in its row",
                req_rel, "blank-cell",
            ))

    # 4. Traceability references are valid - every REQ-NNN cited anywhere in
    #    the file (e.g. a Dependency column) must be one of this file's own
    #    defined IDs; BR-NNN/DEP-NNN/EDGE-NNN citations are cross-checked
    #    against sibling files when those exist.
    defined_set = set(defined_ids)
    cited = set(_common.find_ids(text, "REQ"))
    dangling_req = cited - defined_set
    for rid in sorted(dangling_req):
        findings.append(Finding(
            "Major", f"Reference to {rid} has no defining row in this file",
            req_rel, "dangling-reference",
        ))

    sibling_files = {
        "BR": product_builder_dir / "requirements" / "business-logic.md",
        "DEP": product_builder_dir / "requirements" / "dependency-analysis.md",
        "EDGE": product_builder_dir / "requirements" / "edge-cases.md",
    }
    for scheme, sibling_path in sibling_files.items():
        cited_ids = set(_common.find_ids(text, scheme))
        if not cited_ids:
            continue
        sibling_text = read_text(sibling_path)
        if sibling_text is None:
            findings.append(Finding(
                "Note",
                f"{len(cited_ids)} {scheme}-NNN reference(s) cannot be verified - "
                f"{sibling_path.name} does not exist yet",
                req_rel, "unverifiable-reference",
            ))
            continue
        sibling_defined = set(find_row_defined_ids(sibling_text, scheme))
        for rid in sorted(cited_ids - sibling_defined):
            findings.append(Finding(
                "Major",
                f"Reference to {rid} has no defining row in {sibling_path.name}",
                req_rel, "dangling-reference",
            ))

    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("product_builder_dir", help="Path to a product-builder/ directory.")
    args = parser.parse_args(argv)

    findings = validate(Path(args.product_builder_dir))
    if not findings:
        print("validate-requirements: no findings.")
        return 0
    for f in findings:
        print(f)
    return 1 if any(f.severity in ("Blocker", "Major") for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
