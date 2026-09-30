# Domain Analysis

## Responsibility
The Domain research area: establishing what's actually conventional for
*this* product's domain before any screen exists — common workflows,
terminology, domain-specific patterns, regulatory constraints, and common
information structures. This file is a research *technique* (how to look
and what to conclude); the domain's own stated content is never re-derived
here — it's cited from the two existing domain-knowledge systems.

## What to establish

| Establish | How |
|---|---|
| Common workflows | The domain's typical end-to-end process shape (e.g. quote → order → fulfillment → invoice for e-commerce; intake → triage → treatment → discharge for healthcare) — cite the matched `product-types/*.md` pack's own workflow description, don't reinvent it |
| Domain terminology | The vocabulary users actually use for entities/actions in this domain (an "invoice" vs. a "bill," a "ticket" vs. a "case") — mismatched terminology is itself a usability defect, not a cosmetic one |
| Domain-specific patterns | UI/UX patterns this domain has converged on for a structural reason (e.g. a kanban board for pipeline-shaped work, a calendar grid for scheduling-heavy domains) |
| Regulatory constraints | Any domain-mandated requirement that isn't optional (HIPAA-adjacent audit trails, financial recordkeeping, accessibility bars stricter than baseline) — cite `product-types/domain-standards/`'s matched entry (Rule 17) where one exists |
| Common information structures | How this domain typically organizes information hierarchically (by account vs. by transaction, by patient vs. by encounter) |

## Sourcing, in priority order
1. `product-types/domain-standards/domain-registry.json`'s matched entry, if
   complete (Rule 17) — the most specific, externally-sourced guidance
   available.
2. The matched `product-types/*.md` pack's own 12-point Domain Pack
   Contract answers (Rule 16) — always available for a confidently-matched
   domain.
3. Product Architect's own domain-classification confidence and signals
   (`product-intelligence/domain-classifier.md`) — for a hybrid or partial
   match, state which pack(s) apply to which surface.
4. Where no domain confidently matches at all, `product-types/custom-
   domain.md`'s no-match procedure — research here becomes evidence toward
   a *future* pack (its own graduation rule), not an excuse to skip this
   area.

## Recording the finding
A Domain finding cites its source at the correct evidence tier
(`evidence-model.md` — domain conventions are tier 6) and states its
Insight in terms of what the *user* needs from that convention, not just
that the convention exists (e.g. not "ERP uses dense tables" but "ERP users
process high transaction volumes and need to compare many rows without
paging, which is why dense tables are conventional here").

## Explicitly not here
- The domain pack's own actual content → `product-types/*.md`.
- The finer-grained external standard's own content → `product-types/
  domain-standards/`.
- The domain-matching procedure itself → `product-intelligence/domain-
  classifier.md`, `product-intelligence/domain-standards.md`.
- Interaction- or visual-specific conventions within this domain →
  `interaction-analysis.md`, `visual-analysis.md`.
