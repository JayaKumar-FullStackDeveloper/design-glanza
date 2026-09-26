# Use Case: ERP (Greenfield)

## Responsibility
A validated, concrete worked example of Design-Glanza building a greenfield
ERP module, applying the `product-types/erp.md` overlay.

## Routes through Design-Glanza — not a separate skill
Executed by the same master skill as every other use case here — only the
applied `product-types/*.md` pack and the specific emphases below differ.

## Input
Usually the *fullest* input Design-Glanza sees — ERP requests tend to arrive
as a documented BRD/spec because the multi-module process (procurement,
inventory, finance) is already understood by whoever's requesting it, e.g. a
procurement-to-payment module spec.

## Classification
Strong, specific signals: "purchase order," "approval chain," "cost
center," "GL entry" → confident match to `product-types/erp.md`.

## Analysis
`product-intelligence/dependency-analysis.md` is the single most heavily
exercised file in this use case — cross-module dependencies (a PO touching
procurement, inventory, and finance in sequence) dominate the analysis.
`business-logic.md`'s decision-point and workflow capture is extensive,
given how pervasive multi-level approval chains are; `edge-case-engine.md`'s
partial-approval/rejection/resubmission category gets full treatment.

## Required artifacts
`requirements/dependency-analysis.md`'s cross-module table is the single
most load-bearing artifact in this use case. `requirements/user-roles.md`'s
hierarchy/delegation section is unusually detailed (multi-level approvers,
delegate-while-out-of-office).

## Design-thinking phases
- **Architect** is unusually heavy here: module boundaries (procurement,
  inventory, finance as separate but interlinked) take real reasoning, not
  a quick pass.
- **Ideate** weights the implementation-complexity criterion heavily given
  the multi-module scope — an approach that looks elegant for one module
  but multiplies integration cost across three is rejected, with the
  rejection recorded.
- **Prototype**'s navigation architecture leans on cross-module navigation
  (`ux-engine/navigation-system.md` item 12) and is one of the few domains
  where breadcrumbs genuinely satisfy all three of that file's conditions
  (deep, tree-like, real need to jump to a specific ancestor) rather than
  being omitted by default.

## Product Builder generation
`scripts/create-product-builder.py generate`, `product_type: erp`, `domain`
naming the specific process scope (e.g. "procurement-to-payment"). The
dependency graph gets substantially refined at Architect, not just
initialized at Intake.

## Implementation
Build order is strictly critical-path-driven: auth/roles → core entity CRUD
→ approval-workflow engine → cross-module integration — more strictly
sequenced here than in most domains, because so much rests on the
dependency graph being right before any module is built in isolation.

## QA
Audit specifically checks approval-chain status visibility (`erp.md`'s
named UX risk: requesters/approvers unsure where a request actually sits)
and financial-table accessibility (tabular figures, status never
color-only).

## Completion criteria
Standard nine-dimension coverage, with **B10 (Traceability)** scrutinized
harder than in most domains given how many cross-module links exist — an
orphaned cross-module reference is far more likely here than in a
single-module product.

## How this differs from other use cases
Unlike `admin-panel.md` (efficiency-weighted, single-surface), ERP's Ideate
and Architect phases spend real effort on module decomposition and
implementation-complexity trade-offs before any UX work starts at all.

## Explicitly not here
- The ERP domain reference data itself → `product-types/erp.md`.
- The generic pipeline being demonstrated → `workflows/create-product.md`.
