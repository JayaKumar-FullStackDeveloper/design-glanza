Source: `ux/user-flows.md` | Owning agent: ux-architect.md | Version: v0.1.0

# ProjectFlow — Sitemap

```
Dashboard                              [ROLE-001, ROLE-002, ROLE-003]        <- FLOW-002/003 (status overview)
Projects (list)                        [ROLE-001, ROLE-002, ROLE-003]        <- FLOW-002
  Project Detail — Board view          [ROLE-001, ROLE-002, ROLE-003]        <- FLOW-002, FLOW-003
    Task Detail (drawer)               [ROLE-001, ROLE-002, ROLE-003]        <- FLOW-002, FLOW-003
  Project Detail — List view           [ROLE-001, ROLE-002, ROLE-003]        <- FLOW-002 (alt. view, REQ-012)
  Shared Project (Guest, read-only)    [ROLE-004 only]                       <- FLOW-004
Workspace Settings
  Members                              [ROLE-001 only]                       <- FLOW-001
  Billing                              [ROLE-001 only]                       <- scaffolded only, deferred (product-definition.md)
Notifications (in-app)                 [ROLE-001, ROLE-002, ROLE-003]        <- REQ-009/010
```

Depth: 3 levels at most (Projects → Project Detail → Task Detail) —
justified, since Task Detail genuinely needs its own addressable place
(comments, due date, priority all live there) rather than being flattened
into the board.

Guest's "Shared Project" node is a *separate, permission-scoped* node, not
the same Project Detail node with conditional UI — per `ux-engine/
information-architecture.md`'s permission-aware-structure rule: a node a
role cannot fully access isn't just hidden-but-present, it's a distinct,
intentionally-restricted node (SCREEN-008).

No orphan nodes — every node above traces to a `FLOW-NNN` (cited) or a
requirement (Billing, deferred but still traced to product-definition.md's
explicit scope-boundary log, not silently absent).
