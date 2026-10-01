# Color System

## Responsibility
Palette construction and semantic color mapping, including the *perceptual*
accessibility rules (contrast ratio, color-blind safety) — the color
counterpart to `ux-engine/accessibility.md`'s structural/behavioral rules.

## Palette construction
The starting brand/primary hue itself comes from `product-builder/ui/
design-direction.md`'s Color system field (Rule 18) — never defaulted to
a generic blue-to-purple "SaaS palette" because that's the reflexive
choice with no stated direction to follow. Where the direction genuinely
doesn't specify one (Custom Design/Default mode with no color preference
stated), the choice is still made deliberately per this product's actual
domain/brand context and recorded as such, not defaulted silently — the
same distinction `craft-critique.md`'s anti-cliché catalog draws between a
justified choice and a reflex.

From that one brand/primary hue, generate a **9–10 step ramp** (lightest to
darkest) at consistent lightness intervals, rather than picking individual
shades ad hoc. Generate the same ramp structure for:
- **Primary** — the brand color, used for primary actions and key emphasis.
- **Neutral/gray** — a separate 9–10 step ramp used for backgrounds, borders,
  and text; enterprise UI leans on neutrals far more than on brand color, so
  this ramp needs the same rigor as primary, not an afterthought gray-100.
- **Semantic colors** (below) — each gets its own short ramp, not just one hex.

## Semantic mapping
Fixed meaning across the whole product — never repurposed per screen:

| Semantic | Foreground | Background | Border | Meaning |
|---|---|---|---|---|
| `success` | dark green | pale green | mid green | Completed, valid, positive |
| `danger` | dark red | pale red | mid red | Destructive, error, blocking |
| `warning` | dark amber | pale amber | mid amber | Caution, needs attention, not blocking |
| `info` | dark blue | pale blue | mid blue | Neutral notice |
| `neutral` | from gray ramp | from gray ramp | from gray ramp | Default/inactive |

Each semantic is a **triplet** (foreground/background/border), not a single
color — this is what lets a status badge, an inline alert, and a form error
all use the same `danger` meaning consistently instead of three
independently-invented reds.

**Optional `soft`/`onSoft` extension.** The `background` above is sized for
a larger surface (an inline alert, a toast panel) — a visually lighter,
more tinted treatment the same semantic meaning also needs for a smaller,
denser component (a **badge, chip, status pill, delta indicator, semantic
icon container, or avatar initials/background**) is a genuinely different
background, not the same one at a glance, and is not automatically safe
for the same foreground. `design-tokens/semantic-tokens.md`'s `soft`
(the tinted background) and `onSoft` (the foreground guaranteed to read
against it) name this pairing explicitly so it gets its own check rather
than inheriting the plain triplet's result.

## Contrast compliance rule
Concrete, checked ratios (WCAG AA baseline, matching the conformance target
`ux-engine/accessibility.md` states):
- **4.5:1** minimum for normal body text against its background.
- **3:1** minimum for large text (≥18px, or ≥14px bold) and for UI component
  boundaries/icons that convey meaning.

