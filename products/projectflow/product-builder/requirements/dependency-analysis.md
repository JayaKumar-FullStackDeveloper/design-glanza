Source: Derived from `requirement-matrix.md` and Architect-phase module boundaries | Owning agent: product-architect.md | Version: v0.1.0

# ProjectFlow — Dependencies

## Modules
Workspace & Membership → Projects → Tasks → {Notifications, Reporting/Dashboard}

## Cross-module dependency table

| From module | To module | Nature | DEP-NNN |
|---|---|---|---|
| Projects | Workspace & Membership | sequencing — a project cannot exist without a workspace and ≥1 member | DEP-001 |
| Tasks | Projects | sequencing — a task cannot exist without a project | DEP-002 |
| Notifications | Tasks | data — triggers originate from task events (assign, due-date) | DEP-003 |
| Reporting/Dashboard | Projects, Tasks | data — aggregates both | DEP-004 |
| Notifications | External email/push service | integration | DEP-005 |

## Integration assumptions
`DEP-005`: `[ASSUMPTION: notification delivery (in-app at minimum, email
possibly) relies on an external delivery service \| BASIS: tier 7, standard
SaaS practice, not stated in brief \| IMPACT: if that service is slow or
down, delivery could silently fail — needs a system-error state and a retry
policy; in-app notification (COMPONENT-008) is the MVP-guaranteed channel,
email is not assumed reliable]`.

## Critical path
Workspace & Membership is the critical path — every other module depends on
it directly or transitively. Build order: Workspace & Membership → Projects
→ Tasks → (Notifications, Reporting) in parallel.

## Risk flagging
DEP-005 rests on an Assumed fact (no stated delivery mechanism) — flagged as
higher-risk: if the assumption is wrong (e.g. push notifications are
actually required, not just in-app), Notifications' scope changes
materially. Sequenced last specifically so this risk is discovered before
much else is built on top of it.

## No unresolved circular dependencies
Confirmed — the graph above is a strict DAG (Workspace → Projects → Tasks →
{Notifications, Reporting}), satisfying `config/quality-gates.md`'s
Architect → Prototype gate criterion.
