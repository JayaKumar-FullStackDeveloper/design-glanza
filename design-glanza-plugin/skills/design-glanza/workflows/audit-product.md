# Workflow: Audit Product

## Responsibility
The Test- and Audit-phase procedure: whether the product actually works for
its users (Test) and is correct, complete, and consistent (Audit) —
distinct from either half alone, and never satisfied by the happy path
working (`workflows/execute-product-builder.md`'s completion criteria).

## Executing agent
**`agents/qa-expert.md`**, folding in findings from
**`agents/design-system-expert.md`** (drift) and
**`agents/accessibility-expert.md`** (conformance) — both of which already
ran during Prototype and are re-consulted here, not re-run from scratch.

## Step order
Matches `workflows/execute-product-builder.md`'s actions 37-39 (Order
column — shifted from 36-37 when v1.0.11's new UX scenario-walk action was
inserted between the Test and Audit actions; before that, 34-35 after
v1.0.10's restructured Design Research actions, 32-33 after v1.0.9's new
Design Research and Visual Benchmark & Audit Cycle actions, and originally
25-26 before Design Setup's and Preview & Run's actions were inserted):

1. **Test** — run `methodology/test.md`'s all nine evaluation dimensions
   (task completion, usability, discoverability, error prevention,
   feedback, accessibility, responsiveness, edge cases, business-rule
   correctness) individually against what was actually built, not just the
   spec.
2. **Walk every UX scenario** — for every `covered`-status `SCENARIO-NNN`
   in `product-builder/ux/ux-coverage-matrix.md`, run `ux-scenario-testing/
   continuity-audit.md` against what was actually built (or the spec, for
   a planning-only engagement) and re-run `ux-scenario-testing/
   gap-detection.md`; update the matrix's Checkpoint status (Rule 22).
3. **Audit** — run `scripts/validate-product.py` (aggregating
   `validate-requirements.py`, `validate-screens.py`, `validate-states.py`).
4. Check `product-intelligence/traceability.md`'s chain for orphaned
   requirements or artifacts, and check `product-builder/research/
   research-summary.md`'s mandatory-influence table for any CRITICAL/HIGH
   `RF-NNN` finding still `open` with no cited decision/pattern or Validation
   result — an orphaned finding, per **B16**.
5. Re-run `scripts/validate-visual-regression.py` against every screen
   with an existing baseline — **B20**'s final re-check. Any Critical/
   High/Medium finding with no fix and no approved `visual-regression/
   baseline-updates.md` record is a defect, routed per that file's
   `regression-integration.md` table.
6. Fold in Design System Expert's drift findings and Accessibility Expert's
   conformance notes (re-consulted, not re-run).
7. Score against `evals/evaluation-rubric.md`'s dimensions.
8. Aggregate everything into `product-builder/qa/qa-report.md` and
   `product-builder/qa/traceability.md`, using
   `config/output-contract.md`'s shared severity vocabulary.
9. Determine overall gate status and route every finding to its owning
   agent/file per `methodology/design-thinking.md`'s feedback-routing table
   — this workflow does not fix findings itself, it routes them (Rule 13,
   `config/operating-rules.md`: fix and revalidate is the owning agent's
   job, then Test/Audit re-run only the specific failed gate).

## Gate
Must pass `config/quality-gates.md`'s **Audit → Iterate** gate:
**B10 (Traceability)**, **B11 (QA)**, **B16 (Research-to-Design
Traceability)**'s validation stage, **B17 (UX Scenario Coverage)**'s
walked checkpoint, and **B20 (Visual Regression Integrity)**'s final
re-check all green, with every earlier gate (B1-B9, B12) still holding —
a fix here that silently regresses an earlier gate reopens the scope
rather than passing by association.

## Explicitly not here
- Whether the product solves the user's problem, as a design question
  (as opposed to a build-correctness question) → `methodology/test.md`.
- The UX scenario-walk technique itself → `ux-scenario-testing/*`.
- The baseline/diff technique itself → `visual-regression/*`.
- The scoring rubric itself → `evals/evaluation-rubric.md`.
- The validator scripts' internals → `scripts/*.py`.
- Fixing a finding → whichever `agents/*.md` file the routing table sends
  it to; this workflow reports and routes, per `agents/qa-expert.md`'s own
  "must not do" list.
