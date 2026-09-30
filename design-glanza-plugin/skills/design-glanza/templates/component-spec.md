# Template: Component Spec

## Purpose
The full specification of one component, satisfying
`ui-engine/component-system.md`'s 8-point analysis framework. Reusable
across every domain: a button, a data table, or a form field is specified
the same way regardless of what data it happens to display.

## Required inputs
- `ui-engine/component-system.md`'s 8-point framework and atomic-to-composite
  taxonomy.
- `component-registry/*` (Rule 24) — checked first, before any point below
  is filled from scratch: does a registry entry (or
  `composition-patterns.md` organism) already cover this component?
- `templates/design-system.md`'s tokens (for variants/sizing), addressed by
  their `design-tokens/design-tokens.schema.json` path (e.g.
  `radius.md`, `color.semantic.primary`) — every value a variant/size/state
  uses cites a token path, never a raw value (Rule 23, gate **B6**).
- `ux-engine/state-design.md`'s behavioral states this component must
  visually express.
- `ux-engine/accessibility.md`'s semantic mapping for this component's role.

## Output structure
Exactly the 8 points from `ui-engine/component-system.md`, plus identity:
- **Header** — per `config/output-contract.md`.
- **Registry base** — the `component-registry/*` entry this instantiates
  (e.g. `table`, or the `data-table` composition pattern), or an explicit,
  reasoned "no registry match — new component" (Rule 24, gate **B19**).
- **Category** — atom / molecule / organism.
- **1. Purpose** — the single job this component does.
- **2. Anatomy** — named parts.
- **3. Variants** — the closed set (emphasis, size).
- **4. States** — default/hover/focus/active/disabled/loading, per variant.
- **5. Behavior** — cross-reference to the specific
  `ux-engine/interaction-design.md` rule, not restated.
- **6. Content rules** — text conventions (labels, truncation,
  empty/zero-content fallback).
- **7. Accessibility** — semantic role, keyboard behavior (cross-reference
  `ux-engine/accessibility.md`'s mapping table).
- **8. Responsive behavior** — cross-reference to `responsive-system.md`.

## Quality criteria
- All 8 points are addressed — a spec missing even one (most often
  "content rules" or "responsive behavior") is incomplete, not "mostly
  done."
- Focus state is visually distinct from hover state — a component that
  conflates the two fails keyboard accessibility even if it looks fine with
  a mouse.
- Every variant × state combination is either specified or explicitly
  inherited from a stated base rule — none left undefined by omission.
- Checked against `config/quality-gates.md`'s **B6 — Design System** gate
  (component-level instance) and cross-checked by
  `agents/design-system-expert.md` for reuse-vs-new-variant discipline.
  Every value scanned by `scripts/validate-tokens.py` resolves to a token
  path or carries a logged Token gap entry (`design-tokens/token-audit.md`)
  — no silent raw value.
- Passes `config/quality-gates.md`'s **B19 (Component Registry
  Conformance)** — Registry base is a real entry, a stated composition, or
  an explicit, reasoned "no registry match."

## Example structure
_A generic UI atom present in virtually every product — illustrative, not
domain content._

```
Component: Button                              Category: atom
Registry base: button (component-registry/components-actions-inputs.md)
Purpose:   trigger a single action
Anatomy:   container, icon-slot (optional), label
Variants:  emphasis(primary/secondary/tertiary/destructive), size(sm/md/lg)
States:    default, hover, focus (visibly distinct from hover), active,
           disabled, loading (per variant)
Behavior:  per interaction-design.md's action-feedback table
Content:   verb-led label, sentence case, single line, ellipsis-truncated
Accessibility: role=button; accessible name matches visible label unless
           icon-only, in which case an aria-label is required
Responsive: touch target >=44x44px at mobile/tablet breakpoints
```

## Traceability fields
Owns the `COMPONENT-NNN` scheme (registered via
`product-intelligence/traceability.md`). Cited by
`templates/screen-specification.md` wherever this component is used.

## Explicitly not here
- Taxonomy/anatomy rules themselves → `ui-engine/component-system.md`.
- Which behavioral states exist and why → `ux-engine/state-design.md`.
- Token values (sizes, colors, radii) referenced by variants →
  `templates/design-system.md`.
- The pre-populated guidance a Registry base actually inherits from →
  `component-registry/*`.
