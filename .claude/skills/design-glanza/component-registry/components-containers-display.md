# Registry: Containers & Display

Card, Table, Modal, Drawer, Chart, List, Timeline/Activity Feed — per
`registry-schema.md`'s 13-field shape. Every value cited is a
`design-tokens/token-schema.md` path, never a raw value.

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
   siblings), **selected** (a card in a multi-select picker grid — a
   persistent chosen indicator, `component-system.md` point 4, distinct
   from the transient `active`/pressed moment), **disabled** (the card's
   own action is currently unavailable, e.g. permission-gated — visually
   de-emphasized per `state-design.md`'s `permission denied` state, not
   merely omitted).
6. **Interaction behavior:** Independently reorderable/removable cards
   never depend on another card's state (`layout-system.md`'s Dashboard
   grid note). Footer actions follow Button's own emphasis rule — at most
   one `primary`-emphasis action per card, the same one-primary-action
   discipline B5 already applies at the screen level, applied here at the
   card level; a card whose only affordance is itself being clickable
   states that affordance visually (a hover treatment), never relying on
   cursor style alone.
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
   expandable rows (inline detail disclosure), **density: comfortable
   (default) vs. compact/dense** — `visual-trends.md`'s density axis,
   selected per register/domain, never mixed row-to-row within one table.
5. **States:** default, loading (skeleton rows), empty (zero results,
   states why — `search-ux.md`), error (query/load failed), row-selected,
   **row-hover** (reveals row actions, below).
