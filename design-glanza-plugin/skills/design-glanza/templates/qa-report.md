# Template: QA Report

## Purpose
The Audit phase's output — the record that proves (or disproves) that a
product is actually complete, not just that its happy path works. Reusable
across every domain: findings, severities, and gate status are a fixed
vocabulary regardless of what was audited.

## Required inputs
- `workflows/audit-product.md`'s procedure output.
- `scripts/validate-product.py` (aggregating `validate-requirements.py`,
  `validate-screens.py`, `validate-states.py`) results.
- `evals/evaluation-rubric.md` scores.
- `product-intelligence/traceability.md`'s trace record.
- `product-builder/research/research-summary.md`'s mandatory-influence
  table (Rule 21, `config/quality-gates.md`'s **B16**).
- `product-builder/ux/ux-coverage-matrix.md` and its Checkpoint status
  (Rule 22, `config/quality-gates.md`'s **B17**).
- `visual-regression/templates/visual-diff-report.md` instances (Rule 25,
  `config/quality-gates.md`'s **B20**).
- `product-builder/memory/{product-memory,decision-records}.md` and
  `scripts/validate-memory.py` results (Rule 26, `config/quality-gates.md`'s
  **B21**).
- `agents/design-system-expert.md` and `agents/accessibility-expert.md`
  review notes.
- `methodology/test.md`'s 9-dimension evaluation results for the scope being
  audited.

## Output structure
- **Header** — per `config/output-contract.md`.
- **Findings list** — one per issue: description, severity
  (`config/output-contract.md` vocabulary), owning file/phase for the fix,
  status (open/fixed/deferred).
- **Traceability summary** — orphan requirements/artifacts found, per
  `product-intelligence/traceability.md`, including any CRITICAL/HIGH
  `RF-NNN` research finding with no cited decision/pattern or Validation
  result (**B16**), any `FLOW-NNN` with no `SCENARIO-NNN` coverage or an
  unresolved continuity/gap finding (**B17**), any screen with an
  unresolved Critical/High/Medium visual-diff finding and no approved
  Baseline Update (**B20**), and any significant decision with no
  `ADR-NNN`, or any flagged potential contradiction left unreviewed
  (**B21**).
- **Validator results** — pass/fail summary from `scripts/validate-*.py`.
- **Rubric scores** — per `evals/evaluation-rubric.md` dimensions.
- **Design-system drift notes** — from `agents/design-system-expert.md`.
- **Accessibility conformance notes** — from `agents/accessibility-expert.md`.
- **Test dimension summary** — pass/fail per one of `methodology/test.md`'s
  9 dimensions, explicitly — not collapsed into one overall verdict.
- **Overall gate status** — pass/fail against
  `config/quality-gates.md`'s Audit → Iterate gate.

## Quality criteria
- Every finding has both a severity and a named owning file/phase — a
  finding with neither is not actionable and is itself a defect in the
  report.
- The Test dimension summary reports **all nine** dimensions individually;
  a report that only states "core functionality works" without addressing
  the other eight is rejected on its face, per
  `workflows/execute-product-builder.md`'s completion criteria — the happy
  path working is never sufficient grounds to mark the product complete.
- Overall gate status is explicit pass/fail, never implied — "mostly
  ready" is not a valid value.
- Checked against `config/quality-gates.md`'s **B10 — Traceability** and
  **B11 — QA** gates directly; this report *is* the artifact those two
  gates are checked against.

## Example structure
_Illustrative only — placeholders, not a real audit._

```
Findings:
  [Blocker] SCREEN-011 missing a system-error recovery path
            owner: ux-engine/user-flow-engine.md (FLOW-006) | status: open
  [Minor]   COMPONENT-004 label capitalization inconsistent with content
            rules | owner: ui-engine/component-system.md | status: fixed

Traceability summary: 0 orphaned requirements; 1 orphaned screen (SCREEN-020,
  no REQ-NNN found - routed back to Define for scope confirmation)

Test dimension summary:
  1. Task completion - pass       6. Accessibility - fail (see finding above)
  2. Usability - pass             7. Responsiveness - pass
  3. Discoverability - pass       8. Edge cases - pass
  4. Error prevention - pass      9. Business-rule correctness - pass
  5. Feedback - pass

Overall gate status: FAIL (1 Blocker open) - not complete despite 8/9 Test
  dimensions passing.
```

## Traceability fields
Cites `REQ-NNN`, `FLOW-NNN`, `SCREEN-NNN`, `COMPONENT-NNN`, and `TEST-NNN`
per finding, as applicable — this report is where the full
`product-intelligence/traceability.md` chain gets exercised end to end.

## Explicitly not here
- How findings are generated → `workflows/audit-product.md` and the
  agents/scripts it invokes.
- The scoring rubric's dimensions/definitions → `evals/evaluation-rubric.md`.
- The severity vocabulary itself → `config/output-contract.md`.
