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
Matches `workflows/execute-product-builder.md`'s actions 32-33 (Order
column — shifted from the original 25-26 by Design Setup's 5 actions and
Preview & Run's 2 actions, both inserted earlier in the table):

1. **Test** — run `methodology/test.md`'s all nine evaluation dimensions
   (task completion, usability, discoverability, error prevention,
   feedback, accessibility, responsiveness, edge cases, business-rule
   correctness) individually against what was actually built, not just the
   spec.
2. **Audit** — run `scripts/validate-product.py` (aggregating
   `validate-requirements.py`, `validate-screens.py`, `validate-states.py`).
3. Check `product-intelligence/traceability.md`'s chain for orphaned
   requirements or artifacts.
4. Fold in Design System Expert's drift findings and Accessibility Expert's
   conformance notes (re-consulted, not re-run).
5. Score against `evals/evaluation-rubric.md`'s dimensions.
6. Aggregate everything into `product-builder/qa/qa-report.md` and
   `product-builder/qa/traceability.md`, using
   `config/output-contract.md`'s shared severity vocabulary.
7. Determine overall gate status and route every finding to its owning
   agent/file per `methodology/design-thinking.md`'s feedback-routing table
   — this workflow does not fix findings itself, it routes them (Rule 13,
   `config/operating-rules.md`: fix and revalidate is the owning agent's
   job, then Test/Audit re-run only the specific failed gate).

## Gate
Must pass `config/quality-gates.md`'s **Audit → Iterate** gate:
**B10 (Traceability)** and **B11 (QA)** both green, with every earlier gate
(B1-B9, B12) still holding — a fix here that silently regresses an earlier
gate reopens the scope rather than passing by association.

## Explicitly not here
- Whether the product solves the user's problem, as a design question
  (as opposed to a build-correctness question) → `methodology/test.md`.
- The scoring rubric itself → `evals/evaluation-rubric.md`.
- The validator scripts' internals → `scripts/*.py`.
- Fixing a finding → whichever `agents/*.md` file the routing table sends
  it to; this workflow reports and routes, per `agents/qa-expert.md`'s own
  "must not do" list.