6. **Interaction behavior:** Sort cycle (unsorted→ascending→descending→
   unsorted) on column headers, always visibly indicated
   (`interaction-design.md`'s Sorting section); fixed filter→sort→
   paginate order. **Row actions** (edit/delete/view-detail icon buttons)
   reveal on row hover/focus for a comfortable-density table with few,
   secondary actions; a row with more than ~2 actions, or any table at
   compact/dense where hover-reveal costs too much precision, uses a
   persistent Dropdown ("more actions") in a fixed trailing column
   instead — the choice is stated per table, not left to render
   inconsistently across the product's tables.
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
   explicit close control both dismiss it, never Escape-only. **Scroll
   behavior:** the modal's own header and footer (action buttons) stay
   fixed/sticky; only the body content region scrolls once it exceeds the
   available viewport height — never the whole modal (including its
   actions) scrolling off-screen, which strands the primary action out of
   reach. **Destructive confirmation:** a Modal used as the Confirmation
   entry's irreversible-high-risk case follows that entry's rules
   directly (deliberate secondary step, destructive control never
   auto-focused) rather than restating them here.
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
   exit path mirrors entry path. **Scroll behavior:** same fixed-header/
   footer, scrolling-body-only rule as Modal — a drawer's action buttons
   never scroll out of reach regardless of body content length.
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
   data for this period" — never a blank axis), error, **partial data**
   (the query succeeded but returned fewer points than this chart type
   needs to read cleanly — shown as itself, not silently rendered as
   complete), **insufficient data** (fewer than the ~3-point floor in
   field 3 — a stated message, never a blank-looking chart).
6. **Interaction behavior:** Hover-revealed exact values; every data-
   bearing color also carries a non-color channel (label, pattern, or
   hover value) per `color-system.md`'s color-blind safety rule. Tooltip
   content: exact value, date/time or category, and the prior-period
   value where a comparison period is part of the chart's story
   (`ui-engine/visual-benchmark.md`'s Chart verification pipeline). Where
   a data point/segment reasonably leads to a filtered detail view
   (a bar for one month leading to that month's transaction list), it's a
   real drill-down affordance (`interaction-design.md`), not decoration —
   stated per chart, not assumed. **Responds to every dashboard-level
   filter** (date range, category, status) the same way the screen's
   tables do — `ux-engine/search-ux.md`'s Filter facets section — never
   left unfiltered while an adjacent table narrows.
7. **Accessibility:** A text-equivalent summary or data table alternative
   is available, not visualization-only.
8. **Responsive:** Legend/axis labels reflow or abbreviate rather than
   overlapping at narrow widths; touch devices get tap-to-reveal instead
   of hover-only values.
9. **Content rules:** A meaningful title naming what's measured (never
   "Overview"); a subtitle/context line stating the time period and, where
   relevant, the comparison period; axis labels and units always present;
   a legend present whenever more than one series is shown, omitted
   otherwise; a meaningful highlight (an emphasized endpoint or labeled
   peak/dip) where the data has one.
10. **Validation rules:** Not applicable.
11. **Composition rules:** Commonly composed inside a Card on a
    dashboard (or as the KPI/Stat Card's sparkline variant,
    `composition-patterns.md`); color draws from `color-system.md`'s
    sequential/diverging/categorical ramps matched to the same data-shape
    logic.
12. **Common UX mistakes:** Wrong chart type for the data shape (a pie
    for >6 categories, a sequential ramp for diverging data); color-only
    series encoding with no secondary channel; a blank/empty chart
    indistinguishable from a loading failure; a chart added with no
    stated insight where a KPI/Stat Card would have served the single
    number better; a chart left unfiltered while the rest of the
    dashboard responds to an applied filter.
13. **Domain-specific usage:** Cite the matched domain's own standard
    metrics/visualizations where one exists (e.g. financial candlestick
    charts, `product-types/fintech.md`).

---

## List
1. **Purpose:** Display an ordered or unordered collection of like items in
   a single scannable column, where full column-to-column comparison
   (Table) or independent parallel comparison (Card grid) isn't the point.
2. **When to use:** Items are read top-to-bottom in sequence (a feed, a
   simple record list with 1-3 visible attributes per row) rather than
   compared attribute-by-attribute.
3. **When NOT to use:** More than roughly 3-4 attributes need comparing
   across items — use Table; items are independently meaningful summary
   units meant for parallel scanning, not sequence — use Card grid.
4. **Variants:** Single-line (label only), two-line (label + secondary
   metadata), with/without a leading avatar or icon, with/without a
   trailing action.
5. **States:** default, loading (skeleton rows, per Loading State),
   empty (per Empty State), error (per Error State), row-hover (if
   independently actionable), row-selected (a multi-select list).
6. **Interaction behavior:** A trailing action follows the same row-action
   pattern as Table (hover-reveal for 1-2 actions, a trailing Dropdown for
   more); a clickable row's full-row hit target is stated, not just its
   visible text.
7. **Accessibility:** `role=list`/`listitem` semantics; a clickable row is
   a real focusable, keyboard-activatable element, never a `div` with a
   click handler and no semantic/focus equivalent.
8. **Responsive:** Two-line items may collapse to single-line with
   secondary metadata deferred to a detail view at narrow widths, stated
   per list rather than left to overflow.
9. **Content rules:** Truncation rule stated per line
   (`component-system.md` point 6).
10. **Validation rules:** Not applicable.
11. **Composition rules:** The atomic unit of an Activity Feed (below) and
    of a Sidebar's own item list; composes with Pagination or
    infinite-scroll ("load more," `interaction-design.md`'s Pagination
    rule) for a long collection.
12. **Common UX mistakes:** Using a List where Table's column comparison
    was actually needed (a common under-reach the opposite direction of
    Card's own "used for dense data" mistake); a clickable row with no
    visible hover/focus affordance; inconsistent line count (some items
    one line, some two) with no content-driven reason.
13. **Domain-specific usage:** No domain-specific variance beyond item
    content itself.

---

## Timeline / Activity Feed
1. **Purpose:** Display a chronological sequence of discrete events tied
   to one record or one actor — distinct from List in that order/time is
   itself the organizing information, not just a scan sequence.
2. **When to use:** The events genuinely happened at distinct points in
   time and that sequence is meaningful to the viewer (an audit trail, a
   record's change history, a notification feed).
3. **When NOT to use:** The items aren't actually time-ordered events (use
   List); the full detail of each event needs its own dedicated screen
   (link to it, don't try to inline everything here).
4. **Variants:** Vertical (default), grouped-by-day/date-header for a
   long-running feed.
5. **States:** default, loading (skeleton entries), empty (states why —
   "No activity yet" for first-use, distinct from a filtered-to-zero
   read), error, **loading-more** (appending older entries — distinct
   from the initial `loading` state; only the appended region shows it,
   per Loading State's per-region rule).
6. **Interaction behavior:** New/unread entries are visually distinguished
   (not just theoretically knowable from a timestamp); loading older
   entries uses `interaction-design.md`'s Pagination-equivalent
   ("load more"/infinite-scroll) rule, never a full reload.
7. **Accessibility:** Each entry announced with its actor, action, and
   relative/absolute time — an icon-only or color-only event-type
   indicator has an accompanying text label (`color-system.md`'s
   color-blind safety rule, applied to event-type encoding specifically).
8. **Responsive:** The vertical timeline's connecting line/rail and
   date-grouping remain legible at mobile width — never so compressed the
   time relationship between entries is lost.
9. **Content rules:** Each entry states actor + action + object in plain
   language ("Priya approved Invoice #4821"), never a raw event-code or
   database-field dump.
10. **Validation rules:** Not applicable.
11. **Composition rules:** A List of a specific, time-ordered entry shape;
    commonly composed inside a Drawer or a Record Detail View's Tabs
    (`composition-patterns.md`) as the "Activity" peer tab.
12. **Common UX mistakes:** No visual distinction for new/unread entries;
    "load more" silently re-fetching and duplicating already-shown
    entries; an event described in raw technical terms instead of plain
    actor-action-object language.
13. **Domain-specific usage:** Regulated domains (finance, healthcare)
    often require an immutable, fully-attributed audit-trail variant —
    cite the matched `product-types/domain-standards/` entry where one
    applies.
