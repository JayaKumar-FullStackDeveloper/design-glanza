# Semantic Tokens

## Responsibility
The canonical semantic color-token names — `primary`, `secondary`,
`surface`, `background`, `text`, `muted`, `success`, `warning`, `error`,
`info` — reconciled against `ui-engine/color-system.md`'s existing
vocabulary, which uses some of the same concepts under different spelling.
This file states the mapping explicitly so the two are never mistaken for
competing systems.

## Reconciliation against the existing vocabulary
`color-system.md` and `design-system.md` already name most of these
concepts; this schema is the first place they're assembled into one flat,
machine-readable list with fixed names:

| Schema name | Existing engine concept | Note |
|---|---|---|
| `primary` | `color-system.md`'s Primary ramp | Unchanged — same concept, same ramp |
| `secondary` | Named in `templates/design-direction.md`'s Color system field, never given ramp-construction treatment | **Formalized here** — a secondary/accent hue gets the same 9–10 step ramp technique as primary (`color-system.md`'s Palette construction), used for secondary emphasis, never competing with `primary` for the same action |
| `surface` | `design-system.md`'s Theming rule (`surface` alias) | Unchanged — a raised/contained region's fill (card, panel) |
| `background` | Implied but not separately named in `color-system.md`; listed as its own field in `templates/design-direction.md` | **Formalized here** — the page-level canvas color, distinct from `surface` (a card is a `surface` sitting on the page `background`) |
| `text` | `design-system.md`'s `text-primary`/`text-muted` aliases | Restructured as a nested token: `color.semantic.text.primary`, `color.semantic.text.muted` — same aliases, dot-path form |
| `muted` | `design-system.md`'s `text-muted` alias, generalized | `color.semantic.text.muted` for text; a `muted` variant is also valid on `background`/`surface` where a de-emphasized container is needed, same ramp-step-down technique |
| `success` | `color-system.md`'s `success` semantic | Unchanged |
| `warning` | `color-system.md`'s `warning` semantic | Unchanged |
| `error` | `color-system.md`'s `danger` semantic | **Same meaning, machine-readable name changed** — `error` is the schema's token name; `danger` remains the name used in `color-system.md`'s own prose. Never treated as two different semantics; a component citing `color.semantic.error` and prose describing "the danger triplet" are the same triplet. |
| `info` | `color-system.md`'s `info` semantic | Unchanged |

`neutral` (`color-system.md`'s fifth semantic, used for default/inactive
states) remains a semantic token in the schema
(`color.semantic.neutral.*`) even though it isn't in the user-facing list
above — dropping it would leave default/inactive states with nowhere to
resolve to, which `color-system.md`'s own semantic mapping table already
depends on.

## Structure
Every semantic token is a **triplet** exactly as `color-system.md` already
requires (foreground/background/border) — this schema does not flatten
that structure into a single color per semantic name:

```json
"color": {
  "semantic": {
    "error": {
      "foreground": { "value": {...}, "themeable": true },
      "background": { "value": {...}, "themeable": true },
      "border":     { "value": {...}, "themeable": true }
    }
  }
}
```

## Optional extension: `soft` / `onSoft`
Two additional, optional fields on any semantic entry — **not required**,
and not a fourth required triplet member; a product that never declares
`soft` is unaffected. They exist because the plain `background` field
above is designed for a larger surface (an inline alert, a toast panel)
and is not automatically safe for a visually lighter, more tinted
treatment the same semantic meaning also needs for a smaller, denser
component: a **badge, chip, status pill, delta indicator, semantic icon
container, or avatar initials/background** (`component-registry`'s Badge,
Toast, and Avatar-shaped entries). A benchmark run found exactly this
failure mode: a semantic hue that read correctly as an icon/line color on
a plain surface was reused unchanged as badge text on a lighter, tinted
background and failed WCAG contrast there — passing against one
background does not certify a color against a different one.

```json
"success": {
  "foreground": { "value": {...}, "themeable": true },
  "background": { "value": {...}, "themeable": true },
  "border":     { "value": {...}, "themeable": true },
  "soft":       { "value": {...}, "themeable": true },
  "onSoft":     { "value": {...}, "themeable": true }
}
```

- **`soft`** — the lighter/tinted background a badge, chip, pill, delta
  indicator, icon container, or avatar background actually renders on.
- **`onSoft`** — the foreground guaranteed to read against `soft`
  specifically. Where a product declares `soft` with no dedicated
  `onSoft`, the check falls back to that key's own plain `foreground` —
  which is exactly the "don't assume it's safe" case this extension exists
  to catch, so the fallback is checked, never silently skipped.

## Contrast and color-blind safety still apply unchanged
Every triplet above — and the `soft`/`onSoft` pair where declared — is
still checked against `color-system.md`'s 4.5:1/3:1 contrast rule and
color-blind safety rule, in both themes — this schema adds addressability,
it does not relax or duplicate that check; **B6**/**B8** still own it
(`scripts/validate-tokens.py`'s `_check_contrast`, pass 3 for the
`soft`/`onSoft` pairing specifically).

## Explicitly not here
- Palette-construction technique (ramps, contrast, color-blind safety) →
  `ui-engine/color-system.md`.
- Non-color semantic naming (e.g. spacing/motion don't have "semantic"
  aliases the way color does) → not applicable; `token-schema.md` covers
  those categories directly by scale name.
- Light/dark value pairs for a themeable token → `theming.md`.
