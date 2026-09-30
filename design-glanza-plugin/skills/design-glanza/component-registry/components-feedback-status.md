# Registry: Feedback & Status

Toast, Tooltip, Empty State, Loading State, Error State, Confirmation —
per `registry-schema.md`'s 13-field shape. Every value cited is a
`design-tokens/token-schema.md` path, never a raw value.

---

## Toast
1. **Purpose:** Transient, non-blocking notification of an action's
   result.
2. **When to use:** An action completed (successfully or not) somewhere
   the user doesn't need to keep looking at to know it worked.
3. **When NOT to use:** The result requires the user's immediate decision
   (use Confirmation or a Modal instead — a toast that demands action
   before it disappears is a contradiction of "non-blocking").
4. **Variants:** success, error, info, warning — using
   `color.semantic.*`'s matching triplet, never an independently
   invented color.
5. **States:** entering, visible, exiting (auto-dismiss or manual).
6. **Interaction behavior:** Auto-dismisses after a stated duration
   (long enough to read, per `interaction-design.md`'s feedback-timing
   spirit) unless it carries an action (e.g. "Undo"), in which case it
   persists until acted on or manually dismissed.
7. **Accessibility:** Announced via an `aria-live` region — never
   relying on sighted-only visual appearance.
8. **Responsive:** Repositions to avoid covering primary content/touch
   targets on mobile.
9. **Content rules:** States what happened plainly ("Invoice sent"), not
   a generic "Success!" with no object.
10. **Validation rules:** Not applicable.
11. **Composition rules:** Standalone; never contains a Form or Table.
12. **Common UX mistakes:** A toast demanding a decision before auto-
    dismissing; stacking so many toasts they cover primary content;
    color-only success/error distinction with no icon/text (color-blind
    safety).
13. **Domain-specific usage:** No domain-specific variance.

---

## Tooltip
1. **Purpose:** Supplementary, on-demand explanation of a control or
   truncated content.
2. **When to use:** A control's purpose isn't self-evident from its label
   (e.g. an icon-only button) or content is truncated and the full value
   is useful.
3. **When NOT to use:** The information is necessary to complete the
   task — necessary information belongs in visible content or helper
   text, not behind a hover-only reveal a touch user can't trigger.
