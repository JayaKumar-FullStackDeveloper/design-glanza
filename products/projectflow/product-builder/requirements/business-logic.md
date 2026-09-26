Source: Derived from `requirements/requirement-matrix.md` per `product-intelligence/business-logic.md`'s technique | Owning agent: product-architect.md | Version: v0.1.0

# ProjectFlow — Business Rules

| ID | Rule | Governs |
|---|---|---|
| BR-001 | A task's status follows a fixed lifecycle: `To Do → In Progress → Blocked → In Progress → Done`, plus `Cancelled` from any non-terminal state | REQ-001, REQ-005, REQ-007, REQ-018 |
| BR-002 | Only Owner or Project Manager may assign a task to another member | REQ-006 |
| BR-003 | Guest/Viewer access is read-only and scoped to explicitly shared projects only — never workspace-wide | REQ-016, REQ-017 |
| BR-004 | A task cannot transition to Done while it has an unresolved blocking dependency | REQ-019 |
| BR-005 | A task's due date must be today or later at creation/edit time | REQ-013, REQ-022 |
| BR-006 | Removing a member does not delete their historical activity (comments, past status changes) — only unassigns their open tasks | REQ-020 |
| BR-007 | `[ASSUMPTION: notification triggers fire once per event, no digest/batching in MVP scope \| BASIS: tier 8, nothing stated \| IMPACT: could cause notification fatigue under heavy usage; a digest mode may need revisiting once real usage data exists]` | REQ-009, REQ-010 |

## Status logic — Task lifecycle (state machine)

| State | Entry trigger | Exit trigger(s) → next state(s) | Invalid-transition handling |
|---|---|---|---|
| To Do | Task created (REQ-005) | Assignee starts work → In Progress | — |
| In Progress | Entered from To Do or un-blocked | Marked done → Done; blocker found → Blocked; cancelled → Cancelled | Attempting Done while BR-004 blocks it → `edge-case-engine.md` EDGE-003 |
| Blocked | Blocking dependency unresolved (REQ-018) | Blocker resolved → In Progress | Attempting to skip straight to Done → rejected, `validation error` |
| Done | Marked done, no open blocker (BR-004) | *(terminal, but can be reopened → In Progress, logged as an explicit assumption)* | `[ASSUMPTION: Done is reopenable \| BASIS: tier 7 common PM-tool convention \| IMPACT: if Done is meant to be truly terminal, this needs revisiting]` |
| Cancelled | Explicitly cancelled from To Do/In Progress/Blocked | *(terminal)* | — |

## Decision points
- "Is the actor allowed to assign this task?" → BR-002 → yes (Owner/PM) proceeds to REQ-006; no → `permission denied` state.
- "Does this task have an open blocker?" → BR-004 → yes → Done transition rejected; no → proceeds.
- "Is the due date in the past?" → BR-005 → yes → `validation error`; no → proceeds.

## Operational workflow (assign → complete)
Project Manager creates task (REQ-005, To Do) → assigns to Team Member
(REQ-006, BR-002 checked) → SYSTEM notifies assignee (REQ-009) → Team Member
moves to In Progress (REQ-007) → \[optionally Blocked/In Progress cycle,
REQ-018/BR-004] → Team Member marks Done (REQ-007, BR-004 checked) →
dashboard aggregate updates (REQ-015).

## Success / failure conditions
- **REQ-006 (assign) success:** assignee field set, assignee is a valid
  project member, notification sent. **Failure:** assignee not a member →
  `validation error`; actor lacks permission → `permission denied` (BR-002).
- **REQ-007 (status update) success:** new status stored, matches a valid
  lifecycle transition. **Failure:** invalid transition (e.g. Done while
  blocked) → `validation error` (BR-004).
- **REQ-013 (due date) success:** date stored, ≥ today. **Failure:** date in
  the past → `validation error` (BR-005).

## Explicitly not here
- Edge-case scenarios these rules produce → `edge-cases.md`.
- Role/permission definitions → `user-roles.md`.
- How these states are visually/behaviorally represented → `ux/state-matrix.md`.
