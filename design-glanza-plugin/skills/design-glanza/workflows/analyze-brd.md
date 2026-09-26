# Workflow: Analyze BRD

## Responsibility
The operational, step-by-step Intake procedure: applies
`product-intelligence/brd-analysis.md`'s method to one real input and produces
a filled requirement model. This is "how to actually run it," not the
extraction method itself — that's owned by the `product-intelligence/*`
files this workflow sequences.

## Executing agent
`agents/brd-analyst.md`, invoked once per product at the start of Intake.
Does not self-invoke again mid-pipeline; a gap discovered later routes back
here through `methodology/design-thinking.md`'s feedback table instead of
the agent re-running unprompted.

## Step order
Matches `agents/brd-analyst.md`'s analysis procedure and
`workflows/execute-product-builder.md`'s actions 1, 2, 4-8, in this order:

1. Identify input type(s) present in `products/<slug>/BRD/` and their
   extraction posture (`brd-analysis.md`).
2. Run the full 20-point checklist — **business-logic items are never
   skipped for a UI-only input** — writing raw findings to
   `product-builder/requirements/brd-analysis-notes.md`.
3. Decompose into atomic `REQ-NNN` (`requirement-engine.md`) →
   `product-builder/requirements/requirement-matrix.md`.
4. Derive business rules into `BR-NNN` (`business-logic.md`), including
   backend-assumption derivation for flagged gaps →
   `product-builder/requirements/business-logic.md`.
5. Identify actors and permissions into `ROLE-NNN` (`user-roles.md`) →
   `product-builder/requirements/user-roles.md`.
6. Map initial dependencies into `DEP-NNN` (`dependency-analysis.md`) →
   `product-builder/requirements/dependency-analysis.md`.
7. Enumerate edge cases into `EDGE-NNN` (`edge-case-engine.md`) →
   `product-builder/requirements/edge-cases.md`.
8. Run an initial domain classification with stated confidence
   (`domain-classifier.md`) — handed to `agents/product-architect.md` for
   confirmation at Architect, not finalized here.

## Gate
Must pass `config/quality-gates.md`'s **Intake → Empathize** phase gate,
which resolves to **B1 (Requirement Completeness)** and
**B2 (Business Logic Completeness)** both passing
(`scripts/validate-requirements.py`), before Empathize may begin.

## Definition of done
Every `product-builder/requirements/*` file above exists, every entry
carries a source or `[ASSUMPTION: ...]` tag, and an initial domain
classification with confidence is recorded — per
`config/output-contract.md`'s phase-completion report shape.

## Explicitly not here
- The extraction method/categories themselves →
  `product-intelligence/brd-analysis.md`.
- The requirement-matrix document fields → `templates/requirement-matrix.md`.
- What happens after Intake (Empathize onward) → `create-product.md`,
  `workflows/execute-product-builder.md`.
- The agent's own scope boundaries → `agents/brd-analyst.md`.
