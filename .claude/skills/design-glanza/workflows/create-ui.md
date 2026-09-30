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
Matches `workflows/execute-product-builder.md`'s actions 28-32 (Order
column — shifted from 27-31 when v1.0.11's new spec-level UX
scenario-testing action was inserted immediately before this range; before
that, 25-29 after v1.0.10's restructured Design Research actions (3 rows
replacing 1), 24-27 (extended by one for v1.0.9's mandatory Visual
Benchmark & Audit Cycle action) after v1.0.9's single folded-in Design
Research action, and originally 19-22 before Design Setup's actions were
inserted):

1. Establish/extend the token set and component inventory
   (`ui-engine/design-system.md`, `component-system.md`) →
   `product-builder/ui/design-system.md`, `product-builder/ui/components.md`,
   and their machine-readable twin `product-builder/ui/design-tokens.json`
   (`design-tokens/*`, Rule 23) — run `scripts/validate-tokens.py` before
   proceeding to step 2. Every component checks `component-registry/*`
   first (Rule 24) — instantiate a registry entry/composition pattern with
   a cited Registry base, or log a reasoned "no registry match" before
   specifying anything new.
2. Select the visual register (`visual-trends.md`, informed by
   `product-types/*.md`, Empathize findings, and Design Setup's approved
   `ui/design-direction.md` — chosen for fit, never fashion, per Rule 11).
3. Apply typography, color, and layout (`typography.md`, `color-system.md`,
   `layout-system.md`) following `visual-hierarchy.md`'s emphasis rules →
   `product-builder/ui/ui-rules.md`.
4. Apply responsive reflow (`responsive-system.md`) per composition pattern.
5. Produce final per-screen visuals (`templates/screen-specification.md`'s
   visual fields).
6. Re-check for drift and run the perceptual accessibility pass, including
   `scripts/validate-tokens.py` against the now-complete screen set (Rule
   23) — every flagged raw value mapped to a token or logged as a system
   gap before proceeding.
7. **Run the mandatory visual-benchmark-and-audit cycle** (Rule 20): where
   the screen already has a baseline, diff current vs. baseline first
   (`scripts/validate-visual-regression.py`, Rule 25) and resolve every
   Critical/High/Medium finding; then audit every produced screen against
   `ui-engine/ui-audit-framework.md`'s 11 A–K categories, run `ui-engine/
   visual-benchmark.md`'s three-way Reference/Design-Direction/
   Generated-UI comparison, classify any gap found, apply the refinement,
   and re-check — recorded in `templates/visual-gap-analysis.md` for
   every screen, even one with no gaps found. Once a screen's Final
   status is `pass`, capture/update its `visual-regression/*` baseline.
   The first generated pass is never treated as final; skip this step for
   no screen.

## Gate
Must pass `config/quality-gates.md`'s **B6 (Design System)** gate, **B18
(Token Inheritance Integrity)**, **B19 (Component Registry
Conformance)**, **B20 (Visual Regression Integrity)**'s structural
checkpoint, the perceptual half of **B8 (Accessibility)** (4.5:1 / 3:1
contrast, no color-only encoding), **B9 (Responsive Behavior)**, **B15
(Visual Benchmark & Audit Cycle Completeness)**, **B16
(Research-to-Design Traceability)**'s decision/pattern stage, and **B17
(UX Scenario Coverage)**'s spec-level checkpoint (already passed entering
this workflow, carried forward) — together operationalizing the
Prototype → Implement phase gate — before hand-off to `build-product.md`.

## Explicitly not here
- Any UI reasoning technique itself → the relevant `ui-engine/*.md` file.
- The UX structure being visualized → `create-ux.md`.
- Turning the visual spec into working implementation → `build-product.md`.
- The machine-readable token structure, semantic naming, theming, and
  violation detection → `design-tokens/*`.
- The pre-populated component/composition-pattern library and its
  registry-first enforcement → `component-registry/*`.
- Baseline capture/diffing across passes → `visual-regression/*`.
- The agents' own scope boundaries → `agents/design-system-expert.md`,
  `ui-designer.md`, `accessibility-expert.md`.
