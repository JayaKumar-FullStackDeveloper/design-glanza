Source: `requirements/requirement-matrix.md` + `product-definition.md`'s chosen approach | Owning agent: ux-architect.md | Version: v0.1.0

# ProjectFlow — User Flows

Canonical notation per `ux-engine/user-flow-engine.md`. 4 flows covering the
success-criteria set from `product-definition.md`.

## FLOW-001 — Workspace creation & first project (Owner)
**Trigger:** Owner signs up, no workspace exists yet.
**Goal:** Owner has a workspace and a first project within one session
(success criterion 1).

1. Action: Owner enters workspace name, submits (REQ-001).
   System response: Workspace created; Owner role assigned; dashboard shown
   in **empty** state (EDGE-007) with a guided "Create your first project"
   prompt — not a blank screen.
2. Action: Owner creates a project (REQ-004).
   System response: Project created, empty task list shown.
   Next action: Owner is prompted to invite teammates (REQ-002) — optional,
   not blocking.
3. Decision: Does the Owner invite members now or later?
   → yes: Action: enters email(s), submits → System response: invite(s)
     created, pending (REQ-002/003).
   → no (skip): proceeds directly to Completion.
**Completion:** matches success criterion 1 — workspace + first project
exist.

**Recovery paths:**
- `validation error` at step 1 (empty workspace name) → retry, inline error
  shown, no data lost.
- `system error` at step 3 (invite send fails, DEP-005) → retry once,
  visible "invite not sent, try again" — does not block workspace/project
  creation, which already succeeded.

## FLOW-002 — Assign and track a task (Project Manager)
**Trigger:** A project exists with at least one member.
**Goal:** A task is created, assigned, and its status is visible on the
board (success criterion 2).

1. Action: Project Manager creates a task in a project (REQ-005).
   System response: Task created, **To Do** status, shown on board
   (REQ-011).
2. Action: Project Manager assigns the task to a Team Member (REQ-006).
   Decision: Is the assignee a member of this project? (BR-002/validation)
   → yes: System response: assignee set; SYSTEM notifies assignee
     (REQ-009).
   → no: `validation error` — "assignee must be a project member"
     (EDGE-009).
3. Action: Project Manager optionally sets due date (REQ-013) and priority
   (REQ-014).
   Decision: is due date ≥ today? (BR-005)
   → yes: stored.
   → no: `validation error`, retry with a corrected date.
**Completion:** task visible on board with assignee, status, due date —
matches success criterion 2.

**Recovery paths:**
- Invalid assignee (step 2) → retry with a valid project member.
- Past due date (step 3) → retry with a corrected date; task itself is
  already created and not lost.

## FLOW-003 — Team Member updates task status (highest-frequency flow)
**Trigger:** Team Member has ≥1 assigned task.
**Goal:** Task status reflects current reality (success criterion 3).

1. Action: Team Member opens their assigned task (from board or a
   "my tasks" filter) and moves it to **In Progress** (REQ-007).
   System response: status updated, board column changes.
2. Decision: does the task have an unresolved blocker? (BR-004)
   → no: proceeds normally toward Done.
   → yes: Action: Team Member marks it **Blocked** with a reason (REQ-018).
     System response: task enters Blocked status, reason stored.
3. Action: once unblocked, Team Member moves task to **Done** (REQ-007).
   Decision: is BR-004 satisfied (no open blocker)?
   → yes: System response: status = Done, dashboard aggregate updates
     (REQ-015).
   → no: `validation error` — "cannot complete: blocked by \<task\>".
**Completion:** task status accurately reflects work state — success
criterion 3.

**Recovery paths:**
- Attempted Done while blocked (step 3) → retry once the blocker is
  actually resolved; the task stays visibly Blocked in the interim, not
  silently stuck with no explanation.
- `offline` while updating (EDGE-008) → change shown as pending-sync;
  retries automatically on reconnect, per the `offline` state's recovery
  resolution.

## FLOW-004 — Guest views a shared project (read-only)
**Trigger:** Guest receives a share link/invite (REQ-016).
**Goal:** Guest sees current project status with zero onboarding (success
criterion 4).

1. Action: Guest opens the shared link.
   Decision: is the project still shared/available? (EDGE-004)
   → yes: System response: read-only board rendered (REQ-017), no action
     controls exposed.
   → no: System response: explicit "no longer available" state, not a
     broken page.
**Completion:** Guest can see status without any account setup beyond
accepting the share — success criterion 4.

**Recovery paths:**
- Project no longer shared/deleted (EDGE-004) → abandon-safely: clear
  message, no dead end, no error stack shown.
