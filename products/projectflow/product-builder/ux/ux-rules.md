Source: `ux/screen-architecture.md` | Owning agent: interaction-designer.md | Version: v0.1.0

# ProjectFlow — Interaction Rules

## Task card drag (board, REQ-007)
Direct-manipulation reorder/re-status by dragging a card between columns.
Per `ux-engine/interaction-design.md`'s direct-manipulation rule, ships with
a non-drag alternative from day one: each task card's status can also be
changed via a status dropdown in Task Detail (SCREEN-005) — never
drag-only.

## Sorting and pagination (List view, SCREEN-004; per the just-repaired
`ux-engine/interaction-design.md` technique)
- Sortable columns: Priority, Due Date, Status, Assignee. Clicking a column
  header cycles unsorted → ascending → descending → unsorted; current sort
  shown with an icon **and** a text-equivalent accessible label (never
  icon-only).
- Re-sort triggers a `loading` state on the table region only if it
  requires a server round-trip (>1s); rows stay visible, not blanked,
  during the sort.
- Pagination: 25 tasks per page `[ASSUMPTION: page size, not stated |
  BASIS: tier 7 common default | IMPACT: adjust once real task-volume data
  exists]`. Filtering by status/assignee always resets to page 1.
- Keyboard: sort headers are focusable, `Enter`/`Space`-activatable; page
  controls are Tab-navigable; current page announced to assistive tech.

## Assign action (REQ-006)
Feedback timing: assignment is a fast, local operation (<1s expected) — a
subtle pending indicator on the assignee field is sufficient; no full-page
loading state.

## Undo / confirmation
- Changing task status (REQ-007): reversible, low risk (can be changed
  again) → no confirmation, no undo affordance needed beyond just changing
  it back.
- Removing a member (REQ-020): irreversible in effect on their access,
  high-risk (affects their assigned work, EDGE-001) → confirm before
  acting, with the impact ("N open tasks will be unassigned") stated in the
  confirmation itself.
- Deleting a project: `[ASSUMPTION: not explicitly in the requirement set
  built this pass, but implied by "archive project" — if built, this is
  irreversible + high-risk → confirm + secondary step | BASIS: tier 7 |
  IMPACT: flagged for the next pass, not silently built without this rule]`.

## Error prevention
The assignee dropdown (REQ-006) only lists actual project members — an
invalid assignee is structurally unavailable, not allowed-then-rejected
(per the error-prevention-through-interaction rule), which is why EDGE-009
is a Minor/Low-likelihood edge case rather than a common failure.

## Fast decision-making
When creating a task (REQ-005), "To Do" is pre-selected as the default
status (not an equally-weighted picker) and due date defaults to unset
rather than forcing a choice — the one required field is the title.
