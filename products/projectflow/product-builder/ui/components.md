Source: `ui-engine/component-system.md`'s 8-point framework | Owning agent: ui-designer.md + design-system-expert.md | Version: v0.1.0

# ProjectFlow — Component Specs

8 components. Each addresses all 8 points; abbreviated here to what's
product-specific (behavior/accessibility/responsive cite the engine
technique rather than restate it).

| ID | Component | Category | Purpose | Variants | States | Content rule |
|---|---|---|---|---|---|---|
| COMPONENT-001 | Task Card | molecule | represent one task on board/list | size(compact for list, comfortable for board) | default/hover/dragging/pending-sync (+ full state-matrix row) | title truncates at 2 lines; assignee shown as avatar + name |
| COMPONENT-002 | Status Badge | atom | show a task's status | one per lifecycle status (To Do/In Progress/Blocked/Done/Cancelled) | default (no interactive states — display-only) | label always present alongside color, never color-only |
| COMPONENT-003 | Board Column | organism | group cards by status | one per status | default/empty (EDGE-007 variant)/loading | column header shows status name + count |
| COMPONENT-004 | Data Table | organism | list view of tasks | — | default/loading/empty/sorted (per repaired sorting technique) | tabular figures for due-date column |
| COMPONENT-005 | Task Detail Drawer | organism | full task detail + edit | read-only variant (Guest) | default/loading/saving/conflict (EDGE-002) | see `ux/state-matrix.md` SCREEN-005 row |
| COMPONENT-006 | Invite Member Form | molecule | invite by email + role | — | default/validating/error (EDGE-006 duplicate)/success | one email per invite in this pass; `[ASSUMPTION: no bulk-invite | BASIS: not in requirement-matrix.md]` |
| COMPONENT-007 | Empty State Panel | molecule | guide first action | one per empty context (dashboard, board column, project list) | default only | always includes a specific next action, never just "no data" (saas.md's named risk) |
| COMPONENT-008 | Notification Toast | molecule | transient event notice | info (assignment) / warning (due-soon) | enter/visible/exit | auto-dismiss, but persists in a Notifications list (SCREEN not built this pass — `[ASSUMPTION: notification history screen deferred | BASIS: not in requirement-matrix.md's built scope]`) |

## Reuse discipline
Status Badge (COMPONENT-002) is reused identically across Board, List, and
Task Detail — no per-screen reinvention. Task Card (COMPONENT-001) has one
anatomy with a size variant, not two separate components for board vs. list
— confirmed against the reuse-vs-new-variant rule before creating a second
component.
