# Layout System

## Responsibility
Grid, spacing scale, and alignment rules for composing a page — the structural
skeleton content sits on, at the reference (typically desktop) breakpoint.
Adaptation of that skeleton across screen sizes is `responsive-system.md`'s
job.

## Spacing scale
A single base unit, **4px**, with a linear multiple sequence used everywhere
spacing is needed — never an arbitrary value outside this set:

```
4  8  12  16  24  32  48  64  96
```

Small multiples (4/8/12) space elements *within* a component (icon-to-label
gap, internal padding); mid multiples (16/24/32) space elements *between*
related components within a group; large multiples (48/64/96) space *between*
distinct sections of a page. This three-tier usage convention is what keeps
visual rhythm consistent instead of every screen inventing its own spacing
logic.

**Vertical rhythm:** the gap between stacked elements of the *same kind*
(row-to-row in a list, field-to-field in a form, card-to-card down a
column) stays one single scale value for that context, not a value that
drifts between instances because each was placed independently. Where two
adjacent gaps in the same repeating context differ, one of two things is
true: either the content genuinely differs in a way that justifies it
(stated, not assumed), or it's an accidental gap — an inherited default
margin, a leftover spacer, a component's own internal padding stacking
with its container's gap rather than one or the other being suppressed.
An accidental gap is a defect at this level even when it's only a few
pixels off the intended scale step, per the same "close is not aligned"
standard the Alignment rules above apply.

**A persuasion surface's pivotal section can legitimately exceed 96px.** This
ceiling is calibrated for dense application UI; a single-page conversion
surface (`product-types/landing-page.md`) has far fewer sections competing
for attention, and its highest-stakes section (typically the hero, or
whichever section carries the primary CTA) can use a section-padding value
beyond the top of this scale — real comparable references run considerably
higher for exactly this section, not for every section. This is a scoped
exception for that one product type's pivotal sections, not a change to the
scale's ceiling for ordinary application screens.

## Grid definition
- **Columns:** 12 at the desktop reference breakpoint.
- **Gutter:** 24px between columns.
- **Margin:** 32px minimum page margin at desktop; scales down per
  `responsive-system.md` at smaller breakpoints.

Components span whole-column widths (e.g. a 4-column card, an 8-column form) —
a component spanning a fractional column width is a sign the grid, not the
component, needs revisiting.

## Alignment rules
Elements align to the grid's column edges by default. **Optical alignment
exceptions** are allowed and expected in specific, narrow cases — e.g. an icon
placed beside text needs a few pixels of vertical nudge to *look* centered
even though its bounding box is already grid-aligned — but every such
exception is a deliberate, documented choice in the component's spec
(`templates/component-spec.md`), never an ad hoc pixel-nudge applied
inconsistently across the product.

**Shared alignment edges — checked explicitly, not assumed from "it uses the
grid":** the grid rule above states the default; this is what actually
verifying it means for the specific regions a screen is built from. Every
pair of elements below shares a real edge (left, right, or baseline) — not
an approximately-close one:
- **Header** — its content's left edge aligns with the primary content
  area's left edge below it, not independently margined.
- **Sidebar** — every nav item's left edge (icon and label) shares one
  column; the sidebar's own right edge is a single consistent line the
  whole height of the viewport, not a per-section value.
- **Cards in a row or grid** — top edges align across the row regardless of
  internal content length; where heights are allowed to differ (content-
  driven), tops still align even when bottoms don't.
- **Tables** — every column's content shares one left edge per column
  (right-aligned for numeric/tabular columns, per `typography.md`'s tabular-
  figure rule); header cell text aligns with its column's body-cell content,
  not independently centered while the body is left-aligned.
- **Forms** — every label shares one left edge; every input/control sharing
  a row shares one top edge; the input column's left edge is consistent down
  the whole form regardless of individual label length (a longer label never
  pushes its own input out of the shared column).
- **Icon/text pairs** — the icon's optical center aligns to the adjacent
  text's cap-height or x-height midline (the specific optical-alignment case
  the exception clause above exists for), not to the text's full bounding
  box, which reads as low.
- **Buttons** — a button group's individual buttons share one top edge; a
  button's internal icon+label pairing follows the icon/text rule above.
- **Charts** — a chart's plot area left edge aligns with its own card's
  other content (its title, its legend) — not offset by the axis-label
  gutter with nothing else in the card accounting for that same gutter.

A pair of elements that are *close* but not exactly aligned (a 1-3px drift
from rounding, differing units, or an inherited default) fails this check
the same as a large misalignment — "close enough to not notice at a glance"
is exactly the defect class this checklist exists to catch before it ships,
not a tolerance this rule grants.

## Composition patterns
Canonical page-level shapes, each mapped to the
`ux-engine/information-architecture.md` shape it fits:

| Pattern | Fits when… | Notes |
|---|---|---|
| **List + detail** | A flat collection with drill-in to one record at a time | Two-pane on desktop, collapses to list-then-detail on mobile (`responsive-system.md`) |
| **Dashboard grid** | An overview/landing screen with independent, glanceable cards | Cards are independently reorderable/removable; no card depends on another's state |
| **Single-column form** | A focused data-entry task | Matches `ux-engine/form-design.md`'s single-page form case |
| **Master-detail** | Hierarchical navigation needing persistent context (e.g. a folder tree beside its contents) | Distinct from list+detail: the "master" side is structural/navigational, not just a list of peers |
| **Wizard / full-screen stepper** | A multi-step workflow (`ux-engine/navigation-system.md` item 11) | Takes over the full screen deliberately, to remove peripheral distraction during a committed sequence |

A screen that doesn't cleanly fit one of these patterns is usually a sign its
`templates/screen-architecture.md` region map needs reconsidering before
layout is applied, not a cue to invent a bespoke one-off composition.

The reverse failure is just as real: choosing **Dashboard grid** by
reflex because the screen happens to be labeled a dashboard, rather than
because independent, glanceable cards are actually the right shape for
*this* screen's information priority — a predictable layout chosen by
convention instead of fit is the structural-level instance of
`craft-critique.md`'s anti-cliché catalog, not a separate concern from it.
State which pattern was chosen and why it fits this screen's actual region
map, the same justification discipline `visual-trends.md`'s gate already
requires for a surface-level trend choice.

## Loop position
Consumes `ux-engine/information-architecture.md`'s hierarchy and
`templates/screen-architecture.md`'s region maps at the feature-level loop
(`methodology/design-thinking.md`). Re-entered when a Test responsiveness or
usability finding traces to the underlying composition pattern rather than its
responsive reflow, per that file's routing table.

## Explicitly not here
- Breakpoint values and reflow behavior → `responsive-system.md`.
- Emphasis/priority within the grid → `visual-hierarchy.md`.
- Component-internal layout (padding inside a card, button) →
  `component-system.md`.
- Radius/elevation/motion tokens → `design-system.md`.
