# Product Type: Logistics

## Responsibility
Reusable domain knowledge for products coordinating movement of goods —
shipping, freight, fleet, warehouse, and delivery operations. Applied on top
of the domain-agnostic core per Rule 14 (`config/operating-rules.md`);
contains no individual company's product details (Rule 15) — product-specific
knowledge belongs in a generated Product Builder under `products/`.

## 1. Common product characteristics
Physical-world state lag is inherent — system state (a shipment "in transit")
reflects a real-world process the system doesn't fully control. Multi-party
visibility spans shipper, carrier, and recipient, including external or
lightly-authenticated actors (a tracking-link recipient). Geographic/routing
logic (route optimization, zone rules, ETA calculation) is a distinctive
concern not present in most other domains.

## 2. Common users
Dispatcher/planner, driver/field operator, warehouse staff, shipper/customer,
recipient (often an external/unauthenticated tracking view).

## 3. Common workflows
Order created → route assigned → pickup → in-transit → delivery attempt →
delivered/failed → (if failed) re-attempt/re-route — spanning dispatch,
field, and external-recipient vantage points on the same underlying shipment.

## 4. Common information structures
Map-centric IA as a primary surface, not a secondary widget bolted onto a
list — alongside a list/table view of the same shipment data for
non-spatial tasks.

## 5. Common navigation patterns
Field/driver navigation must be radically simpler than dispatch navigation —
large touch targets, minimal hierarchy, glanceable status, matched to the
actual operating environment (moving, outdoors, often one-handed).

## 6. Common UI patterns
Dispatch/planning follows the dense-enterprise register. Driver/field
surfaces prioritize outdoor-readable contrast and large touch targets over
density — a materially different register within the same product.

## 7. Common operational concerns
Failed-delivery and re-routing handling; connectivity loss in the field as a
*default-expected* condition, not a rare edge case; resource (vehicle/driver)
conflict prevention.

## 8. Common edge cases
An address needs correction mid-transit; a recipient is unavailable at the
delivery attempt; a driver app loses connectivity mid-route and must
reconcile state on reconnect; a route is reassigned mid-transit due to a
vehicle issue.

## 9. Domain-specific terminology
Shipment, route, dispatch, proof-of-delivery, manifest, last-mile, ETA.

## 10. Domain-specific UX risks
Designing the field/driver experience with the same information density as
dispatch tooling — a mismatch with the actual operating environment.
Assuming constant connectivity in the field app's state model when
intermittent connectivity is the expected condition.

## 11. Domain-specific accessibility considerations
Driver-facing surfaces need especially high contrast and large targets given
outdoor/motion conditions — treat this as a genuine accessibility
requirement, not merely a "mobile-friendly" nicety. Map-centric views need a
non-visual equivalent (a list of stops/status) for screen-reader users.

## 12. Domain-specific scalability considerations
Map views must perform with large numbers of simultaneous active shipments/
routes (clustering, not rendering every pin unconditionally). Dispatch
tooling must handle fleet-wide reassignment operations without manual
one-by-one re-routing at scale.

## Explicitly not here
- The general reasoning technique any point above specializes →
  `product-intelligence/user-roles.md` (users), `business-logic.md`
  (workflows), `ux-engine/information-architecture.md` /
  `navigation-system.md` (structures/navigation), `ui-engine/visual-trends.md`
  (UI register), `ux-engine/accessibility.md` / `ui-engine/color-system.md`
  (accessibility), `product-intelligence/dependency-analysis.md`
  (scalability/dependencies).
- Product-specific knowledge for one actual logistics product → that
  product's generated Product Builder under `products/`.
