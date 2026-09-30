"""
validate-memory.py

Responsibility
--------------
Deterministic, structural checks of a product's persisted decision
records (`product-builder/memory/decision-records.md`, one or more
`ADR-NNN` blocks per `product-memory/adr-schema.md`'s shape):

- Duplicate ADR IDs.
- Required fields present and non-blank (Context, Problem, Decision,
  Reason, Alternatives considered, Impact, Status, Related).
- Status is one of the five recognized lifecycle values.
- `Supersedes`/`Superseded by` point to a real ADR defined in this same
  file, and the pairing is internally consistent (a `Supersedes` target's
  own Status is actually `superseded`; a `superseded` ADR actually has a
  `Superseded by` value).
- `Related` REQ-NNN/FLOW-NNN/SCREEN-NNN/COMPONENT-NNN citations resolve
  against their owning sibling files, the same cross-file referential
  pattern `validate-requirements.py` already uses for BR-NNN/DEP-NNN/
  EDGE-NNN.
- Two `accepted` ADRs whose `Related` sets overlap on a SCREEN-NNN or
  COMPONENT-NNN with no supersession link between them, flagged as a
  **potential** unresolved contradiction for review
  (`product-memory/contradiction-prevention.md`) — never asserted as a
  definitive semantic conflict, which is a judgment call this script does
  not make.

What this deliberately does NOT check
--------------------------------------
Whether two decisions are *actually* semantically contradictory (a
judgment call, `agents/qa-expert.md`'s job per `product-memory/
contradiction-prevention.md`), whether a decision was actually
*significant* enough to warrant an ADR in the first place
(`product-memory/auto-recording.md`, reasoning-based), or the Product
Memory index's own completeness (`product-memory/templates/
product-memory.md`'s own field-presence check, structurally identical to
this script's but over a different file — left as a natural extension
rather than duplicated here).

Status: implemented.
"""

from __future__ import annotations

import argparse
import re
import sys
from itertools import combinations
from pathlib import Path

import _common
from _common import Finding, find_row_defined_ids, read_text

VALID_STATUSES = {"proposed", "accepted", "superseded", "rejected", "deprecated"}

REQUIRED_FIELDS = [
    "Context", "Problem", "Decision", "Reason", "Alternatives considered",
    "Impact", "Status", "Related",
]

FIELD_LINE_RE = re.compile(r"^([A-Za-z][A-Za-z /]*?):\s*(.*)$")

# Sibling files a Related citation might resolve against, per
# product-intelligence/traceability.md's chain. Mirrors
# validate-requirements.py's own sibling_files dict.
SIBLING_FILES = {
    "REQ": ("requirements", "requirement-matrix.md"),
    "FLOW": ("ux", "user-flows.md"),
    "SCREEN": ("ux", "screen-architecture.md"),
    "COMPONENT": ("ui", "components.md"),
}


def _split_blocks(text: str) -> list[list[str]]:
    """Split decision-records.md into one line-list per 'ID: ADR-NNN'
    block, up to (not including) the next such line or EOF."""
    lines = text.splitlines()
    starts = [i for i, line in enumerate(lines) if re.match(r"^ID:\s*ADR-\d+", line.strip())]
    blocks = []
    for idx, start in enumerate(starts):
        end = starts[idx + 1] if idx + 1 < len(starts) else len(lines)
        blocks.append(lines[start:end])
    return blocks


def _parse_block(block_lines: list[str]) -> dict:
    fields: dict[str, str] = {}
    for line in block_lines:
        stripped = line.strip()
        match = FIELD_LINE_RE.match(stripped)
        if not match:
            continue
        key, value = match.group(1).strip(), match.group(2).strip()
        if key not in fields:  # first occurrence wins (the field's own line)
            fields[key] = value
    return fields


