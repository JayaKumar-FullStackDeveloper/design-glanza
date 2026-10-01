# Design Sample: Fintech

Status: **partially populated** — 6 curated reference images added
(source: user-supplied, unattributed third-party dashboard shots collected
from general design-inspiration sources — treat as Inferred-confidence
visual reference, not a licensed/attributed asset).

## Reference assets
| File | What it shows |
|---|---|
| `dashboard-fintech-wallet-overview.jpg` | Multi-currency wallet dashboard: balances, send/request money, income/spend chart, recent activity table |
| `dashboard-fintech-banking-cards-transactions.jpg` | Card management + quick money transfer + contacts list + transaction insights chart |
| `dashboard-fintech-invoice-management.jpg` | Invoice-focused dashboard: overdue/due/avg-time-to-pay summary, unpaid-invoice list with detail panel |
| `dashboard-fintech-wallet-savings.jpg` | Personal-finance wallet: account balance, expenses/savings, savings-plan goals, recent transactions |
| `dashboard-fintech-payment-wallet.jpg` | Payment-goal-focused dashboard: engagement-rate chart, payment history table |
| `dashboard-fintech-earnings-spending.jpg` | Earnings/spending/savings summary cards, transactions-overview chart, spending-category breakdown |

## Measurable reference characteristics (new this version)
Approximate, visually-estimated ranges, in the same **REFERENCE AS DESIGN
LANGUAGE** (not DIRECT VISUAL TARGET) spirit as `design-samples/saas/
README.md`'s fuller version of this section — read that file's opening
paragraph for the full caveat on how these numbers are meant to be used
and checked; not repeated here in full.

- **Spacing scale** — the same ~8/16/24/32px rhythm as the saas set
  (icon-label / card-internal / inter-card / section gaps).
- **Card radius** — moderate, ~10-14px, slightly tighter than the saas
  set's — fintech surfaces in this set favor a slightly crisper edge.
- **Surface hierarchy** — page background, card surface, and a distinct
  inset tone for balance/amount emphasis blocks and table header rows.
- **Typography scale** — a balance/amount figure is the dominant text
  (tabular numerals, largest on screen); transaction-list rows stay one
  consistent body size, with the amount column right-aligned and weighted
  heavier than the description column.
- **Density** — comfortable; transaction/invoice lists favor generous
  row height over cramming more rows into view, consistent with a
  domain where misreading a number has real consequences.
- **Component dimensions** — balance/summary cards share one height
  within a row; status pills (paid/overdue/pending) are compact, pill-
  radius = half their own height.
- **Layout proportions** — a summary/balance region sits above a
  chart-and-table region, in that top-to-bottom order, in every reference
  in this set — not a uniform grid.
- **Color relationships** — a single restrained accent for primary
  actions/active chart series; semantic status (paid/overdue/error) is
  reserved strictly for status pills, never a card's own background.

## Suggested starting register
Dense Enterprise (back-office) / Modern SaaS (consumer-facing) (`ui-engine/visual-trends.md`) — used as the named starting
point by `design-reference-engine/reference-selection.md` mode 4 (Default
Design-Glanza) until real curated references are added here.

## Matched by
`product-types/fintech.md`'s domain slug, via
`reference-selection.md`'s exact-match rule.

## To populate
Add curated reference images, a token file, or a written style brief to
this folder, then update this README to describe what was added, its
source, and its confidence — mirroring `product-types/domain-standards/`'s
"complete" vs. "pending" distinction.
