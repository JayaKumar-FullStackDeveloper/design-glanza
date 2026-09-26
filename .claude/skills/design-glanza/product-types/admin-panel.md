# Product Type: Admin Panel

## Responsibility
Reusable domain knowledge for internal back-office/operations tooling —
usually a companion surface to a customer-facing product rather than the
whole product. Applied on top of the domain-agnostic core per Rule 14
(`config/operating-rules.md`); contains no individual company's product
details (Rule 15) — product-specific knowledge belongs in a generated Product
Builder under `products/`.

## 1. Common product characteristics
Internal, back-office companion surface to a customer-facing product. Audience
is trained staff, not end customers — designed for efficiency and
error-avoidance over delight or acquisition. Heavy on bulk operations and
audit trail.

## 2. Common users
Super-admin, operator/support agent, read-only auditor/viewer — a narrower,
more clearly hierarchical role set than most other domains.

## 3. Common workflows
- Search → filter → act-on-many is the dominant workflow shape, distinct from
  most domains' single-record-at-a-time flows.
- Impersonation / support-assist (acting on a customer's behalf), tightly
  audited from entry to exit.
- Config/feature-flag toggling.

## 4. Common information structures
Table-first IA. Entity CRUD screens are usually generated from one common
pattern repeated across many entity types, so the IA is often organized "one
section per entity type" rather than task-oriented grouping.

## 5. Common navigation patterns
A sidebar with role-scoped sections is near-universal (both breadth and depth
tend to be high here). Saved filters/views act as a navigation shortcut layer
on top of the raw entity sections — treat them as first-class nav aids, not
an optional extra.

## 6. Common UI patterns
Dense/compact register by default (`ui-engine/visual-trends.md`'s Dense
Enterprise register). A data table is the primary component on nearly every
screen. Minimal decoration; information density is the priority.

## 7. Common operational concerns
Every destructive or bulk action must be audit-logged. Permission boundaries
must fail closed (deny by default, never allow-by-default). Impersonation
sessions must be visibly, unmistakably flagged for the entire duration
they're active.

## 8. Common edge cases
A bulk action partially fails mid-batch — must report per-record outcome, not
a single pass/fail for the whole batch. An impersonation session is left open
or forgotten. Two staff members concurrently edit the same record.

## 9. Domain-specific terminology
Back-office, impersonation, feature flag, audit log, bulk action, role scope.

## 10. Domain-specific UX risks
Designing power-user tooling with the same onboarding-friendly hand-holding
patterns as a consumer product — this audience needs speed, not guidance.
Hiding destructive bulk actions behind too few confirmation steps because
"it's just internal" — internal does not mean low-stakes.

## 11. Domain-specific accessibility considerations
Density is not an excuse to shrink below accessible contrast or touch-target
minimums — dense tables must still meet the same thresholds as any other
screen. Keyboard-driven bulk-select must be fully operable without a mouse,
since power users in this domain specifically often prefer keyboard-first
workflows.

## 12. Domain-specific scalability considerations
Entity lists must assume very large record counts from day one — pagination
or virtualization, never "load all records client-side and filter." Audit
logs must remain searchable/filterable at scale, not just chronologically
browsable one page at a time.

## Explicitly not here
- The general reasoning technique any point above specializes →
  `product-intelligence/user-roles.md` (users), `business-logic.md`
  (workflows), `ux-engine/information-architecture.md` /
  `navigation-system.md` (structures/navigation), `ui-engine/visual-trends.md`
  (UI register), `ux-engine/accessibility.md` / `ui-engine/color-system.md`
  (accessibility), `product-intelligence/dependency-analysis.md`
  (scalability/dependencies).
- Product-specific knowledge for one actual admin panel → that product's
  generated Product Builder under `products/`.
