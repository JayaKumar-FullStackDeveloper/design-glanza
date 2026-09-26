# Workflow: Create UI

## Responsibility
The operational procedure for turning validated UX artifacts (from
`create-ux.md`) into the visual system and screen designs — consuming
Design Setup's approved `product-builder/ui/design-direction.md` as
mandatory input throughout (Rule 18), never re-deciding the visual
direction from scratch at this point.

## Executing agents, in sequence
1. **`agents/design-system-expert.md`** runs **first** — establishes or
   extends the token set and component inventory before any screen is
   visually realized (Rule 5, `config/operating-rules.md`: system before
   screen; reversing this order is the single most common way this workflow
   gets violated).
2. **`agents/ui-designer.md`** — applies that governed token/component set:
   register, layout, typography, color, and final screen visuals.
3. **`agents/design-system-expert.md`** again — reviews for drift
   (undocumented one-offs) once screens exist.
4. **`agents/accessibility-expert.md`** — the perceptual half (contrast,
   color-blind safety) now that color exists to check; the structural half
   already ran in `create-ux.md`.
5. **`agents/ui-designer.md`** and **`agents/design-system-expert.md`**
   again — the mandatory visual-benchmark-and-audit cycle (Rule 20), never
   skipped even for a clean first draft.

## Step order
Matches `workflows/execute-product-builder.md`'s actions 25-29 (Order
column — shifted from 24-27 when v1.0.9's new Design Research action was
inserted earlier in the table, then extended by one to include v1.0.9's
new mandatory Visual Benchmark & Audit Cycle action; originally 19-22
before Design Setup's actions were inserted):

1. Establish/extend the token set and component inventory
   (`ui-engine/design-system.md`, `component-system.md`) →
   `product-builder/ui/design-system.md`, `product-builder/ui/components.md`.
2. Select the visual register (`visual-trends.md`, informed by
   `product-types/*.md`, Empathize findings, and Design Setup's approved
   `ui/design-direction.md` — chosen for fit, never fashion, per Rule 11).
3. Apply typography, color, and layout (`typography.md`, `color-system.md`,
   `layout-system.md`) following `visual-hierarchy.md`'s emphasis rules →
   `product-builder/ui/ui-rules.md`.
4. Apply responsive reflow (`responsive-system.md`) per composition pattern.
5. Produce final per-screen visuals (`templates/screen-specification.md`'s
   visual fields).
6. Re-check for drift and run the perceptual accessibility pass.
7. **Run the mandatory visual-benchmark-and-audit cycle** (Rule 20): audit
   every produced screen against `ui-engine/ui-audit-framework.md`'s 11
   A–K categories, run `ui-engine/visual-benchmark.md`'s three-way
   Reference/Design-Direction/Generated-UI comparison, classify any gap
   found, apply the refinement, and re-check — recorded in
   `templates/visual-gap-analysis.md` for every screen, even one with no
   gaps found. The first generated pass is never treated as final; skip
   this step for no screen.

## Gate
Must pass `config/quality-gates.md`'s **B6 (Design System)** gate, the
perceptual half of **B8 (Accessibility)** (4.5:1 / 3:1 contrast, no
color-only encoding), **B9 (Responsive Behavior)**, and **B15 (Visual
Benchmark & Audit Cycle Completeness)** — together operationalizing the
Prototype → Implement phase gate — before hand-off to `build-product.md`.

## Explicitly not here
- Any UI reasoning technique itself → the relevant `ui-engine/*.md` file.
- The UX structure being visualized → `create-ux.md`.
- Turning the visual spec into working implementation → `build-product.md`.
- The agents' own scope boundaries → `agents/design-system-expert.md`,
  `ui-designer.md`, `accessibility-expert.md`.
