# Design Token Intelligence Layer

## Responsibility
The **machine-readable structure** that every scale/rule already scattered
across `ui-engine/*` assembles into — one JSON file per product
(`product-builder/ui/design-tokens.json`), one canonical semantic naming
layer, one theming shape, one master↔product inheritance rule, and one
violation-detection technique. This is the elaboration of Rule 23
(`config/operating-rules.md`) and gates **B6** (sharpened) and **B18**
(`config/quality-gates.md`).

## What is genuinely new here, and what is not
`ui-engine/*` already defines nearly every scale value Design-Glanza uses.
This folder does not re-derive a single one of them — it gives them one
addressable, consumable shape, and adds the handful of pieces that
genuinely didn't exist before:

| Genuinely new | Already exists — cited, never restated |
|---|---|
| One JSON schema all 14 requested categories resolve into (`design-tokens.schema.json`) | Every scale's actual values — spacing, radius, elevation, motion, icon size, border-width, sizing, z-index → `ui-engine/design-system.md`; type scale → `typography.md`; grid → `layout-system.md`; breakpoints → `responsive-system.md` |
| The canonical semantic-token *names* (`primary`, `secondary`, `surface`, `background`, `text`, `muted`, `success`, `warning`, `error`, `info`), reconciled against the engine's existing vocabulary | The palette-construction technique and contrast rules → `ui-engine/color-system.md` |
| Theming expressed as a data shape (`{value: {light, dark}}`) rather than only a prose rule | The theming *rule* (semantic alias, remap per theme, dark-mode elevation-via-lighter-layers) → `design-system.md`, `color-system.md` |
| The Master Token Set ↔ Product Token Set inheritance/override contract | Rule 15 (Product Isolation) and Rule 16 (Extensibility) themselves — this file operationalizes them for one specific artifact type, doesn't restate them |
| `scripts/validate-tokens.py` — a real, deterministic violation detector | The *judgment* form of the same check — `agents/design-system-expert.md`'s drift review, `ui-engine/ui-audit-framework.md`'s categories C–G |

Border-width, component-dimension (sizing), and an explicit numeric
z-index scale did **not** exist anywhere before this pass — those three
were added directly to `ui-engine/design-system.md`'s own token taxonomy
(the file that already owns "token families with no other home"), not
invented fresh here. This folder only structures them once they exist.

## File map

| File | Owns |
|---|---|
| `token-schema.md` | The 14-category structure, each row citing its owning `ui-engine/*` scale |
| `semantic-tokens.md` | The canonical semantic names, reconciled against `color-system.md`'s existing vocabulary |
| `theming.md` | Light/dark as a data shape; when theming applies and when it's legitimately skipped |
| `token-inheritance.md` | Master Token Set vs. Product Token Set — what a product may override/extend vs. what stays closed, operationalizing Rule 15/16 |
| `token-audit.md` | What counts as a violation, the justified-exception mechanism (reusing `design-system.md`'s existing "logged system gap" rule, not a new one), and what `scripts/validate-tokens.py` mechanically checks vs. what still needs agent judgment |
| `design-tokens.schema.json` | The actual JSON Schema for one product's `design-tokens.json` |
| `templates/design-tokens.json` | A domain-neutral starter instance |

## Explicitly not here
- Any scale's actual values → `ui-engine/design-system.md`, `typography.md`,
  `layout-system.md`, `color-system.md`, `responsive-system.md`.
- Component anatomy/variants/states → `ui-engine/component-system.md`.
- The document (prose) form of a product's token set →
  `templates/design-system.md` (this folder is its machine-readable twin,
  kept in sync with it, never a competing document).
- Per-screen visual audit → `ui-engine/{craft-critique,ui-audit-framework}.md`.
