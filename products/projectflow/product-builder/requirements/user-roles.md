Source: BRD/brief.md + `product-types/saas.md` domain convention | Owning agent: brd-analyst.md | Version: v0.1.0

# ProjectFlow — User Roles & Permissions

## Roles

| ID | Role | Scope |
|---|---|---|
| ROLE-001 | Owner | Whole workspace |
| ROLE-002 | Project Manager | Whole workspace (all projects) |
| ROLE-003 | Team Member | Assigned tasks + projects they're a member of |
| ROLE-004 | Guest/Viewer | One explicitly shared project, read-only |
| SYSTEM | Automated triggers | Notifications, scheduled reminders |

`[ASSUMPTION: exactly these 4 human roles, no finer-grained custom-role
system | BASIS: tier 6, standard PM-SaaS role set per product-types/saas.md
and general domain convention | IMPACT: if the real team needs custom
per-project roles beyond this, ROLE-NNN and the permission matrix below
would need extending, not redesigning]`.

## Permission matrix

| Role | Resource/Action | Access | Condition |
|---|---|---|---|
| ROLE-001 | Manage billing, workspace settings | Allow | — |
| ROLE-001 | Invite/remove members | Allow | — |
| ROLE-001 | Create/edit/delete any project | Allow | — |
| ROLE-002 | Manage billing | Deny | — |
| ROLE-002 | Create/edit/archive projects | Allow | — |
| ROLE-002 | Create/assign/edit tasks | Allow | Within workspace |
| ROLE-002 | Invite Guest to a project | Allow | Only projects they manage |
| ROLE-003 | Create tasks | Allow | Within projects they're a member of |
| ROLE-003 | Assign tasks to others | Deny | — (BR-002) |
| ROLE-003 | Update status/comment on own or unassigned tasks | Allow | — |
| ROLE-003 | Edit workspace/project settings | Deny | — |
| ROLE-004 | View project board/list | Allow | Only the specific shared project |
| ROLE-004 | Any write action | Deny | — |
| ROLE-004 | View other workspace projects | Deny | Fails closed by default (Rule 5-adjacent: permission fails closed) |

Deny is the default for anything not explicitly listed — fail-closed, per
`product-intelligence/user-roles.md`'s permission-matrix technique.

## Hierarchy / delegation
Owner implicitly has every Project Manager permission (hierarchy, not a
separate grant). No delegation mechanism in this scope — `[ASSUMPTION: no
"acting on behalf of" delegation in MVP | BASIS: tier 8 | IMPACT: if a
Project Manager goes on leave, tasks must be manually reassigned (see
EDGE-001), not auto-delegated]`.

## Multi-tenancy
Every role is scoped to exactly one workspace; a person who belongs to two
workspaces holds independent role assignments in each (no cross-workspace
visibility).

## System actor
`SYSTEM` initiates REQ-009 (assignment notification) and REQ-010 (due-date
reminder) — see `requirements/business-logic.md` §3 for trigger conditions.
