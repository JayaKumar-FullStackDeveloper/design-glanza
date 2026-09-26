# Use Case: New SaaS (Greenfield)

## Responsibility
A validated, concrete worked example of Design-Glanza building a greenfield
SaaS product, applying the `product-types/saas.md` overlay. Distinct from
that file itself: `product-types/saas.md` is reference specialization data;
this file shows the master engine's reasoning actually applied end to end on
one example input.

## Routes through Design-Glanza — not a separate skill
Every stage below is executed by the one master skill (`SKILL.md`,
`config/`, `methodology/`, `product-intelligence/`, `ux-engine/`,
`ui-engine/`, `agents/`, `workflows/`). Nothing here is a separate SaaS
skill — the only thing that varies by domain is which `product-types/*.md`
pack gets applied at Architect, and which workflow entry point runs
(`create-product.md`, here).

## Input
A greenfield idea, usually a plain-language description or a light PRD —
SaaS requests are frequently the *sparsest* input Design-Glanza sees, e.g.
"a tool for small teams to split and track shared expenses."

## Classification
`product-intelligence/domain-classifier.md` scores strong signals almost
immediately: multi-tenant vocabulary ("team," "workspace"), no named
regulatory concern, no multi-module cross-referencing implied → confident
match to `product-types/saas.md`.

## Analysis
Because the input is sparse, `brd-analysis.md`'s confidence tagging skews
toward **Inferred**/**Assumed** rather than **Explicit** — most of the
structure (subscription lifecycle, seat model, onboarding flow) comes from
`saas.md`'s domain conventions (Rule 2 tier 6), not from the input directly,
and every one of those inferences is tagged with its impact, per Rule 10.
`business-logic.md` derives the trial → active → past-due → churned state
machine largely by convention since the input never specified it.

## Required artifacts
`product/product-definition.md` names the onboarding/activation flow as the
single highest-leverage flow, per `saas.md`'s characteristics — this gets
called out explicitly rather than discovered later. `requirements/
user-roles.md` distinguishes account-level from workspace-level roles from
the start.

## Design-thinking phases
- **Empathize** centers on new-user activation anxiety: a brand-new
  workspace starts with nothing.
- **Define**'s product objective is framed around time-to-first-value, not
  feature completeness.
- **Ideate** compares onboarding patterns (forced linear tour vs.
  contextual, in-flow guidance) against `saas.md`'s explicit UX-risk
  warning — the forced-tour pattern is usually rejected here, with the
  rejection recorded, not just the winner.
- **Prototype** builds the workspace-creation + invite-teammate flow
  *first* (the riskiest, least-proven assumption), per
  `methodology/prototype.md`'s sequencing rule.

## Product Builder generation
`scripts/create-product-builder.py generate` (fresh — no prior builder
exists), with `product_type: saas` and a `domain` describing the specific
product (e.g. "team expense tracking"). The generated `SKILL.md` cites
`saas.md` for onboarding/billing conventions from the very first Architect
pass.

## Implementation
Build order (`workflows/build-product.md`) puts auth/workspace/roles ahead
of any billing-gated feature — a SaaS-specific instance of Rule 5, since
almost every other feature is scoped to a workspace that must exist first.

## QA
`workflows/audit-product.md` specifically checks `saas.md`'s named UX risks:
the empty-state design actually guides toward first value (not just "no
data"), and usage/quota indicators are never color-only signals of
approaching-limit vs. over-limit.

## Completion criteria
Standard nine-dimension Test coverage
(`workflows/execute-product-builder.md`) plus a SaaS-specific scalability
check: the workspace switcher and member list are designed for a user in
many large workspaces, not just the single-workspace demo case.

## How this differs from other use cases
Unlike `erp.md` or `hrms.md` (below), there is usually no pre-existing
organizational structure to reverse-engineer — Empathize/Define do more
inferential work here than almost any other domain because the input is so
sparse, while Architect's module-boundary work is comparatively light (SaaS
products are often one dominant object type, not many interlinked modules).

## Explicitly not here
- The SaaS domain reference data itself → `product-types/saas.md`.
- The generic pipeline being demonstrated → `workflows/create-product.md`.
