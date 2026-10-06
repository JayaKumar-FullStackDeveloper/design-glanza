# Localization

## Responsibility
Structural and layout consequences of supporting more than one language/locale
— what changes about the interface itself when it isn't Latin-script,
left-to-right, or single-locale, as distinct from `ui-engine/typography.md`'s
Non-Latin script typography section (which owns the *type* consequences —
line-height, word-break, tracking — of a non-Latin script specifically). This
file applies only when a product's requirements actually call for more than
one locale; a single-locale product has nothing here to apply.

## Text expansion
Translated text is not the same length as its source. As a rough, checkable
planning figure: German and other Germanic/Romance languages commonly run
20–35% longer than English for the same meaning; some East Asian languages
run shorter in character count but need more width per character. A layout
sized to fit its source-language copy exactly, with no reserved slack, is a
structural defect once translated — component width/height (`ui-engine/
component-system.md`) must tolerate this range, not just the one string it
was designed against.

## RTL (right-to-left) mirroring
When a locale requires RTL (Arabic, Hebrew, and others), the interface
mirrors horizontally — but **not everything mirrors**, and treating the two
lists as symmetric is the most common defect:
- **Mirrors:** reading direction and text alignment, navigation/menu order
  (a left-sidebar becomes a right-sidebar), icons that imply direction
  (a "next"/forward arrow, a back-navigation chevron), progress indicators
  that read left-to-right.
- **Does not mirror:** logos and brand marks, clock faces and time-of-day
  icons, mathematical notation and numerals, video/media player controls
  (play/pause/scrub retain their universal left-to-right convention
  regardless of surrounding text direction), and any icon depicting a
  real-world object with an inherent orientation (e.g. a physical device).

Layout and component specs (`ui-engine/layout-system.md`,
`component-system.md`) express direction using **logical properties**
("start"/"end") rather than physical ones ("left"/"right") wherever a
component's spec is meant to hold across both directions — a spec written in
physical left/right terms has to be separately re-authored for RTL instead of
automatically flipping.

## Locale-aware formatting
Dates, numbers, currency, and name order are formatted per the active
locale's convention, not hardcoded to one — this is a `product-intelligence/
business-logic.md`-level data-requirement (which locale format applies to
which field) as much as a display concern; a date field's format is part of
its Data-type requirement (`product-intelligence/requirement-engine.md`),
not an afterthought applied at render time. Concretely, each of these
varies by locale independently — never assume one locale choice fixes all
four: **dates** (MM/DD/YYYY vs. DD/MM/YYYY vs. ISO 8601 — ambiguous
numeric-only dates are a defect regardless of which convention is chosen,
since 03/04 is a different day depending on the reader); **numbers**
(decimal vs. thousands separator — `1,000.50` vs. `1.000,50`); **currency**
(symbol position — prefix vs. suffix — and whether the currency code or
symbol is shown, since a bare `$` is ambiguous across multiple
dollar-denominated locales); **name/address order** (given-family name
order varies, and an address's field order and required fields are not
uniform — a fixed "Street/City/State/Zip" form is a US-specific structure,
not a universal one).

## Cultural meaning of color and icons
A color or icon's meaning is not universal (`ui-engine/color-system.md`'s
semantic mapping is written from one cultural default) — where a product's
actual audience spans cultures with materially different associations for a
semantic color or icon (this varies by symbol and culture; verify for the
specific locales in scope rather than assuming), flag it as a domain-specific
consideration for the relevant `product-types/*.md` pack rather than silently
keeping the default mapping.

## When this file applies
Flagged during `methodology/empathize.md` dimension 8 (Environment) the same
way a non-Latin script is — if the source material's actual locale/audience
scope is single-locale and Latin-script, none of the above changes anything
and this file has nothing to apply.

**Optional Gemini content second-pass (GC-4, `ui-engine/
gemini-capability.md`):** when this file applies and the copy volume/
complexity for a specific locale makes it worthwhile, a Gemini text-model
pass may suggest naturalness refinements to drafted interface copy for
that locale — suggestions only, reviewed against `ux-writing.md`'s
existing content rules before acceptance, never auto-applied. Skipped
(unavailable, or this file doesn't apply) falls back to Design-Glanza's
own existing content-authoring process, unchanged.

## Explicitly not here
- Non-Latin script line-height/word-break/tracking rules →
  `ui-engine/typography.md`'s Non-Latin script typography section.
- The semantic color/contrast rules themselves → `ui-engine/color-system.md`.
- Domain-mandated locale requirements (e.g. a regulatory date-format
  requirement) → the relevant `product-types/*.md`.
