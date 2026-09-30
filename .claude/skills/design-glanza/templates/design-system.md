# Template: Design System (Deliverable)

## Purpose
The one canonical reference for a product's visual consistency — the
assembled token set, component inventory, and usage guidelines every screen
and component draws from. Reusable across every domain: the token
*categories* and their default scales come from the domain-agnostic
`ui-engine/*` files; only a chosen register (`ui-engine/visual-trends.md`)
and brand primary color vary per product, never the underlying structure.

## Required inputs
- `ui-engine/design-system.md`'s token taxonomy (radius, elevation, motion,
  icon size, border-width, sizing, z-index).
- `ui-engine/typography.md`'s type scale, `color-system.md`'s palette
  technique, `layout-system.md`'s spacing scale.
- `ui-engine/visual-trends.md`'s register selection for this product.
- `design-tokens/*` — the machine-readable structure this document's
  values are also expressed as, in `ui/design-tokens.json`
  (Rule 23, `config/quality-gates.md`'s **B6**/**B18**).

## Output structure
- **Header** — per `config/output-contract.md`.
- **Token tables** — spacing, radius, elevation, motion, icon size,
  border-width, sizing, z-index (values, not the rules that produced them
  — rules live in their owning `ui-engine/*` file).
- **Type scale** — from `typography.md`.
- **Color palette + semantic mapping** — from `color-system.md`, with
  contrast compliance noted per pairing.
- **Component inventory** — list of components with links to
  `templates/component-spec.md` entries.
- **Theming** — light/dark token remapping via the semantic alias layer.
- **Usage guidelines** — do/don't notes for maintaining consistency.

## Quality criteria
- Every token category required by `ui-engine/design-system.md` is present
  — no missing category silently skipped.
- Every semantic color pairing states its contrast ratio and passes the
  4.5:1 / 3:1 rule (`color-system.md`) in both light and dark theme.
- The component inventory lists every component actually used anywhere in
  the product — an inventory that's stale relative to what screens actually
  reference is the exact drift `agents/design-system-expert.md` exists to
  catch.
- Checked against `config/quality-gates.md`'s **B6 — Design System** gate.

## Example structure
_The scale shapes below are the domain-agnostic engine defaults — reusable
as-is; only the brand primary hue and chosen register are product-specific._

```
Spacing scale:  4 8 12 16 24 32 48 64 96
Radius scale:   none / sm(4px) / md(8px) / lg(12px) / full
Elevation:      0 (flat) .. 4 (modal)
Motion:         fast(100ms) / base(200ms) / slow(350ms)
Border-width:   none(0) / hairline(1px) / thick(2px)
Sizing:         control-sm(32px) / control-md(40px) / control-lg(48px)
Z-index:        0 / 100 / 200 / 300 / 400 (per elevation level)
Type scale:     caption 12 / body 14 / body-lg 16 / h3 18 / h2 24 / h1 32
Semantic color: primary / secondary / surface / background / text / muted /
                success / warning / error / info, each theme-mapped
                (light/dark) per design-tokens/semantic-tokens.md
Register:       <Modern SaaS | Dense Enterprise | Consumer Playful>
                (per ui-engine/visual-trends.md, chosen for this product)
```

## Traceability fields
No enumerable ID of its own (one per product); component inventory entries
cite `COMPONENT-NNN`. This document's values are also expressed
machine-readably in `product-builder/ui/design-tokens.json`
(`design-tokens/design-tokens.schema.json`) — the two are kept in sync,
never allowed to drift apart; the JSON file is what `scripts/
validate-tokens.py` and generated component code actually consume.

## Explicitly not here
- The assembly rules/logic → `ui-engine/design-system.md`.
- Per-component detail → `templates/component-spec.md`.
- The register-selection reasoning → `ui-engine/visual-trends.md`.
- The machine-readable schema, semantic-token naming, theming structure,
  master/product inheritance, and violation-detection technique →
  `design-tokens/*`.
