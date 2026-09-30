# Memory Integration

## Responsibility
The explicit wiring into the Quality Engine, Component Registry, Design
Tokens, and UX Scenario Testing this task asked for by name — each is
already citable through its own existing mechanism; this file states the
concrete connection point rather than leaving the integration implicit.

## Quality Engine
- **`config/quality-gates.md`**'s new **B21 (Product Memory Integrity)**,
  checked at two points: (1) Prototype/Design-time — the acting agent
  states which of `consultation-rule.md`'s three outcomes applied before
  proceeding; (2) Audit — `agents/qa-expert.md` runs `scripts/
  validate-memory.py` and reviews any flagged overlapping-Related,
  no-supersession ADR pair.
- **`templates/qa-report.md`** — an unresolved memory-integrity finding
  (a missing ADR for a significant decision, or a flagged potential
  contradiction) folds into the existing Findings list, same severity
  vocabulary, never a parallel report.
- **`evals/evaluation-rubric.md`** gains a matching Tier B dimension.

## Component Registry
`component-registry/registry-integration.md`'s registry-first check now
runs *inside* `consultation-rule.md`'s lookup, not as a second, separate
scan — checking the master registry and checking Product Memory's prior
component ADRs happen together, since both answer the same question
("has this need already been decided"). A registry-first "no match, new
component" call is always significant (`auto-recording.md`) and always
gets an ADR — this is the one registry-integration.md event that was
previously logged only in `components.md`'s own inventory, now also
indexed in Product Memory so a *different* screen's later pass can find
it without re-discovering the same gap.

## Design Tokens
`design-tokens/token-inheritance.md`'s override rules (which paths a
product may set vs. which stay closed) are themselves architecture-level
decisions — a product's first departure from a master default (a brand
primary hue, a `product.*` addition) gets an ADR the first time, per
`auto-recording.md`'s significance criteria ("departs from... a closed
token scale, with a stated reason"); every *subsequent* screen using that
same already-decided token value just cites the existing ADR, it doesn't
re-litigate the choice.

## UX Scenario Testing
`ux-scenario-testing/coverage-matrix.md`'s `not-applicable`/`deferred`
cells (a scenario type deliberately not covered, with a stated reason)
are exactly the kind of decision Product Memory indexes — a `not-
applicable` call on a core-workflow flow is significant and gets an ADR;
a `not-applicable` call that's genuinely obvious (no Offline scenario on
a server-side batch flow) stays in the matrix's own cell, per `auto-
recording.md`'s proportionality. `ux-scenario-testing/scenario-model.md`'s
**UI interactions** field — the binding from a scenario step to a real
`COMPONENT-NNN` — is what a Product Memory contradiction check actually
walks: two scenarios binding to contradictory component decisions with no
supersession link is `contradiction-prevention.md`'s concrete failure
case for this integration specifically.

## Explicitly not here
- Each integrated system's own technique → `component-registry/*`,
  `design-tokens/*`, `ux-scenario-testing/*` (cited above, never
  restated).
- B21's exact pass criterion → `config/quality-gates.md`.
- The validator's own implementation → `scripts/validate-memory.py`.
