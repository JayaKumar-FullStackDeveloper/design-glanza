# Domain Classifier

## Responsibility
Decide which `product-types/*.md` specialization(s) apply to an incoming product
— the routing logic between the domain-agnostic core and the domain overlays.
Runs after `brd-analysis.md`'s extraction (it needs facts to classify from) and
before `business-logic.md`/`user-roles.md` apply domain-typical conventions.

## Classification signals
Score against each recognized domain (`config/master-config.md`'s domain
registry) using signal strength, not a single keyword match:

| Signal type | Example | Strength |
|---|---|---|
| Named entity vocabulary | "purchase order," "vendor," "approval chain" → ERP; "patient," "appointment," "treatment plan" → healthcare | Strong |
| Named role vocabulary | "approver," "requester," "cost center" → ERP; "dispatcher," "driver" → logistics | Strong |
| Regulatory/compliance mention | any health-data or financial-services regulation mentioned → healthcare/fintech | Strong |
| Structural pattern | two clearly distinct actor populations with a matching/transaction relationship → marketplace | Medium |
| Workflow shape | multi-level approval chains → ERP; pipeline/stage progression → CRM | Medium |
| Single-page, single-conversion-action shape with no persistent-login application behind it (a launch page, waitlist, marketing site) | → landing-page | Strong |
| Generic SaaS scaffolding alone (accounts, seats, billing) with no other domain signal | → saas | Weak (default, not a positive match) |

A single weak signal does not classify a domain; multiple independent strong
signals do. Score cumulatively across `brd-analysis.md`'s extracted facts (all
20 items are fair game — business rules, roles, and data requirements are
usually the richest signal sources).

## Classification output
- **Confident single match** — one domain's signals dominate: apply that
  `product-types/*.md` overlay directly.
- **Multi-domain / hybrid** — two domains both show strong signals (e.g. a
  marketplace with fintech-grade payouts/escrow): apply both overlays, and
  explicitly flag the overlap so downstream files know which parts of each
  overlay actually apply versus conflict.
- **No confident match** — signals are all weak or contradictory: route to
  `product-types/custom-domain.md`'s no-match procedure rather than forcing a
  poor-fit classification. Do not default to the nearest-sounding domain out of
  convenience — a wrong classification actively misleads every downstream file
  that reads its overlay.
- **Partial match** — one domain's signals are present but incomplete (e.g. some
  healthcare vocabulary but no clinical workflow signal at all): apply
  `product-types/custom-domain.md`'s partial-match procedure — borrow only the
  specific characteristics that clearly apply, name which ones, mark the rest
  not-applicable.

## Confidence reporting
State the classification with its confidence level and the specific signals that
drove it (per `config/output-contract.md`'s phase-completion report shape) — a
silent, unexplained classification is not acceptable even when correct, because
it can't be checked or revised if new signal emerges later.

## Re-classification
Classification is not a one-time judgment. If later phases (Architect, Ideate,
or a Test finding at the feature-level loop) surface a domain signal
`brd-analysis.md`'s original pass missed, re-run this classification — a wrong
early classification, left uncorrected, misapplies an entire domain overlay's
worth of conventions.

## Explicitly not here
- The domain registry list itself → `config/master-config.md`.
- What a given domain's specialization actually contains → each
  `product-types/*.md` file.
- Worked classification examples → `use-cases/*.md`.
- The no-match/partial-match/graduation procedures themselves (this file only
  triggers them) → `product-types/custom-domain.md`.
- The separate, finer-grained domain-standards registry match (a different
  question, run alongside this one at Architect, not a replacement for it) →
  `product-intelligence/domain-standards.md`.
