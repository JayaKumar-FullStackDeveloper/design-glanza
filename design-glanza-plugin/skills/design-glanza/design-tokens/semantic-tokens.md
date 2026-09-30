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

## Contrast and color-blind safety still apply unchanged
Every triplet above is still checked against `color-system.md`'s 4.5:1/3:1
contrast rule and color-blind safety rule, in both themes — this schema
adds addressability, it does not relax or duplicate that check; **B6**
still owns it.

## Explicitly not here
- Palette-construction technique (ramps, contrast, color-blind safety) →
  `ui-engine/color-system.md`.
- Non-color semantic naming (e.g. spacing/motion don't have "semantic"
  aliases the way color does) → not applicable; `token-schema.md` covers
  those categories directly by scale name.
- Light/dark value pairs for a themeable token → `theming.md`.
