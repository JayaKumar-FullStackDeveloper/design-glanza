# Use Case: Existing Product (Cold Brownfield)

## Responsibility
A validated, concrete worked example of Design-Glanza analyzing an existing
application that has **no prior Design-Glanza product builder** — the input
modality is different from every greenfield use case above, not the domain.
This use case can pair with *any* `product-types/*.md` pack; what's distinct
here is Intake, not which domain is involved.

## Routes through Design-Glanza — not a separate skill
Executed by the same master skill as every other use case here — reverse-
engineering an existing product is a different *Intake posture*, handled
entirely within `product-intelligence/brd-analysis.md`'s existing input-type
recognition, not a separate process.

## Input
Screenshots, a live-app walkthrough description, or existing source code —
explicitly **no** written BRD/PRD. This is the sparsest, lowest-confidence
input category `brd-analysis.md` recognizes.

## Classification
`product-intelligence/domain-classifier.md` runs on reverse-engineered
signals (visible terminology, observed roles, code-level entity names)
rather than explicit text — typically **lower confidence** than a
written-spec case, stated as such rather than rounded up to "confident."

## Analysis
`brd-analysis.md`'s "existing product" and "existing code" postures apply:
behavioral inference through interaction for a live app (what's actually
observable, not assumed); as-built-vs-intended divergence checked explicitly
for code (the code's actual behavior may not match what any accompanying
description implies — both are recorded, not silently reconciled).
Confidence tags skew heavily toward **Inferred**/**Assumed** rather than
**Explicit** — this is the single biggest analytical difference from every
greenfield use case above.

## Required artifacts
`requirements/brd-analysis-notes.md` carries substantially more inferred
content with explicit lower-confidence tags than a greenfield pass would.
`product/product-definition.md`'s assumptions section is correspondingly
larger.

## Design-thinking phases
Per `methodology/prototype.md`'s redesign variant: **the current live
product *is* the low-fidelity baseline** — Prototype skips straight to
evaluating that baseline against `methodology/test.md`'s heuristics rather
than building a new low-fidelity pass from nothing. This is the single
biggest *behavioral* difference from a greenfield use case: there is
already something to react to, not a blank page.

## Product Builder generation
A **fresh** `scripts/create-product-builder.py generate` call — even though
the underlying product already exists in the wild, no Design-Glanza builder
exists for it yet, so this is `workflows/redesign-product.md`'s "no product
builder exists yet" case, not `--update`.

## Implementation
`workflows/build-product.md`'s escalation-on-spec-gaps rule is exercised
more than usual here, since a reverse-engineered spec is more likely to
have gaps surface mid-build than a spec derived from explicit
requirements.

## QA
Audit's traceability check matters just as much here as anywhere — every
artifact still traces to a source or an assumption tag, even when that
source is "inferred from screenshot 4" rather than a BRD line number.

## Completion criteria
The same gates as any other use case, **plus** an explicit report-level
caveat in `qa/qa-report.md`: the Confidence-field distribution across the
requirement model (mostly Inferred/Assumed rather than Explicit) is
surfaced, not hidden — a reviewer must be able to see how much of this
product's spec rests on inference before treating it as settled fact.

## How this differs from other use cases
Unlike `product-redesign.md` (next), there is no prior Design-Glanza
artifact trail to build on at all — everything starts from reverse-
engineered inference. Once this pass completes and a product builder
exists, any *subsequent* change to this same product is
`product-redesign.md`'s use case, not this one again.

## Explicitly not here
- The reverse-engineering extraction technique's categories →
  `product-intelligence/brd-analysis.md`.
- The redesign procedure being demonstrated → `workflows/redesign-product.md`.
- Redesigning a product that already has a Design-Glanza builder →
  `use-cases/product-redesign.md`.
