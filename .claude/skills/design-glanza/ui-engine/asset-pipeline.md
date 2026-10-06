# Asset Pipeline

## Responsibility
Concrete generation/processing technique for the non-photographic assets
every built product needs — favicon/app-icon packages, resized/optimized
images, OG social-share cards, and custom SVG icon sets — consumed by
`workflows/build-product.md`'s asset step. Distinct from
`ui-engine/visual-asset-generation.md`: that file owns *photographic/
illustrative* imagery generation (the dual-path native+API method); this
file owns mechanical processing and small-vector-graphics generation,
which needs no generative model at all.

## Favicon / app-icon package
Every product that ships a deployable `output/` gets a complete package,
never a single favicon.ico left over from a framework default:
- `favicon.svg` (vector, modern browsers), `favicon.ico` (16+32px,
  legacy), `apple-touch-icon.png` (180×180, **solid background** — a
  transparent background renders as a black square on iOS, this is not
  optional), `icon-192.png` / `icon-512.png` (Android/PWA), and a web
  manifest (`name`, `short_name`, `icons`, `theme_color`, `background_color`).
- Source: extract the icon element from an existing logo when one exists
  (center in a 32×32 viewBox, simplify for small-size legibility); a
  monogram (bold-weight initials, regular weight disappears at 16×16) or
  a branded shape (circle/rounded-square/shield, chosen per the product's
  `design-direction.md` register) when no logo icon exists. The primary
  color comes from the approved palette (`color-system.md`), never an
  arbitrary placeholder blue.
- **Test at 16×16 before calling it done** — if the mark isn't legible at
  that size, simplify it further; a product never ships a CMS/framework
  default favicon.

## Image resize/optimize/OG-card pipeline
Applied to every raster asset Implement produces or receives (a supplied
photo, a generated illustration from `visual-asset-generation.md`):
- **Format selection**: WebP for photos/hero imagery (best compression,
  wide support); PNG for anything needing transparency (logos, icons);
  JPG only as a last-resort fallback for legacy support.
- **Resize**: preserve aspect ratio when only one dimension is given;
  high-quality resampling (never nearest-neighbor) for any downscale.
- **Trim**: auto-crop surrounding whitespace from a supplied logo/icon via
  its alpha bounding box before using it anywhere sized tightly (a
  favicon source, an icon slot).
- **OG card** (1200×630): composite the product's name/tagline over a
  background (brand color or a generated hero crop) with a readability
  overlay where text sits on an image — this is the image
  `seo-local-business`'s generalized meta-tag technique
  (`product-types/landing-page.md`) references as `og:image`, never left
  as a placeholder gray box.
- **Budget awareness**: this pipeline is itself part of what
  `ui-audit-framework.md`'s performance-adjacent checks and the Preview &
  Run performance budget (`workflows/preview-run.md` step 7a) evaluate —
  an unoptimized multi-megabyte hero image is a defect this pipeline
  exists to prevent, not a separate finding to fix later.

## Bundled icon packages — check first
Before reaching for a product's own stack library or building anything
custom, check `icon-packages/` (sibling to this file) — Design-Glanza ships
two complete, permissively-licensed sets directly: **Lucide** (2130 line
icons, the default) and **Heroicons** (324 icons × outline/solid/mini
variants, for a filled-icon register or an outline/solid state pair). See
`icon-packages/README.md` for the full picking guide, each package's
`index.json` for a fast name lookup, and `icon-packages/preview.html` for
visual browsing. Both already use `currentColor` exclusively — no
post-processing needed to satisfy `component-system.md`'s color-inheritance
rule. This is the first thing to check, not an afterthought beside the
product's own stack library — most icon needs across every domain
Design-Glanza covers are already in one of these two sets.

## Custom SVG icon sets
Reached only when `component-system.md`'s Iconography section's own
inventory has no fitting icon, the bundled `icon-packages/` (above) has
no fitting icon either, **and** no icon library the product's stack
already uses (beyond the two bundled here) covers the need — a custom set
is a deliberate, consistency-engineered deliverable, not a default. When
warranted:
- **One shared style spec, enforced on every icon**: identical `viewBox`,
  identical root `stroke-width`/`stroke-linecap`/`stroke-linejoin` across
  the whole set (pick one of Clean/Sharp/Soft/Minimal/Bold per the
  product's register, matching `visual-trends.md`'s selection, not
  per-icon taste), `currentColor` only (never a hardcoded `fill`/`stroke`
  hex — `component-system.md`'s color-inheritance rule already requires
  this), no root-level transform, no `id`/`class` attributes, coordinates
  snapped to a half-pixel grid (max 2 decimal places).
- **Optical corrections**, not just mechanical consistency: a curved-path
  icon (phone, globe) reads thinner than a straight-edged one at the same
  stroke width — compensate with slightly larger paths, not a different
  stroke weight; pointed shapes (arrows, chevrons) overshoot ~0.5px past
  where a square edge would stop, or they read smaller than their
  siblings; a visually simple icon (a single chevron) needs to be drawn
  slightly larger/more substantial than a complex one (a gear) so neither
  reads lighter or heavier than the set as a whole.
- **Deliverable**: one `.svg` file per icon plus a self-contained preview
  HTML (every icon inlined, shown at native size and 2×, against both a
  light and dark section) so visual consistency is actually checkable
  before the set is handed off — the same "don't ship unverified" posture
  `visual-benchmark.md` already requires of screens, applied here to an
  icon set as its own reviewable artifact.

## Explicitly not here
- Photographic/illustrative image generation (native + API dual-path,
  provenance, QA) → `ui-engine/visual-asset-generation.md`.
- Icon semantics, sizing scale, color-inheritance rule, interactive vs.
  decorative accessibility treatment → `ui-engine/component-system.md`'s
  Iconography section (this file implements the consistency mechanics
  that section's rules presume exist).
- Meta-tag/structured-data/sitemap technique that consumes the OG card →
  `product-types/landing-page.md`.
- Where this runs in the pipeline → `workflows/build-product.md`.
