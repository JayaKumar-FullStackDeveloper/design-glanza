# Product Type: Marketplace

## Responsibility
Reusable domain knowledge for two-sided (or multi-sided) platforms connecting
distinct supply-side and demand-side actors (e.g. sellers and buyers, hosts
and guests, freelancers and clients). Applied on top of the domain-agnostic
core per Rule 14 (`config/operating-rules.md`); contains no individual
company's product details (Rule 15) — product-specific knowledge belongs in a
generated Product Builder under `products/`.

## 1. Common product characteristics
Two-sidedness is structural, not incidental — nearly every feature has a
supply-side and a demand-side variant. Trust/reputation mechanisms (ratings,
reviews, verification) are usually load-bearing for the whole platform's
function, not a nice-to-have. Take-rate/commission and payout logic sits
between both sides and often overlaps with fintech concerns (escrow, payout
timing, dispute holds) — classify as hybrid via
`product-intelligence/domain-classifier.md` when this is substantial.

## 2. Common users
Supply-side actor (seller/provider/host), demand-side actor
(buyer/client/guest), platform admin/trust-and-safety, dispute mediator.

## 3. Common workflows
Listing creation (supply-side) and discovery → booking/purchase
(demand-side) are two independently-optimized primary workflows, not mirror
images of each other. A transaction workflow (booking/order → fulfillment →
review) is shared by both sides, each experiencing it from a different
vantage point. A dispute/resolution workflow activates when either side flags
a problem.

## 4. Common information structures
A dual IA: a supply-side "manage my listings/orders" structure and a
demand-side "discover and transact" structure, sharing an underlying data
model but not a UI structure.

## 5. Common navigation patterns
In-platform messaging needs explicit IA placement as the connective tissue
between discovery and transaction — never buried as a secondary feature.
Cross-navigation between "my listings" and "my purchases" matters for actors
who are both supply and demand at different times.

## 6. Common UI patterns
Demand-side leans visual-forward (similar to an e-commerce storefront).
Supply-side leans toward a lighter operational register (similar to a light
admin panel) for listing/order management — two registers within one
product.

## 7. Common operational concerns
Escrow/payout timing; dispute holds; trust-signal (rating/review) integrity
against manipulation.

## 8. Common edge cases
A cancellation or no-show affects both sides simultaneously and needs a
dual-sided state design, not a single-actor state machine. A dispute is
opened after payout has already been released. A listing is edited
mid-transaction, changing terms the other side already agreed to.

## 9. Domain-specific terminology
Listing, booking/order, take rate, payout, escrow, dispute, rating/review.

## 10. Domain-specific UX risks
Designing the transaction state machine from only one side's perspective,
leaving the other side's view inconsistent or missing at the same real-world
event. Under-investing in messaging IA because it doesn't look like a "core"
feature despite being the platform's actual connective tissue of trust.

## 11. Domain-specific accessibility considerations
Rating/trust signals must not rely on star-icon color alone — pair with the
numeric value as text. Dual-sided status displays must announce *which
side's* action is pending, not just "pending," for screen-reader users.

## 12. Domain-specific scalability considerations
Discovery/search must perform over a large, constantly-changing listing
inventory with near-real-time availability, not stale cached results.
Messaging must scale to high-volume concurrent conversations without becoming
the product's performance bottleneck.

## Explicitly not here
- The general reasoning technique any point above specializes →
  `product-intelligence/user-roles.md` (users), `business-logic.md`
  (workflows), `ux-engine/information-architecture.md` /
  `navigation-system.md` (structures/navigation), `ui-engine/visual-trends.md`
  (UI register), `ux-engine/accessibility.md` / `ui-engine/color-system.md`
  (accessibility), `product-intelligence/dependency-analysis.md`
  (scalability/dependencies).
- Product-specific knowledge for one actual marketplace product → that
  product's generated Product Builder under `products/`.
