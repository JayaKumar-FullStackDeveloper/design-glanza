# Design System (Reasoning)

## Responsibility
Establish one coherent token set — the system — before any screen is produced
in volume. This file is the direct enforcement point of Rule 5
(`config/operating-rules.md`: system before screen) at the UI layer, mirroring
how `methodology/prototype.md` enforces Rule 4/5 at the UX layer. It owns the
token families with no other home (radius, elevation, motion, icon sizing) and
assembles them alongside typography/color/spacing (owned by their own files)
into one theming-ready system. The blank deliverable this reasoning fills is
`templates/design-system.md`.

## Figma token mapping (where a Figma Design Context exists)
Where `product-builder/BRD/figma/figma-context.json` exists
(`design-reference-engine/figma-reference.md`), establish each token
category below by mapping that context's `tokens.*` entries onto the
category's own scale directly — citing the source Figma variable by name
per token — rather than inferring values from pixels, per
`design-reference-engine/figma-context-consumption.md`'s precedence rule.
A category with no matching Figma entry still uses this file's own default
scale below, unchanged, kept consistent with whatever Figma language was
extracted for the rest of the product. This does not add a second
token-establishment mechanism — it is the existing establishment procedure
below, given a richer, better-cited input where one is available.

## Token taxonomy

### Spacing & grid
Owned and derived in `layout-system.md`; assembled here as tokens (not
re-derived) — the base unit and its multiples are the single source every
other spacing-like scale below aligns to for visual rhythm.

### Radius scale
A closed, named scale — not arbitrary per-component values:

| Token | Value | Usage |
|---|---|---|
| `radius-none` | 0 | Dense tabular surfaces, data tables |
| `radius-sm` | 4px | Inputs, buttons, small controls |
| `radius-md` | 8px | Cards, panels, dropdowns |
| `radius-lg` | 12px | Modals, large containers |
| `radius-full` | 9999px | Pills, avatars, badges |

A component reaching for a radius value outside this scale is drift —
`agents/design-system-expert.md` catches it. Reaching for `radius-lg`/
`radius-full` on every container *within* the scale is a different failure
— not drift, but the reflexive "everything is a rounded card" default
`craft-critique.md`'s anti-cliché catalog names — pick the step each
container's actual role calls for, not the roundest available option by
habit.

### Elevation scale
Communicates stacking/hierarchy — what's "on top of" what — expressed as a
shadow-depth level, not a raw shadow value per component:

| Level | Typical use | Shadow depth |
|---|---|---|
| 0 | Flat, inline content | none |
| 1 | Resting cards | subtle |
| 2 | Hovered/raised cards, dropdowns | moderate |
| 3 | Popovers, tooltips | pronounced |
| 4 | Modals, dialogs | strongest |

Elevation level also implies z-index ordering — a level-4 surface (modal) must
never be visually beneath a level-2 surface (a dropdown left open behind it).
This is the token-level backing for `visual-hierarchy.md`'s grouping and
scanning rules.

**A level-4 surface requires a scrim** (a dimmed layer behind it, over
everything below) — this is what keeps figure-ground unambiguous for a modal
specifically, distinct from level-1/2/3 surfaces which don't interrupt the
rest of the screen and so don't need one. Absence of a scrim behind a modal
is a defect at this token level, not a stylistic choice.

**Dark theme uses lighter fill layers, not stronger shadows, to communicate
elevation.** A shadow reads as a dark cast falling *onto* a lighter surface —
against an already-dark background there's little contrast left for a shadow
to darken further. The dark-theme expression of this same 0–4 scale is
instead a progressively **lighter surface fill** at each higher level (level
2's card fill is a step lighter than level 1's, etc.), optionally paired with
a subtle low-opacity border for edge definition where fill contrast alone is
too subtle — the level *meaning* (stacking order) stays identical across
themes per the Theming rule below; only which visual channel expresses it
changes.

### Motion tokens
Durations and easings, defined once and reused — never a bespoke duration per
component:

| Token | Duration | Easing | Use |
|---|---|---|---|
| `motion-fast` | 100ms | ease-out | Micro state changes (toggle, hover) |
| `motion-base` | 200ms | ease-out (enter) / ease-in (exit) | Component-level transitions (dropdown, drawer) |
| `motion-slow` | 350ms | ease-in-out | Screen-level/layout transitions |

**Motion where relevant, not everywhere:** motion is applied to a state
*transition* that benefits from continuity (something entering, exiting, or
reordering) — never applied to high-frequency, low-stakes interactions purely
for decoration (Rule 11, `config/operating-rules.md`), and every motion token
respects a user's reduced-motion preference by degrading to an instant or
near-instant transition rather than being disabled inconsistently per
component (see `ux-engine/interaction-design.md`'s motion section for the one
nuance: a transition carrying real state-indication meaning is shortened
first, not necessarily zeroed). Which specific component transitions use
which token is `component-system.md`'s call, citing these tokens by name.

**These three tokens stay closed** — this is the enforcement point for a
recurring external pattern of continuous, per-component-type duration ranges
(e.g. "150–500ms depending on distance/size"): that kind of finer-grained
guidance is legitimate as informative help for *choosing which of the three
tokens fits a given transition* (`ux-engine/interaction-design.md`'s
frequency/purpose rules do that job), never as grounds for adding a fourth
token or a bespoke duration outside this set — the same drift
`agents/design-system-expert.md` already catches for radius/elevation values
applies here.

