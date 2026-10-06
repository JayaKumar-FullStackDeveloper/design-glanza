# Icon Packages

## Responsibility
Two complete, bundled, permissively-licensed icon libraries a Product
Builder reaches for **before** `ui-engine/asset-pipeline.md`'s "Custom SVG
icon sets" section ever runs — most icon needs (nav, actions, status,
domain objects) are already covered by one of these, so a custom set is the
fallback, not the default. Referenced from `ui-engine/asset-pipeline.md`
and `ui-engine/component-system.md`'s Iconography section; this file is the
concrete inventory those two only point at.

## What's bundled

| Package | Version | License | Count | Style |
|---|---|---|---|---|
| [`lucide/`](lucide/) | 1.52.0 | ISC (`lucide/LICENSE`) | 2130 icons | Single style: 24×24 viewBox, `stroke="currentColor"`, `stroke-width="2"`, `stroke-linecap="round"`, `stroke-linejoin="round"`, `fill="none"` — line icons only. |
| [`heroicons/`](heroicons/) | 2.2.0 | MIT (`heroicons/LICENSE`) | 324 icons × 4 variants | `16-solid/` (16×16, filled), `20-solid/` (20×20, filled), `24-outline/` (24×24, `stroke-width="1.5"`, line), `24-solid/` (24×24, filled). |

Both already use `currentColor` exclusively (fill or stroke, per variant) —
no hardcoded hex anywhere in either set, so `component-system.md`'s
color-inheritance rule is satisfied natively, with zero post-processing.

## Picking a package
- **Default: Lucide.** Broadest coverage (2130 icons), one consistent line
  style, matches the stroke-based icon convention most of
  `design-samples/`'s reference screens and generated products already
  converge on. Use it unless one of the reasons below applies.
- **Use Heroicons when:** the product's register specifically wants a
  **filled/solid** icon treatment (Heroicons' `24-solid`/`20-solid`/
  `16-solid`) rather than line icons, or the stack is Tailwind-ecosystem
  and visual consistency with Tailwind UI/Headless UI components matters,
  or you need the exact same icon in both an outline (unselected/default)
  and solid (selected/active) state pair — Heroicons' `24-outline` /
  `24-solid` folders share icon names 1:1, making that state pair a direct
  filename swap (`heart.svg` in both folders, same name, different fill).
- **Mixing:** don't mix Lucide and Heroicons within one icon *role* on one
  screen (e.g. all sidebar nav icons must come from the same package) —
  consistency within a role matters more than which package wins; it's
  fine for different roles on the same product to use different packages
  if there's a real reason (e.g. Lucide for nav, Heroicons solid/outline
  pair for a toggle-state icon that specifically needs that pairing).

## Finding an icon
Each package has a flat `index.json` ( `lucide/index.json`,
`heroicons/index.json` ) listing every available icon name — grep/search
that before opening `preview.html`, it's faster for a one-off lookup.
`preview.html` (open directly in a browser, fully self-contained, no build
step) is for visual browsing/comparison: search-as-you-type across both
packages, filter by set/variant, click any icon to copy its relative path.

## Using an icon
Each `.svg` file is ready to use as-is: inline its contents directly into
the generated screen's HTML/JSX (don't `<img src>` a functional UI icon —
that blocks `currentColor` inheritance and per-instance sizing via CSS,
the same reasoning `asset-pipeline.md`'s custom-icon-set rules already
apply). Strip the Lucide license-comment line and any `class="lucide ..."`
/ `data-slot="icon"` attributes the source file carries if the target
stack doesn't use them — keep `viewBox`, `fill`/`stroke`, and the path
data untouched. Size via the wrapping element's `width`/`height` (or a CSS
class), color via `color`/`currentColor` on an ancestor — never edit stroke-
width/viewBox per-instance, that's what breaks a set's consistency
(`asset-pipeline.md`'s "one shared style spec" rule applies to a bundled
package exactly as it applies to a custom one).

## Attribution
Neither license requires in-UI attribution. Keep each package's `LICENSE`
file in place in this repo (already done) — that satisfies both the ISC
and MIT license conditions on redistribution. No action needed in a
generated product's own `output/`.

## Explicitly not here
- The decision procedure for when a custom icon set is warranted instead
  (neither bundled package nor the product's own stack library has the
  needed icon) → `ui-engine/asset-pipeline.md`'s "Custom SVG icon sets"
  section.
- Icon semantics, sizing scale, interactive-vs-decorative accessibility
  treatment → `ui-engine/component-system.md`'s Iconography section.
- Photographic/illustrative imagery (not an icon need at all) →
  `ui-engine/visual-asset-generation.md`.
