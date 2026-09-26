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
