# Template: Research Brief

## Purpose
The kickoff record for a research pass — scope, inputs available, and the
complexity classification (`design-research/research-engine.md`'s full vs.
lightweight threshold) — written before any finding is recorded, so the
depth of research actually run is a stated decision, not an accident of how
much time was available.

## Required inputs
- The requirement/BRD material this pass researches against
  (`product-intelligence/brd-analysis.md`'s output).
- Product Architect's confirmed domain classification
  (`product-builder/domain/domain-application-notes.md`).
- Any supplied references (`design-reference-engine/reference-analysis.md`'s
  13 recognized forms) and any named competitor.

## Output structure
- **Header** — per `config/output-contract.md`.
- **Scope** — which module/feature/screen set this brief covers (a whole
  product's first pass, or one feature's narrower pass).
- **Complexity classification** — Full or Lightweight, with the stated
  reason (per `design-research/research-engine.md`): core-workflow/new-
  module → Full; small, already-understood, non-core change → Lightweight,
  citing which prior `RF-NNN` findings it reuses instead of re-researching.
- **Inputs available** — which of `design-research/research-methodology.md`'s
  research-input categories actually exist for this pass (BRD, domain
  standard, existing product, supplied reference, named competitor,
  accessibility bar, prior visual benchmarks) — and, for each one absent,
  a plain statement that it's absent rather than silence.
- **Research areas in scope** — which of User (cites Empathize)/Domain/
  Interaction/Visual will actually be researched this pass, and whether
  competitor/pattern analysis applies (only where a named reference/
  competitor exists).
- **Planned output** — which artifacts this pass will produce
  (`research-findings.md` entries, `research-summary.md`, and/or a
  `competitor-analysis.md`/`pattern-analysis.md` instance).

## Quality criteria
- The complexity classification is stated with a reason, never silently
  defaulted to Lightweight to save effort on a product that actually needs
  Full research (Rule 21).
- Every input category is addressed — present or explicitly absent, never
  omitted without comment.

## Explicitly not here
- The findings themselves → `templates/research-finding.md`.
- The roll-up once research is complete → `templates/research-summary.md`.
