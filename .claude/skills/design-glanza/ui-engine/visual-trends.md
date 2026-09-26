# Visual Trends

## Responsibility
Contemporary style calibration — keeping output from looking dated or generic.
This is a **contextual options menu**, not a source of mandatory styling: a
trend is adopted only when it fits the product's register and audience, never
because it's currently fashionable. This file is a taste/calibration
reference, not a systematic rule set like the other `ui-engine/*` files, and
it can never override one of them.

## Style registers
Named, recognizable registers relevant to production-oriented SaaS/enterprise
work — most products in scope for Design-Glanza sit in the first two:

| Register | Density (`visual-hierarchy.md`) | Radius/shadow (`design-system.md`) | Color use | Typical fit |
|---|---|---|---|---|
| **Modern SaaS** | Comfortable | `radius-md`/`lg`, soft level-1/2 shadows | Restrained brand accent, generous neutral space | Account-facing SaaS surfaces (`product-types/saas.md`) |
| **Dense Enterprise** | Compact/dense | `radius-sm`, minimal shadow (flat, level-0/1) | Neutral-dominant, semantic color reserved for status only | Admin/ERP/back-office (`product-types/admin-panel.md`, `erp.md`) |
| **Consumer Playful** | Comfortable/spacious | `radius-lg`/`full`, bolder shadow | Bolder, more saturated brand color, illustration-friendly | Marketing/onboarding surfaces only — rarely the application interior |

## Density as an explicit axis
The table's Density column is each register's *default*, not a fixed
property of the register — density can be exposed as its own selectable
setting distinct from the register itself when a real user need supports it
(e.g. a Modern-SaaS product offering an opt-in "compact" table mode for
power users who've outgrown the comfortable default). Where this is done,
it's still a `visual-hierarchy.md` density-scale value applied via
`layout-system.md`'s spacing multiples exactly as the register table already
specifies — an explicit density setting is a controlled override of which
value applies, never a separate ad hoc spacing system of its own.

## Register-selection rule
Chosen by `product-types/*.md` conventions and
`methodology/empathize.md` audience findings — never picked for visual appeal
alone. A product can legitimately use two registers for two different
surfaces (e.g. Modern SaaS for the account-facing app, Consumer Playful for
its marketing site) as long as the split is deliberate and stated, not an
accident of different screens being designed at different times.

## Trend adoption gate
A specific visual trend (a particular shadow/blur treatment, a gradient
style, an illustration style, a currently-popular corner-radius extreme) is
adopted only if **all three** hold:
1. It doesn't compromise contrast compliance (`color-system.md`).
2. It doesn't compromise legibility or hierarchy
   (`typography.md`, `visual-hierarchy.md`).
3. It's chosen because it fits the selected register above — stated as a
   reason, not defaulted to because it's currently common in the industry.

Failing any one of the three means the trend is not adopted, regardless of how
current it is. This is Rule 11 (`config/operating-rules.md`) made mechanical:
"never apply a visual trend simply because it is fashionable" is enforced by
requiring an explicit pass on this three-point gate, not by exhortation alone.

## Trend vs. system — the boundary rule
A trend choice affects **surface treatment**: which shadow depth reads as
"soft" vs. "flat," how much corner radius is used, whether illustration or
photography accompanies empty states, how saturated the brand accent is
allowed to be within its ramp. A trend choice never changes the underlying
**token values that ensure consistency or accessibility** — the spacing
scale, the type scale, contrast ratios, and the state/variant model stay fixed
regardless of register. A register is a skin over the system, not a
replacement for it.

## Staleness check
Because this file calibrates to *current* convention rather than fixed
principle (unlike the rest of `ui-engine/*`), it needs periodic reassessment —
a style register description is only useful as long as its reference points
still read as current; when Design-Glanza is used repeatedly over time, this
file is the one most likely to need refreshing, and that refresh should never
silently ripple into changing the structural rules of the other files.

## Explicitly not here
- The systematic rules themselves (type scale, palette construction, contrast,
  spacing) → their respective `ui-engine/*` files.
- Domain-mandated conventions that aren't a matter of taste (e.g. healthcare's
  need for calm, low-stimulation palettes) → the relevant `product-types/*.md`.
- A concrete, numeric self-critique checklist for a finished composition
  (hierarchy ratios, restraint, anti-cliché tells) → `ui-engine/craft-critique.md`,
  which cites this file's gate rather than restating it.
- Researching what's actually current before a screen exists to critique →
  `design-reference-engine/design-research.md` (Design Setup's Step 0),
  which cites this file's three-point gate as the check any trend finding
  it surfaces must still pass — this file never gets bypassed by an
  earlier research step finding something "current."
