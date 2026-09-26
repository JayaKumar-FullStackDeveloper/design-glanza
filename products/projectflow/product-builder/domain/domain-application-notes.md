Source: `product-intelligence/domain-classifier.md` applied to BRD/brief.md | Owning agent: product-architect.md | Version: v0.1.0

# ProjectFlow — Domain Classification & Pack Application

## Classification
**Confident match: `saas`.** Signals: explicit "Type: SaaS" statement
(strong, stated), "Project Management" domain naming (strong, stated). No
signals for any other pack (no multi-module ERP-style cross-referencing, no
regulatory/healthcare/financial terms, no marketplace two-sidedness). No
hybrid or partial-match handling needed — this is the clean, high-confidence
case.

## `product-types/saas.md` conventions applied
- **Multi-tenancy assumed by default** — every entity (project, task) is
  workspace-scoped; reflected in `user-roles.md`'s multi-tenancy note.
- **Onboarding/activation named as highest-leverage flow** — directly drove
  `FLOW-001` being the first flow built and its screen (dashboard empty
  state, EDGE-007) getting explicit design attention rather than being an
  afterthought.
- **Subscription/billing lifecycle** — `[ASSUMPTION: a trial → active →
  past-due → churned state machine applies at the workspace level, per
  saas.md convention \| BASIS: tier 6 \| IMPACT: no billing requirement was
  actually stated in the brief; this is deferred (see product-definition.md
  "explicitly deferred") rather than built, since the brief gave no signal
  about pricing model at all — building it now would be inventing business
  rules the source doesn't support (Rule 10)]`. Billing settings screen
  (SCREEN-007) is scaffolded as a placeholder location, not populated.
- **Empty-state UX risk** — explicitly designed for (EDGE-007), per saas.md's
  named risk that new workspaces starting empty is common and must guide
  toward first value, not just say "no data."

## No core-file changes
Nothing in `config/`, `methodology/`, `product-intelligence/`, `ux-engine/`,
or `ui-engine/` was modified to produce this product — every decision above
cites the existing `saas.md` pack and general engine technique. Confirms
Rule 14 (domain-agnostic core) held throughout this exercise.
