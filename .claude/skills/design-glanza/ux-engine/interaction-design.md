# Interaction Design

## Responsibility
Behavior rules for how the interface responds to user action at the micro
level — what happens on click/tap/hover/drag/gesture/keystroke. Behavior only;
how it *looks* while doing so belongs to `ui-engine/*`. Every rule below is in
service of `user-flow-engine.md`'s optimization criteria, cited by name rather
than restated.

## Action-feedback rules
Every user-initiated action gets feedback, timed by what it's waiting on:
- **< 100ms** — perceived as instant; no explicit feedback needed beyond the
  action's own visible result.
- **100ms – 1s** — show a subtle pending indicator (a button's own state
  change) so the action registers as received.
- **> 1s** — show an explicit loading/processing indicator
  (`state-design.md`'s `loading`/`processing` states) — silence past one
  second reads as the system having missed the action entirely, which
  violates operational clarity (`user-flow-engine.md` criterion 8).

**Skeleton vs. spinner, when a `loading` state is shown:** use a skeleton
(a placeholder matching the eventual layout's shape) when that layout is
already known before the data arrives — it reads as faster because the user
can already see *where* content is landing. Use a spinner/indeterminate
indicator when the eventual layout genuinely isn't known yet (a search
whose result count/shape can't be predicted). A skeleton for a layout that
isn't actually fixed yet is worse than a plain spinner — it promises a shape
that then has to visibly reflow.

**Optimistic UI, where the action's outcome is highly predictable:** for an
action whose failure is rare and cheap to reverse (a like, a reorder, a
toggle), update the interface immediately to the expected result rather than
waiting on the round-trip, then reconcile silently on the real response —
and if the response contradicts the optimistic update, roll it back with a
visible, explained correction rather than a silent revert. Reserve this for
exactly that low-risk/high-predictability case; the reversibility×risk
matrix below still governs every action outside it — an irreversible or
high-risk action is never shown as done before it actually is.

## Direct-manipulation patterns
Drag-drop, resize, and reorder are appropriate when the action's *spatial*
relationship is itself the information (reordering a priority list, resizing a
panel). Every direct-manipulation interaction must ship with a non-drag
alternative (e.g. move-up/move-down actions, an explicit position field) from
the moment it's designed — not as a later accessibility patch. This is the
concrete, interaction-level enforcement of the accessibility-by-construction
check already applied at `methodology/ideate.md`'s selection stage.

Concrete thresholds, so "drag" and "long-press" are specified rather than
left to feel: a drag gesture activates only after roughly **10–15px** of
pointer movement (a smaller threshold makes an ordinary click/tap
mis-register as a drag); a long-press activates at roughly **500ms** of
sustained contact, distinct from a tap. Where a platform reserves a
gesture for its own system-level use (e.g. an edge-swipe for OS
navigation), the product's own gesture never overrides it — the system
gesture always takes priority, and the product's interaction is reachable
another way on that platform.

## Undo / confirmation rules
Chosen by crossing reversibility with risk, not by habit:

| | Low risk | High risk |
|---|---|---|
| **Reversible** | No confirmation; offer an undo affordance after the fact | Confirm before acting (a lightweight inline confirm is enough) |
| **Irreversible** | Confirm before acting | Confirm before acting **and** require a deliberate secondary step (e.g. typing a confirmation phrase) before the action fires |

"Risk" here is set by the business rule the action triggers
(`product-intelligence/business-logic.md`) — an action whose failure condition
is expensive or hard to recover from is high-risk regardless of how simple its
UI is.

## Gesture / input-modality rules
Every interaction defined here must have an equivalent across mouse, touch, and
keyboard — stated per interaction, not assumed:

| Interaction | Mouse | Touch | Keyboard |
|---|---|---|---|
| Activate | Click | Tap | Enter / Space |
| Reorder (direct-manipulation) | Drag | Long-press + drag | Move-up/move-down action (see above) |
| Reveal secondary content | Hover | Tap-to-reveal (not hover — hover doesn't exist on touch) | Focus-triggered reveal |
| Multi-select | Click + Shift/Ctrl | Explicit "select" mode toggle | Shift/Ctrl + Enter equivalent, or an explicit select-mode toggle |

A hover-only reveal is a defect the moment it's specified — it has no touch
equivalent by construction, which fails `methodology/ideate.md`'s accessibility
check retroactively if it slips through.

## Affordance clarity
Two distinct, equally common defects, worth distinguishing by name: a
**false affordance** — an element that looks interactive (button-like
styling, a pointer cursor) but isn't wired to anything — and a **missing
affordance** — an element that *is* interactive but reads as static text or
plain content, giving the user no visual reason to try it. Every interactive
element must look interactive and every look-interactive element must
actually be interactive; a screen review that only checks "does the primary
action look prominent" (`ui-engine/visual-hierarchy.md`) without checking
both directions on secondary/tertiary elements misses this class of defect.

## Recovery space after an error
Once an error is shown and the user begins correcting it, leave a brief,
deliberate pause — roughly **300–600ms** — before surfacing the *next*
prompt or validation result, even if the system could respond instantly.
Immediately chaining a second correction demand onto the first (or
re-validating faster than the user can read the first message) reads as
the system rushing them past a mistake rather than giving them room to
absorb and fix it — the same asymmetric-timing principle in this file's
Motion and animation section, applied here to error-recovery pacing
specifically rather than motion.

## Error prevention through interaction, not just messaging
Prefer making an invalid action *unavailable* (disabled state, filtered
options) over allowing it and then rejecting it with an error message after
the fact — this is `user-flow-engine.md` criterion 5 applied at the
interaction level. Where an action can't be disabled ahead of time (its
validity depends on a check only the system can run, e.g. a uniqueness check),
the rejection must arrive as fast as the action-feedback timing rules above
allow, not as a delayed surprise.

## Fast decision-making through interaction
Where a business rule (`product-intelligence/business-logic.md`) identifies a
recommended or default choice, the interaction surfaces it as visually and
interactionally primary (first in tab order, pre-selected, or the default
button) rather than presenting equally-weighted options the user must
evaluate from scratch each time — `user-flow-engine.md` criterion 2.

## Sorting and pagination
Two of the most common interaction patterns on any list/table, specified
explicitly rather than left to be improvised per screen:

- **Sorting.** Activating a sort control (typically a column header) cycles
  through a defined, closed state sequence (e.g. unsorted → ascending →
  descending → unsorted) — never an undiscoverable or inconsistent toggle.
  The current sort column and direction are always visibly indicated, and
  never by an icon alone (pair with the icon's accessible name — this is the
  list-sorting instance of the color/icon-only-encoding prohibition in
  `ui-engine/color-system.md`). If re-sorting requires a server round-trip,
  it follows the same action-feedback timing rules above (a `loading` state
  per `state-design.md` past the 1s threshold) — the existing rows stay
  visible while re-sorting, not replaced by a blank loading screen, so the
  user doesn't lose their place.
- **Pagination.** Page-change controls (next/previous, explicit page
  numbers, or "load more") trigger the same `loading` state on the affected
  content region only — never a full-page reload feel. Boundary behavior is
  explicit: "previous" is disabled (not silently inert) on page 1, "next" is
  disabled on the last page, and the current page plus total
  pages/items is always visible, never left for the user to infer by
  trial and error.
- **Accessibility and keyboard behavior.** Both patterns are fully
  keyboard-operable per the gesture/input-modality table above: a sort
  control is a focusable, `Enter`/`Space`-activatable element (never a
  bare click-only header with no semantic role), and its new state is
  announced to assistive technology (e.g. an `aria-sort`-equivalent
  semantic on the column), not conveyed visually only. Pagination controls
  are Tab-navigable in reading order, and the current page is announced,
  not just highlighted.
- **Interaction with search/filter.** Sorting, filtering, and pagination
  apply in one fixed, defined order — **filter → sort → paginate** — so
  results are deterministic and never depend on which the user touched
  most recently. Where a query (not just a filter) produces the working
  result set, `ux-engine/search-ux.md` governs the query/ranking step itself;
  this fixed order still applies to whatever set the query produces. Changing a filter or search term always resets pagination
  back to page 1 (never silently show "page 3" of a result set that no
  longer has a page 3). If filtering or searching produces zero results,
  that's the `empty` state (`state-design.md`), not a blank list
  indistinguishable from "still loading" or a bug.

## Motion and animation
Motion is a behavior decision, not a decoration decision — specified here by
*whether/why* it happens; the concrete duration/easing token used to execute
it stays `ui-engine/design-system.md`'s (motion-fast/base/slow). Converged
independently across multiple external design-engineering sources (Apple's
WWDC interface guidance; Emil Kowalski's design-engineering practice), so
treated as a stable principle rather than one author's taste.

- **Frequency-based animate/don't-animate gate.** Before specifying any
  motion, ask how often the actor sees this exact transition
  (`methodology/empathize.md` dimension 7, the same frequency signal
  `ideate.md` and `design-judgment.md` already use). An interaction seen 100+
  times/day (e.g. a checkbox toggle, a tab switch) gets no motion or the
  fastest token only — a delight animation there reads as friction, not
  polish, once seen for the hundredth time. An occasional action gets the
  standard token. A rare or first-time-only moment (onboarding, a completed
  milestone) can justify a slower, more expressive treatment. This is the
  same frequency-vs-guidance trade-off `ideate.md` item 2 already applies to
  choosing an interaction model, applied one level down to whether that
  interaction's transition should move at all.
- **Purpose-must-be-stated rule.** Every motion spec names which job it's
  doing — spatial consistency (below), state indication, explaining a
  relationship between two views, direct feedback for an action, or
  preventing a jarring/disorienting change. A motion spec with no named
  purpose is not specified, it's decorated; send it back rather than
  accepting "it looks smoother."
- **Interruptibility.** An in-progress transition must remain interactive —
  animate from the interface's current, actual position/state, never lock
  input until a scripted target state is reached. A user who acts again
  mid-transition is not a special case to handle later; it is the default
  case the transition must already support.
- **Spatial consistency ("return to origin").** Where something opens,
  closes, or is dismissed, its exit path mirrors its entry path — a
  popover/menu/drawer closes back toward the control that opened it, not to
  an unrelated point. This reinforces (does not change) the modal/drawer/
  overlay distinctions already in `navigation-system.md` items 8–10: the
  *return path* is part of specifying which of those three a given
  interaction uses.
- **Asymmetric timing.** Where the user is deciding, allow the interaction to
  feel unhurried (e.g. a destructive hold-to-confirm gesture); where the
  system is responding to a decision already made, respond fast. Don't apply
  one uniform speed to both halves of an interaction — they're answering
  different questions (the user weighing a choice vs. the system confirming
  one was made).
- **Reduced-motion is gentler, not necessarily zero.** `design-system.md`'s
  default of degrading to an instant/near-instant transition is correct for
  purely decorative motion. Where a transition is itself carrying the
  purpose-must-be-stated meaning above (e.g. indicating that a row moved
  rather than vanished-and-reappeared), prefer a shortened, low-intensity
  version of the same motion over removing it outright — removing it
  entirely can cost the state-indication information the motion existed to
  convey, not just its polish.

## Loop position
Consumes flows from `user-flow-engine.md` at the feature-level loop.
Re-entered when a Test finding on usability or feedback (dimensions 2 and 5)
traces to an execution problem here rather than the underlying flow/approach,
per `methodology/design-thinking.md`'s routing table.

## Explicitly not here
- Visual styling/animation spec of the feedback → `ui-engine/*`.
- Form-specific interaction rules (validation timing, field behavior) →
  `form-design.md`.
- The resulting UI state set (loading/error/etc.) → `state-design.md`.
- Which flow/approach an interaction belongs to → `user-flow-engine.md`.
