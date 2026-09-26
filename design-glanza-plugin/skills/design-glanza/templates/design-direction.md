# Template: Design Direction

## Purpose
The complete record of the Design Setup phase's output — the product's
approved visual and interaction direction, established once, before
Prototype's UI pass, and cited from that point forward by every UI-facing
agent instead of each one improvising a direction independently.

## Required inputs
- `design-reference-engine/reference-analysis.md`'s extracted patterns, if
  any references were provided.
- `design-reference-engine/design-questionnaire.md`'s answers.
- `design-reference-engine/reference-selection.md`'s classified mode
  (Reference-Driven / Guideline-Driven / Custom Design / Default
  Design-Glanza) and, for Default mode, the selected `design-samples/`
  entry.
- Product Architect's confirmed domain classification (for Default-mode
  sample selection and for citing the applicable `product-types/*.md`
  pack's own UI-pattern conventions).

## Output structure
- **Header** — per `config/output-contract.md`.
- **Design objective** — one or two sentences: what this direction is
  trying to achieve for this specific product and audience, not a generic
  design-philosophy statement.
- **Reference classification** — the mode from `reference-selection.md`,
  stated with its rationale and evidence (which references/guidelines/
  answers drove it), plus per-surface splits if more than one mode applies
  across different parts of the product.
- **Visual style** — design style, brand personality, visual density, level
  of visual expression.
- **Design principles** — 3–5 stated principles this product's design
  answers to (not a restatement of Design-Glanza's own general principles —
  specific to this product's direction).
- **Reference analysis** — per reference provided: what it is, what was
  extracted from it, and its confidence tag (Explicit/Inferred/Assumed),
  per `reference-analysis.md`. Empty/not-applicable if no references were
  provided (Custom Design or Default mode).
- **Design inspiration** — the named starting point (a cited reference, a
  cited guideline, or the selected `design-samples/` entry) this direction
  builds from.
- **Layout system** — grid preference, container behavior, spacing
  density, card usage, section structure, nav-placement preference,
  desktop/mobile priority.
- **Typography** — font preference, hierarchy expectations, heading/body
  style, numeric/data typography needs.
- **Color system** — primary/secondary/accent/background/surface/semantic
  colors, dark/light theme requirement, stated contrast requirements.
- **Spacing** — base unit and density preference (feeds
  `ui-engine/layout-system.md`'s scale, doesn't redefine it).
- **Grid** — column count/gutter preference if stated, otherwise
  not-applicable (defers to `layout-system.md`'s default).
- **Radius** — preference along `ui-engine/design-system.md`'s closed
  radius scale (not a new value outside it).
- **Elevation** — preference along the closed elevation scale.
- **Iconography** — stroke/fill convention preference, icon-library
  preference if stated.
- **Components** — direction/expectations per component category (buttons,
  inputs, cards, tables, tabs, dropdowns, modals, drawers, toasts, badges,
  navigation, charts, forms) — direction only; full specs are
  `templates/component-spec.md`'s job later.
- **Interaction patterns** — hover/selection/loading behavior expectations,
  transition expectations, modal-vs-drawer preference, inline-editing and
  confirmation-pattern expectations, drag/drop expectations.
- **Responsive rules** — desktop/tablet/mobile priority, breakpoint
  expectations, responsive nav/table/form expectations.
- **Accessibility rules** — contrast/keyboard/focus/screen-reader/
  touch-target expectations beyond the stated baseline
  (`ux-engine/accessibility.md`'s baseline still applies regardless; this
  section only records anything *additional* this direction commits to).
- **Motion guidelines** — any stated preference for motion intensity/
  restraint, reconciled against — never overriding —
  `ux-engine/interaction-design.md`'s Motion and animation section and
  `ui-engine/design-system.md`'s closed 3-token motion scale.
- **Do / Don't rules** — concrete, falsifiable rules (per
  `design-direction.md`'s guidance on what makes one useful), not
  restatements of the Visual style section in imperative mood.
- **Reference assets** — file names/links/paths to every reference actually
  used, so a later reviewer can go back to the source.
- **Design-system decisions** — the explicit hand-off list: which of the
  above are binding constraints `agents/design-system-expert.md` must
  satisfy when establishing tokens, vs. which are soft preferences that
  yield to a genuine accessibility/technical constraint if they conflict.
- **Approval status** — confirmed (with date/context) or waived (with the
  stated reason), per Step 5.

## Quality criteria
- Checked against `config/quality-gates.md`'s **B13 (Design Direction
  Completeness)** gate — every field above filled or explicitly marked
  not-applicable with a reason; 0 fields silently blank.
- The reference classification names its evidence, not just its label — a
  classification with no stated rationale fails this template's own bar the
  same way an unstated domain classification would fail
  `domain-classifier.md`'s.
- Every Do/Don't rule is falsifiable against a finished screen — a rule
  that can't be checked against an actual screen isn't concrete enough for
  this section.
- Approval status is either a real confirmation or a stated waiver reason —
  never blank, never fabricated.

## Example structure
_Illustrative, domain-neutral — not real product content._

```
Design objective: A calm, high-trust surface for reviewing and approving
financial transactions; the direction favors legibility and restraint over
visual expression, since the primary user is scanning dense tabular data
under time pressure.

Reference classification: Guideline-Driven — the company's existing brand
guideline PDF specifies primary color, logo usage, and a mandated font
family; no product screenshots or Figma references were provided.

Visual style: Enterprise, low visual density variation, minimal ornament.
Design principles: (1) legibility over personality, (2) status is always
color+icon, never color alone, (3) no screen has more than one primary CTA.

Layout system: Sidebar navigation (>5 top-level sections, per
navigation-system.md item 2's threshold), comfortable-to-compact density
depending on screen type.
...
Do / Don't:
  Do: use the danger-semantic triplet for any destructive/blocking status.
  Don't: introduce a second accent color beyond the one named in the brand
  guideline, even for a single feature — flag the need back to Design
  Setup instead of improvising one.

Approval status: Confirmed 2026-09-30 — user reviewed the summary and
approved without changes.
```

## Traceability fields
Cited by `agents/ui-designer.md` (visual register/layout/typography/color
application) and `agents/design-system-expert.md` (token establishment) as
a mandatory input from Prototype's UI pass onward. A component or screen
decision that departs from a stated field here without a recorded reason is
a drift finding, routed the same way `agents/design-system-expert.md`
already routes token/component drift.

## Explicitly not here
- How references are analyzed and questions are asked → `design-reference-
  engine/{reference-analysis,design-questionnaire}.md`.
- How the four-way mode is decided → `design-reference-engine/
  reference-selection.md`.
- The approval-gate procedure itself → `design-reference-engine/
  design-direction.md`.
- The actual token values/component specs this direction constrains →
  `templates/design-system.md`, `templates/component-spec.md`.
