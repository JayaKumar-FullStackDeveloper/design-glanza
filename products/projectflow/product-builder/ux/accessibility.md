Source: `ux/screen-architecture.md`, `ux/ux-rules.md`, `ux/state-matrix.md` | Owning agent: accessibility-expert.md | Version: v0.1.0

# ProjectFlow — Accessibility (Structural/Behavioral)

## Focus order
Board (SCREEN-003): column order left-to-right, cards top-to-bottom within
a column — matches the visual scan order (`ui-engine/visual-hierarchy.md`'s
F-pattern for this data-dense screen). Task Detail drawer: focus moves into
the drawer on open (title field first) and returns to the originating card
on close.

## Keyboard operability
- **Drag-to-reorder/re-status (board):** keyboard equivalent is the status
  dropdown in Task Detail (`ux-rules.md`) — confirmed non-drag path exists
  for every drag interaction.
- **Sort headers (list view):** focusable, `Enter`/`Space`-activatable,
  per the sorting/pagination repair applied to `interaction-design.md`.
- **Pagination controls:** Tab-navigable; boundary controls (prev on page
  1, next on last page) are `disabled` (announced as such), never silently
  inert.
- **Multi-select on the list (future bulk actions):** `[ASSUMPTION: not
  built in this pass — no bulk actions in the requirement set | BASIS: not
  in requirement-matrix.md | IMPACT: if added later, needs the Shift/Ctrl +
  explicit select-mode-toggle equivalence from interaction-design.md]`.

## Semantic / ARIA mapping
- Board columns: each column is a labeled region (`aria-label` = status
  name); cards within are a list.
- Task Detail: `dialog`-adjacent semantics for a drawer (per
  `ux-engine/accessibility.md`'s drawer mapping — `complementary`, since it
  supplements rather than fully interrupts the board behind it).
- Sort state: `aria-sort` (or equivalent) on the active column header.
- Status Badge (COMPONENT-002): status conveyed by an accessible label,
  never color alone — directly enforces `ui-engine/color-system.md`'s
  color-blind-safety rule for the single most status-dependent component in
  this product.

## Screen-reader flow
Dashboard's status-summary cards are announced in priority order (overdue
count first, since it demands the most urgent action — matching
`state-design.md`'s state-priority logic applied to content, not just
states).

## Recovery-path and permission-denied accessibility
- `offline` pending-sync badges (EDGE-008) carry an accessible label
  ("Saving — will sync when back online"), not just a visual icon.
- Guest's hidden controls (SCREEN-008) are absent from the DOM/focus order
  entirely, not merely visually hidden — a screen-reader user gets no
  false affordance to try an action that will fail permission checks.

## Conformance target
`[ASSUMPTION: WCAG AA baseline, per ux-engine/accessibility.md's default |
BASIS: no stricter domain mandate applies — saas.md/project-management has
none | IMPACT: none — this is the standard default, not a deviation]`.
