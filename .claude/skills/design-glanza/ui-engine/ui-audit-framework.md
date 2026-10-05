# UI Audit Framework

## Responsibility
The strict, 11-category structural audit for a finished screen/UI pass —
distinct from `craft-critique.md` (a numeric self-critique focused on
composition craft) and from `methodology/test.md` (product-level validation
against user needs). This file is the **completeness checklist**: for each
category, name what must be verifiable on the actual screen, citing the
file that owns the underlying rule rather than restating it. Two of the
eleven categories (A, B) are genuinely new — nothing else in the engine
currently checks whether a screen represents the *actual product* or
follows an *approved reference's* language; the rest organize existing,
already-enforced rules into one audit pass so a reviewer runs one checklist,
not a dozen.

## When this runs
At Prototype's UI pass (`agents/ui-designer.md`, `agents/design-system-expert.md`),
after `craft-critique.md`'s composition-level checks, and again at Audit. Feeds
`ui-engine/visual-benchmark.md`'s gap analysis directly — a finding here is
exactly the kind of thing that analysis compares against the reference and
the approved direction.

## The 11 categories

### A. Product Fit
Does the UI actually represent *this* product and *this* workflow, not a
generic template that happens to have the right words on it? Check: does
every screen trace to a real flow step (`ux-engine/user-flow-engine.md`) and
a real requirement (`product-intelligence/traceability.md`'s chain);
does the content use this product's own domain terminology
(`ux-engine/information-architecture.md`'s labeling convention), not
placeholder or generic SaaS language; does the screen's structure match
what this actor actually does at this step, not a stock dashboard shape
applied regardless of task. **Fails when:** the screen would be equally at
home in an unrelated product with only the logo swapped — the same test
`craft-critique.md` check 6 already applies to visual composition, applied
here to the screen's *substance*.

**Where a Figma Design Context exists (added v1.0.33):** this category
additionally checks **structural completeness against that context** — a
real benchmark run (the PerkyPet root-cause audit) found a screen can pass
every other check in this framework while a whole Figma-derived section
(a hero, a composed-from region, a 3-step explainer) is simply absent, and
nothing had caught it. Concretely: for the screen being audited, walk
`figma-context.json`'s `screens[].composedFrom` for this screen's entry —
every named region it composes from must actually appear in the generated
screen, or `figma-context-consumption.md`'s Completion verification must
show an explicit, recorded reason it was changed or removed. **Fails
when:** a `composedFrom`-named region is silently absent, with no recorded
reason — this is a Blocker-severity "Missing pattern" gap
(`visual-benchmark.md`'s gap-type table), not a lesser finding, regardless
of how well every other category scores.

### B. Reference Match
Where `product-builder/ui/design-direction.md` classifies as
Reference-Driven or Guideline-Driven, does the generated screen actually
follow the extracted design language (`design-reference-engine/
reference-analysis.md`'s output), not a superficially similar but
independently-invented one? Check: token values (radius, spacing, type
scale) match what was extracted or explicitly reconciled if they diverge;
the register selected in `design-direction.md` is the one actually
rendered; a stated Do/Don't rule from the direction document isn't quietly
violated. Where the mode is Custom Design or Default, this category checks
the equivalent — does the screen match what was *actually decided* in
Design Setup, not something decided fresh at this later step. **Fails
when:** the direction document and the screen disagree with no recorded
reason.

### C. Visual Hierarchy
Can a viewer immediately name the primary action, the most important
information, secondary information, status, and how to navigate? **Checked
by:** `ui-engine/visual-hierarchy.md`'s full rule set, `craft-critique.md`
checks 1–3.

### D. Layout
Alignment to grid, spacing-scale adherence, container width, density
appropriate to the register, grouping matching the IA, whitespace deployed
deliberately. **Checked by:** `ui-engine/layout-system.md`,
`visual-hierarchy.md`'s Grouping/Density/Whitespace sections,
`craft-critique.md` check 4.

### E. Typography
Hierarchy, readability (measure, line-height), scale correctness per role,
weight usage, tabular figures for numeric/data columns. **Checked by:**
`ui-engine/typography.md` in full.

### F. Color
Semantic meaning applied correctly, contrast ratios met, consistent
palette use, restrained/non-decorative application, emphasis expressed
through the primary/danger/etc. tokens rather than ad hoc values. **Checked
by:** `ui-engine/color-system.md`, `craft-critique.md`'s anti-cliché catalog.

### G. Components
Consistency and reuse (no near-duplicate components), every state
specified, correct sizing per context, clear interactive affordance (never
a false or missing affordance). **Checked by:**
`ui-engine/component-system.md`'s 8-point framework,
`ux-engine/interaction-design.md`'s Affordance clarity section.

**Where a Figma Design Context exists (added v1.0.33):** this category
additionally checks **cross-screen recurrence** — walk every
`figma-context.json` component carrying a `recurrence` list, and for each
screen named in it, confirm the component (or its state-appropriate
variant) is actually present in that screen's generated output. This is
specifically the check that catches a component correctly built for one
state/variant of a screen (e.g. an active-progress dashboard) but silently
dropped when a second variant is generated (e.g. its empty-state or
completed-state sibling) — a real, confirmed failure mode from the
PerkyPet root-cause audit, where a recurring badge-icon and a recurring
3-step explainer were present on one dashboard variant and absent on
others with no recorded reason. Also check **visual-asset fidelity**: a
component whose Figma source names a specific illustration or icon
treatment (`figma-context.json`'s `imagery`/`iconography` fields) must be
rendered as a faithful equivalent per `figma-context-consumption.md`'s
visual asset fidelity rule — not emoji, not a generic gradient, not an
unrelated icon standing in for it. **Fails when:** a `recurrence`-named
screen is missing the component with no recorded reason, or a named
illustration/icon is replaced with something that doesn't preserve its
visual character per that rule.

### H. Interaction
Two things, checked together because a state with no feedback is really an
interaction failure, and feedback with no corresponding state is really a
state-coverage failure: **state completeness** (every applicable state from
the mandatory set is actually designed for this component/screen — hover,
focus, active, disabled, loading, success, error, empty, and, where
relevant, a confirmation step) and **interaction quality** (real, observable
feedback for each of those states, not just their existence on paper).
**Checked by:** `ux-engine/state-design.md`'s 13 mandatory states,
`ux-engine/interaction-design.md`'s Action-feedback rules and
Undo/confirmation matrix. Zero blank cells, per B7.

### I. Accessibility
Contrast, full keyboard operability, visible focus indication, correct
semantic/ARIA roles and labels, touch-target sizing. **Checked by:**
`ux-engine/accessibility.md`, `ui-engine/color-system.md`'s contrast rule,
B8.

### J. Responsive Design
Run as `ui-engine/responsive-system.md`'s own Responsive verification
pipeline (Desktop baseline → Tablet restructuring → Mobile transformation
→ Adaptation-decision audit → Not-accepted defect scan): desktop, tablet,
and mobile each independently verified, not assumed from the desktop
treatment alone; navigation adapts per `ux-engine/navigation-system.md`'s
responsive guidance; tables and forms have a stated collapse/reflow
behavior; every changed element has one of the seven named adaptation
decisions (stack/collapse/hide/move/become-scrollable/become-alternative-
component/remain-fixed); content never silently overflows. **Fails when:**
any item on that pipeline's "Not accepted" defect list is present at any
supported breakpoint. **Checked by:** `ui-engine/responsive-system.md`, B9.

### K. Domain Conventions
Does the screen follow the established patterns for *this specific
domain* — the matched `product-types/<domain>.md` pack's UI-pattern point,
and any loaded `product-types/domain-standards/` entry (Rule 17)? A
healthcare screen that reads like a generic admin panel, or an ERP screen
with consumer-app visual flourish, fails this category even if every other
category passes — domain fit is checked as its own dimension, not assumed
from passing the others.

## Reconciling the 15-point critique checklist
Design-Glanza's critique-and-iteration loop (`ui-engine/visual-benchmark.md`)
is sometimes described by a flatter, 15-item vocabulary (alignment,
spacing, grid, typography, component quality, state completeness, data
visualization, interaction, accessibility, responsive behavior, visual
hierarchy, modern UI quality, product-context fit, content realism,
pixel-level polish). Every one of those 15 already has a home in this
engine — this table is the explicit cross-reference, never a 12th
taxonomy running alongside the 11 categories above:

| Critique dimension | Checked by |
|---|---|
| Alignment | Category D (alignment half) / pixel pipeline's Alignment step |
| Spacing | Category D (spacing half) / pixel pipeline's Spacing step |
| Grid | Category D / pixel pipeline's Structure step (12-column/gutter/margin grid) |
| Typography | Category E / pixel pipeline's Typography step |
| Component quality | Category G / pixel pipeline's Component step, `component-system.md`'s Production-readiness pipeline |
| State completeness | Category H's state-completeness half, per B7 |
| Data visualization | `visual-benchmark.md`'s Chart verification pipeline (runs for any screen with a chart, inside this same cycle) |
| Interaction | Category H's interaction-quality half |
| Accessibility | Category I, `ux-engine/accessibility.md`'s pipeline, per B8 |
| Responsive behavior | Category J, `responsive-system.md`'s pipeline, per B9 |
| Visual hierarchy | Category C |
| Modern UI quality | `craft-critique.md`'s anti-cliché catalog (check 8) + this file's Final Visual QA closing question, the **Generic/templated** gap type |
| Product-context fit | Category A |
| Content realism | `craft-critique.md`'s anti-cliché catalog's placeholder-content tell, and the Chart pipeline's Data Realism step for chart values specifically |
| Pixel-level polish | Pixel pipeline's Micro-polish step, this file's own namesake discipline |

Every finding against any of these 15 still uses this file's **Observation
→ Problem → Fix** triad, still gets a gap type from `visual-benchmark.md`'s
table, and still gets a P0-P3 priority from that same file's Priority
classification — one reporting convention, regardless of which of the 15
angles surfaced it.

## Pixel-level verification pipeline
The 11 categories above are checked in a specific, mandatory **order** for
a pixel-precision pass — the same categories, not a second taxonomy
alongside them, sequenced because each step depends on the previous one
already holding (checking alignment against a structurally wrong skeleton
just confirms the wrong thing precisely):

```
GENERATE → STRUCTURE → ALIGNMENT → SPACING → SIZING → TYPOGRAPHY →
COMPONENT → RESPONSIVE → MICRO-POLISH → FINAL VISUAL QA
```

| Step | Runs | What specifically gets checked |
|---|---|---|
| **Structure** | Category A + D's composition half | The composition pattern (`layout-system.md`'s five patterns) is correctly selected, the region map is complete, the 12-column/gutter/margin grid is actually applied, and — where a Figma Design Context exists — every `composedFrom`/`recurrence`-expected region and component is actually present (Category A/G's v1.0.33 addition) — checked before anything below, since it's meaningless to check alignment on the wrong, or an incomplete, skeleton. |
| **Alignment** | Category D's alignment half | `layout-system.md`'s Shared alignment edges rule, per region: header, sidebar, cards, tables, forms, icon/text baseline, buttons, charts — each a real shared edge, not an approximately-close one. |
| **Spacing** | Category D's spacing half | Spacing-scale adherence, the three-tier usage convention, vertical rhythm, internal-padding-vs-external-gap (`craft-critique.md` check 4), and a scan for accidental gaps (`layout-system.md`'s Vertical rhythm rule). |
| **Sizing** | Category G's dimension half | Every control height, card dimension, icon/avatar size, table row height, chart proportion, sidebar width, and header height resolves to a named token in `design-system.md`'s closed scales — zero arbitrary pixel values. |
| **Typography** | Category E | `typography.md` in full: scale, weight, line-height, letter-spacing, tabular numeric alignment, truncation and long-content behavior. |
| **Component** | Category G's remaining half | `component-system.md` point 4's same-component-same-state rule, badge/tooltip positioning, overflow behavior, table row/column consistency. |
| **Responsive** | Category J | `responsive-system.md`'s own Responsive verification pipeline, run in full — every breakpoint independently verified, every changed element's adaptation decision recorded, zero unresolved items from its Not-accepted defect list. |
| **Micro-polish** | Category F + `craft-critique.md` check 10 | Radius/border/shadow/motion tokens applied consistently (`design-system.md`), plus the numeric alignment-and-uniformity scan (row/card height uniformity, overlap/clipping, drift-from-scale spot check). |
| **Final Visual QA** | The full pass, together | `visual-benchmark.md`'s three-way comparison and `craft-critique.md` checks 1-10, run once everything above already holds individually — confirming the screen passes *as a whole*, not just check-by-check in isolation, then closed by the question below. |

### The closing question
Every Final Visual QA pass ends by answering, explicitly and in writing —
not silently assumed "no" because every step above already passed:

> **Does this interface look intentionally designed for this product, or
> could the same screen have been generated for any unrelated SaaS
> product?**

This is not a restatement of check 6 (Specificity test) or the anti-cliché
catalog (check 8) — it's the summary judgment those checks exist to answer,
asked once more at the end because a screen can pass every individual
check above and still read as generic in aggregate (a row of correctly-
aligned, correctly-sized, correctly-typed KPI cards is still a generic
template if nothing about it reflects *this* product's actual domain). If
the honest answer is that the screen reads as generic:
1. **Identify why** — cite the specific check(s) from checks 6/8 or the
   pipeline steps above that the generic read traces back to; "it just
   feels generic" is not an answer, a named cause is.
2. **Modify the visual direction** — the fix belongs at whichever level
   the cause actually lives: a token/component-level fix if it's a
   surface tell (an anti-cliché catalog item), or a `product-builder/ui/
   design-direction.md` revision if the direction itself was generic to
   begin with (routed to `agents/design-setup-specialist.md` in that
   case, not patched locally).
3. **Regenerate/refine** — per `visual-benchmark.md`'s existing mandatory
   refinement cycle (steps 1-2) — this is that same loop, not a separate
   mechanism.
4. **Re-evaluate** — re-ask the closing question against the refined
   screen; a second generic verdict routes the same way, it does not get
   waved through on a second pass.

A modern-looking treatment never answers this question by itself — per
`visual-trends.md`'s Trend Adoption Gate, every surface choice already
needs a stated contrast/legibility/register-fit reason, and this question
checks whether that reasoning actually produced something specific to
*this* product rather than a technically-compliant but generic result.

**Not accepted at any step, regardless of how minor it looks in isolation:**
approximate alignment, inconsistent spacing, arbitrary margins, arbitrary
component dimensions, visually misaligned icons, inconsistent typography,
inconsistent card heights, uneven grids, accidental whitespace, overlapping
elements, clipped content, broken responsive layouts. Each is a Minor
finding at smallest (per `config/output-contract.md`'s severity vocabulary)
— never waved through as "close enough" — and a screen with any of these
unresolved has not cleared this pipeline, regardless of how the screen
reads at a glance. The default posture for every step above is to actively
look for these defects, not to assume the first generated layout already
avoided them.

#### Text overflow — a first-class, explicitly measured defect
"Clipped content" above is not sufficient coverage on its own — text
overflow is common enough, and easy enough to miss by reading source
rather than observing the rendered result, that it gets its own explicit
sub-list. Each of these is the *same* underlying defect (rendered content
larger than the box holding it) wearing a different surface, and each is
checked for by name, not assumed covered by a general "looks fine" read:

- Text overflowing a fixed-width or fixed-height container.
- Clipped text (cut off mid-character/mid-word with no visual
  indication it was truncated).
- Horizontal overflow (content wider than its container, forcing an
  unintended scrollbar or silently escaping the container's edge).
- Vertical overflow (content taller than its container).
- Content escaping its container entirely (overlapping a neighboring
  element rather than staying clipped within its own bounds).
- Ellipsis failures — an ellipsis (`text-overflow: ellipsis` or
  equivalent) applied to a container that doesn't actually have the
  `overflow`/`white-space` properties needed for it to render, so the
  text clips raw instead.
- Overflowing buttons, badges, pills, chips, or table cells
  specifically — these are named separately from the general case
  because their small, fixed dimensions make them the most common place
  a slightly-longer-than-expected real value (a longer status label, a
  longer localized string, a wider number) breaks first.

**This is measured from the actual rendered result, never inferred by
reading the HTML/CSS and judging whether it "looks like it would fit."**
Wherever `scripts/capture-render.py` is available (see that script's and
`ui-engine/visual-benchmark.md`'s Render-and-measure evidence section),
`scripts/validate-rendered-layout.py`'s overflow check is the authority
here: a real `scrollWidth`/`scrollHeight` vs. `clientWidth`/`clientHeight`
comparison against the live DOM, at every required breakpoint and theme —
not a visual estimate. A Blocker-severity finding from that script is this
sub-list's own finding, carried into the gap analysis as a **Rendered-
layout defect** (`visual-benchmark.md`'s gap-type table), not a separate,
redundant check. Where rendering isn't available in the current
environment, this sub-list is still checked qualitatively (does any
string plausibly exceed its container at realistic content length/
localization, per `craft-critique.md`'s content-realism discipline) and
the absence of rendering evidence is disclosed, not silently treated as
"passed."

## Reporting shape
Every finding uses the same **Observation → Problem → Fix** triad
`craft-critique.md` already established, with a pass/minor/major rating per
category, mapped onto `config/output-contract.md`'s Blocker/Major/Minor/Note
severity vocabulary — one reporting convention across every UI-quality
check in the engine, never a competing scale.

## Explicitly not here
- The numeric composition-craft checks (hierarchy ratio, deletion test,
  anti-cliché catalog) → `ui-engine/craft-critique.md` (cited throughout,
  not restated).
- Comparing the audited screen against the reference/direction to produce a
  gap analysis → `ui-engine/visual-benchmark.md`.
- The 22 named design principles this framework's categories draw on →
  `ui-engine/ui-design-principles.md`.
- Product-level validation against user needs (task completion, business-
  rule correctness) → `methodology/test.md`.
