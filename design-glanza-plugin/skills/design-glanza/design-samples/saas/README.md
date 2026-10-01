# Design Sample: Saas

Status: **partially populated** — 7 curated reference images added
(source: user-supplied, unattributed third-party dashboard/UI shots
collected from general design-inspiration sources — treat as
Inferred-confidence visual reference, not a licensed/attributed asset).

## Reference assets
| File | What it shows |
|---|---|
| `saas-auth-gradient-hero-login.jpg` | Auth screen: split layout, gradient hero panel (brand mark + value prop) against a plain white form panel (email/password, social-login row) |
| `dashboard-saas-finance-wealthio-earnings-spending.jpg` | Finance dashboard: 3 KPI cards with icon chips, bar-chart transactions-overview panel, horizontal segmented spending-breakdown bar, card-details widget, recent-orders table with status pills |
| `dashboard-saas-banking-citibank-cards-transactions.jpg` | Banking dashboard: icon-rail sidebar, card visual + quick-transfer panel, contacts list, gradient-fill line chart with a callout/annotation bubble, recent-transactions feed with icon avatars |
| `dashboard-saas-logistics-dropify-fleet-tracking.jpg` | Operations/logistics dashboard: 3 KPI cards with small inline charts, order-detail timeline/stepper, radial speed gauge, live map panel — the closest reference match to an "operations command center" shape |
| `dashboard-saas-project-coursie-task-analytics.jpg` | Project-ops dashboard: 4 KPI cards (one bold-color hero tile among neutral ones — a deliberate emphasis pattern, not parity), bar-per-day analytics row, team-member list with status pills, donut completion gauge, promo card |
| `dashboard-saas-ecommerce-shodai-product-table.jpg` | Data-table-dense admin screen: filter bar (category/status/price/store selects), sortable table with inline status dropdown and edit/delete row actions, pagination |
| `dashboard-saas-finance-finexy-wallet-overview.jpg` | Finance dashboard: top nav with pill-shaped active tab, 4 KPI cards (2 bold-color hero tiles among neutral ones), bar chart with profit/loss legend, recent-activity table with icon avatars and status pills |

## Visual language observed across this set
- **Light, cool-neutral page background** (white or soft gray/lavender)
  with **white, low-elevation cards** — a thin border or a barely-visible
  shadow separates a card from the page, never a heavy drop shadow.
- **Differential KPI emphasis** (Coursie, Finexy): one or two KPI tiles get
  a bold, solid accent-color fill while the rest stay neutral/white — the
  same hero-weighting technique `ui-engine/visual-hierarchy.md` already
  names, independently confirmed here across two unrelated references.
- **Icon-chip badges**: a small rounded-square or circular tinted
  container holding a glyph, used consistently for KPI-card icons, nav
  items, and activity-feed entries.
- **Status pills** (colored dot/background + label) for table/activity
  status — never a color-only indicator.
- **Left sidebar navigation** (icon + label, a pill or bar-accent marking
  the active item) is the dominant pattern (5 of 7); one reference
  (Finexy) uses a top nav with pill-shaped tabs instead.
- Charts favor a **restrained single accent hue** with a light tint/gradient
  fill under a line, or flat bars — never a multi-color rainbow treatment.

## Measurable reference characteristics (new this version)
Approximate, visually-estimated ranges distilled from this set — a
starting numeric anchor for Design Setup's direction-extraction step, not
a pixel measurement taken by a script (no reference-image pixel-extraction
tool exists; `scripts/compare-reference-visual.py` compares a reference
against a *generated* screenshot, it does not itself measure a reference
in isolation). Treat every number below as **REFERENCE AS DESIGN
LANGUAGE** — the register and rhythm to work within — never **REFERENCE
AS DIRECT VISUAL TARGET**: a generated screen landing within these ranges
is not "matching the sample," and one that deliberately departs from a
range for a stated reason (a denser data-table screen, a sparser landing
page) is not a gap merely for falling outside it. Only a departure with
*no* stated design-direction reason is a gap (`visual-benchmark.md`'s
Reference mismatch gap type) — and that gap is detected from the actual
generated+reference comparison at audit time, not from a static number in
this file.

- **Approximate spacing scale** — an 8px base unit reads consistently
  across this set: ~8px (icon-to-label gaps), ~16px (card internal
  padding, inter-element gaps within a card), ~24px (gap between cards in
  a row/grid), ~32px (section-to-section vertical gaps). Consistent with
  `ui-engine/layout-system.md`'s spacing-scale discipline, not a
  competing scale.
- **Card radius** — a consistently moderate rounding, roughly in the
  12-16px range (never sharp 0px corners, never an exaggerated 24px+
  "pill-card" treatment) across every dashboard in the set.
- **Surface hierarchy** — three layers, not two: page background (the
  cool-neutral base), card surface (white, one step up), and an inset
  surface within a card (a KPI icon chip, a table header row, a
  segmented-bar track — a third, subtly distinct tone). A screen using
  only page-vs-card with no third inset tone reads flatter than this set.
- **Typography scale** — a KPI's headline number is the largest text on
  the screen by a clear margin (roughly 2-2.5x a card's own label size);
  card/section labels sit one step below body text in size but are
  distinguished more by weight and color (muted) than by size alone;
  table/list body text stays close to a single base size throughout, with
  weight (not size) marking emphasis (e.g. a table's primary column vs.
  its secondary columns).
- **Density** — comfortable-to-compact, never dense: a dashboard KPI row
  typically shows 3-4 cards, not 6+ crammed into the same width, and a
  data table keeps visible row height generous enough for a status pill
  plus label to sit without crowding.
- **Component dimensions** — KPI cards within a row share one height;
  icon chips are small and square-ish (roughly 32-40px), never dominating
  the card; status pills are compact (small horizontal padding, pill
  radius = half the pill's own height, never a sharp-cornered badge
  pretending to be a pill).
- **Layout proportions** — where a sidebar is present (5 of 7
  references), it occupies a narrow fixed-width rail, never more than
  roughly a sixth of the screen's total width; the main content area's
  own internal grid (KPI row → chart/detail row → table/list row) reads
  as a clear top-to-bottom hierarchy, not a uniform grid of same-weight
  tiles.
- **Visual rhythm** — the repeating card/row pattern (same radius, same
  padding, same internal label-then-value structure) is what makes the
  set read as "from one family" even across 7 unrelated products — this
  rhythm, not any single color or icon choice, is the actual design
  language worth carrying into a generated screen.
- **Color relationships** — one restrained accent hue carries both the
  "active/selected" state and a chart's primary series; semantic colors
  (success/warning/error) appear only on status pills and deltas, never
  as a KPI card's own background (the "differential KPI emphasis" pattern
  above uses the *brand* accent for a hero tile, not a semantic color).

## Suggested starting register
Modern SaaS (`ui-engine/visual-trends.md`) — used as the named starting
point by `design-reference-engine/reference-selection.md` mode 4 (Default
Design-Glanza) until further curated references are added here.

## Matched by
`product-types/saas.md`'s domain slug, via
`reference-selection.md`'s exact-match rule.

## To populate further
Add curated reference images, a token file, or a written style brief to
this folder, then update this README to describe what was added, its
source, and its confidence — mirroring `product-types/domain-standards/`'s
"complete" vs. "pending" distinction.
