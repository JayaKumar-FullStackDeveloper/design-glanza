"""
validate-screens.py

Responsibility
--------------
Deterministic, structural checks of a product's screen artifacts
(`product-builder/ux/screen-architecture.md`, cross-checked against
`requirements/requirement-matrix.md`):

- Screen IDs exist (SCREEN-NNN definitions are present).
- Screen specifications contain required sections (a keyword-presence check
  for the topics `templates/screen-specification.md` requires: region,
  component, interaction, state, responsive, accessibility - not whether
  those sections are well-written).
- Screen-to-requirement mapping exists (every SCREEN-NNN is cited from at
  least one row in requirement-matrix.md's Downstream artifacts column).

What this deliberately does NOT check
--------------------------------------
Whether a screen's layout is good, whether its content is clear, or
whether its visual hierarchy is correct - those require sighted, contextual
judgment. This script checks presence and referential integrity only.
Visual/UX quality review is `agents/ui-designer.md`'s and
`agents/ux-architect.md`'s job, not this script's.

Status: implemented.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _common import Finding, find_row_defined_ids, find_ids, read_text

REQUIRED_SECTION_KEYWORDS = [
    "region", "component", "interaction", "state", "responsive", "accessibility",
]


def validate(product_builder_dir: Path) -> list[Finding]:
    findings: list[Finding] = []
    screen_path = product_builder_dir / "ux" / "screen-architecture.md"
    screen_rel = "ux/screen-architecture.md"
    text = read_text(screen_path)

    if text is None:
        findings.append(Finding(
            "Blocker", "screen-architecture.md not found", screen_rel, "missing-file"
        ))
        return findings

    # 1. Screen IDs exist.
    defined_screens = find_row_defined_ids(text, "SCREEN")
    if not defined_screens:
        findings.append(Finding(
            "Major", "No SCREEN-NNN definitions found", screen_rel, "empty",
        ))
        return findings

    # 2. Required sections present (keyword presence only - not a quality
    #    check of what's written under each).
    lowered = text.lower()
    for keyword in REQUIRED_SECTION_KEYWORDS:
        if keyword not in lowered:
            findings.append(Finding(
                "Minor",
                f"No mention of '{keyword}' found - required topic from "
                "templates/screen-specification.md may be missing",
                screen_rel, "missing-section",
            ))

    # 3. Screen-to-requirement mapping exists.
    req_path = product_builder_dir / "requirements" / "requirement-matrix.md"
    req_text = read_text(req_path)
    if req_text is None:
        findings.append(Finding(
            "Note",
            "Cannot verify screen-to-requirement mapping - "
            "requirements/requirement-matrix.md does not exist yet",
            screen_rel, "unverifiable-reference",
        ))
    else:
        cited_screens = set(find_ids(req_text, "SCREEN"))
        for screen_id in sorted(set(defined_screens)):
            if screen_id not in cited_screens:
                findings.append(Finding(
                    "Major",
                    f"{screen_id} has no requirement mapping - not cited in any "
                    "requirement's Downstream artifacts",
                    screen_rel, "orphaned-screen",
                ))

    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("product_builder_dir", help="Path to a product-builder/ directory.")
    args = parser.parse_args(argv)

    findings = validate(Path(args.product_builder_dir))
    if not findings:
        print("validate-screens: no findings.")
        return 0
    for f in findings:
        print(f)
    return 1 if any(f.severity in ("Blocker", "Major") for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
