# Product Type: ERP

## Responsibility
Reusable domain knowledge for enterprise resource planning systems —
cross-functional, multi-module systems coordinating operational processes
(procurement, inventory, finance, manufacturing, etc.). Applied on top of the
domain-agnostic core per Rule 14 (`config/operating-rules.md`); contains no
individual company's product details (Rule 15) — product-specific knowledge
belongs in a generated Product Builder under `products/`.

## 1. Common product characteristics
Cross-functional, multi-module by nature. Long-lived records with extensive
history/versioning requirements (a purchase order, an invoice) rather than
ephemeral records. Approval-chain workflows are pervasive — most business
logic involves multi-step, role-gated approval rather than a single actor
acting alone.

## 2. Common users
Requester, multi-level approver (manager → finance → executive), procurement
officer, warehouse/inventory clerk, finance controller, system administrator.

## 3. Common workflows
Create request → route through an approval chain → fulfill/execute →
reconcile — spanning multiple modules for a single business transaction (e.g.
a purchase order → inventory receipt → invoice → general-ledger entry).

## 4. Common information structures
Deep cross-referencing between records (a PO references a vendor and line
items, which reference SKUs) — the IA needs strong record-to-record
cross-linking, not just hierarchical drill-down through one module at a time.

## 5. Common navigation patterns
Cross-module navigation (`ux-engine/navigation-system.md` item 12) is
unusually load-bearing here — almost every record view needs an in-context
jump to related records in other modules. Breadcrumbs are often genuinely
appropriate given real, deep, tree-like hierarchy — but still subject to that
file's 3-condition test, never assumed by default just because the domain is
"enterprise."

## 6. Common UI patterns
Dense-enterprise register. Tabular financial precision: right-aligned
numerals, tabular figures (`ui-engine/typography.md`), and clear
totals/subtotals rows distinguished by weight, not color alone.

## 7. Common operational concerns
Multi-level approval routing and delegation; budget/cost-center enforcement;
period-close/reconciliation processes.

## 8. Common edge cases
Partial approval, rejection, or resubmission of a request; an approver is
unavailable and delegation applies; a line-item quantity or price changes
after partial fulfillment; a budget is exceeded mid-approval-chain.

## 9. Domain-specific terminology
Purchase order, vendor/supplier, cost center, general-ledger (GL) entry,
requisition, approval chain, line item, fulfillment.

## 10. Domain-specific UX risks
Exposing raw financial/accounting complexity directly in the primary flow
instead of progressively disclosing it — overwhelms a requester who just
wants to submit a request. Under-designing approval-chain status visibility,
leaving approvers and requesters both unsure where a request actually sits.

## 11. Domain-specific accessibility considerations
Multi-level approval status must be conveyed with text or icon, not color
alone — a strong temptation given how naturally status maps to
red/yellow/green. Dense financial tables need real keyboard navigation
between cells, not just row-level focus.

## 12. Domain-specific scalability considerations
Approval chains must survive organizational restructuring (a manager change
mid-chain) without orphaning in-flight requests. Cross-module reference
tables must perform at real enterprise transaction volumes (thousands of line
items per day), not demo-scale data.

## Explicitly not here
- The general reasoning technique any point above specializes →
  `product-intelligence/user-roles.md` (users), `business-logic.md`
  (workflows), `ux-engine/information-architecture.md` /
  `navigation-system.md` (structures/navigation), `ui-engine/visual-trends.md`
  (UI register), `ux-engine/accessibility.md` / `ui-engine/color-system.md`
  (accessibility), `product-intelligence/dependency-analysis.md`
  (scalability/dependencies).
- Product-specific knowledge for one actual ERP product → that product's
  generated Product Builder under `products/`.