Every semantic triplet's foreground-on-background pairing is checked against
these ratios **in both light and dark theme** — a pairing that passes in light
theme but fails after dark-theme remapping is a defect, not an acceptable
theme limitation. Icons and other meaningful graphical elements are held to
the same ratios as the text/boundary they're paired with — an icon
inheriting `currentColor` (`component-system.md`'s Iconography rule) is
already covered by its host text's own checked pairing; an icon carrying
its own explicit semantic color (a `danger`-toned warning icon) is checked
as that semantic triplet's own foreground-on-background pairing, not
assumed safe by association with the text near it.

**Disabled-state exemption.** WCAG explicitly excludes inactive/disabled
UI components from the contrast minimums above — a `disabled` control's
own dimmed treatment is not a Contrast-rule failure by design, since it's
deliberately communicating unavailability, not meant to be a primary
reading/interaction target. This exemption applies only to the control's
own disabled-state color; the same control's `disabled` state must still
be communicated through more than color alone (never dimmed as the sole
signal — pair with a stated cursor/label/icon change, per the color-blind
safety rule below and `ux-engine/accessibility.md`'s Permission-denied
accessibility section), and a *label* explaining *why* something is
disabled is never itself styled at disabled-level contrast — only the
disabled control itself is exempt, not surrounding explanatory content.

**Pairing contract, not a one-time pass.** This rule certifies the specific
pairings it's actually run against — the semantic triplets defined above,
and the `soft`/`onSoft` pairing where declared. It does not automatically
certify a *new* pairing a later screen improvises (e.g. reusing `primary`
as a badge fill under `text-primary`, a combination never checked because
it's outside the defined triplets). A semantic key's plain foreground/
background pair passing is likewise never treated as certifying that same
key's `soft` background — they are checked independently, since `soft` is
a different, lighter background, not the same one restated. Treat the set
of checked pairings as an explicit, named contract (`agents/design-system-
expert.md`'s inventory): a new component proposing a color combination
outside it is a fresh check against this rule, not an assumed pass by
association with an already-cleared color. This is the same discipline Rule
13 (Iteration) already applies to a failed gate — re-check, don't assume —
applied here to a class of check (color pairing) that's easy to treat as
"settled once" instead.

## Color-blind safety rule
Never encode meaning by hue alone. Every semantic use (success/danger/warning
especially) pairs color with a second channel — an icon, a label, a pattern,
or position. **Red/green specifically** — the most common color-vision
deficiency confusion — must never be the *only* signal distinguishing two
states (e.g. a valid vs. invalid field indicated only by a green vs. red
border, with no icon or text change, is a defect).

## Dark/light theming
Semantic tokens (`success`, `danger`, `neutral`, etc.) and structural aliases
(`surface`, `border`, `text-primary`, `text-muted` — per `design-system.md`'s
theming rule) remap between themes while keeping their *meaning* stable:
`danger` stays recognizably red-ish in both themes, adjusted in lightness so
it still clears the contrast rule above against the theme's background;
`surface` is near-white in light theme and near-black (not pure black, which
crushes elevation shadows) in dark theme. `text-primary` in dark theme is
near-white but likewise never pure white against a near-black surface —
full-strength white-on-black produces a visible halation/vibration effect
that reduces comfortable readability at length, the same "near-, not pure-"
correction applied to the background for a different reason.

**Selecting a theme:** default to the OS/browser-level `prefers-color-
scheme` signal so the product matches the user's own system setting without
requiring a decision from them, and additionally expose a manual override
control when the product has its own persistent per-user setting to store
it in — auto-detection and a manual override are not alternatives, a
product offers both where it can.

## Data-visualization ramps
Distinct from the semantic UI ramps above (which encode fixed *meaning* —
success is always green-ish) — chart/data color needs its own ramps, chosen
by what the data itself is:
- **Sequential** — one hue, increasing in saturation/darkness, for data with
  a low-to-high order (a heatmap, a magnitude scale).
- **Diverging** — two hues meeting at a neutral midpoint, for data with a
  meaningful zero/center (variance from a target, positive-vs-negative
  change) — never a sequential ramp for this shape, which hides where the
  midpoint actually falls.
- **Categorical** — hues chosen for maximum mutual distinguishability (not
  from a single-hue ramp), for unordered categories (segments, regions) —
  capped at roughly 8 distinct series before an additional visual channel
  (pattern, direct labeling) is needed, since beyond that count hue alone
  stops reliably distinguishing series.

All three still pass the color-blind safety rule above (categorical
especially — red/green adjacent categories in an unordered legend are exactly
the confusion that rule exists to prevent) and the contrast rule where a
series color also carries a text/label. Chart-type selection itself
(matching a data shape to bar/line/scatter/etc.) is
`ui-engine/component-system.md`'s concern — this section owns only the color
ramps such a chart draws from.

## Loop position
Consumes `visual-trends.md`'s register selection (which informs how saturated/
restrained the primary palette is) at the feature-level loop. Re-entered when
a Test accessibility finding (dimension 6) traces to a perceptual cause —
contrast or color-only encoding — per `methodology/design-thinking.md`'s
routing table; structural accessibility causes route to
`ux-engine/accessibility.md` instead.

## Explicitly not here
- Structural/keyboard/ARIA accessibility → `ux-engine/accessibility.md`.
- How color combines with type/whitespace for hierarchy → `visual-hierarchy.md`.
- How color tokens fold into the assembled system's theming layer →
  `design-system.md`.
