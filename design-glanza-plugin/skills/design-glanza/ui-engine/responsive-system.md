# Responsive System

## Responsibility
Breakpoint strategy and reflow rules: how `layout-system.md`'s composition
patterns adapt across device classes.

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
