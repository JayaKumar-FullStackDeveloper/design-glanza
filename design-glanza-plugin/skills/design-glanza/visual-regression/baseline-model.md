# Baseline Model

## Responsibility
What a baseline snapshot actually captures, and — since Design-Glanza
reasons over structured artifacts, not pixels — why a **structured,
addressable snapshot** is the right representation of "visual structure,"
not an image.

## Why structure, not pixels
Design-Glanza has no screenshot/rendering capability of its own; every
visual fact already exists as structured data by the time a screen is
generated — a region map (`templates/screen-architecture.md`), a
component list with registry bases (`component-registry/*`,
`templates/component-spec.md`), and the token paths each component
actually resolves to (`design-tokens/*`). A baseline captures exactly
these facts, addressably, so two snapshots can be **diffed field by
field** — a structural diff that's exact and reproducible, where a
pixel-diff would be approximate and require capability this system
doesn't have.

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
baselines instead of tokens.

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
