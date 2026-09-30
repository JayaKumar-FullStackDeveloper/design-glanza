# Template: UX Coverage Matrix

## Purpose
The full roll-up artifact `config/quality-gates.md`'s **B17** is checked
against — every `FLOW-NNN` × every scenario type, per
`ux-scenario-testing/coverage-matrix.md`'s shape.

## Required inputs
- Every `SCENARIO-NNN` record (`templates/scenario.md`) produced for this
  product.
- `ux-scenario-testing/{gap-detection,continuity-audit}.md` findings.

## Output structure
- **Header** — per `config/output-contract.md`.
- **Matrix** — one row per `FLOW-NNN`, one column per scenario type, per
  `ux-scenario-testing/coverage-matrix.md`'s exact shape. Zero blank
  cells.
- **Open findings** — every `gap-detection.md`/`continuity-audit.md`
  finding not yet resolved, in the same shape those files define, grouped
  by routing target (`agents/*.md`).
- **Checkpoint status** — B17's two checkpoints (spec-level,
  Prototype → Implement; walked, Audit → Iterate), each pass/fail with the
  specific blocking finding(s) if fail.
- **Not-applicable log** — every N/A cell with its stated reason, so a
  reviewer can see the omission was a decision, not an oversight.

## Quality criteria
- Every `FLOW-NNN` in `ux/user-flows.md` has a row — a flow with no
  matrix row at all is itself a Blocker-severity gap.
- Every cell is `SCENARIO-NNN: <status>`, `N/A (<reason>)`, or `deferred
  (<reason>)` — never blank.
- A `covered` status never coexists with an open Blocker/Major finding
  against that same `SCENARIO-NNN`.

## Traceability fields
Every `SCENARIO-NNN` cited here traces to its `FLOW-NNN`, and transitively
to the `REQ-NNN`/`ROLE-NNN` that flow serves
(`product-intelligence/traceability.md`'s existing chain) — this matrix
adds a new sideways-reference layer, it does not fork the chain.

## Explicitly not here
- Individual scenario detail → `templates/scenario.md`.
- The gate's exact two-checkpoint pass criteria →
  `ux-scenario-testing/coverage-matrix.md`, `config/quality-gates.md`.
