# Component System

## Responsibility
Component taxonomy and anatomy, and the 8-point analysis framework every
component must satisfy before it's considered spec-complete. Behavioral states
(loading/error/empty) are defined in `ux-engine/state-design.md` — this file
owns how each is expressed *visually* per component.

## Atomic-to-composite hierarchy
**Atom** (a button, an icon, an input) → **molecule** (a form field: label +
input + error text) → **organism** (a data table, a full form, a nav bar) —
the naming convention used across every `templates/component-spec.md` entry.
A component's category determines how much it's allowed to vary: atoms have
the tightest, smallest variant sets; organisms are compositions of
already-specified atoms/molecules, not places to introduce new one-off styling.

## The 8-point component analysis framework
Every component in the inventory is specified against all eight points below.
A component missing any point is not yet spec-complete.

### 1. Purpose
The single job this component does. A button triggers an action; it does not
also carry navigation semantics (that's a link, styled differently even if
visually similar) — a component accumulating unrelated responsibilities is a
sign it should split into two.

### 2. Anatomy
Named parts, e.g. a button: `container`, `icon-slot` (optional, leading or
trailing), `label`. Anatomy is what `templates/component-spec.md` enumerates
per component, and what the variants below are allowed to vary.

### 3. Variants
A closed set — never an open-ended "and other styles as needed":
- **Emphasis:** primary / secondary / tertiary / destructive (per
  `visual-hierarchy.md`'s primary/secondary-action rules).
- **Size:** sm / md / lg, using `layout-system.md`'s spacing scale for
  internal padding at each size.

### 4. States
The visual expression of `ux-engine/state-design.md`'s behavioral states, per
component: `default`, `hover`, `focus` (always visually distinct from hover —
focus must remain visible for keyboard users even when hover has no meaning),
`active`, `disabled`, and — where the component can trigger an action —
`loading`. Two further states apply wherever they're genuinely relevant to
the component (not added by default to every entry): **`selected`** — a
persistent chosen indicator for a component that can be one of several
picked items (a card in a multi-select grid, a table row, a list item,
a tab) — distinct from `active`, which is the transient moment of being
pressed/current, not a lasting choice; and **`read-only`** — content the
current context doesn't allow editing but that still represents a
confirmed, legible value, not an unavailable control — visually distinct
from `disabled` specifically because read-only content is never dimmed
the way a genuinely unavailable control is. Every variant × state
combination is either specified or explicitly inherited from a base rule;
none are left undefined — and a state that genuinely doesn't apply to a
given component (most components have no `selected` state at all) is
stated as not-applicable, never silently omitted with no reasoning shown.

**The same component's same state uses the same visual language everywhere
it appears** — a primary button's `hover` treatment (darken/lighten amount,
transition duration from `design-system.md`'s motion tokens) is one rule
applied to every primary button, never re-decided per screen; a `focus`
indicator's thickness/offset/color is likewise one rule (per
`ux-engine/accessibility.md`'s Focus appearance criterion), not a value
that happens to differ because two screens were built at different times.
Two instances of the same component with visibly different hover/focus/
disabled treatment is drift, the same category `agents/design-system-
expert.md` already catches for token values, applied here to state
*behavior* rather than static appearance.

### 5. Behavior
Cross-reference, not redefinition: cite the specific
`ux-engine/interaction-design.md` rule that applies to this component type
(e.g. a button's click-feedback timing, per that file's action-feedback
table) rather than restating the behavior rule here.

### 6. Content rules
Concrete text conventions, fixed once and applied everywhere:
- Button labels: verb-led ("Save changes," not "Changes"), sentence case, not
  Title Case.
- Truncation: single-line text truncates with an ellipsis at a defined max
  width; multi-line content (table cells, cards) defines a max line count
  before truncating.
- Empty/zero-content handling: what a component shows when it has nothing to
  display (distinct from `ux-engine/state-design.md`'s `empty` *state* — this
  is the component's own content-level fallback, e.g. a user-avatar
  component's initials fallback when no image exists).

### 7. Accessibility
Cite `ux-engine/accessibility.md`'s semantic mapping table for this
component's role and keyboard behavior rather than restating it; add only
what's specific to this component (e.g. a button's accessible name must match
its visible label, or explain the mismatch if using an icon-only button —
see Iconography below).

### 8. Responsive behavior
Cite `responsive-system.md`'s general reflow rule and state how *this*
component specifically adapts — e.g. a data table (organism) collapses to
stacked cards on mobile per that file's content-reflow rule; a button
(atom) rarely changes shape across breakpoints beyond touch-target sizing.

## Production-readiness pipeline
The 8 points above are checked in a specific, mandatory order — the same
points, not a second framework — because a component isn't spec-complete
just because its default state happens to look good:

```
Component exists → States identified → States designed → Interaction
behavior defined → Responsive behavior defined → Accessibility behavior
defined → Visual consistency verified
```

| Step | Maps to | What "done" actually means |
|---|---|---|
| **Component exists** | Points 1-3 | Purpose, anatomy, and the closed variant set are named — not yet a claim that it's finished. |
| **States identified** | Point 4, first half | Every state relevant to *this* component (per the relevance criteria below) is named — a list, not yet designed behavior. |
| **States designed** | Point 4, in full | Each identified state has an actual visual treatment specified, including `selected`/`read-only` where relevant — a named-but-undesigned state fails this step. |
| **Interaction behavior defined** | Point 5 | The cited `interaction-design.md`/`form-design.md` rule is confirmed to actually apply and produce a concrete behavior for this component, not just a citation with no verified fit. |
| **Responsive behavior defined** | Point 8 | A stated reflow rule exists for this specific component, not inherited silently from a sibling. |
| **Accessibility behavior defined** | Point 7 | Semantic role, keyboard path, and accessible name are stated, not assumed correct by default. |
| **Visual consistency verified** | Cross-cutting | This component's states match the same component's treatment everywhere else it appears (the same-component-same-state rule above), checked against `agents/design-system-expert.md`'s drift review — the step that catches a component that passed every prior step in isolation but still drifted from its own other instances. |

**Do not add a state just for completeness.** Which states are actually
relevant to a given component is determined by, and only by:
- **Component type** — a static display element (a Badge) has no
  `hover`/`focus` states of its own; an interactive one does.
- **User action** — a state only exists if some real action or event can
  actually produce it (no `loading` state for a component that never
  fetches anything).
- **Business context** — `selected` only applies where multi-select or
  picking is an actual product behavior, not a default add-on.
- **Data availability** — `empty` only applies where the component can
  legitimately show zero results; a component that always has content by
  construction doesn't need it.
- **Failure conditions** — `error`/`validation error` only apply where
  the underlying action can actually fail; not every component has a
  failure mode worth a dedicated state.
- **Permissions** — `disabled`/`permission denied` only apply where the
  product's actual role model can restrict this action for someone.

A component with every state from every registry entry bolted on
regardless of fit is not more production-ready than one with only the
states that actually apply — it's a sign the relevance check above was
skipped, the same failure this pipeline's first two steps exist to catch
before States designed is ever reached.

**A component is not production-ready because its default state looks
good.** The pipeline above is not satisfied by a single, polished-looking
resting-state screenshot — every step must be independently checked, the
same "considered vs. shown" discipline `visual-benchmark.md`'s mandatory
refinement step 3a already applies to screen-level states, applied here
at the component level.

## Iconography
Icons are a component type in their own right, with the same rigor as any
other atom:
- **Size:** from `design-system.md`'s icon size scale — never an arbitrary
  pixel value.
- **Stroke/fill convention:** pick one style (e.g. 1.5–2px outline stroke) and
  apply it everywhere — never mix filled and outline icon styles within one
  product.
- **Color inheritance:** an icon inherits `currentColor` (the surrounding
  text/label color) by default; it only takes an explicit semantic color
  (`color-system.md`) when it is itself conveying status (a `danger`-colored
  warning icon), not as a decorative choice.
- **Interactive vs. decorative:** an icon-only interactive element (an
  icon-only button) requires an accessible name via a label, not just visual
  recognizability; a decorative icon paired with visible text is hidden from
  assistive tech (`aria-hidden`) so it isn't announced redundantly — this is
  the concrete instance of accessibility point 7 above, applied to icons
  specifically.
- **Meaning, not decoration:** every icon's conventional meaning matches
  what it actually does — a generic chart/graph icon reused for every
  analytics-adjacent action regardless of the specific action, or an icon
  whose common meaning contradicts its adjacent label, is the icon-level
  instance of `craft-critique.md`'s anti-cliché catalog. An icon chosen
  because it fills the slot, not because it's the correct symbol for this
  specific action, fails point 1 (Purpose) above.

## Badge, tooltip, and overflow positioning
Three specific micro-polish cases worth naming explicitly since they're the
most common source of a component that's individually well-specified but
breaks at its own edges:
- **Badge positioning** — a status/count badge anchors to a fixed corner or
  edge of its host element (e.g. top-right of an icon, per a stated offset
  from the spacing scale) — the same anchor point and offset for every
  instance of that host/badge pairing, never eyeballed per screen.
- **Tooltip positioning** — opens toward whichever side of the trigger has
  room in the viewport (flips rather than clipping/overflowing off-screen
  when the default side doesn't fit), with a fixed offset from the trigger
  (spacing scale) and a consistent pointer/arrow treatment across every
  tooltip in the product.
- **Overflow behavior** — any component whose content can exceed its
  container (a long label, a long table cell, a crowded toolbar) has a
  *stated* resolution — truncate with ellipsis (point 6), wrap, scroll
  within its own container, or collapse into an overflow menu — never left
  unstated such that the actual behavior is whatever the browser/framework
  defaults to. Content silently overlapping a neighboring element or being
  visually clipped with no scroll/truncation affordance is a defect, not
  an acceptable edge case, regardless of how rarely the triggering content
  length actually occurs.

## Tables
A table is an organism specified against the same 8-point framework, with
three dimensions worth naming explicitly since they're the most common
source of a table that "looks fine at a glance" but is measurably
inconsistent under inspection:
- **Row height** — one fixed height per density (`visual-hierarchy.md`'s
  comfortable/compact/dense scale), derived from the spacing scale
  (`layout-system.md`), held constant for every row regardless of that
  row's own content — a row containing a two-line value does not grow
  taller than its neighbors; content that doesn't fit at the fixed height
  truncates (point 6's truncation rule) rather than expanding the row.
- **Column alignment** — text columns left-align, numeric/tabular columns
  right-align with tabular figures (`typography.md`), and every column's
  header label shares its body cells' alignment — a right-aligned numeric
  column with a centered or left-aligned header is the specific,
  easy-to-miss defect this rule exists to name. Column left/right edges
  hold down the entire table per `layout-system.md`'s Shared alignment
  edges rule; a column whose content width varies by row (e.g. an
  unpadded number) still keeps its edge fixed via the column's own
  consistent width, not per-row.
- **Row spacing** — the vertical gap is entirely the row height above
  (padding, not a separate margin between rows); a table mixing row
  height *and* an inter-row margin produces uneven-looking rows even when
  every individual row height is technically identical, so only one
  mechanism is ever used, never both.

A sortable/filterable data table additionally follows
`component-registry/composition-patterns.md`'s Data Table pattern
(search + filters + sorting + pagination + selection + bulk actions +
states) rather than being specified from scratch.

## Data visualization
Charts are a component type in their own right, specified against the same
8-point framework — chart-type selection specifically is a function of what
relationship the data has, not visual preference. The prior question, before
any type is chosen, is whether a chart is warranted at all: **a single
tracked number with no meaningful trend or comparison to show uses
`composition-patterns.md`'s KPI/Stat Card, not a chart** — a chart adds
decoding effort a plain number doesn't need, so it's justified only when
there's an actual shape (trend/comparison/composition/distribution/
correlation) for the viewer to read. Once a chart is genuinely warranted:

| Data shape | Chart type |
|---|---|
| Change over time | Line (continuous trend) or bar (discrete periods) |
| Part-to-whole at one point in time | Stacked bar or a single pie/donut — never a pie for more than ~5–6 slices, a stacked bar reads better past that count |
| Comparison across categories | Bar (horizontal when category labels are long) |
| Correlation between two variables | Scatter |
| Distribution | Histogram or box plot |

A chart's color draws from `color-system.md`'s data-visualization ramps
(sequential/diverging/categorical — matched to the same data-shape logic
above, not chosen independently), and every data-bearing color additionally
carries a non-color channel (direct labels, a legend with pattern/texture, or
hover-revealed values) per the color-blind safety rule. A chart's `empty`
state (`state-design.md`) shows a stated reason ("no data for this period"),
never a blank axis with no data indistinguishable from a loading failure.
Chart *type* is this table's decision; chart *placement* relative to
everything else on the screen is `visual-hierarchy.md`'s Information
priority call, not a default slot — a chart placed top-right or paired
side-by-side with another chart because "dashboards have charts there" is
the placement-level instance of `craft-critique.md`'s anti-cliché catalog,
distinct from picking the right chart type for the data.

Bar and column charts specifically start their value axis at **zero** — a
truncated/non-zero baseline visually exaggerates the difference between
values and is a defect regardless of how much clearer it makes a small
difference look; a line chart's axis may legitimately start elsewhere when
trend shape, not magnitude comparison, is the point, per the data-shape
table above.

Axis and tick labels are content, subject to the same no-placeholder
discipline Rule 10 already applies everywhere else — a real calendar date,
a real category name, a real unit, never a sequential index standing in for
one ("Day 1," "Item 2," "Category A"). An index label is a tell that the
underlying data was fabricated rather than sourced/derived, exactly the
signal `craft-critique.md`'s anti-cliché catalog and category A (Product
Fit) of `ui-audit-framework.md` already watch for elsewhere on the screen —
this is that same check, applied to chart axes specifically since they're
otherwise easy to treat as "just formatting." Data realism extends past the
axis to every plotted value — a revenue chart with suspiciously round
numbers, or values outside the plausible range for this product's actual
stated scale, is the numeric-data instance of the same defect.

**A chart tells its own story, not just plots values.** Every chart states:
a **title** naming what's actually being measured (never a generic
"Overview"); a **subtitle or context line** giving the time period and,
where relevant, the comparison period ("vs. prior 30 days"); correct
**units/currency** matching the rest of the screen's convention; and, where
the data has one, a **meaningful highlight** — an emphasized endpoint or a
labeled peak/dip — that gives the viewer a starting interpretation rather
than a bare, uninterpreted plot. A **legend** appears only when more than
one series is shown (a single-series chart carrying a legend is clutter,
not clarity per the Contrast-of-weight discipline `visual-hierarchy.md`
already applies elsewhere); each entry's label and color match the plotted
series exactly, and its position has a stated responsive behavior at
narrow widths rather than silently overlapping. A **tooltip**, on hover and
focus (`interaction-design.md`'s hover-and-focus rule), reveals the exact
value, its date/time or category, and — where a comparison period is part
of the chart's story — the prior-period value alongside it, formatted with
the same units/locale convention as the rest of the screen. Beyond `empty`,
a chart distinguishes **partial data** (the query succeeded but returned
fewer points than this chart type needs to read cleanly — shown as itself,
never silently rendered as if the picture were complete) from
**insufficient data** (fewer than the ~3-point floor named above — a
stated message, never a blank-looking chart indistinguishable from
`loading`). The full checkable sequence — Purpose, Type, Data Realism,
Axis, Legend, Tooltip, Filter, State, Accessibility, Responsive, Visual
Storytelling — is `visual-benchmark.md`'s Chart verification pipeline, run
before any dashboard is considered final; a chart that fails Visual
Storytelling even after passing every mechanical step is rejected and
redesigned, not shipped as a technically-correct but silent plot.

## Motion at the component level
Which specific state transitions use `design-system.md`'s motion tokens is
decided here, per component: a modal's enter/exit uses `motion-base`; a
dropdown's open/close uses `motion-fast`; a toast's enter/exit uses
`motion-base`. High-frequency, low-stakes state changes (a checkbox toggle, a
hover color shift) either use `motion-fast` or no transition at all — never a
slower token, which would make frequent interactions feel sluggish rather than
polished.

## Reuse rule
A new screen's need is met by an existing component variant whenever the need
fits within an already-specified variant/size/state combination; a genuinely
new component is justified only when the purpose (point 1) doesn't match
anything in the inventory — checked first against the master
`component-registry/*` (Rule 24, `config/operating-rules.md`), then against
the product's own inventory. `agents/design-system-expert.md` governs this
decision on an ongoing basis, not just at a component's creation.

## Loop position
Consumes `design-system.md`'s tokens and `ux-engine/state-design.md`'s
behavioral states at the feature-level loop. Re-entered when a Test usability
or accessibility finding traces to a specific component's execution, or when
`agents/design-system-expert.md` flags drift, per
`methodology/design-thinking.md`'s routing table.

## Explicitly not here
- Which behavioral states exist and why → `ux-engine/state-design.md`.
- Page-level composition of multiple components → `layout-system.md`.
- The concrete spec document per component → `templates/component-spec.md`.
- Token values (radius, elevation, motion durations, icon sizes) →
  `design-system.md`.
- Pre-populated, professionally-reasoned instances of this framework for
  ~29 common components and their composition patterns →
  `component-registry/*` (this file remains the single source for the
  framework itself; that folder never restates it, only instantiates it).