def validate(product_builder_dir: Path) -> list[Finding]:
    findings: list[Finding] = []
    path = product_builder_dir / "memory" / "decision-records.md"
    rel = "memory/decision-records.md"
    text = read_text(path)

    if text is None:
        findings.append(Finding(
            "Note", "decision-records.md not found - no ADRs recorded yet",
            rel, "missing-file",
        ))
        return findings

    blocks = _split_blocks(text)
    if not blocks:
        findings.append(Finding(
            "Note", "No ID: ADR-NNN blocks found - file exists but is empty",
            rel, "empty",
        ))
        return findings

    records: dict[str, dict] = {}
    seen_ids: dict[str, int] = {}

    for block_lines in blocks:
        fields = _parse_block(block_lines)
        adr_id = fields.get("ID", "")
        if not adr_id:
            continue
        seen_ids[adr_id] = seen_ids.get(adr_id, 0) + 1
        records[adr_id] = fields  # last-defined wins for content checks below

    for adr_id, count in seen_ids.items():
        if count > 1:
            findings.append(Finding(
                "Blocker", f"Duplicate ADR ID {adr_id} defined {count} times",
                rel, "duplicate-id",
            ))

    for adr_id, fields in records.items():
        for field in REQUIRED_FIELDS:
            if not fields.get(field):
                findings.append(Finding(
                    "Major", f"{adr_id}: missing or blank '{field}' field",
                    rel, "missing-field",
                ))

        status = fields.get("Status", "")
        if status and status not in VALID_STATUSES:
            findings.append(Finding(
                "Major",
                f"{adr_id}: Status '{status}' is not one of {sorted(VALID_STATUSES)}",
                rel, "invalid-status",
            ))

        supersedes = fields.get("Supersedes", "")
        if supersedes:
            if supersedes not in records:
                findings.append(Finding(
                    "Major", f"{adr_id}: Supersedes '{supersedes}' has no matching ADR in this file",
                    rel, "dangling-supersedes",
                ))
            elif records[supersedes].get("Status") != "superseded":
                findings.append(Finding(
                    "Major",
                    f"{adr_id}: supersedes {supersedes}, but {supersedes}'s own "
                    f"Status is '{records[supersedes].get('Status')}', not 'superseded'",
                    rel, "inconsistent-supersession",
                ))

        superseded_by = fields.get("Superseded by", "")
        if superseded_by and superseded_by not in records:
            findings.append(Finding(
                "Major", f"{adr_id}: Superseded by '{superseded_by}' has no matching ADR in this file",
                rel, "dangling-superseded-by",
            ))
        if status == "superseded" and not superseded_by:
            findings.append(Finding(
                "Major", f"{adr_id}: Status is 'superseded' but no 'Superseded by' value is recorded",
                rel, "missing-superseded-by",
            ))

        if "Related" in fields and not fields["Related"]:
            findings.append(Finding(
                "Minor", f"{adr_id}: no Related citation — governs nothing traceable",
                rel, "no-related-citation",
            ))

    # Cross-file referential integrity for Related citations.
    for adr_id, fields in records.items():
        related = fields.get("Related", "")
        if not related:
            continue
        for scheme, (subdir, filename) in SIBLING_FILES.items():
            cited = set(_common.find_ids(related, scheme))
            if not cited:
                continue
            sibling_path = product_builder_dir / subdir / filename
            sibling_text = read_text(sibling_path)
            if sibling_text is None:
                findings.append(Finding(
                    "Note",
                    f"{adr_id}: {len(cited)} {scheme}-NNN reference(s) cannot be "
                    f"verified - {subdir}/{filename} does not exist yet",
                    rel, "unverifiable-reference",
                ))
                continue
            defined = set(find_row_defined_ids(sibling_text, scheme))
            for missing in sorted(cited - defined):
                findings.append(Finding(
                    "Major",
                    f"{adr_id}: Related cites {missing}, no defining row in {subdir}/{filename}",
                    rel, "dangling-reference",
                ))

    # Potential unresolved contradictions: two `accepted` ADRs whose
    # Related sets overlap on a SCREEN/COMPONENT, with no direct
    # supersession link between them either way.
    accepted = [
        (adr_id, fields) for adr_id, fields in records.items()
        if fields.get("Status") == "accepted"
    ]
    for (id_a, fields_a), (id_b, fields_b) in combinations(accepted, 2):
        related_a = set(re.findall(r"\b(?:SCREEN|COMPONENT)-\d+\b", fields_a.get("Related", "")))
        related_b = set(re.findall(r"\b(?:SCREEN|COMPONENT)-\d+\b", fields_b.get("Related", "")))
        overlap = related_a & related_b
        if not overlap:
            continue
        linked = (
            fields_a.get("Supersedes") == id_b or fields_b.get("Supersedes") == id_a
        )
        if linked:
            continue
        findings.append(Finding(
            "Minor",
            f"{id_a} and {id_b} both 'accepted', both govern {sorted(overlap)}, "
            "with no supersession link between them — potential unresolved "
            "contradiction, needs review (not a confirmed conflict)",
            rel, "potential-contradiction",
        ))

    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("product_builder_dir", help="Path to a product-builder/ directory.")
    args = parser.parse_args(argv)

    findings = validate(Path(args.product_builder_dir))
    if not findings:
        print("validate-memory: no findings.")
        return 0
    for f in findings:
        print(f)
    return 1 if any(f.severity in ("Blocker", "Major") for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
