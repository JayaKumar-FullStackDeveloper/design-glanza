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

### H. Interaction
Every applicable state from the mandatory set is actually designed for this
component/screen — hover, focus, active, disabled, loading, success, error,
empty, and, where relevant, a confirmation step — with real, observable
feedback for each. **Checked by:** `ux-engine/state-design.md`'s 13
mandatory states, `ux-engine/interaction-design.md`'s Action-feedback rules
and Undo/confirmation matrix. Zero blank cells, per B7.

### I. Accessibility
Contrast, full keyboard operability, visible focus indication, correct
semantic/ARIA roles and labels, touch-target sizing. **Checked by:**
`ux-engine/accessibility.md`, `ui-engine/color-system.md`'s contrast rule,
B8.

### J. Responsive Design
Desktop, tablet, and mobile all have a defined reflow rule; navigation
adapts per `ux-engine/navigation-system.md`'s responsive guidance; tables
and forms have a stated collapse/reflow behavior; content never silently
overflows; density adjusts appropriately per breakpoint. **Checked by:**
`ui-engine/responsive-system.md`, B9.

### K. Domain Conventions
Does the screen follow the established patterns for *this specific
domain* — the matched `product-types/<domain>.md` pack's UI-pattern point,
and any loaded `product-types/domain-standards/` entry (Rule 17)? A
healthcare screen that reads like a generic admin panel, or an ERP screen
with consumer-app visual flourish, fails this category even if every other
category passes — domain fit is checked as its own dimension, not assumed
from passing the others.

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
