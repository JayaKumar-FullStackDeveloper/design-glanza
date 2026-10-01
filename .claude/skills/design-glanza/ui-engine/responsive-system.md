# Responsive System

## Responsibility
Breakpoint strategy and reflow rules: how `layout-system.md`'s composition
patterns adapt across device classes — as deliberate **behavioral
adaptation** (what a screen's structure and priorities *do* at each tier),
never simple proportional scaling of the desktop treatment.

## Breakpoint set
| Breakpoint | Range | Notes |
|---|---|---|
| `mobile` | < 640px | Single column by default |
| `tablet` | 640–1024px | 2-column allowances for some patterns |
| `desktop` | 1024–1440px | Reference breakpoint — `layout-system.md`'s 12-column grid |
| `wide` | > 1440px | Extra column headroom; used by data-dense domains (`product-types/erp.md`, `admin-panel.md`) to show more columns/detail side-by-side rather than just stretching whitespace |

## Reflow rules per composition pattern
| Pattern (`layout-system.md`) | Mobile | Tablet | Desktop/Wide |
|---|---|---|---|
| List + detail | List only; tap opens detail as a full view (back returns to list, per `ux-engine/navigation-system.md` item 6) | Same as mobile, or two-pane if width allows | Two-pane, list + detail side by side |
| Dashboard grid | Cards stack single-column, ordered by priority (`visual-hierarchy.md`) | 2-column | Full multi-column grid |
| Single-column form | Unchanged — already single-column | Unchanged | Unchanged, width-capped to the typography measure |
| Master-detail | Same collapse as list+detail | Same as list+detail | Master pane + detail pane, master pane narrower than in list+detail |
| Wizard/stepper | Full-screen single step, step indicator condensed to "Step X of Y" | Same as mobile or full stepper if width allows | Full stepper with all step labels visible |

## Per-breakpoint decision framework
Responsive design is behavioral layout adaptation, not desktop scaled down
— at each breakpoint tier, a specific set of decisions is made deliberately,
citing the file that actually owns each decision rather than re-deriving it
here:

**Desktop** (the reference breakpoint, `layout-system.md`'s 12-column grid):
- **Information hierarchy** — `visual-hierarchy.md`'s full rule set applies
  at full strength; this is the tier every other tier's reflow is *measured
  against*, not a tier with its own separate hierarchy logic.
- **Grid** — the full 12-column grid, `layout-system.md`'s composition
  patterns applied in their desktop/wide form (the Reflow rules table's
  rightmost column).
- **Navigation** — the pattern `navigation-system.md` item 2 selected
  (sidebar vs. top nav) rendered in full, every item visible per its own
  frequency-ranked priority.
- **Density** — the register's own default (`visual-trends.md`) or an
  explicit user-selected density setting, at its most information-dense
  expression.
- **Primary actions** — `visual-hierarchy.md`'s one-primary-action rule,
  positioned first in scan order with no space constraint forcing a
  compromise.

**Tablet** (640–1024px — the tier most often wrongly treated as "a slightly
narrower desktop"):
- **Layout restructuring** — not a proportional shrink: a two-pane pattern
  (List+detail, Master-detail) may narrow its master pane or collapse to
  single-pane depending on actual available width for both panes to stay
  legible, per the Reflow rules table; a multi-column Dashboard grid drops
  to 2-column, not a scaled 12-column grid with tiny cards.
- **Navigation adaptation** — a sidebar may narrow to icon-only (collapsed,
  per the Sidebar registry entry's own collapsed state) before it becomes a
  full overlay — tablet is the tier where a nav pattern's *intermediate*
  state, not just its desktop and mobile extremes, actually matters.
- **Content priority** — `visual-hierarchy.md`'s information-priority
  ranking starts actively shedding/deferring lower-priority content here,
  not held at full desktop density until mobile forces the issue.
- **Component resizing** — sizes from `design-system.md`'s closed scales
  only (never an arbitrary intermediate value invented for this one
  breakpoint) — a control steps between named scale values, it doesn't
  interpolate continuously with viewport width.

**Mobile** (< 640px):
- **Single-column behavior** — every multi-column pattern collapses to one
  column, per the Reflow rules table; this is the floor, not a target to
  approach gradually.
- **Navigation transformation** — sidebar/top-nav becomes an off-canvas
  overlay/drawer (Sidebar and Navigation registry entries' own Responsive
  fields), triggered by a visible, labeled control — never assumed
  discoverable from a bare icon with no accessible name.
- **Content stacking** — content ranked highest by information priority
  survives into the mobile view first (Priority-preservation rule, below);
  lower-priority content is progressively disclosed, not simply omitted
  with no path to reach it.
- **Table adaptation** — the Data table responsive technique, below:
  stacked cards or horizontal scroll, decided by the data shape, never
  defaulted to whichever is easier to implement.
- **Action prioritization** — the primary action stays immediately
  reachable (Priority-preservation rule); secondary actions collapse into
  an overflow menu before the primary action is ever displaced.
- **Touch targets** — the 44×44px minimum, below — mobile is where this
  bar is unconditionally live, not a "nice to have if there's room" check.
- **Overflow handling** — every element with content that can exceed its
  container at this width has a *stated* resolution (truncate, wrap,
  scroll within its own container, collapse into an overflow control) per
  `component-system.md`'s Overflow behavior rule — never left to whatever
  the browser/framework defaults to, which is how accidental horizontal
  scroll and clipped content actually happen.

## The adaptation decision
For any element that doesn't fit its desktop treatment at a smaller
breakpoint, the choice is one of seven, made deliberately per element —
never a reflexive "just shrink everything proportionally":

| Decision | Use when |
|---|---|
| **Stack** | A multi-column layout's columns are each independently meaningful and can read top-to-bottom in priority order (Dashboard grid, a multi-column form). |
| **Collapse** | A structural element has a smaller/summary form that preserves its function (a sidebar → icon rail before it becomes an overlay; a table → stacked cards). |
| **Hide** | The content is genuinely lower-priority and the user can reach it another way (progressive disclosure, a "show more") — never used for the primary action or any item the Priority-preservation rule protects. |
| **Move** | The element's *position* changes but its content doesn't (utility nav items relocating into a header overflow menu; a filter panel moving from an inline row to a drawer). |
| **Become scrollable** | The content is inherently wider/taller than the viewport and comparison across it is the point (a wide data table, per the Data table responsive technique) — scroll preserves the structure a Collapse would lose. |
| **Become an alternative component** | The same underlying data needs a genuinely different presentation, not a resized version of the same one (a Table becoming a List/stacked-cards view; a multi-column Chart legend becoming a tap-to-reveal summary) — cite the specific registry entries involved. |
| **Remain fixed** | The element's function depends on staying put regardless of viewport (a sticky header/footer inside a Modal/Drawer, per those entries' scroll-behavior rule; the primary action itself, per Priority-preservation). |

An element with no stated decision from this list is the actual mechanism
behind "desktop UI simply scaled down" — every element crossing a
breakpoint boundary has one of these seven, recorded, not left implicit.

## Priority-preservation rule
The primary action (`visual-hierarchy.md`) must remain reachable without
scrolling at the smallest breakpoint that supports the pattern — secondary
actions may collapse into an overflow menu before the primary action is ever
displaced or hidden. Content ranked highest by information priority
(`visual-hierarchy.md`) is what survives into the mobile single-column reflow
first; lower-priority content may be progressively disclosed
(`visual-hierarchy.md`) rather than shown by default at small sizes.

## Touch-target sizing
Interactive elements meet a **minimum 44×44px** touch target at
touch-relevant breakpoints (mobile, tablet), coordinated with
`ux-engine/interaction-design.md`'s input-modality table — a target sized for
precise mouse pointing at desktop is not automatically acceptable once touch
is the primary input.

## Data table responsive technique
Tables are the hardest common case in enterprise/SaaS products and get an
explicit rule rather than an improvised one per screen:
- **Few, all-critical columns:** collapse to **stacked cards**, one record per
  card, each field labeled — legible but loses at-a-glance column comparison.
- **Many columns, or column comparison is the point** (e.g. financial/ERP
  tables per `product-types/erp.md`): keep tabular layout with **horizontal
  scroll**, and pin the identifying first column (sticky) so context isn't
  lost while scrolling right.

Which technique applies to a given table is decided at that table's
`templates/component-spec.md`, citing this rule rather than reinventing it.

## Not accepted, at any breakpoint
Regardless of how correct the desktop treatment is, none of the following
are acceptable outcomes of a reflow — each maps to a specific rule above
or in a cited sibling file, not a vague "looks broken" impression:
- **Overflow / clipping** — content cut off with no scroll or truncation
  affordance (`component-system.md`'s Overflow behavior rule).
- **Overlapping elements** — two elements occupying the same space at a
  breakpoint neither was actually tested at.
- **Accidental horizontal scroll** — the *page* scrolling sideways because
  one element exceeded the viewport width; deliberate horizontal scroll is
  only ever a stated, contained Become-scrollable decision (above) on one
  specific element (a wide table), never the whole page.
- **Broken alignment** — a shared edge from `layout-system.md`'s Shared
  alignment edges rule that held at desktop but silently drifts at a
  narrower breakpoint.
- **Unreadable text** — a line length that violates `typography.md`'s
  45–75 character measure once a container narrows, or a font size reduced
  below its named type-scale role to force a fit.
- **Compressed controls** — a control rendered smaller than its
  `design-system.md` sizing-scale token, or below the touch-target minimum
  below, to squeeze into available width — the scale steps between named
  values (Component resizing, above), it never shrinks past the smallest
  one.
- **Inconsistent card sizing** — cards in the same responsive grid that
  don't share a height/width relationship at a given breakpoint the way
  they did at desktop (`craft-critique.md` check 10's row/card height
  uniformity scan, re-applied at every breakpoint, not just the reference
  one).
- **Broken charts** — a chart whose legend/axis labels overlap or get
  clipped at a narrower width instead of following the Chart registry
  entry's own reflow/abbreviate rule (`visual-benchmark.md`'s Chart
  verification pipeline, Responsive step).
- **Inaccessible drawers** — a Drawer/Modal that loses its focus trap,
  Escape-to-close, or scroll-behavior rule specifically at a breakpoint
  where it becomes full-screen (`ux-engine/accessibility.md`'s Modal/
  Drawer pipeline step still applies at every breakpoint, not just
  desktop).
- **Hidden critical actions** — the primary action, or any action the
  Priority-preservation rule protects, missing or requiring more than one
  extra step to reach at a smaller breakpoint.

## Responsive verification pipeline
Gate **B9**'s mandatory, explicitly ordered pass, run for every screen at
every breakpoint it supports — the same rules above, sequenced:

```
Desktop baseline → Tablet restructuring → Mobile transformation →
Adaptation-decision audit → Not-accepted defect scan
```

1. **Desktop baseline** — confirm the reference-breakpoint treatment
   itself is correct (this file's Desktop section) before checking how it
   adapts; a flawed baseline makes every downstream reflow check
   meaningless.
2. **Tablet restructuring** — the four Tablet-tier decisions above are
   each explicitly made, not defaulted from desktop or skipped to mobile.
3. **Mobile transformation** — the seven Mobile-tier decisions above are
   each explicitly made.
4. **Adaptation-decision audit** — every element that changed between
   breakpoints has one of the seven named decisions (stack/collapse/hide/
   move/become-scrollable/become-alternative-component/remain-fixed)
   recorded — an undecided element (one that just "got smaller") fails
   this step.
5. **Not-accepted defect scan** — the list above, checked against the
   actual reflow at each breakpoint, not assumed clear because the layout
   didn't visibly break in the one viewport size it happened to be
   reviewed at.

A screen is not production-ready at "looks fine at the desktop width it
was designed at" — every breakpoint this product supports is independently
verified, the same "considered vs. shown" discipline this engine already
applies to component states and chart data.

## Loop position
Consumes `layout-system.md`'s composition patterns at the feature-level loop.
Re-entered when a Test responsiveness finding (dimension 7) traces to a
specific pattern's reflow rule, per `methodology/design-thinking.md`'s routing
table.

## Explicitly not here
- The base grid/spacing values being adapted → `layout-system.md`.
- What counts as priority content → `visual-hierarchy.md`.
- Touch vs. mouse interaction behavior itself → `ux-engine/interaction-design.md`.
- Per-component responsive detail beyond the table rule above →
  `component-system.md`'s point 8 (Responsive behavior), citing this file.
