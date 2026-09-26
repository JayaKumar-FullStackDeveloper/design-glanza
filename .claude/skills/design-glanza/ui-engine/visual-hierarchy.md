# Visual Hierarchy

## Responsibility
Make important things look important. This file governs *relative* visual
weight across a screen; the concrete type scale and color values used to
express it live in `typography.md` and `color-system.md`.

## Primary action
Exactly one primary action per screen/context — the action
`templates/screen-architecture.md` names as this screen's dominant purpose.
Visual treatment: highest contrast (filled, using the `primary` semantic
color), largest button size available at that density, and positioned first
in scan order (see Scanning, below). Two "primary-looking" buttons on one
screen is a hierarchy failure, not a stylistic choice — it forces the user to
evaluate which one actually matters.

## Secondary action
Visually subordinate but still clearly actionable — an outline or ghost
button style, never full-strength `primary` fill. A destructive secondary
action (delete, remove) uses the `danger` semantic color at reduced visual
weight relative to the primary action, so it reads as available but not as the
recommended path — reserved sparingly, per Rule 11
(`config/operating-rules.md`), to avoid alarm fatigue where every screen has a
red button.

A high-risk destructive action (per `interaction-design.md`'s reversibility×
risk matrix) is additionally placed with real **spatial** distance from the
primary/frequent action, not just reduced visual weight — visual subordination
alone doesn't prevent an accidental click/tap when the two sit close together;
physical separation reduces that risk independent of color/weight. Screen
edges and corners are effectively unmissable, easy-to-hit targets (a cursor or
finger's motion path tends to land there) — reserve them for persistent,
frequently-reached controls (primary nav, not an occasional destructive
action).

## Information priority
Map content importance to visual weight using the same source
`ux-engine/user-flow-engine.md`'s "information prioritization" optimization
criterion draws from: what's needed for the *current* decision gets top-of-
scan placement and the highest contrast; a status or error affecting whether
the user can even proceed outranks everything else on the screen; secondary
detail (metadata, timestamps, secondary metrics) recedes in size/contrast and
is positioned later in scan order.

## Grouping
Visual proximity and enclosure (whitespace gaps, card boundaries, dividers)
mirror `ux-engine/information-architecture.md`'s logical groupings exactly —
a visual group must never cut across an IA grouping boundary, since that
mismatch is what makes a screen "look organized" while actually confusing the
user's mental model of what belongs together.

Grouping is expressed through five distinct visual signals, not proximity
alone — checking only proximity misses real grouping defects the other four
would catch:
- **Proximity** — related items placed closer together than unrelated ones.
  This is the primary mechanism and the one most screens rely on by default.
- **Similarity** — items sharing visual treatment (color, shape, size) read
  as one category even when *not* spatially adjacent. This can also work
  against a design: a single visually-deviant item inside an otherwise
  spatially-grouped set reads as belonging to a different category despite
  its placement — similarity overrides proximity when the two disagree, so a
  one-off style exception inside a group is rarely a safe cosmetic choice.
- **Figure/ground** — what reads as foreground content vs. background
  context must stay unambiguous; this is the perceptual basis for
  `design-system.md`'s modal-scrim requirement and for never placing text
  directly on a busy photograph with no separation layer (a scrim, a solid
  panel) behind it.
- **Continuity** — elements aligned along a shared line or path read as a
  connected sequence (this is the perceptual basis for `layout-system.md`'s
  alignment-to-grid rule and its large-spacing-multiple-signals-a-new-section
  convention — a bigger gap breaks continuity on purpose).
- **Closure** — the eye completes a implied boundary from partial cues, which
  means a full enclosing border is often more than the grouping actually
  needs. Prefer the **weakest boundary that still reads as a group** — a
  single divider line, a subtle background-color shift, or whitespace alone —
  before reaching for a full card border on every group; over-enclosing
  everything in its own bordered box is itself a hierarchy problem (too many
  equally-strong boundaries flattens emphasis, the same failure the
  Contrast-of-weight rule below names for emphasis levels).

Applying only proximity while ignoring similarity is the most common way a
screen "passes" a casual grouping check while still confusing users — treat
all five as one checklist, not proximity as a stand-in for the others.

## Scanning
Choose the scan pattern the layout supports, per content type:
- **F-pattern** — text-heavy or list-based content (data tables, settings
  lists, most enterprise/admin screens per `product-types/admin-panel.md`,
  `erp.md`): left-aligned, scannable columns, most important content in the
  leftmost/topmost position.
- **Z-pattern** — low-density, marketing-style or onboarding content: a single
  clear path from top-left to bottom-right ending at one call-to-action.

Most of a production SaaS/enterprise product uses F-pattern; Z-pattern is
reserved for the minority of screens that are genuinely low-density and
persuasive rather than operational (onboarding, empty-state calls to action).

## Density
A named density scale — **comfortable / compact / dense** — selected per
`visual-trends.md`'s register (informed by `product-types/*.md`): dense
enterprise/admin/ERP surfaces default to compact or dense; consumer-facing or
low-frequency-use surfaces default to comfortable. Density is expressed
entirely through which multiple of `layout-system.md`'s spacing scale is used
between rows/elements — it is not a separate system, just a smaller spacing
multiple applied consistently.

## Whitespace
Whitespace is priority signal, not just tidiness: more space *around* an
element increases its perceived importance relative to its neighbors, deployed
deliberately (around the primary action, around a critical alert) rather than
applied uniformly "for cleanliness" everywhere, which flattens hierarchy
instead of creating it.

## Progressive disclosure
Show only what's needed now; defer secondary detail behind an explicit,
visually-actionable affordance (an "expand," "show more," or drill-in
control) — the visual realization of `ux-engine/navigation-system.md`'s deep-
navigation and overlay patterns and `user-flow-engine.md`'s information-
prioritization criterion. The disclosure affordance itself must be visually
legible as interactive (not blend in as plain text) — a progressive-disclosure
control that doesn't look clickable defeats its own purpose.

## Contrast-of-weight rule
Limit a single screen to roughly **3–4 distinct emphasis levels** (primary,
secondary, tertiary/muted, disabled) — beyond that, additional "levels" stop
reading as hierarchy and start reading as visual noise, undermining every rule
above.

**Isolation inflation** is how this rule erodes over time rather than all at
once: each new feature, considered on its own, seems to deserve a highlight
treatment to stand out — but if every feature added this way gets one, the
screen accumulates emphasis levels past the 3–4 cap without any single change
looking like the violation. This is a drift check, not a one-time design
decision — `agents/design-system-expert.md`'s periodic drift review
(already checking token/component drift) is the right point to also ask "how
many things on this screen are now visually shouting," not just at a
component's creation.

## Explicitly not here
- The actual type scale values → `typography.md`.
- The actual color values used for emphasis → `color-system.md`.
- Grid/spacing scale definitions → `layout-system.md`.
- Screen-reader reading order (a structural/semantic concern, not visual) →
  `ux-engine/accessibility.md`.
