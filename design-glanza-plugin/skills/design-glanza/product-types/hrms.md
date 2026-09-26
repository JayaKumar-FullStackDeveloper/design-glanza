# Product Type: HRMS

## Responsibility
Reusable domain knowledge for human resource management systems — employee
lifecycle, organizational structure, and HR operational processes. Applied on
top of the domain-agnostic core per Rule 14 (`config/operating-rules.md`);
contains no individual company's product details (Rule 15) — product-specific
knowledge belongs in a generated Product Builder under `products/`.

## 1. Common product characteristics
Organizational hierarchy (reporting lines, departments, cost centers) is a
structural backbone most other modules reference. Sensitive personal data
(compensation, performance reviews, personal identifiers) commonly needs
finer-grained, per-*field* visibility, not just per-feature access. Periodic/
cyclical processes (payroll runs, review cycles, leave-year resets) are
common, with hard time-based triggers.

## 2. Common users
Employee (self-service), manager, HR administrator, payroll administrator,
executive/reporting viewer.

## 3. Common workflows
Leave request → manager approval → calendar/payroll update. Onboarding
checklist → provisioning across systems. Performance review cycle →
self-assessment → manager review → calibration → finalize.

## 4. Common information structures
Org-chart-anchored IA for admin/HR views (department/reporting-line
navigation) versus a flat, personal-record-anchored IA for employee
self-service (their own data only) — these are two distinct structures over
related data, not one shared hierarchy.

## 5. Common navigation patterns
Two effectively separate navigation systems for two audiences within one
product: self-service (shallow, simple) and HR/admin (deep, dense). Never
force one navigation pattern to serve both audiences.

## 6. Common UI patterns
Self-service leans toward the approachable/comfortable register; HR/admin
leans toward the dense-enterprise register — two registers within one
product, deliberately.

## 7. Common operational concerns
Payroll run accuracy and cutoff timing; mid-cycle organizational changes
(transfers, manager changes); compliance with leave/benefits eligibility
rules.

## 8. Common edge cases
An employee is transferred department mid-review-cycle; a manager changes
mid-leave-approval, orphaning a pending request; a payroll run needs
correction after a mid-cycle data change.

## 9. Domain-specific terminology
Employee record, org chart, cost center, leave balance, review cycle, payroll
run, benefits enrollment.

## 10. Domain-specific UX risks
Exposing sensitive compensation/review data through a permission model
designed only at the feature level, not the field level — a common,
specifically-HRMS gap. Designing rarely-used self-service flows (a once-a-
year benefits enrollment) as if the user has returning-user familiarity they
will not actually have.

## 11. Domain-specific accessibility considerations
Org-chart visualizations need a non-visual (list/table) equivalent providing
the same navigation, not a chart-only representation. Sensitive-data masking/
reveal controls must be keyboard-operable and clearly announced when toggled.

## 12. Domain-specific scalability considerations
Org-chart navigation must remain usable at large-headcount scale
(search/filter, not expand-all-nodes browsing). Leave/approval workflows must
handle reorganizations affecting many in-flight requests at once without
requiring manual per-request cleanup.

## Explicitly not here
- The general reasoning technique any point above specializes →
  `product-intelligence/user-roles.md` (users), `business-logic.md`
  (workflows), `ux-engine/information-architecture.md` /
  `navigation-system.md` (structures/navigation), `ui-engine/visual-trends.md`
  (UI register), `ux-engine/accessibility.md` / `ui-engine/color-system.md`
  (accessibility), `product-intelligence/dependency-analysis.md`
  (scalability/dependencies).
- Product-specific knowledge for one actual HRMS product → that product's
  generated Product Builder under `products/`.
