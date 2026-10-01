# Registry: Actions & Inputs

Button, Input, Select, Search, Filter, Date Picker, Upload — per
`registry-schema.md`'s 13-field shape. Every value cited is a
`design-tokens/token-schema.md` path, never a raw value.

---

## Button
1. **Purpose:** Trigger a single, immediate action.
2. **When to use:** The action happens on this screen, right now, with no
   further destination to navigate to.
3. **When NOT to use:** The control navigates instead of acting — use a
   link, styled per `visual-hierarchy.md`, not a button (`component-
   system.md` point 1's own distinction).
4. **Variants:** Emphasis primary/secondary/tertiary/destructive; size
   sm/md/lg (`sizing.controlSm/Md/Lg`) — `component-system.md` point 3;
   **label form: labeled (default) vs. icon-only** — icon-only is a
   deliberate density choice (a dense toolbar, a table's row actions),
   never the default just because it's more compact.
5. **States:** default, hover, focus (visually distinct from hover),
   active, disabled, loading (where the action can be triggered) —
   `component-system.md` point 4.
6. **Interaction behavior:** Feedback timing per `interaction-design.md`'s
   action-feedback table; destructive/irreversible variants require the
   Undo/confirmation matrix's confirm-before-acting rule. **Icon-only
   requires a visible Tooltip** (the Tooltip registry entry, revealed on
   hover and focus) in addition to its accessibility name below — the
   `aria-label` alone serves assistive tech, but a sighted mouse/keyboard
   user has no other way to learn what an unlabeled icon does; an
   icon-only button with no tooltip is incomplete regardless of how
   familiar the icon seems.
7. **Accessibility:** `role=button`; accessible name matches visible
   label unless icon-only, which requires an `aria-label`
   (`accessibility.md`) — distinct from, and in addition to, the visible
   Tooltip above; the two serve different users, neither substitutes for
   the other.
8. **Responsive:** ≥44×44px touch target at mobile/tablet breakpoints
   (`responsive-system.md`).
9. **Content rules:** Verb-led label, sentence case, single line
   (`component-system.md` point 6, `ux-writing.md`).
10. **Validation rules:** Not applicable.
11. **Composition rules:** The atomic unit inside every organism in
    `composition-patterns.md`; a screen's one primary action is always a
    `primary`-emphasis Button (**B5**'s one-primary-action criterion).
12. **Common UX mistakes:** More than one `primary`-emphasis button on
    one screen (ambiguous CTA, per `ux-scenario-testing/
    continuity-audit.md`'s check 3); a destructive action with no
    confirmation step; a label that doesn't name its outcome ("Submit"
    instead of "Send invoice").
13. **Domain-specific usage:** No domain-specific variance.

---

## Input
1. **Purpose:** Capture one field of free-text/numeric data.
2. **When to use:** The value has no fixed, enumerable option set.
3. **When NOT to use:** The value has a fixed option set — use Select;
   the value is a date — use Date Picker.
4. **Variants:** text/number/email/password/textarea; size sm/md/lg.
5. **States:** default (empty, showing placeholder), **filled** (holds a
   value — visually identical to default beyond the value itself; not a
   separate treatment, named here only to distinguish it from empty),
   hover, focus, disabled, **read-only** (holds a confirmed value the
   current context doesn't allow editing — e.g. a Record Detail View
   rendered for a view-only role, or a field the business rule locks
   after submission; visually distinct from `disabled`: read-only content
   looks like normal, legible text with no dimming, since it's the
   definitive current value, not an unavailable control), validation
   error, **success** (passed a meaningful validation check worth
   confirming, e.g. an async availability check — used sparingly; not
   every valid field needs a success treatment, only ones where the user
   was genuinely uncertain), (rarely) loading (an async-validated field,
   e.g. a uniqueness check).
6. **Interaction behavior:** `form-design.md`'s Validation-timing rule
   (inline where cheap, on-submit where it requires a round-trip) and
   Error-messaging behavior (adjacent to the field, clears on fix).
   `read-only` never has a `disabled`-looking dimmed treatment applied to
   it and never intercepts focus/selection/copy — a user can still select
   and copy read-only text, just not edit it.
7. **Accessibility:** Label programmatically associated (`for`/`aria-
   labelledby`); error announced via `aria-describedby`, not color alone.
8. **Responsive:** Full-width on mobile within the form's column span;
   touch target height meets the 44px minimum.
9. **Content rules:** Placeholder is an example, never a substitute for a
   label; helper text states format expectations before an error occurs.
10. **Validation rules:** Field-level vs. cross-field, per `form-
    design.md`'s two shapes — always traces to a Data-type requirement
    (`REQ-NNN`).
11. **Composition rules:** The atomic unit of `composition-patterns.md`'s
    Form organism, grouped per `form-design.md`'s Field-grouping rule.
12. **Common UX mistakes:** Placeholder used as the only label (vanishes
    on focus, fails accessibility); validating on every keystroke instead
    of on blur/submit for round-trip-dependent checks; an error message
    that persists after the user already fixed it.
13. **Domain-specific usage:** No domain-specific variance beyond field
    content itself (owned by the domain's own requirements, not this
    entry).

---

## Select
1. **Purpose:** Choose one (or a bounded few) values from a fixed,
   enumerable option set.
2. **When to use:** Options are known in advance and few enough to
   scan (roughly ≤15) without needing search-within-options.
3. **When NOT to use:** The option list is long/searchable — use a
   searchable combobox variant, citing `search-ux.md`'s query-input
   technique for the in-list search itself; the choice is genuinely
   binary — use a toggle/checkbox instead of a 2-option select.
4. **Variants:** single-select, multi-select; inline vs. dropdown-panel
   (`navigation-system.md` item 10, Overlays).
5. **States:** default, hover, focus, disabled, validation error, empty
   (no options available — states why, per `state-design.md`).
6. **Interaction behavior:** Opens/closes per `navigation-system.md`
   item 10's overlay rule; keyboard: arrow keys move selection, Enter
   commits, Escape closes without changing value.
7. **Accessibility:** `role=listbox`/`combobox` semantics; selected
   option announced; keyboard-fully-operable (never mouse-only).
8. **Responsive:** On mobile, a dropdown-panel select may render as a
   native platform picker where that improves touch ergonomics
   (`responsive-system.md`'s touch-target rule).
9. **Content rules:** Options ordered meaningfully (frequency, alphabetic,
   or a stated domain order) — never left in arbitrary insertion order.
10. **Validation rules:** Required/optional per the Data-type requirement;
    a default/placeholder option is never itself a silently-valid choice
    unless the requirement states it is.
11. **Composition rules:** A Form field atom, same grouping rule as Input.
12. **Common UX mistakes:** A 2-option select where a toggle would be
    faster; a long, unsearchable option list forcing manual scanning;
    losing the current selection's visibility once the panel closes.
13. **Domain-specific usage:** No domain-specific variance beyond the
    option set's own content.

---

## Search
1. **Purpose:** Find/narrow a working result set via a typed query.
2. **When to use:** Per `ux-engine/information-architecture.md`'s Breadth
   rule — a level too wide for pure browsing, or the actor's primary
   interaction model is search-first (`methodology/ideate.md` item 2).
3. **When NOT to use:** A small, fixed, already-visible list — Filter or
   plain scanning serves better; don't add search where browsing is
   already fast.
4. **Variants:** Inline (always visible) vs. invoked (icon expands to a
   field) — chosen by frequency of use, same logic as `navigation-
   system.md` item 1.
5. **States:** default, focus, loading (query in flight), empty (zero
   results — `search-ux.md`'s Zero-results handling), error.
6. **Interaction behavior:** `search-ux.md`'s Query input (autocomplete
   past a minimal character count) and Ranking and relevance sections in
   full; composes with filter→sort→paginate exactly as that file states.
7. **Accessibility:** `role=search`; result count announced to assistive
   tech on update, not just visually.
8. **Responsive:** Invoked variant is the mobile default when horizontal
   space is scarce (`responsive-system.md`).
9. **Content rules:** States what's actually searched if not obvious
   ("Search by name or ID") — never a bare, ambiguous "Search" placeholder.
10. **Validation rules:** Not applicable (a query is never "invalid," only
    zero-result).
11. **Composition rules:** The entry point for `composition-patterns.md`'s
    Data Table organism; composes with Filter, never duplicates its job
    (search narrows by query, Filter narrows by facet).
12. **Common UX mistakes:** A search box that silently searches fewer
    fields than the user assumes (`search-ux.md`'s own named defect); no
    zero-results messaging (looks broken/loading forever); search and
    filter implemented as two competing, uncoordinated narrowing
    mechanisms instead of one composed result set.
13. **Domain-specific usage:** No domain-specific variance beyond what's
    indexed.

---

## Filter
1. **Purpose:** Narrow a visible result set by one or more facets.
2. **When to use:** The result set has structured, facetable attributes
   (status, date range, category) a user commonly narrows by.
3. **When NOT to use:** There's only one plausible facet and few enough
   values that a Tabs control (switching between fixed views) is simpler
   than a filter panel.
4. **Variants:** Inline chips (few, always-visible facets) vs. panel/
   drawer (many facets) — per `search-ux.md`'s Filter facets section.
5. **States:** default, applied (count badge showing active filters),
   empty (a facet with zero valid options for the current query), loading.
6. **Interaction behavior:** Fixed filter→sort→paginate order
   (`interaction-design.md`); applying a filter resets pagination to page
   1; facet options scoped to what's actually available in the current
   result set (`search-ux.md`'s Filter facets rule).
7. **Accessibility:** Active filter count announced; each facet control
   keyboard-operable; clearing all filters is a single, reachable action.
8. **Responsive:** Collapses to a drawer/sheet on mobile
   (`responsive-system.md`); active-filter chips remain visible even when
   the panel itself is collapsed.
9. **Content rules:** Each facet labeled by its actual attribute name, not
   a generic "Filter 1"/"Filter 2."
10. **Validation rules:** Not applicable.
11. **Composition rules:** Composes with Search and Pagination in
    `composition-patterns.md`'s Data Table organism, in the fixed order
    above — never a competing, independent narrowing mechanism.
12. **Common UX mistakes:** A facet offering an option that yields zero
    results once combined with the current query (`search-ux.md`'s named
    defect); filters that don't visibly show which are active; forgetting
    to reset pagination on filter change.
13. **Domain-specific usage:** Cite the matched `product-types/*.md`
    pack's own filter-facet conventions where a domain has standard ones
    (e.g. date-range + status for financial/ERP records).

---

## Date Picker
1. **Purpose:** Capture a date (or date range) value.
2. **When to use:** The field is a Date-type requirement.
3. **When NOT to use:** A free-text date field with no picker — never;
   unstructured date text is a validation and locale-ambiguity risk by
   construction.
4. **Variants:** single date, date range, date+time.
5. **States:** default, focus, disabled, validation error (out-of-range/
   invalid combination), loading (rare — e.g. blocked-date lookup).
6. **Interaction behavior:** Opens as an overlay (`navigation-system.md`
   item 10); keyboard arrow keys move by day/week, Enter commits; typed
   entry is still accepted and validated, not picker-only.
7. **Accessibility:** Grid semantics (`role=grid` on the calendar),
   current/selected day announced, keyboard-fully-operable.
8. **Responsive:** Full-screen overlay on mobile rather than a small
   fixed-position popover (touch-target rule, `responsive-system.md`).
9. **Content rules:** Displayed format matches the product's stated
   locale convention, stated explicitly, never silently ambiguous
   (DD/MM vs. MM/DD).
10. **Validation rules:** Range/relative constraints (not-before-today,
    end-date-after-start-date) cite `business-logic.md`'s validation
    rules directly.
11. **Composition rules:** A Form field atom; a date-range variant is
    itself two composed Inputs plus one shared overlay.
12. **Common UX mistakes:** Free-text-only date entry with no picker;
    an ambiguous locale format; a range picker that allows an end date
    before the start date with no prevention or clear error.
13. **Domain-specific usage:** Healthcare/financial domains often need a
    stricter not-in-the-future or not-before-a-threshold constraint —
    cite the matched `product-types/*.md`/`domain-standards` entry.

---

## Upload
1. **Purpose:** Attach one or more files to a record.
2. **When to use:** The Data-type requirement is a file/document/image.
3. **When NOT to use:** The content is short text that could be typed —
   don't reach for Upload as a generic "attach anything" escape hatch.
4. **Variants:** single-file, multi-file, drag-drop zone + button
   fallback (drag-drop always ships a non-drag alternative, per
   `interaction-design.md`'s Direct-manipulation patterns rule).
5. **States:** default/empty, drag-over, uploading (`processing`, with
   progress), success, validation error (wrong type/too large), system
   error (upload failed mid-transfer).
6. **Interaction behavior:** Progress shown per-file for anything past
   the 1s feedback threshold (`interaction-design.md`); a failed upload
   is retryable per-file, not a reason to restart the whole batch.
7. **Accessibility:** The drop zone has a real, focusable, keyboard-
   activatable button equivalent — never drag-only.
8. **Responsive:** Native file picker on mobile (drag-drop has no mobile
   equivalent by construction).
9. **Content rules:** States accepted file types/size limit before the
   user attempts an upload, not only after rejecting one.
10. **Validation rules:** File type/size constraints cite `business-
    logic.md`'s validation rules; rejected files state which rule failed.
11. **Composition rules:** A Form field atom when attached to a record;
    standalone when the whole screen's purpose is upload (e.g. a bulk
    import flow).
12. **Common UX mistakes:** Drag-only with no button fallback (fails
    accessibility by construction); silent size/type rejection with no
    stated reason; one failed file blocking the rest of a batch upload.
13. **Domain-specific usage:** No domain-specific variance beyond
    accepted file types, which come from the domain's own requirements.
