# Baseline Model

## Responsibility
What a baseline snapshot actually captures, and — since Design-Glanza
reasons over structured artifacts, not pixels — why a **structured,
addressable snapshot** is the right representation of "visual structure,"
not an image.

## Why structure, not pixels (the primary baseline layer)
Every visual fact already exists as structured data by the time a screen
is generated — a region map (`templates/screen-architecture.md`), a
component list with registry bases (`component-registry/*`,
`templates/component-spec.md`), and the token paths each component
actually resolves to (`design-tokens/*`). A baseline captures exactly
these facts, addressably, so two snapshots can be **diffed field by
field** — a structural diff that's exact and reproducible, which is why
this stays the primary, always-on baseline mechanism: it requires no
extra capability, degrades to nothing when unavailable (there is nothing
to degrade), and distinguishes a legitimate token-scale/rebrand change
from an accidental drift in a way a pixel-diff alone cannot (see
`diff-detection.md`). This primary layer is unchanged by the optional
second layer below — nothing about it is replaced, weakened, or made
conditional on rendering being available.

## Optional second layer: rendered visual baseline
Where rendering is available (`scripts/capture-render.py` — see
`ui-engine/visual-benchmark.md`'s Render-and-measure evidence section),
a **second, complementary** baseline layer is also captured per
`SCREEN-NNN`, in addition to the structural baseline above, never
instead of it:

- **Full-page and viewport screenshots**, per breakpoint
  (desktop/tablet/mobile) and theme (light/dark).
- **The DOM-geometry manifest** `capture-render.py` produces alongside
  each screenshot (every element's real bounding box, scroll-vs-client
  dimensions, computed overflow) — the same manifest
  `scripts/validate-rendered-layout.py` analyzes for the current pass.
- **Component-level snapshots** where practical — the same sibling-set
  grouping `validate-rendered-layout.py` uses (navigation, header, KPI
  cards, forms, buttons, filters, tables, charts, badges, alerts, modals,
  drawers, empty states, loading states) cropped from the full-page
  screenshot, so a later diff can localize a drift to one component
  region rather than only "something changed on this screen."

This layer exists because the structural baseline, by design, cannot
catch a drift that doesn't change any structural field (e.g. a spacing
*value* that drifted within the same token slot due to a cascade bug, or
a rendering-engine difference) — exactly the class of defect this
version's rendering capability was built to catch in the first place. **Do
not make pixels the only regression mechanism:** the rendered layer is
additional corroborating evidence, consulted alongside the structural
diff, not a replacement path that could let a structural regression pass
because "the screenshot still looked the same," nor a path that invents a
pixel-tolerance scheme of its own — a meaningful difference here is
reported as a **Rendered-layout defect** or routed through
`validate-rendered-layout.py`'s own measurement, the same as any other
rendered-evidence finding in this version, never a separate pixel-delta
severity scale.

Storage for this layer sits alongside the structural baseline (below),
under its own `render-baseline/` subfolder so the two never overwrite
each other and a tool reading only the structural JSON is unaffected by
whether the rendered layer exists for a given screen. Wherever rendering
isn't available in the current environment, this second layer is simply
absent — the structural baseline alone still satisfies **B20** in full,
exactly as it always has.

## What one baseline snapshot captures, per `SCREEN-NNN`
- **Regions** — the region map's structure (names, order) from
  `screen-architecture.md`.
- **Components per region** — each `COMPONENT-NNN`, its
  `component-registry/*` Registry base, and its size/emphasis variant.
- **Token paths used** — the specific `design-tokens/token-schema.md`
  paths each component/region resolves to (spacing, radius, color,
  typography role) — not the raw values themselves, which is exactly what
  makes a later token-scale change (e.g. a rebrand) distinguishable from
  an accidental drift (see `diff-detection.md`).
- **Design Direction summary** — register and density in effect
  (`product-builder/ui/design-direction.md`), since a later legitimate
  register change explains an otherwise-flagged diff.
- **Breakpoint behavior** — which reflow technique
  (`ui-engine/responsive-system.md`) applies at each breakpoint for this
  screen's composition pattern.
- **Capture metadata** — the pass/iteration number and date this snapshot
  was taken, and which `templates/visual-gap-analysis.md` instance
  confirmed the screen clean at that point (the baseline is only ever
  captured from a screen that has already passed **B15**, never from an
  unreviewed draft).
- **Figma provenance (where applicable)** — where this screen's Design
  Direction cited a `figma-context.json` entry
  (`design-reference-engine/figma-context-consumption.md`), the baseline
  references that same entry, so a later Iterate pass re-diffing against
  this baseline can also re-check Figma-spec conformance
  (`ui-engine/visual-benchmark.md`'s Level B), not only its own prior
  render. Folds into this file's existing Design Direction summary field
  above — not a new field category, not a 10th `diff-detection.md`
  category.

## What it deliberately does not capture
- Raw pixel values, images, or rendered screenshots — not this system's
  representation (see above).
- Content/copy text itself — a copy change is `ux-writing.md`'s concern,
  not a visual regression, unless it changes truncation/overflow behavior
  (which shows up structurally, as a region/state change).
- Business logic or state-machine behavior — `product-intelligence/
  business-logic.md`'s and `ux-engine/state-design.md`'s concern.

## Storage
One entry per `SCREEN-NNN` in `product-builder/ui/visual-baselines.md`
(human-readable roll-up, `templates/visual-baseline.md`'s shape) plus its
machine-readable twin, one JSON file per screen under
`product-builder/ui/baselines/<SCREEN-NNN>.json` — the same
document-plus-machine-readable-twin pattern `design-tokens/*` already
established for `design-system.md`/`design-tokens.json`, applied here to
baselines instead of tokens. Where the optional rendered layer above was
also captured, its screenshots and manifests live under
`product-builder/ui/baselines/render-baseline/<SCREEN-NNN>/` — present
only when rendering was available at capture time, and its absence never
invalidates the structural JSON beside it.

## When a baseline is captured or replaced
- **First capture:** immediately after a screen's `templates/
  visual-gap-analysis.md` instance reaches Final status `pass`
  (`visual-benchmark.md`'s mandatory refinement cycle) — never from an
  unconfirmed draft.
- **Replaced:** only via an explicit Baseline Update
  (`baseline-updates.md`) — never silently overwritten by a later pass
  just because that pass also finished.

## Explicitly not here
- Comparing two snapshots and classifying the differences →
  `diff-detection.md`.
- The tolerance model → `tolerance-thresholds.md`.
- The explicit update mechanism → `baseline-updates.md`.
- The document/JSON field shapes → `templates/{visual-baseline}.md`.
- The rendering/capture mechanism itself → `scripts/capture-render.py`;
  the geometric analysis run against a capture (this pass or a stored
  baseline alike) → `scripts/validate-rendered-layout.py`.
