# Typography

## Responsibility
Type scale, pairing, and text-block rules — the specific values
`visual-hierarchy.md` draws on to express emphasis, and that `design-system.md`
assembles into tokens.

## Type scale
A fixed step scale, named by role rather than raw size, so a role's use is
consistent everywhere it appears:

| Role | Size | Weight | Line-height |
|---|---|---|---|
| `caption` | 12px | 400 | 1.4 |
| `body` | 14px | 400 | 1.5 |
| `body-large` | 16px | 400 | 1.5 |
| `h3` | 18px | 600 | 1.3 |
| `h2` | 24px | 600 | 1.3 |
| `h1` | 32px | 700 | 1.2 |
| `display` | 40px+ | 700 | 1.15 |

Body sizes stay in the 14–16px range deliberately — this is a
production-oriented enterprise/SaaS system, where information density and
extended reading (data tables, forms, dense dashboards) matter more than the
larger body sizes a marketing site would use.

## Font pairing rule
Default: **one well-hinted system/sans family**, distinguished by weight
(400/500/600/700) rather than a second display face. Enterprise density and
legibility at small sizes are better served by one robust family than by
managing two. A distinct display face is only introduced when
`visual-trends.md`'s register selection specifically calls for more brand
personality (typically marketing/onboarding surfaces, not the dense
application interior) — and even then, the second face is reserved for
`display`/`h1` roles only, never for body or data text.

## Line-height and measure
- **Line-height** per role is set above; headings are tighter (1.2–1.3) than
  body text (1.5) because short heading lines don't need the breathing room
  long paragraphs do. **This tighter-heading rule is a Latin-script default**
  — see Non-Latin script typography below for where it doesn't hold.
- **Measure** (line length) for body paragraphs: **45–75 characters**. Below
  45, text feels choppy; above 75, the eye loses its place on the line wrap.
  Tabular/data text is exempt from this measure constraint — a data table
  column is as wide as its content requires, not constrained to a reading
  measure.

## Hierarchy via type alone
Heading levels must be distinguishable by weight + size together even with
color and layout position stripped away (grayscale, screen-reader "skip to
heading" navigation) — the scale above is constructed so no two adjacent roles
share both the same weight and a visually-similar size.

## Tabular/numeric data treatment
Any column of numbers (prices, quantities, IDs) uses **tabular figures**
(fixed-width numerals) so digits align vertically across rows — proportional
numerals in a data table make column scanning materially harder and are a
common, easily-avoided defect in enterprise UI specifically.

## Non-Latin script typography
Everything above is written from a Latin-script default; a product whose
locale requires a non-Latin script (CJK, and others) needs specific
departures rather than a straight font swap — flagged early, per
`methodology/empathize.md`'s locale/script note, so it isn't discovered as a
correction after the type scale above is already applied:
- **Single-family-across-weights, not a display/body pairing** — the same
  posture this file's Font pairing rule already defaults to for density
  reasons, but here it's closer to a requirement than a preference: many
  non-Latin scripts have far fewer well-hinted display faces available, and
  mixing families is more likely to visibly clash than in Latin type.
- **Heading line-height is not tighter than body** — pre-composed syllable
  blocks (e.g. Hangul) read as cramped at Latin display-heading line-heights
  even at large sizes; a non-Latin heading role keeps body-level or looser
  line-height rather than following the tighter-heading default above.
- **Word-break defaults to keep-all, not Latin's overflow-wrap: anywhere** —
  CJK text wraps at meaningful unit boundaries, not at an arbitrary character
  when a line is full.
- **Negative letter-tracking on display type is a Latin-only technique** —
  applying it to non-Latin display headings tends to read as cramped/harder
  to parse rather than "confident," the effect it's reached for in Latin
  type; don't carry it over by default.
- **Mixed-script text (a product name or numerals inside non-Latin body
  text) needs distinct optical sizing at the same nominal font-size** — Latin
  glyphs read visually smaller next to CJK glyphs at an identical point size,
  so a mixed string can need the Latin portion sized up slightly to read as
  visually matched.

Confidence note: these five points are best-verified for scripts using
pre-composed syllable blocks; treat them as a starting checklist to verify
against the specific script in play, not a substitute for a native-script
review.

## Explicitly not here
- How type-driven emphasis combines with whitespace/scale into overall
  hierarchy → `visual-hierarchy.md`.
- How type tokens get folded into the assembled system → `design-system.md`.
- Color of text (including for accessibility contrast) → `color-system.md`.
