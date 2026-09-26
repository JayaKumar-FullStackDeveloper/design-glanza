# Product Type: E-commerce

## Responsibility
Reusable domain knowledge for online retail — browsing/discovery through
purchase and post-purchase, on both the storefront and operational sides.
Applied on top of the domain-agnostic core per Rule 14
(`config/operating-rules.md`); contains no individual company's product
details (Rule 15) — product-specific knowledge belongs in a generated Product
Builder under `products/`.

## 1. Common product characteristics
Two distinct user populations with almost no UI overlap: a shopper-facing
storefront and merchant-facing operations. Conversion-path sensitivity is
unusually high in checkout — every added step has a measurable cost.
Inventory/fulfillment lifecycle is shared by both sides of the product.

## 2. Common users
Guest shopper, registered customer (storefront); merchant/store owner,
catalog manager, fulfillment staff, customer support (operations).

## 3. Common workflows
Browse → cart → checkout → order confirmation (storefront). Order received →
pick/pack → ship → deliver → (optional) return/refund (operations). Both
reference the same underlying inventory/order state machine from two
different vantage points.

## 4. Common information structures
Storefront IA is organized by merchandising taxonomy (category/collection);
operations IA is organized by process stage (orders/inventory/fulfillment) —
these are two distinct hierarchies over the same data, not one shared IA.

## 5. Common navigation patterns
Faceted search/filter is a first-class IA concern on the storefront, not an
afterthought filter bar. Operations favors dense list+detail (order list →
order detail) with strong cross-module links to the related customer and
inventory records.

## 6. Common UI patterns
The storefront is visual-forward — imagery-led visual hierarchy. Operations
follows the dense-enterprise register instead. These are deliberately two
registers within one product, not a single compromise style.

## 7. Common operational concerns
Inventory accuracy across concurrent orders (oversell prevention); payment
failure/retry handling; shipping/fulfillment SLAs.

## 8. Common edge cases
An item goes out of stock while sitting in another shopper's cart; price
changes mid-cart; payment is authorized but fulfillment subsequently fails; a
multi-item order is partially shipped or partially refunded.

## 9. Domain-specific terminology
SKU, cart, checkout, fulfillment, chargeback, return/RMA, variant.

## 10. Domain-specific UX risks
Minimizing checkout friction to the point of removing necessary trust signals
(address confirmation, payment security cues) — friction reduction and trust
signals must be balanced, not fully traded off against each other. Treating
out-of-stock as a rare edge case instead of a routine, must-design-for state.

## 11. Domain-specific accessibility considerations
Imagery-led storefronts must never depend on an image alone to convey
availability, price, or variant selection — always paired with text.
Checkout forms need the same rigor as any high-stakes form: clear
label-to-error association, never placeholder-only labels.

## 12. Domain-specific scalability considerations
Catalog browsing/search must perform over large catalogs (tens of thousands
of SKUs) via faceted filtering, not an ever-growing unpaginated grid.
Operations order lists must handle high-volume periods (sales events)
without degrading the underlying list/table performance patterns.

## Explicitly not here
- The general reasoning technique any point above specializes →
  `product-intelligence/user-roles.md` (users), `business-logic.md`
  (workflows), `ux-engine/information-architecture.md` /
  `navigation-system.md` (structures/navigation), `ui-engine/visual-trends.md`
  (UI register), `ux-engine/accessibility.md` / `ui-engine/color-system.md`
  (accessibility), `product-intelligence/dependency-analysis.md`
  (scalability/dependencies).
- Product-specific knowledge for one actual e-commerce product → that
  product's generated Product Builder under `products/`.
