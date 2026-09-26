# Reference Analysis

## Responsibility
The extraction technique for turning a provided visual/design reference into
**design direction** — the Design Setup counterpart to
`product-intelligence/brd-analysis.md`, which extracts *business-logic*
signal from the same kind of input. Both files can run against the same
screenshot; they extract different, non-overlapping things from it, and
neither substitutes for the other (see the boundary rule below).

## The 13 recognized reference forms
Detected during Intake alongside the requirement material, then handed to
this file at Design Setup:

Reference images · UI screenshots · existing-product screenshots · Figma
designs (file or link) · website references · design-system files · brand
guidelines · color guidelines · typography guidelines · component
references · existing application UI · visual examples · written design
guidelines.

A reference doesn't need to be all of these at once — a single screenshot
is enough to run this technique; more references simply mean more to
reconcile (see Reconciling multiple references, below).

## What gets extracted, per reference

| Extract | What to look for |
|---|---|
| Visual patterns | Overall aesthetic register — density, ornamentation level, flatness vs. depth, illustration/photography use |
| Interaction patterns | What responds to hover/press, how transitions read, whether disclosure is progressive or flat |
| Design-system characteristics | Whether a token-like system is visible (consistent radius/spacing/type steps) vs. ad hoc per-screen values |
| Reusable components | Recurring UI pieces (cards, nav bars, modals) worth naming as components rather than one-off layouts |
| Layout structure / grid | Grid structure, composition shape (list+detail, dashboard grid, single-column, etc. — the same vocabulary `ui-engine/layout-system.md` names) |
| Typography | Type-scale steps actually in use, pairing (one family vs. two), weight usage |
| Color | Palette breadth, saturation level, how semantic meaning (success/danger/warning) is expressed if at all |
| Visual hierarchy | How the reference itself signals primary vs. secondary vs. tertiary — worth extracting even when it isn't perfect, since a flawed hierarchy is itself a signal about what to depart from |
| Spacing / density | Apparent base unit and multiple pattern (tight/comfortable/spacious), and which density register that implies |
| Border treatment | Whether borders are used at all for separation vs. whitespace/shadow alone, weight, and where (cards, inputs, dividers) |
| Radius | Corner-radius register — sharp, subtly rounded, or pill-shaped, and whether it's applied consistently by component type |
| Shadows / elevation | Shadow depth and frequency — flat, subtly layered, or heavily skeuomorphic — and whether it maps to a stacking/importance signal or is applied decoratively |
| Iconography | Stroke vs. fill convention, size consistency, whether icons carry meaning or are decorative |
| Navigation | Sidebar vs. top nav vs. tabs, breadcrumb presence, how deep navigation is exposed |
| Tabs | Whether tabs are used for peer content switching, their visual treatment (underline, pill, boxed) |
| Tables | Row density, header treatment, whether numeric columns use tabular figures, sort/filter affordance placement |
| Filters | Inline vs. panel/drawer filters, how many are exposed by default vs. behind an "more filters" disclosure |
| Forms | Field grouping, label placement (top vs. inline), validation-message placement |
| Cards | Anatomy (image/header/body/footer combination), density, and when the reference reaches for a card vs. a plain list row |
| Status indicators | Badge vs. dot vs. text-only, color usage, whether a non-color channel accompanies the color (accessibility signal) |
| Responsive behavior | Only inferable from multiple reference states (e.g. a mobile screenshot alongside a desktop one) — otherwise flagged as unknown, not guessed |

## The boundary rule — design direction, never business requirements
Every fact extracted here is tagged **design direction**. It is never
merged into `product-intelligence/requirement-engine.md`'s `REQ-NNN` model,
`business-logic.md`'s `BR-NNN` rules, or `user-roles.md`'s `ROLE-NNN` model
— those come only from `brd-analysis.md`'s own extraction technique, applied
to the same input independently. A screenshot showing an "Approve" button
tells this file about button styling and label conventions; it tells
`brd-analysis.md` about a possible approval business rule — two separate
facts from one image, extracted by two separate files, neither one
implying the other automatically. Where the two disagree about something
that matters (a screenshot implies a workflow the written BRD doesn't
mention), that's `brd-analysis.md`'s gap-detection to flag, not something
this file resolves.

## Extract the language, not the screen
The goal is the underlying visual *system* a reference implies, not a
literal copy of what's on screen — a reference's specific copy, specific
data, and specific one-off layout quirks are not the point; its type scale,
its spacing rhythm, its color role assignments, and its component vocabulary
are. Two references from the same design system look different screen to
screen but should extract to the *same* underlying direction; extracting a
different direction from every individual screen of one coherent product is
a sign of over-fitting to specifics rather than finding the pattern.

## Reconciling multiple references
Where more than one reference is provided:
- References that agree reinforce the extracted pattern with higher
  confidence.
- References that conflict (one shows a dense enterprise table, another a
  spacious marketing hero) are not silently averaged — name the conflict
  and ask which surface each pattern actually belongs to (the same
  reconciliation posture `brd-analysis.md` already uses for conflicting
  input facts), since a product can legitimately use two registers for two
  different surfaces (`ui-engine/visual-trends.md`'s existing rule).
- A reference to an unrelated product with no stated reason to emulate it
  specifically (e.g. "make it modern like everyone else's app") is weak
  signal — treat it the same way `domain-classifier.md` treats a single
  weak signal: noted, not acted on alone.

## Confidence tagging
Every extracted pattern carries the same three-level confidence
`brd-analysis.md` uses — **Explicit** (directly visible/stated), **Inferred**
(a reasonable reading, e.g. "this looks like an 8px base unit"), or
**Assumed** (no visual evidence, filled from a written guideline's
description alone) — carried forward into
`product-builder/ui/design-direction.md` exactly as an assumption tag would
be.

## Explicitly not here
- Extracting business logic/requirements from the same input →
  `product-intelligence/brd-analysis.md`.
- What's conventional for this domain in general, independent of any one
  supplied reference → `design-research.md` (runs *before* this file, as
  Design Setup's Step 0).
- The structured question set used when references are absent or
  incomplete → `design-questionnaire.md`.
- Deciding Reference-Driven vs. Guideline-Driven vs. Custom vs. Default →
  `reference-selection.md`.
- The document shape this feeds → `design-direction.md`,
  `templates/design-direction.md`.
- Comparing the eventual generated screen back against this extraction →
  `ui-engine/visual-benchmark.md`.
