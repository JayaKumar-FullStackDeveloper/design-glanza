# Use Case: Healthcare (Greenfield)

## Responsibility
A validated, concrete worked example of Design-Glanza building a greenfield
healthcare/clinical product, applying the `product-types/healthcare.md`
overlay.

## Routes through Design-Glanza — not a separate skill
Executed by the same master skill as every other use case here — only the
applied `product-types/*.md` pack and the specific emphases below differ.

## Input
Often a described clinical workflow (e.g. appointment scheduling) with **no
named regulation** — regulatory context is frequently implied, never
stated.

## Classification
Signals: "patient," "appointment," "clinical," "provider" →
`product-types/healthcare.md`. Confidence in the *domain* match is usually
high even when confidence in specific *regulatory* facts is low — these are
tracked separately, never conflated.

## Analysis
This is where Rule 10 (`config/operating-rules.md`) is exercised hardest of
any domain: `brd-analysis.md`'s gap detection flags every unstated
regulatory/consent question explicitly, and **no specific regulatory regime
is ever assumed** — each gap becomes a tagged, impact-stated assumption in
`product/product-definition.md`, not a silent default.
`edge-case-engine.md`'s "double-booked resource" and "clinical note left
in-progress" categories get full treatment given the safety stakes.

## Required artifacts
`product/product-definition.md`'s assumptions section is unusually long and
is surfaced prominently, not buried — a reviewer must be able to see every
open regulatory/consent question at a glance. `ux/state-matrix.md`'s
error/permission-denied states get extra design rigor: per
`healthcare.md`, a clinically significant action never loses its
confirmation step for the sake of "fewer clicks."

## Design-thinking phases
- **Test**'s business-rule-correctness dimension gets the heaviest scrutiny
  of any domain in this use case — a scheduling conflict or a
  mis-transitioned clinical state is a safety issue, not just a UX
  annoyance.
- **Prototype**'s UI half deliberately selects the calm, high-contrast,
  low-ornamentation register (`ui-engine/visual-trends.md`'s mapping for
  this domain) rather than defaulting to whatever the team finds visually
  appealing.

## Product Builder generation
`scripts/create-product-builder.py generate`, `product_type: healthcare`,
`sub_domain` set when a specific clinical niche is named (e.g. "dental
practice management," per `healthcare.md`'s explicit sub-case).

## Implementation
Consent-capture and scheduling-conflict-prevention logic is built and
tested *before* any patient-facing feature ships — these are treated as
prerequisite infrastructure, not features to add later.

## QA
Audit enforces redundant signaling of critical values (color + icon + text)
with zero tolerance for color-only encodings — the single strictest
accessibility bar of any domain use case here — and every open regulatory
assumption from Intake is re-surfaced explicitly in `qa/qa-report.md` rather
than assumed resolved by the time Audit runs.

## Completion criteria
An explicit, additional gate beyond the standard nine dimensions: **zero**
Blocker findings related to safety-critical business-rule correctness,
regardless of how well everything else scores. A product cannot be marked
complete on the strength of eight good dimensions if the ninth concerns
patient safety.

## How this differs from other use cases
Unlike `fintech`-adjacent domains (not built as a named use case here, but
comparable in stakes), healthcare's highest-stakes failure mode is a missed
or wrong *clinical* action rather than an ambiguous *financial* one — the
same rigor (Rule 10, redundant signaling) applies, aimed at a different
consequence.

## Explicitly not here
- The healthcare domain reference data itself → `product-types/healthcare.md`.
- The generic pipeline being demonstrated → `workflows/create-product.md`.
