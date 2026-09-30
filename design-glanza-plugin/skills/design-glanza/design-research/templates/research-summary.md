# Template: Research Summary

## Purpose
The roll-up view across every `RF-NNN` finding produced this pass — what
was found, by priority and area, and which findings actually influenced the
design vs. were deferred/rejected. This is the artifact
`agents/design-setup-specialist.md` folds into `ui/design-direction.md`'s
Design principles field (the condensed version), and what Audit checks
against for **B16**.

## Required inputs
- Every `RF-NNN` finding from this pass (`templates/research-finding.md`
  instances in `product-builder/research/research-findings.md`).

## Output structure
- **Header** — per `config/output-contract.md`.
- **Findings by priority** — a count and one-line list per priority
  (CRITICAL/HIGH/MEDIUM/LOW), each line: ID, one-sentence Insight, Status.
- **Findings by area** — the same findings grouped by User/Domain/
  Interaction/Visual/Competitor/Pattern, so a reviewer can see whether any
  area was under-researched.
- **Mandatory-influence check** — every CRITICAL/HIGH finding listed with
  its Status: `applied` (with the citing UX Decision/UI Pattern artifact),
  `deferred` (with the stated reason), or `open` (flagged — this is the
  B16 failure condition if it persists past Design Setup → Prototype).
- **Researched-and-rejected register** — every pattern that failed the
  Anti-Generic Design challenge, with its reason, so a later reviewer
  doesn't re-propose the same pattern without seeing it was already
  considered and rejected (mirrors `methodology/ideate.md`'s rejected-
  concepts register).
- **Design principles derived** — the condensed list feeding
  `ui/design-direction.md`'s own Design principles field.
- **Areas not researched, and why** — an explicit statement for any of
  User/Domain/Interaction/Visual not covered this pass (e.g. Lightweight
  complexity classification, per `research-engine.md`), never silently
  absent.

## Quality criteria
- Every CRITICAL/HIGH finding appears in the mandatory-influence check with
  a real status — none silently omitted.
- The researched-and-rejected register is non-empty for any product where
  the Anti-Generic Design challenge actually ran and rejected at least one
  candidate — an empty register on a product with several common patterns
  in play is itself worth a second look (did the challenge actually run?).

## Traceability fields
This is the artifact `config/quality-gates.md`'s **B16** is checked
against directly, the same relationship `templates/qa-report.md` has to
B10/B11.

## Explicitly not here
- Individual finding detail → `templates/research-finding.md`.
- How a finding is produced in the first place → `design-research/
  research-methodology.md` and the area-specific files it indexes.
- The priority classification and mandatory-influence rule themselves →
  `design-research/research-to-design.md`.
