Source: `ux/sitemap.md` + `ux/user-flows.md` | Owning agent: ux-architect.md | Version: v0.1.0

# ProjectFlow — Screen Architecture

8 screens. Composition patterns per `ui-engine/layout-system.md`.

| ID | Screen | Composition pattern | Primary action | Regions | Traces to |
|---|---|---|---|---|---|
| SCREEN-001 | Dashboard | dashboard-grid | Create project (if empty, EDGE-007) / — (otherwise, purely informational) | header, status-summary cards, recent-activity list | FLOW-001, REQ-015 |
| SCREEN-002 | Projects (list) | list + detail (list side) | Create project | header, project list | FLOW-002, REQ-004 |
| SCREEN-003 | Project Detail — Board | custom (board columns, master-detail-like) | Create task | header (Board/List tabs), status columns, task cards | FLOW-002, FLOW-003, REQ-011 |
| SCREEN-004 | Project Detail — List | list + detail (list side) | Create task | header (Board/List tabs), sortable/filterable task table | REQ-012 |
| SCREEN-005 | Task Detail (drawer) | drawer, not a full page | Update status | title/status header, details (assignee, due date, priority), comments | FLOW-002, FLOW-003, REQ-007/008/013/014 |
| SCREEN-006 | Workspace Settings — Members | single-column-form/list | Invite member | member list, invite control | FLOW-001, REQ-002/020 |
| SCREEN-007 | Workspace Settings — Billing | single-column-form | — (scaffolded, deferred) | placeholder only | product-definition.md (deferred) |
| SCREEN-008 | Shared Project (Guest, read-only) | custom (board, no controls) | none — read-only | header (project name only, no settings), status columns, task cards (view-only) | FLOW-004, REQ-017 |

Every screen has **exactly one** primary action (or explicitly none, for
read-only/informational screens SCREEN-001-secondary-state, SCREEN-007,
SCREEN-008) — no screen has two competing primary actions.

## Explicitly not here
Full content/interaction/state detail per screen → this file's companion
`ux-rules.md` (interaction) and `state-matrix.md` (states); visual detail →
`ui/*`.
