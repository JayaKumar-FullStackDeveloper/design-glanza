# Product Type: SaaS

## Responsibility
Reusable domain knowledge for multi-tenant, subscription-based software
products — applied on top of the domain-agnostic core
(`product-intelligence/*`, `ux-engine/*`, `ui-engine/*`) per Rule 14
(`config/operating-rules.md`), never a replacement for it. This file contains
**patterns common across SaaS products in general** — no individual company's
product is described or referenced here (Rule 15, Product Isolation);
anything specific to one actual product belongs in that product's generated
Product Builder under `products/`, not here.

## 1. Common product characteristics
Multi-tenancy is usually load-bearing: nearly every entity is scoped to an
account/workspace by default. Subscription/billing lifecycle (trial → active →
past-due → churned → reactivated) is a first-class, always-present state
machine. Self-service onboarding is often the primary growth channel, not an
afterthought. Usage-based or seat-based metering is common and frequently
gates feature access.

## 2. Common users
Account owner, workspace/organization admin, member/collaborator, billing
contact — often with per-workspace role variants distinct from per-account
roles (a user can be an admin in one workspace and a member in another).

## 3. Common workflows
- Signup → workspace creation → first-value action ("aha moment") — usually
  the single highest-leverage workflow in the whole product.
- Trial → conversion → active subscription.
- Invite teammate → accept invite → onboarding into an existing workspace.
- Plan upgrade/downgrade → proration → billing update.

## 4. Common information structures
Shallow-to-medium IA depth. Settings splits into **account-level** and
**workspace-level** sections — conflating the two is a frequent, avoidable IA
defect. The primary work surface is usually one dominant object type (or a
small, tightly related set), not a sprawl of unrelated top-level sections.

## 5. Common navigation patterns
Sidebar or top nav depending on breadth (rarely both — pick one per
`ux-engine/navigation-system.md`'s selection framework). A workspace switcher
is a persistent, easily-discoverable control whenever multi-workspace
membership exists. Settings live in one consistent, separate area rather than
being scattered inline across feature screens.

## 6. Common UI patterns
Empty states carry disproportionate weight — a brand-new workspace starts with
nothing, and its empty state must actively guide toward the first-value
action, not just report "no data." Usage/quota indicators (progress-bar style)
are surfaced near the limits they track, not buried in a separate report.

## 7. Common operational concerns
Seat-limit and usage-limit enforcement; failed-payment/dunning handling;
data export and deletion on churn.

## 8. Common edge cases
Payment method expires mid-billing-cycle; a user is removed from a workspace
mid-action; a workspace is deleted while an invite to it is still pending;
a seat limit is reached during an in-progress invite flow.

## 9. Domain-specific terminology
Workspace / organization / tenant, seat, plan / tier, trial, churn, usage
metering. (Business metrics like MRR/ARR are business vocabulary, not UI
requirements, unless a requirement explicitly calls for surfacing them.)

## 10. Domain-specific UX risks
Over-designing onboarding as one linear forced tour instead of contextual,
in-flow guidance — leads to tour-fatigue and skipped steps. Treating
billing/plan complexity as a settings-page afterthought when it is actually a
primary conversion surface deserving real design attention.

## 11. Domain-specific accessibility considerations
Usage/quota visualizations must not rely on color-only proximity-to-limit
cues — "approaching limit" vs. "over limit" needs a non-color signal
(icon, text) as well, per `ui-engine/color-system.md`'s color-blind-safety
rule applied to this specific pattern.

## 12. Domain-specific scalability considerations
IA and navigation must not assume "a few workspaces" — a user in many
organizations needs a workspace switcher that scales past a simple dropdown
(search/filter). A "workspace members" list must handle organizations with
thousands of members, using the same large-dataset table patterns as any
other domain at scale, not a demo-scale assumption.

## Explicitly not here
- The general reasoning technique any point above specializes →
  `product-intelligence/user-roles.md` (users), `business-logic.md`
  (workflows), `ux-engine/information-architecture.md` /
  `navigation-system.md` (structures/navigation), `ui-engine/visual-trends.md`
  (UI register), `ux-engine/accessibility.md` / `ui-engine/color-system.md`
  (accessibility), `product-intelligence/dependency-analysis.md`
  (scalability/dependencies).
- Product-specific knowledge for one actual SaaS product → that product's
  generated Product Builder under `products/`.