**Choreography, when multiple elements animate together (a staggered list
entering, a group of cards reordering):** offset each element's start by
roughly 30–50ms from the previous one — enough to read as a sequence, not so
much it feels sluggish — and cap the total sequence duration around 500ms
regardless of how many elements are involved (many items means a smaller
per-item offset, not a longer total wait). Elements that logically move
together keep a consistent direction between their enter and exit (an
element that slides in from the right exits back to the right, not
downward) — this is the same spatial-consistency/return-to-origin principle
in `interaction-design.md`'s motion section, applied to a group rather than
one element. These are choreography rules for *when* and *in what order* the
existing tokens fire, not new duration values.

### Icon size scale
| Token | Size | Pairing |
|---|---|---|
| `icon-sm` | 16px | Inline with body text |
| `icon-md` | 20px | Inline with UI labels/buttons |
| `icon-lg` | 24px | Standalone, nav items |
| `icon-xl` | 32px+ | Empty states, feature illustration |

Full iconography rules (stroke weight, fill convention, color inheritance,
accessible-vs-decorative distinction) are `component-system.md`'s job; this
file only fixes the size scale.

### Border-width scale
Distinct from the radius scale above (radius is corner curvature; this is
line weight) and from a border's *color* (`color-system.md`'s semantic
triplets own that) — a closed scale, not a value chosen per component:

| Token | Value | Usage |
|---|---|---|
| `border-none` | 0 | No border; separation by whitespace/shadow alone |
| `border-hairline` | 1px | Default: inputs, cards, dividers, table rows |
| `border-thick` | 2px | Emphasis/focus rings, selected states — never for ordinary separation |

### Sizing scale (component dimensions)
Control heights, derived from the same 4px base unit the spacing scale
uses (`layout-system.md`) — not a second, independent number system:

| Token | Value | Usage |
|---|---|---|
| `size-control-sm` | 32px | Compact controls: dense-table inline actions, small buttons |
| `size-control-md` | 40px | Default control height: buttons, inputs, selects |
| `size-control-lg` | 48px | Primary CTAs, touch-priority contexts |

Internal padding at each size still comes from the spacing scale
(`component-system.md` point 3's existing Size variant rule) — this scale
only fixes the control's outer height, so a button and an input at the
same size token align to the same row height when placed side by side.

**Avatar scale** — a closed set, distinct from the icon scale above (an
avatar represents an identity, not an action/label, and is sized by
context rather than paired with a fixed adjacent element):

| Token | Size | Usage |
|---|---|---|
| `avatar-xs` | 20px | Inline in dense table rows/comment threads |
| `avatar-sm` | 28px | List rows, compact cards |
| `avatar-md` | 36px | Default: cards, headers, profile summaries |
| `avatar-lg` | 64px | Profile pages, empty-state illustration context |

Every avatar of the same role (e.g. "customer row avatar" across every
table in the product) uses the same token — a table whose rows use
`avatar-sm` on one screen and an unnamed 30px value on another is the
sizing-consistency defect this scale exists to prevent, the same drift
`agents/design-system-expert.md` already catches for radius/elevation.

### Z-index scale
The elevation scale above already states that "elevation level also
implies z-index ordering" — this makes that implication a concrete,
checkable integer scale rather than a qualitative statement, with room
between levels for component-internal stacking (a dropdown's own open
menu vs. the dropdown trigger) without needing a new named level:

| Elevation level | Z-index value |
|---|---|
| 0 (flat) | 0 |
| 1 (resting cards) | 100 |
| 2 (hovered/raised, dropdowns) | 200 |
| 3 (popovers, tooltips) | 300 |
| 4 (modals, dialogs) | 400 |

A z-index value outside this set (e.g. an arbitrary `9999`) is drift, the
same category `agents/design-system-expert.md` already catches for
radius/elevation/motion — never introduced to "just make sure it's on
top."

## Consistency rule
Once a token is set, every component and screen uses it — no one-off value
introduced outside this set without it being logged as a system gap and either
absorbed into the token set (if genuinely needed everywhere) or rejected.
`agents/design-system-expert.md` is the ongoing enforcement mechanism.

## Theming rule
Every token above is exposed through a semantic alias layer (`surface`,
`border`, `text-primary`, `text-muted`, `danger`, etc.) that maps to different
raw values per theme (light/dark) — components and screens reference the
semantic alias, never the raw value directly, so adding a theme is a token
remap, not a rebuild. Color aliases are defined in `color-system.md`; this file
requires every non-color token family above (radius, elevation, motion, icon
size) to be theme-invariant unless a specific theme genuinely needs a
different value (rare — e.g. elevation shadows may need to be more pronounced
against a dark background to remain visible).

## Establish before screens
Before `workflows/build-product.md` mass-produces
`templates/screen-specification.md` instances, the token set above and
`component-system.md`'s inventory must exist and be gate-passed
(`config/quality-gates.md`, B6 — Design System). Screens built against an
unstable or incomplete token set are exactly the failure mode Rule 5 exists to
prevent.

## Explicitly not here
- The specific type scale/pairing → `typography.md`.
- The specific palette/semantic color mapping → `color-system.md`.
- The specific grid/spacing values → `layout-system.md`.
- Per-component anatomy, variants, and iconography detail → `component-system.md`.
- The deliverable document fields → `templates/design-system.md`.
- The machine-readable structure these token families assemble into, the
  semantic naming layer, theming as a data shape, master/product
  inheritance, and violation detection → `design-tokens/*` (this file
  remains the single source for the scale *values* themselves; that folder
  never restates them, only structures and enforces them).
