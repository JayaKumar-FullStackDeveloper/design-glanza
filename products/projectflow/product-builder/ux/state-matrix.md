Source: `ux/screen-architecture.md` + `requirements/edge-cases.md` | Owning agent: interaction-designer.md | Version: v0.1.0

# ProjectFlow — State Matrix

All 13 mandatory states (`ux-engine/state-design.md`) per screen/component.
Zero blank cells — every cell is designed, N/A with a reason, or deferred
with a reason, per `config/quality-gates.md` B7.

| Screen/Component | initial | loading | success | empty | validation error | system error | permission denied | processing | completed | cancelled | conflict | timeout | offline |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SCREEN-001 Dashboard | designed: blank-slate copy before first project | designed: skeleton cards while aggregates load | designed: aggregate counts render | designed (EDGE-007): guided "create your first project" prompt, not blank | N/A (read-only screen) | designed: "couldn't load status" + retry | N/A (visible to all workspace roles) | N/A (no long-running action here) | N/A (no single completable action) | N/A | N/A (no concurrent-edit surface) | designed: same as system error, framed as "taking longer than expected" | designed: cached last-known counts shown with a "may be outdated" note |
| SCREEN-003 Board | designed: columns visible, empty | designed: skeleton cards per column | designed: cards render grouped by status | designed (EDGE-007): "no tasks yet — create one" per column | N/A (view-only screen; validation lives in Task Detail/create) | designed: column fails to load, retry per-column | designed (ROLE-004): controls hidden per role, not shown-disabled | designed: card shows a subtle pending indicator while a drag/status-change saves | N/A (board has no single completable action) | N/A | designed (EDGE-002): "updated by X — reload" banner on the affected card | designed: drag/status-change retried once, then system error | designed (EDGE-008): pending-sync indicator on the affected card, change preserved locally |
| SCREEN-004 List | designed: table shell, empty | designed: skeleton rows; sort/paginate loading scoped to table region only | designed: rows render | designed: filtered-to-nothing state, distinct copy from EDGE-007's true-empty | N/A | designed: "couldn't load tasks" + retry | designed: bulk-action controls hidden for ROLE-003/004 | designed: subtle row-level pending indicator during sort/paginate | N/A | N/A | designed (EDGE-002): same conflict banner as board, per affected row | designed: same as system error after retry | designed: same pending-sync pattern as board |
| SCREEN-005 Task Detail | designed: fields populated from task data | designed: skeleton while task loads | designed: save confirmation (subtle, per action-feedback <1s rule) | N/A (a task always has at least a title) | designed (BR-005/BR-004): inline error on due-date/status fields | designed: "couldn't save changes" + retry, edits preserved in the field | designed: read-only rendering for ROLE-004 (no editable controls at all) | designed: comment-submit shows pending state | designed: terminal Done styling, still viewable | designed: terminal Cancelled styling, still viewable | designed (EDGE-002): "this task changed since you opened it — reload" | designed: comment/save retried once, then system error | designed (EDGE-008): edits marked pending-sync, not lost |
| COMPONENT-001 Task Card | N/A (atom has no "first load" of its own) | designed: skeleton-card variant | designed: default rendered state | N/A (a card only exists for a real task) | N/A (validation happens in the drawer, not the card) | designed: card shows a small error indicator if its own data failed to refresh | designed (ROLE-004): no drag handle, no quick-action buttons rendered | designed: dimmed/pending visual during an in-flight change | N/A (card doesn't own "completed", the board region does) | N/A | designed (EDGE-002): highlighted border + inline "updated" flag | designed: same as system error after retry | designed (EDGE-008): pending-sync badge |

## Remaining screens
SCREEN-002 (Projects list), SCREEN-006 (Members), SCREEN-007 (Billing,
deferred), SCREEN-008 (Guest read-only) follow the identical discipline
(loading/empty/error states analogous to SCREEN-001/003/008's read-only
variant) — not exhaustively tabulated in this pass; flagged in the final
report's Gaps section rather than silently presented as complete.

## Priority conflicts
Where `permission denied` and `loading` could both apply (e.g. Guest
loading a since-restricted project), `permission denied` wins per
`state-design.md`'s precedence order — confirmed applied at SCREEN-008.