4. **Variants:** Text-only, rich (with a short structured layout) —
   rich variants stay small; a tooltip that needs a data-viz or a
   `processing` state has outgrown "tooltip" (`navigation-system.md`
   item 10's own overlay-scope rule).
5. **States:** hidden, visible (on hover/focus).
6. **Interaction behavior:** Reveals on both hover **and** focus (never
   hover-only — `interaction-design.md`'s gesture/input-modality table);
   touch gets tap-to-reveal, not hover.
7. **Accessibility:** Associated via `aria-describedby`; dismissible via
   Escape when triggered by focus.
8. **Responsive:** Repositions to stay on-screen at narrow viewports.
9. **Content rules:** Short — a sentence, not a paragraph.
10. **Validation rules:** Not applicable.
11. **Composition rules:** Attaches to any other registry component;
    never nests another overlay inside it.
12. **Common UX mistakes:** Hover-only reveal with no touch/keyboard
    equivalent (a Blocker-class accessibility defect by construction);
    burying necessary task information inside a tooltip instead of
    visible content.
13. **Domain-specific usage:** No domain-specific variance.

---

## Empty State
1. **Purpose:** Communicate that a query/list/section legitimately has
   zero results, distinct from still-loading or broken.
2. **When to use:** Every list/table/search/chart that can legitimately
   return zero results (`state-design.md`'s `empty` state — never
   optional).
3. **When NOT to use:** The zero-result condition is actually a system
   error — use Error State instead; conflating the two hides a real
   failure behind a benign-looking message.
4. **Variants:** First-use empty (nothing created yet — offers a create
   action), filtered-to-zero empty (offers clearing the filter/query,
   `search-ux.md`'s Zero-results handling).
5. **States:** This *is* a state (`state-design.md`), not a component
   with its own further states.
6. **Interaction behavior:** Where feasible, offers a concrete next step
   (a create action, a broadened query suggestion) rather than a dead
   end (`user-flow-engine.md`'s recovery-path discipline applied to a
   null result).
7. **Accessibility:** Announced to assistive tech on appearance (e.g.
   after a filter change), not just visually rendered.
8. **Responsive:** Illustration/copy reflows, never overflows, at narrow
   widths.
9. **Content rules:** States plainly that nothing matched/exists, names
   why when known (filtered vs. first-use), never a bare "No data."
10. **Validation rules:** Not applicable.
11. **Composition rules:** Replaces Table/Card-grid/Chart content
    entirely when triggered — never shown alongside stale content from a
    previous query.
12. **Common UX mistakes:** Indistinguishable from a loading state (no
    visual/textual difference); a first-use empty state offering no
    create action when one exists; conflating a real error with a
    legitimate zero-result.
13. **Domain-specific usage:** No domain-specific variance.

---

## Loading State
1. **Purpose:** Communicate that existing data is being fetched, not yet
   available.
2. **When to use:** Any fetch exceeding the 100ms–1s feedback threshold
   (`interaction-design.md`'s action-feedback rules).
3. **When NOT to use:** An action in progress (not a fetch) — that's
   `processing`, a distinct mandatory state (`state-design.md`); under
   100ms — no explicit indicator needed at all.
4. **Variants:** Skeleton (layout already known) vs. spinner
   (layout genuinely unknown yet) — `interaction-design.md`'s Skeleton
   vs. spinner rule decides which, not preference.
5. **States:** This *is* a state (`state-design.md`).
6. **Interaction behavior:** For a re-sort/re-filter/re-paginate, only
   the affected content region shows loading — existing rows/cards stay
   visible, never a full blank reload (`interaction-design.md`'s Sorting
   and Pagination sections).
7. **Accessibility:** Announced as busy (`aria-busy`), not silently
   swapped with no assistive-tech signal.
8. **Responsive:** Skeleton shape matches the responsive layout actually
   in effect at the current breakpoint, not the desktop shape scaled
   down.
9. **Content rules:** No copy needed for a skeleton; a spinner used for
   an unusually long wait states what's happening ("Generating report…").
10. **Validation rules:** Not applicable.
11. **Composition rules:** Applies per-region (a Table's rows, one
    Card, a Chart's plot area) — never a single full-screen blocker for
    a partial-content refresh.
12. **Common UX mistakes:** A skeleton promising a layout shape that then
    visibly reflows once data arrives; a full-page reload feel for a
    partial re-sort/re-filter; silence past 1 second with no indicator
    at all.
13. **Domain-specific usage:** No domain-specific variance.

---

## Error State
1. **Purpose:** Communicate that something failed outside the user's
   control, distinct from a validation error the user caused.
2. **When to use:** `state-design.md`'s `system error` state — a failed
   fetch, a dependency outage, an unexpected exception.
3. **When NOT to use:** The user's own input was invalid — that's a
   validation error, shown adjacent to the field (`form-design.md`),
   never as a full-region error state.
4. **Variants:** Region-level (a Table/Card/Chart failed to load) vs.
   full-page (the whole screen failed), chosen by blast radius.
5. **States:** This *is* a state (`state-design.md`); recovery-path
   resolution (retry/abandon-safely/escalate,
   `user-flow-engine.md`) is mandatory, never left unset.
6. **Interaction behavior:** Offers the stated recovery action directly
   (a Retry button for `retry`, a way back for `abandon-safely`, a
   support link for `escalate`) — never a dead end.
7. **Accessibility:** Announced via an `aria-live` region on appearance.
8. **Responsive:** Recovery action remains reachable without scrolling
   at every breakpoint (`responsive-system.md`'s priority-preservation
   rule).
9. **Content rules:** States what failed in plain terms and what the
   user can do next — never a raw stack trace/error code with no
   human-readable explanation (`ux-writing.md`'s error-message formula).
10. **Validation rules:** Not applicable (this state is by definition
    not a validation failure).
11. **Composition rules:** Replaces the affected region's content only
    (a Table's rows, one Card) unless the failure is genuinely page-wide.
12. **Common UX mistakes:** A dead end with no recovery action; a raw
    technical error surfaced verbatim to the user; a region-level failure
    incorrectly escalated to a full-page error, hiding otherwise-working
    content.
13. **Domain-specific usage:** No domain-specific variance.

---

## Confirmation
1. **Purpose:** Require an explicit, deliberate acknowledgment before an
   action proceeds.
2. **When to use:** `interaction-design.md`'s Undo/confirmation matrix —
   any reversible-high-risk or irreversible action; irreversible-high-
   risk additionally requires a deliberate secondary step (e.g. typing a
   confirmation phrase).
3. **When NOT to use:** A reversible, low-risk action — offer an undo
   affordance after the fact instead of interrupting before it (the same
   matrix's other cell); confirming *every* action regardless of risk is
   itself a defect (alert fatigue that trains users to click through
   without reading).
4. **Variants:** Lightweight inline confirm (a reversible-high-risk
   action) vs. a Modal with a secondary deliberate step
   (irreversible-high-risk).
5. **States:** default, confirming (the secondary step in progress,
   e.g. typed phrase not yet matching), confirmed/processing.
6. **Interaction behavior:** The confirming control is disabled until
   the deliberate secondary step (where required) is actually satisfied
   — never enabled by default and only checked on click.
7. **Accessibility:** Focus lands on the confirmation's primary control
   (usually the safer, non-destructive option is NOT auto-focused for a
   destructive confirm, to avoid an accidental Enter-key confirm).
8. **Responsive:** Same Modal responsive rules as the Modal entry when
   rendered as one.
9. **Content rules:** States the specific consequence ("This will
   permanently delete 12 records") — never a generic "Are you sure?"
   with no stated stakes.
10. **Validation rules:** The deliberate secondary step (typed phrase)
    is validated live, no round-trip needed.
11. **Composition rules:** Wraps a Button's destructive-emphasis action;
    rendered as an inline confirm or a Modal per risk tier above.
12. **Common UX mistakes:** A generic "Are you sure?" with no stated
    consequence; confirming low-risk reversible actions (fatigue); the
    destructive action auto-focused, one accidental Enter from firing.
13. **Domain-specific usage:** Regulated domains (finance, healthcare)
    often require a stricter, audited confirmation for specific actions
    — cite the matched `product-types/domain-standards/` entry.
