Source: `ui-engine/responsive-system.md` | Owning agent: ui-designer.md | Version: v0.1.0

# ProjectFlow — Responsive Behavior

| Screen | Desktop | Tablet | Mobile |
|---|---|---|---|
| SCREEN-003 Board | Full multi-column board | Horizontal-scroll columns (still board metaphor) | Single status column at a time, swipe/select to change column (data-table-style collapse adapted for board layout) |
| SCREEN-004 List | Full table, all columns | Full table, priority columns only | Stacked-card-per-row (per `responsive-system.md`'s data-table technique — few-critical-columns case) |
| SCREEN-005 Task Detail | Drawer, board/list visible behind it | Drawer, narrower | Full-screen takeover (drawer metaphor doesn't fit — priority content, per `visual-hierarchy.md`, must stay reachable at the smallest breakpoint) |
| SCREEN-001 Dashboard | Multi-column card grid | 2-column | Single column, stacked, overdue count first (priority-preservation rule) |

Touch targets ≥44×44px on tablet/mobile for all task-card actions and
status-pill controls. Primary action ("Create task"/"Create project")
remains reachable without scrolling at the smallest breakpoint, per the
priority-preservation rule — secondary actions (bulk operations, if any)
collapse into an overflow menu first.
