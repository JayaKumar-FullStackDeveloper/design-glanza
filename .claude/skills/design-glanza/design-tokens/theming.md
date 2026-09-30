# Theming

## Responsibility
Express `design-system.md`'s existing Theming rule and `color-system.md`'s
existing Dark/light theming section as one concrete **data shape**, so
"add a theme is a token remap, not a rebuild" (`design-system.md`'s own
phrase) is literally true of the JSON file, not just true in spirit.

## The shape
Any token marked `themeable: true` (`token-schema.md`) carries a
mode-keyed value instead of a bare one:

```json
{
  "value": { "light": "#1A73E8", "dark": "#8AB4F8" },
  "themeable": true
}
```

A non-themeable token (most of spacing, radius, motion, sizing, grid,
breakpoints, z-index — per `design-system.md`'s existing rule that
non-color families are theme-invariant by default) carries a bare `value`,
no mode object — never a `{ "light": X, "dark": X }` pair with identical
values standing in for "doesn't actually vary," which would just be
noise.

## "Where applicable" — theming is not mandatory
Per the master engine's existing posture (nothing in `color-system.md` or
`design-system.md` requires dark mode to exist), a product's
`design-tokens.json` may declare only a `light` mode. Where dark mode is
in scope, both modes are required for **every** themeable token — a token
with a `light` value and no `dark` value is incomplete, not "defaulting to
light," per the same zero-blank-cell discipline `templates/
state-matrix.md` already applies to states.

## What must hold across modes, unchanged from existing rules
- Every semantic triplet's contrast ratio still clears 4.5:1/3:1 **in
  both modes independently** (`color-system.md`'s Contrast compliance
  rule — already stated, not new here).
- A semantic token's *meaning* stays stable across modes (`danger`/`error`
  stays recognizably red-ish in both) — already stated in
  `color-system.md`'s Dark/light theming section.
- Elevation communicates stacking via progressively lighter surface fills
  in dark mode, not stronger shadows (`design-system.md`'s existing rule)
  — this is exactly why `elevation.*` is one of the rare non-color
  families that may legitimately be `themeable: true`.

## Resolving a themeable token at generation time
A generated screen/component always resolves to the **active mode's**
value at the point of use — never bakes in one mode's hex value directly
into generated code/markup where a token reference would do, since that
would silently break the "remap, not rebuild" property this whole
structure exists to guarantee.

## Explicitly not here
- Which specific tokens are themeable by default vs. by exception →
  `design-system.md`'s Theming rule (cited, not restated).
- The semantic names being themed → `semantic-tokens.md`.
- Detecting a token that skipped this shape (a raw value baked into
  generated output) → `token-audit.md`.
