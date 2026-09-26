# Product Type: Fintech

## Responsibility
Reusable domain knowledge for products handling money movement, accounts, or
financial data directly (payments, lending, banking-adjacent, investing).
Applied on top of the domain-agnostic core per Rule 14
(`config/operating-rules.md`); contains no individual company's product
details (Rule 15) — product-specific knowledge belongs in a generated Product
Builder under `products/`.

## 1. Common product characteristics
Near-zero tolerance for ambiguous states around money — trust is the defining
constraint. Ledger/transaction integrity is foundational: most other features
build on trusting the ledger. Identity verification/fraud-prevention steps
(KYC, step-up authentication) are recurring, *expected* flow interruptions,
not exceptions to design around.

## 2. Common users
Account holder/customer, business/merchant account admin, compliance/risk
reviewer, support agent (usually with restricted, auditable access to
financial data).

## 3. Common workflows
Initiate transfer/payment → verification/step-up (if triggered) → execution →
confirmation/receipt is the canonical high-stakes workflow — it must always
end in an unambiguous, persisted state, never a state the user can't
interpret.

## 4. Common information structures
Account/ledger-centric IA — every other view (transactions, disputes,
statements) hangs off an account, with strict, auditable, chronological
history ordering.

## 5. Common navigation patterns
Back-behavior during a money-moving flow must never silently discard an
in-progress transaction. Recovery paths after a failed transaction must be
completely unambiguous about whether money actually moved.

## 6. Common UI patterns
Restrained, decoration-free register. Every status is redundantly signaled
(color + icon + label) given the stakes of misreading a transaction status.
Numeric formatting must never introduce truncation ambiguity around an amount.

## 7. Common operational concerns
Reconciliation and dispute/chargeback handling; fraud/risk review workflows;
regulatory reporting (again: never assume a specific regime).

## 8. Common edge cases
A transaction times out with unclear success/failure; a duplicate transfer is
submitted (double-click or retry); a dispute is opened on a transaction
already reconciled; a step-up verification is abandoned mid-flow, leaving the
transaction in limbo.

## 9. Domain-specific terminology
Ledger, transfer, settlement, chargeback/dispute, KYC, step-up
authentication, reconciliation.

## 10. Domain-specific UX risks
Showing a transaction as "processing" indefinitely with no resolution path —
this is operational clarity's highest-stakes failure point across every
domain Design-Glanza supports. Treating verification friction as purely a
conversion cost to minimize, rather than a necessary step deserving real
design attention.

## 11. Domain-specific accessibility considerations
Transaction status must never rely on color alone — arguably the single most
important instance of the color-blind-safety rule across every domain, given
the stakes. Confirmation/receipt screens must be fully screen-reader-
navigable in the exact order a later dispute investigation would need to
reference them.

## 12. Domain-specific scalability considerations
Transaction history must perform at high-volume-account scale (pagination/
search, never a full-history load). Fraud/risk review queues must handle
high-volume flagged-transaction throughput without the reviewer losing
context between cases.

## Explicitly not here
- The general reasoning technique any point above specializes →
  `product-intelligence/user-roles.md` (users), `business-logic.md`
  (workflows), `ux-engine/information-architecture.md` /
  `navigation-system.md` (structures/navigation), `ui-engine/visual-trends.md`
  (UI register), `ux-engine/accessibility.md` / `ui-engine/color-system.md`
  (accessibility), `product-intelligence/dependency-analysis.md`
  (scalability/dependencies).
- Product-specific knowledge for one actual fintech product → that product's
  generated Product Builder under `products/`.
