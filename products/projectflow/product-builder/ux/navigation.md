Source: `ux/sitemap.md` | Owning agent: ux-architect.md | Version: v0.1.0

# ProjectFlow — Navigation

## Pattern selection (per `ux-engine/navigation-system.md`'s rule, not convention)
Top-level sections: Dashboard, Projects, Notifications, Workspace Settings =
**4 sections** — this does **not** meet the sidebar rule's threshold (>5
top-level sections *and* depth beyond 2 levels). Despite SaaS "convention"
often defaulting to a sidebar, the actual rule is followed here: **top
navigation bar** is used for primary navigation, not a sidebar. This is a
deliberate example of ruling by the stated technique rather than domain
habit.

## Primary navigation
Top nav bar: Dashboard | Projects | Notifications | \[Workspace name ▾ →
Settings, for ROLE-001 only, hidden entirely for others per role-based
navigation — Deny is not shown-disabled].

## Secondary navigation
Within Project Detail: **Board | List** tabs (REQ-012's view toggle) — a
tab pattern, since it's two sibling views of one dataset, not a hierarchy.

## Deep navigation
Task Detail is reached by clicking a task card directly (one click from
Board/List), not by a forced drill-through — satisfies the minimal-
user-effort criterion for this daily-frequency interaction.

## Back behavior
Closing the Task Detail drawer returns to the exact board/list scroll
position and filter state it was opened from — never a full reload back to
an unfiltered board.

## Breadcrumbs — the explicit 3-condition test applied
- At **Dashboard, Projects list, Project Detail**: depth < 3 from root, and
  "back" already covers the need → **no breadcrumbs**.
- At **Task Detail**: depth reaches 3-4 (Projects → Project → Task), there's
  a genuine need to jump directly back to "Projects" (skipping "this
  project"), and the hierarchy is a strict tree (a task belongs to exactly
  one project) → **all three conditions hold. Breadcrumbs are used here**:
  `Projects > [Project Name] > [Task Name]`.
This is not applied uniformly — it's the one screen where the rule's
conditions are actually satisfied.

## Modal vs. drawer vs. overlay
- **Task Detail → drawer** (not a modal): keeps the board/list context
  visible behind it, since users frequently reference the board while
  reading a task (per the drawer-vs-modal rule).
- **Invite Member → modal**: short, focused, fully interrupting task with
  no need to see the members list behind it while filling the form.
- **Notification → toast (overlay)**: transient, dismissible, never used
  for anything with a `processing` state.

## Multi-step workflows
None in this scope — every flow in `user-flows.md` is short enough to stay
single-step/single-screen; no stepper pattern needed here.

## Cross-module navigation
From Task Detail, a link to "View assignee's other tasks" would cross into
a filtered board view — `[ASSUMPTION: deferred to a later pass; not built
in this exercise | BASIS: not in the stated success criteria | IMPACT: none
for this MVP scope]`.

## Role-based navigation
Workspace Settings is entirely absent from ROLE-002/003/004's nav — not
shown-disabled, per the Deny-by-default rule (`user-roles.md`). Guest
(ROLE-004) sees only the Shared Project node — no Dashboard, no Projects
list, no Settings at all.
