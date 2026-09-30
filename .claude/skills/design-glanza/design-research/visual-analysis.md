# Visual Analysis

## Responsibility
The Visual research area: evaluating hierarchy, composition, density,
typography, color, spacing, navigation, and component patterns in whatever
references/competitors/domain-conventions are available — and extracting
the **principle** each one embodies, never copying the **style** itself.
This is the research-stage counterpart to `ui-engine/craft-critique.md`
(applied to a *finished* screen) and `design-reference-engine/reference-
analysis.md` (applied to *one supplied reference*) — this file is broader:
what's visually conventional for this domain/density/audience in general.

## Extract principles, not styles
"This competitor uses a purple gradient hero" is a style observation — not
useful evidence on its own, because it doesn't say *why* it works or
whether it would work here. The research-grade version: "the gradient hero
creates strong visual separation between the marketing header and the
dense functional content below it — the principle (strong register
separation between a product's marketing surface and its functional
surface) transfers even if this product's actual color/gradient choice
doesn't." Every visual observation in this file's output must be phrased as
a transferable principle, evaluated against `pattern-analysis.md`'s "why
does this pattern work" test, before it's allowed to influence this
product's own direction.

## What to evaluate, per category

| Category | What to extract as a principle | Owning technique the principle feeds |
|---|---|---|
| Hierarchy | How primary/secondary/tertiary emphasis is signaled, and why that mapping serves this task | `ui-engine/visual-hierarchy.md` |
| Composition | Grid shape, list+detail vs. dashboard-grid vs. single-column, and what task shape it serves | `ui-engine/layout-system.md` |
| Density | What density register this domain/task/audience combination actually needs, not a universal default | `ui-engine/visual-hierarchy.md`'s density scale, `methodology/design-judgment.md`'s information-density factor |
| Typography | Type-scale steps and pairing conventions, and whether numeric/tabular data is a first-class concern here | `ui-engine/typography.md` |
| Color | Palette breadth, saturation register, and how semantic meaning is conventionally expressed in this domain | `ui-engine/color-system.md` |
| Spacing | Base unit and rhythm this density register implies | `ui-engine/layout-system.md` |
| Navigation | Which navigation surface (sidebar/top/tabs) this IA shape is conventionally paired with visually | `ux-engine/navigation-system.md` (structural choice), `ui-engine/layout-system.md` (visual realization) |
| Component patterns | Which recurring component (card vs. row vs. tile) this content type is conventionally rendered as, and why | `ui-engine/component-system.md` |

## The anti-trend-slave discipline still applies
Every principle extracted here is still subject to
`ui-engine/visual-trends.md`'s 3-point trend-adoption gate and
`methodology/design-judgment.md`'s anti-fashion strip-away test before it's
adopted — visual research surfaces the option set, it does not pre-select
the currently-fashionable option from it (the same discipline `design-
reference-engine/design-research.md` already states, restated here because
this file is now that discipline's actual research technique, not a
one-paragraph summary of it).

## Explicitly not here
- The actual token values, contrast rules, and scale definitions → the
  `ui-engine/*` file named in the table.
- Extracting what one specific supplied reference does → `design-reference-
  engine/reference-analysis.md` (narrower and product-specific; this file is
  broader and domain-general).
- Comparing a finished generated screen back against this research →
  `ui-engine/visual-benchmark.md`.
- Naming a competitor/reference product specifically → `competitor-
  analysis.md`.
