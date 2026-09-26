# Template: Screen Specification

## Purpose
The full, implementation-ready detail of one screen — the final artifact
`workflows/build-product.md` builds from. Builds directly on
`screen-architecture.md`'s region map by adding real content, components,
interactions, states, responsive behavior, and accessibility notes. Reusable
across every domain: it is a composition of already-generic component and
state references, never a place to define new business logic.

## Required inputs
- `templates/screen-architecture.md`'s region map for this screen.
- `ui-engine/component-system.md`'s component inventory.
- `templates/state-matrix.md`'s row for this screen.
- `ui-engine/responsive-system.md`'s reflow rule for this screen's
  composition pattern.
- `ux-engine/accessibility.md`'s structural rules.

## Output structure
- **Header** — per `config/output-contract.md`, with the region-map
  reference.
- **Per-region content/component list** — which `COMPONENT-NNN`(s) populate
  each region, with real (not placeholder) content.
- **Per-region interaction spec** — cross-reference to the specific
  `ux-engine/interaction-design.md` / `form-design.md` rule that applies.
- **State coverage** — cross-reference to this screen's row in
  `templates/state-matrix.md`.
- **Responsive behavior** — cross-reference to `responsive-system.md`'s
  reflow rule for this screen's pattern.
- **Accessibility notes** — screen-specific focus order/ARIA notes beyond
  the system-wide rules already in `ux-engine/accessibility.md`.

## Quality criteria
- Every component cited already exists in `component-system.md`'s inventory
  — an undocumented one-off component introduced here is drift
  (`agents/design-system-expert.md`'s check).
- Every mandatory state from `state-matrix.md` is referenced, not just the
  success/happy-path state — a spec that only describes the working case is
  incomplete by definition (this is the screen-level instance of "the happy
  path is not enough," per `workflows/execute-product-builder.md`'s
  completion criteria).
- Responsive behavior and accessibility notes are present and specific, not
  boilerplate placeholders repeated unchanged from another screen.
- Jointly checked against `config/quality-gates.md`'s **B5, B6, B7, B8, B9**
  gates — this is the single most gate-dense artifact in the whole system,
  since it's where structure, system, state, accessibility, and
  responsiveness all have to hold together at once.

## Example structure
_Illustrative only — placeholders, not a real screen._

```
Region: primary content
  Components: COMPONENT-004 (data table), COMPONENT-009 (empty-state panel)
  Interaction: row click opens detail panel (per interaction-design.md
    action-feedback rule: <100ms)
  States covered: loading, empty, error, success (see state-matrix.md row
    SCREEN-011)
  Responsive: collapses to stacked cards below `tablet` breakpoint
    (responsive-system.md's data-table technique)
  Accessibility: table rows keyboard-navigable; empty state's action button
    is focus-reachable and announced
```

## Traceability fields
Cites `SCREEN-NNN` (its own identity), `COMPONENT-NNN`(s) used, and links
forward to `TEST-NNN` once `methodology/test.md` evaluates this screen.

## Explicitly not here
- The region map itself → `templates/screen-architecture.md`.
- Component anatomy/variants → `templates/component-spec.md`.
- State enumeration logic → `ux-engine/state-design.md`.
- The visual/token values applied → `ui-engine/design-system.md`.
