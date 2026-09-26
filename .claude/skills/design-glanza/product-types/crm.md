# Product Type: CRM

## Responsibility
Reusable domain knowledge for customer/relationship-management systems —
tracking people, organizations, and the interactions/pipeline between them.
Applied on top of the domain-agnostic core per Rule 14
(`config/operating-rules.md`); contains no individual company's product
details (Rule 15) — product-specific knowledge belongs in a generated Product
Builder under `products/`.

## 1. Common product characteristics
Relational core object model (contact ↔ company ↔ deal ↔ activity) — most
features are really about traversing these relationships. Pipeline/stage
progression is usually visualized directly (kanban-style), not hidden in a
status field. Activity logging (calls, emails, notes) is high-frequency,
low-friction input.

## 2. Common users
Sales rep, sales manager, account owner, marketing user (if lead-gen is in
scope), admin.

## 3. Common workflows
Lead capture → qualification → pipeline-stage progression → won/lost is the
canonical workflow. Activity logging (call/email/note) is a constantly
repeated micro-workflow running alongside it, not a separate feature.

## 4. Common information structures
Entity-relationship-heavy IA — a contact's page surfaces its company, its
deals, and its activity history all in context, rather than siloed
per-entity sections a user must navigate between manually.

## 5. Common navigation patterns
Cross-module navigation between contact/company/deal is essential
(`ux-engine/navigation-system.md` item 12). A persistent "recently viewed" or
quick-switch pattern supports the high context-switching frequency inherent
to sales work.

## 6. Common UI patterns
A pipeline board (kanban) is an alternate *view* of the same data as the
list/table view — treated as views of one dataset, not separate features.
Quick-add/inline-edit patterns dominate over full-page forms for routine
updates. Semantic color for pipeline stage is always paired with a text
label, never color alone.

## 7. Common operational concerns
Duplicate contact/company detection and merge; data ownership/reassignment
when a rep leaves or a territory changes.

## 8. Common edge cases
Duplicate records created by near-simultaneous entry from two channels; a
deal reassigned mid-pipeline loses its activity context; a merge conflict
between two contact records with conflicting field values.

## 9. Domain-specific terminology
Lead, contact, account/company, deal/opportunity, pipeline stage, activity,
forecast.

## 10. Domain-specific UX risks
Making activity logging heavyweight (a full form for every call or note) when
the domain demands near-zero-friction logging to actually get used.
Over-relying on color alone to convey pipeline stage.

## 11. Domain-specific accessibility considerations
Kanban board interactions (dragging a deal between stages) need a full
keyboard/screen-reader equivalent — an explicit "move to stage" action, not
just drag, per the direct-manipulation accessibility rule
(`ux-engine/interaction-design.md`).

## 12. Domain-specific scalability considerations
Pipeline boards must remain usable with thousands of deals per stage
(virtualized columns, filtering/segmentation — never an ever-scrolling,
unfiltered column). Duplicate-detection logic must perform at large
contact-database scale, not just flag obvious exact matches on small data.

## Explicitly not here
- The general reasoning technique any point above specializes →
  `product-intelligence/user-roles.md` (users), `business-logic.md`
  (workflows), `ux-engine/information-architecture.md` /
  `navigation-system.md` (structures/navigation), `ui-engine/visual-trends.md`
  (UI register), `ux-engine/accessibility.md` / `ui-engine/color-system.md`
  (accessibility), `product-intelligence/dependency-analysis.md`
  (scalability/dependencies).
- Product-specific knowledge for one actual CRM product → that product's
  generated Product Builder under `products/`.
