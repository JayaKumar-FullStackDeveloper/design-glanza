"""
validate-states.py

Responsibility
--------------
Deterministic, structural checks of a product's state matrix
(`product-builder/ux/state-matrix.md`):

- Required states are represented: all 13 mandatory states from Rule 6
  (`config/operating-rules.md`) appear as column headers, and no data row
  has a blank cell (config/quality-gates.md's B7 zero-blank-cells rule,
  checked mechanically here).
- State references are valid: any EDGE-NNN cited in a cell has a defining
  row in `requirements/edge-cases.md`, when that file exists.

What this deliberately does NOT check
--------------------------------------
Whether a state's *designed behavior* is good UX, or whether "not
applicable" was the right call for a given cell - those require judgment.
This script only checks that every cell has *something* in it (or an
explicit not-applicable/deferred marker) and that cited edge cases exist;
whether the something is well-designed is `agents/interaction-designer.md`'s
and `agents/qa-expert.md`'s job, not this script's.

Status: implemented.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _common import Finding, MANDATORY_STATES, find_ids, find_row_defined_ids, read_text, split_table_rows


def validate(product_builder_dir: Path) -> list[Finding]:
    findings: list[Finding] = []
    state_path = product_builder_dir / "ux" / "state-matrix.md"
    state_rel = "ux/state-matrix.md"
    text = read_text(state_path)

    if text is None:
        findings.append(Finding(
            "Blocker", "state-matrix.md not found", state_rel, "missing-file"
        ))
        return findings

    rows = split_table_rows(text)
    if not rows:
        findings.append(Finding(
            "Major", "No markdown table found in state-matrix.md", state_rel, "empty",
        ))
        return findings

    header = rows[0]
    header_lower = [h.lower() for h in header]

    # 1a. Required states represented as columns.
    for state in MANDATORY_STATES:
        if not any(state in col for col in header_lower):
            findings.append(Finding(
                "Major",
                f"State matrix header is missing the mandatory '{state}' column "
                "(Rule 6, config/operating-rules.md)",
                state_rel, "missing-state-column",
            ))

    # 1b. Zero-blank-cells rule (B7) - every data row's cells, aligned to
    #     the header's column count, must be non-empty.
    data_rows = rows[1:]
    col_count = len(header)
    for row in data_rows:
        if not row or not row[0]:
            continue
        row_label = row[0]
        # Pad/compare only up to the shorter of the two - a row with fewer
        # cells than the header is itself a structural gap, reported once.
        if len(row) != col_count:
            findings.append(Finding(
                "Minor",
                f"{row_label}: row has {len(row)} cells, header has {col_count} "
                "- row may be missing a state column",
                state_rel, "row-column-mismatch",
            ))
        blanks = sum(1 for cell in row[1:] if not cell)
        if blanks:
            findings.append(Finding(
                "Blocker",
                f"{row_label}: {blanks} blank state cell(s) - every cell must be "
                "designed / not-applicable (with reason) / deferred (with reason)",
                state_rel, "blank-cell",
            ))

    # 2. State references are valid - EDGE-NNN cells cross-checked against
    #    requirements/edge-cases.md.
    cited_edges = set(find_ids(text, "EDGE"))
    if cited_edges:
        edge_path = product_builder_dir / "requirements" / "edge-cases.md"
        edge_text = read_text(edge_path)
        if edge_text is None:
            findings.append(Finding(
                "Note",
                f"{len(cited_edges)} EDGE-NNN reference(s) cannot be verified - "
                "requirements/edge-cases.md does not exist yet",
                state_rel, "unverifiable-reference",
            ))
        else:
            defined_edges = set(find_row_defined_ids(edge_text, "EDGE"))
            for edge_id in sorted(cited_edges - defined_edges):
                findings.append(Finding(
                    "Major",
                    f"Reference to {edge_id} has no defining row in edge-cases.md",
                    state_rel, "dangling-reference",
                ))

    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("product_builder_dir", help="Path to a product-builder/ directory.")
    args = parser.parse_args(argv)

    findings = validate(Path(args.product_builder_dir))
    if not findings:
        print("validate-states: no findings.")
        return 0
    for f in findings:
        print(f)
    return 1 if any(f.severity in ("Blocker", "Major") for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
