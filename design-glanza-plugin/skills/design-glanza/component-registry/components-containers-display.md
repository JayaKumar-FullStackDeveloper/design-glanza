# Registry: Containers & Display

Card, Table, Modal, Drawer, Chart — per `registry-schema.md`'s 13-field
shape. Every value cited is a `design-tokens/token-schema.md` path, never
a raw value.

---

## Card
1. **Purpose:** Group one independent, self-contained unit of summary
   information for rapid scanning/comparison against its peers.
2. **When to use:** `design-research/research-to-design.md`'s worked
   example — content that needs rapid parallel comparison, each unit
   independently meaningful without reading its neighbors first
   (`layout-system.md`'s Dashboard grid pattern).
3. **When NOT to use:** The content is a dense, comparable, many-row
   dataset — use Table instead (rows keep column-to-column comparison
   `Card` grids lose); the content is a single, focused record's full
   detail — use a plain detail region, not a card wrapper.
4. **Variants:** With/without image, with/without footer actions, compact
   vs. comfortable density.
5. **States:** default, hover (if independently actionable/reorderable),
   loading (skeleton matching the card's own layout — `interaction-
   design.md`'s Skeleton vs. spinner rule), empty (zero content to show),
   error (this card's own data failed to load, independent of its
   siblings).
6. **Interaction behavior:** Independently reorderable/removable cards
   never depend on another card's state (`layout-system.md`'s Dashboard
   grid note).
7. **Accessibility:** If the whole card is a single click target, it has
   one accessible name summarizing its content, not a set of
   independently-focusable spans forced into one link.
8. **Responsive:** Stacks single-column on mobile, ordered by
   `visual-hierarchy.md` priority (`responsive-system.md`'s Dashboard grid
   reflow row).
9. **Content rules:** Truncation rule stated (`component-system.md` point
   6) for any card whose content can overflow its fixed height.
10. **Validation rules:** Not applicable.
11. **Composition rules:** The atomic unit of a Dashboard grid; may
    itself contain a Chart or a small Table excerpt.
12. **Common UX mistakes:** Using cards for a dense, many-column dataset
    that actually needs Table's row-comparison; one card's loading/error
    state blocking or hiding its siblings; inconsistent card heights
    within one grid causing ragged, hard-to-scan rows.
13. **Domain-specific usage:** Cite the matched `product-types/*.md`
    pack's own dashboard-composition convention.

---

## Table
1. **Purpose:** Display a dense, comparable, many-row dataset with
   column-to-column comparison as the primary task.
2. **When to use:** Many columns, or column comparison is the point
   (`responsive-system.md`'s Data table responsive technique).
3. **When NOT to use:** Few, independently-meaningful records better
   served by parallel scanning — use Card grid instead.
4. **Variants:** Standard rows, selectable rows (checkbox column),
   expandable rows (inline detail disclosure).
5. **States:** default, loading (skeleton rows), empty (zero results,
   states why — `search-ux.md`), error (query/load failed), row-selected.
6. **Interaction behavior:** Sort cycle (unsorted→ascending→descending→
   unsorted) on column headers, always visibly indicated
   (`interaction-design.md`'s Sorting section); fixed filter→sort→
   paginate order.
7. **Accessibility:** `role=table`/`row`/`columnheader` semantics; a
   sort control is focusable and `Enter`/`Space`-activatable, its new
   state announced via an `aria-sort`-equivalent.
8. **Responsive:** Few-critical-columns tables collapse to stacked cards
   on mobile; many-column/comparison tables keep tabular layout with
   horizontal scroll and a pinned first column
   (`responsive-system.md`'s Data table responsive technique — the
   decision is made once, per table, in its own `component-spec.md`).
9. **Content rules:** Numeric columns use tabular figures
   (`typography.md`); truncation defined per column.
10. **Validation rules:** Not applicable to the table itself; inline-edit
    cells inherit Input's validation rules.
11. **Composition rules:** The centerpiece of the Data Table organism
    (`composition-patterns.md`) — composes with Search, Filter,
    Pagination, and bulk-action Buttons.
12. **Common UX mistakes:** Sort/filter state not visibly indicated;
    a table collapsing to cards when column comparison was actually the
    point (wrong responsive technique for the data shape); pagination not
    resetting on filter change.
13. **Domain-specific usage:** Cite the matched `product-types/erp.md`/
    `admin-panel.md` (or a loaded `domain-standards/` entry) for
    domain-typical density and column priority.

---

## Modal
1. **Purpose:** A short, focused, interrupting task with small scope that
   doesn't warrant leaving the current context.
2. **When to use:** `navigation-system.md` item 8 — a confirmation, a
   quick create-one-thing form.
3. **When NOT to use:** A multi-step workflow (use the Wizard/stepper
   pattern instead); a task where the user needs the originating context
   visible while acting (use Drawer instead) — item 8's own boundary.
4. **Variants:** Confirmation (small), form (medium), content (large) —
   sized by content, never oversized to "feel more important."
5. **States:** default/open, loading (its own content, e.g. a confirm
   action in flight), validation error (a form modal's fields).
6. **Interaction behavior:** Elevation level 4 (`design-system.md`) —
   **requires a scrim**; exit path mirrors entry path; Escape and an
   explicit close control both dismiss it, never Escape-only.
7. **Accessibility:** Focus trapped within the modal while open, returned
   to the trigger on close; `role=dialog`, labeled by its own heading.
8. **Responsive:** Full-screen on mobile rather than a small centered
   box that wastes most of the viewport as backdrop.
9. **Content rules:** A clear heading naming the task; primary/secondary
   actions follow the Button entry's emphasis rule (one primary action).
10. **Validation rules:** A form modal's fields inherit Input/Select's
    validation rules unchanged.
11. **Composition rules:** May contain a Form; never contains a full
    Data Table (that scope belongs on its own screen or in a Drawer).
12. **Common UX mistakes:** Missing scrim (figure-ground ambiguity, a
    Blocker per `design-system.md`'s elevation rule); Escape-only
    dismissal with no visible close control; a modal used for a task that
    actually needed the originating list visible (should be a Drawer).
13. **Domain-specific usage:** No domain-specific variance.

---

## Drawer
1. **Purpose:** A slide-in panel that keeps the originating context
   visible alongside the task.
2. **When to use:** `navigation-system.md` item 9 — viewing/editing a
   record's detail while its list stays in view.
3. **When NOT to use:** The task should fully interrupt (use Modal); the
   task is the screen's whole purpose, not a supplementary view (use a
   dedicated screen, per `layout-system.md`'s List+detail pattern).
4. **Variants:** Right-side (default, most locales), size sm/md/lg by
   content.
5. **States:** default/open, loading (its own content), validation error
   (a form drawer's fields).
6. **Interaction behavior:** Elevation level 3; the underlying list
   remains scrollable/visible per item 9's context-preservation rule;
   exit path mirrors entry path.
7. **Accessibility:** Focus moves into the drawer on open, returns to the
   trigger on close; landmark/dialog semantics same as Modal.
8. **Responsive:** Becomes full-screen (loses the "context visible"
   property by necessity) below the tablet breakpoint — stated as an
   accepted trade-off, not a silent behavior change.
9. **Content rules:** Same heading/primary-action rules as Modal.
10. **Validation rules:** Same as Modal — inherited from the contained
    Form's fields.
11. **Composition rules:** The detail pane of Master-detail/List+detail
    compositions where a full second screen isn't warranted.
12. **Common UX mistakes:** Using a drawer when the task should fully
    interrupt (loses the forcing function a modal provides); the
    underlying list losing its scroll position when the drawer closes.
13. **Domain-specific usage:** No domain-specific variance.

---

## Chart
1. **Purpose:** Visualize a data relationship (trend, comparison,
   distribution, correlation, part-to-whole).
2. **When to use:** `component-system.md`'s Data visualization table —
   chart type selected by the data's actual shape, never by preference.
3. **When NOT to use:** The precise value matters more than the trend/
   shape — use a Table (or a single stat) instead; fewer than ~3 data
   points (a chart of 2 points is a sentence, not a visualization).
4. **Variants:** Per `component-system.md`'s data-shape table (line, bar,
   stacked bar, pie/donut capped at 5–6 slices, scatter, histogram/box
   plot).
5. **States:** default, loading (skeleton axes, never a blank chart
   indistinguishable from "no data"), empty (states the reason, e.g. "no
   data for this period" — never a blank axis), error.
6. **Interaction behavior:** Hover-revealed exact values; every data-
   bearing color also carries a non-color channel (label, pattern, or
   hover value) per `color-system.md`'s color-blind safety rule.
7. **Accessibility:** A text-equivalent summary or data table alternative
   is available, not visualization-only.
8. **Responsive:** Legend/axis labels reflow or abbreviate rather than
   overlapping at narrow widths; touch devices get tap-to-reveal instead
   of hover-only values.
9. **Content rules:** Axis labels and units always present; a legend
   present whenever more than one series is shown.
10. **Validation rules:** Not applicable.
11. **Composition rules:** Commonly composed inside a Card on a
    dashboard; color draws from `color-system.md`'s sequential/diverging/
    categorical ramps matched to the same data-shape logic.
12. **Common UX mistakes:** Wrong chart type for the data shape (a pie
    for >6 categories, a sequential ramp for diverging data); color-only
    series encoding with no secondary channel; a blank/empty chart
    indistinguishable from a loading failure.
13. **Domain-specific usage:** Cite the matched domain's own standard
    metrics/visualizations where one exists (e.g. financial candlestick
    charts, `product-types/fintech.md`).
