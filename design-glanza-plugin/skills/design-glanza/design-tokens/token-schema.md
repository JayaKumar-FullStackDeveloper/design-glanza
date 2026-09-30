# Token Schema

## Responsibility
The canonical, machine-readable structure all 14 token categories resolve
into — one dot-addressable path per token (e.g. `color.semantic.primary`,
`spacing.24`, `radius.md`), so a component spec or generated code can
reference a token by path instead of a raw value. Every value behind every
path below is owned and defined elsewhere; this file only fixes the shape.

## The 14 categories, each mapped to its owning scale

| Category | Path prefix | Values owned by |
|---|---|---|
| Colors | `color.*` | `ui-engine/color-system.md` (ramps, semantic triplets); names reconciled in `semantic-tokens.md` |
| Typography (family/pairing) | `typography.family.*` | `ui-engine/typography.md`'s Font pairing rule |
| Font sizes | `typography.size.*` | `ui-engine/typography.md`'s type scale (`caption`…`display`) |
| Font weights | `typography.weight.*` | `ui-engine/typography.md`'s type scale (400/500/600/700) |
| Line heights | `typography.lineHeight.*` | `ui-engine/typography.md`'s type scale |
| Letter spacing | `typography.letterSpacing.*` | `ui-engine/typography.md`'s letter-spacing (tracking) scale |
| Spacing | `spacing.*` | `ui-engine/layout-system.md`'s spacing scale (4 8 12 16 24 32 48 64 96) |
| Grid | `grid.*` | `ui-engine/layout-system.md`'s grid definition (columns/gutter/margin) |
| Border radius | `radius.*` | `ui-engine/design-system.md`'s radius scale |
| Borders (width) | `border.width.*` | `ui-engine/design-system.md`'s border-width scale |
| Shadows/elevation | `elevation.*` | `ui-engine/design-system.md`'s elevation scale |
| Component dimensions | `sizing.*` | `ui-engine/design-system.md`'s sizing scale |
| Breakpoints | `breakpoint.*` | `ui-engine/responsive-system.md`'s breakpoint set |
| Motion | `motion.*` | `ui-engine/design-system.md`'s motion tokens |
| Z-index/layers | `zIndex.*` | `ui-engine/design-system.md`'s z-index scale |

## Path convention
`<category>.<subcategory?>.<token-name>` — lowercase, dot-separated,
matching `design-tokens.schema.json`'s object nesting exactly (a path is
just the JSON key sequence to reach that value). A token's *name* segment
matches its existing `ui-engine/*` token name wherever one already exists
(e.g. `radius.md` for the existing `radius-md` token, `motion.base` for
`motion-base`) — this schema renames the *separator* (dash to dot-nesting,
for machine addressability), it does not rename the tokens themselves.

## Value shape
Every leaf token is an object, not a bare value, so metadata travels with
it:

```json
{
  "value": "8px",
  "themeable": false,
  "description": "Cards, panels, dropdowns"
}
```

`themeable: true` marks a token whose `value` is instead a
`{ "light": ..., "dark": ... }` pair — see `theming.md`. Non-color families
are theme-invariant by default per `design-system.md`'s existing Theming
rule ("every non-color token family... is theme-invariant unless a
specific theme genuinely needs a different value") — `themeable` is
`false` by default and only set `true` where that stated exception
applies (e.g. an elevation shadow needing a different value against a dark
background).

## Consuming a token
A component spec (`templates/component-spec.md`) or generated code
references a token by its path, never by re-typing its raw value — the
same discipline `design-system.md`'s Consistency rule already states
("every component and screen uses it"), now checkable because the path is
addressable. `token-audit.md` defines what happens when a raw value
appears instead.

## Explicitly not here
- Any category's actual values → the owning `ui-engine/*` file (table
  above).
- The semantic color-token names → `semantic-tokens.md`.
- The theming data shape in full → `theming.md`.
- Which paths a product may override vs. which stay closed →
  `token-inheritance.md`.
- The JSON Schema itself → `design-tokens.schema.json`.
