# Use Case: Product Redesign (Existing Design-Glanza Builder)

## Responsibility
A validated, concrete worked example of Design-Glanza iterating on a product
that **already has a populated `product-builder/`** — a change request
against Design-Glanza's own prior work, not a cold analysis of an unrelated
existing product (`use-cases/existing-product.md`, above, is that case).
This is `methodology/design-thinking.md`'s continuous loop and
`config/operating-rules.md`'s Rule 13 (Iteration) in their most literal,
everyday form.

## Routes through Design-Glanza — not a separate skill
Executed by the same master skill as every other use case here. A redesign
is not a different skill or a fresh pipeline run — it is the same Iterate
phase every product passes through, invoked deliberately rather than
triggered by a failed gate.

## Input
A change request against an already-built product: a new feature ("add
bulk export"), a reported problem ("checkout has poor conversion"), or a
scheduled revisit. Unlike every other use case here, the input references
something that already has a `products/<slug>/` folder.

## Classification
`product-intelligence/domain-classifier.md` is **not** re-run from scratch —
the existing `product.json`'s `product_type`/`domain` is authoritative
unless the change request itself surfaces a signal that contradicts it (the
re-classification trigger `domain-classifier.md` already defines), in which
case it's re-run deliberately, not routinely.

## Analysis
`brd-analysis.md`'s delta-scoping technique applies directly: only the
changed or new material gets fresh extraction. The existing
`requirements/requirement-matrix.md`, `business-logic.md`, `user-roles.md`,
etc. are read and consulted, not silently redone — a redesign that
re-extracts everything from scratch has skipped this step, not followed it
carefully.

## Required artifacts
Only the artifacts the change actually touches get updated via `--update`.
`workflows/execute-product-builder.md`'s content-preservation behavior (the
generator re-parses a prior `SKILL.md` so an unresupplied section survives)
is exactly the mechanism that makes this safe — the alternative would be
re-deriving the whole product-builder on every small change.

## Design-thinking phases
This is `methodology/design-thinking.md`'s loop in direct action, at
feature- or screen-level granularity: a "checkout has poor conversion"
report is a Test finding, routed per that file's feedback-routing table
to **Ideate** and **Prototype** for the checkout flow specifically — not a
full Intake redo, and not silently patched at Prototype alone if the
underlying approach is actually what's wrong.

## Product Builder generation
`scripts/create-product-builder.py generate --update` — **never** a bare
`generate`. The Factory's conflict guard (verified when the script was
built: a bare `generate` on an existing slug refuses and reports the
conflict) is exactly the safety mechanism this use case depends on to avoid
accidentally overwriting prior work instead of building on it.

## Implementation
`workflows/build-product.md`'s escalation-on-spec-gaps rule matters less
here than in a greenfield build (the spec is already mature); the real risk
is **regression** — `workflows/execute-product-builder.md`'s completion
criteria state this explicitly: a fix that silently regresses an
already-passing gate reopens the scope, it doesn't pass by association with
the new fix.

## QA
`workflows/audit-product.md`'s step 7 applies precisely: routes the
specific finding, then **Test/Audit re-run only the specific failed
gate(s)** that prompted this redesign pass — not the whole pipeline from
scratch — but Audit also spot-checks that untouched areas' previously-passed
gates still hold, specifically to catch the regression risk above.

## Completion criteria
Ties directly to `methodology/design-thinking.md`'s loop-termination rule:
this pass is complete when **both** hold — the specific finding that
triggered it no longer reproduces, **and** no previously-passing gate
(`config/quality-gates.md` B1-B12) has regressed. A redesign that fixes the
reported problem while breaking something else is not complete.

## How this differs from other use cases
Unlike every greenfield use case above, Architect and Intake are mostly
*consulted*, not *re-executed* — the defining discipline of this use case is
touching only what changed and proving nothing else moved, which is exactly
the opposite instinct from a fresh build.

## Explicitly not here
- Reverse-engineering a product with no prior Design-Glanza builder at all
  → `use-cases/existing-product.md`.
- The redesign procedure's mechanics themselves →
  `workflows/redesign-product.md`.
- The loop mechanics and feedback-routing table →
  `methodology/design-thinking.md`.
