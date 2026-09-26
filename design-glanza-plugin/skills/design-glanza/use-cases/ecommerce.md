# Use Case: E-commerce (Greenfield)

## Responsibility
A validated, concrete worked example of Design-Glanza building a greenfield
e-commerce product, applying the `product-types/ecommerce.md` overlay and
showing its storefront/operations split explicitly.

## Routes through Design-Glanza — not a separate skill
Executed by the same master skill as every other use case here — only the
applied `product-types/*.md` pack and the specific emphases below differ.

## Input
Often two implicit input sets at once — a storefront experience description
and an operations/fulfillment description — sometimes as one spec, sometimes
as a plain-language want plus reference screenshots of a comparable site.

## Classification
Strong signals: "cart," "checkout," "SKU," "fulfillment" →
`product-types/ecommerce.md`. `domain-classifier.md` also flags the
two-population structure early, since it changes how IA and register
decisions get scoped later.

## Analysis
`brd-analysis.md` explicitly extracts inventory/oversell edge cases rather
than treating them as rare — `ecommerce.md`'s named UX risk is exactly this
(out-of-stock treated as an afterthought). `edge-case-engine.md`'s
boundary-value and concurrency categories are both critical here: stock
count at zero, price change mid-cart.

## Required artifacts
Two internally-separated IA branches within **one** `products/<slug>/`
builder — a storefront sitemap organized by merchandising taxonomy, and an
operations sitemap organized by process stage — per `ecommerce.md`'s
explicit framing, not two separate product builders.
`ux/state-matrix.md` includes out-of-stock and payment-failure as
mandatory states, not optional additions.

## Design-thinking phases
- **Ideate** compares checkout-flow patterns explicitly against the
  efficiency criterion — every added step in checkout has a measurable
  cost, per `ecommerce.md`, more so than almost any other flow in any
  domain.
- **Prototype** builds the checkout flow first — the single riskiest,
  most conversion-sensitive part of the whole product.

## Product Builder generation
`scripts/create-product-builder.py generate`, `product_type: ecommerce`.
The generated `SKILL.md`'s Navigation and UI Rules sections both note the
storefront/operations split explicitly, so a reader doesn't mistake it for
an oversight later.

## Implementation
Inventory-accuracy logic (oversell prevention) is built and tested *before*
checkout ships — checkout's correctness depends on accurate stock, so this
dependency is enforced in the build order, not assumed.

## QA
Audit specifically checks that the mandatory out-of-stock/payment-failure
states are actually designed (not just listed) and that the storefront and
operations registers stay visually distinct and internally consistent each
on its own terms — a blended, compromise register would be a defect here,
per `ecommerce.md`'s explicit two-registers-deliberately framing.

## Completion criteria
Standard nine-dimension coverage, plus a scalability check specific to this
domain: catalog browsing/search is designed for tens of thousands of SKUs
via faceted filtering, not an ever-growing unpaginated grid.

## How this differs from other use cases
Unlike `hrms.md` (below), which splits its two IA branches by *audience*
(employee vs. HR admin), e-commerce splits by *process stage* (discovery/
purchase vs. fulfillment/operations) — the same "two registers, one
product" pattern, applied for a different underlying reason.

## Explicitly not here
- The e-commerce domain reference data itself → `product-types/ecommerce.md`.
- The generic pipeline being demonstrated → `workflows/create-product.md`.
