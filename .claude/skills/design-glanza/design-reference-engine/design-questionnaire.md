# Design Questionnaire

## Responsibility
The structured question set Design Setup asks (or infers, when references
already answer a question — see below) before any UI is generated. Covers
the same nine categories every time, so a design direction is never
established from an incomplete, ad hoc subset of preferences.

## When a question is asked vs. inferred
A question is **asked directly** when a real user is present and no
reference/guideline already answers it with real confidence
(`reference-analysis.md`'s Explicit/Inferred tiers). A question is
**answered by inference** when `reference-analysis.md` or a stated brand
guideline already gives a confident answer — re-asking a question the
references already answered is redundant and, worse, invites a contradicting
answer that then has to be reconciled. Either way, every answer in the
final `design-direction.md` states which of the two happened.

## The nine categories

### 1. Visual style
Design style (modern / minimal / premium / futuristic / editorial /
playful / enterprise / clinical / etc.), brand personality, visual density,
level of visual expression (restrained vs. expressive).

### 2. Layout
Grid preference, container behavior (fixed-width vs. fluid), spacing
density, card usage, section structure, sidebar/header/navigation
preference, desktop vs. mobile priority.

### 3. Typography
Font preference (named family or a mood description), typography
hierarchy expectations, heading style, body-text style, numeric/data
typography needs (tabular figures, monospace for codes/IDs).

### 4. Color
Primary color, secondary colors, accent colors, background colors, surface
colors, semantic colors (success/danger/warning/info), dark/light theme
requirement, any stated contrast requirement beyond the baseline.

### 5. Components
Expectations for buttons, inputs, cards, tables, tabs, dropdowns, modals,
drawers, toasts, badges, navigation, charts, forms — not full specs (that's
`ui-engine/component-system.md`'s job later), just direction and any
explicit preference/constraint ("no modals, drawers only" is a real,
recordable preference at this stage).

### 6. Interaction patterns
Hover behavior, selection behavior, loading behavior, transition
expectations, modal-vs-drawer preference, inline-editing expectations,
confirmation-pattern expectations, drag/drop where relevant.

### 7. Responsive design
Desktop/tablet/mobile priority, breakpoint expectations, responsive
navigation preference, responsive table/form behavior expectations.

### 8. Accessibility
Contrast expectations beyond the baseline, keyboard-navigation priority,
focus-state expectations, screen-reader considerations already known to
matter for this audience, touch-target expectations.

### 9. Brand / guidelines
Existing brand rules, logo usage constraints, forbidden colors/styles,
existing design tokens, existing component library to align with or
replace.

## Recording an unanswered question
A question with no answer — not inferred from a reference, not answered by
the user, no guideline covering it — is recorded as a genuine gap and filled
per Rule 2's lower tiers (`ui-engine/*`'s own defaults) with an assumption
tag, exactly like any other unresolved fact in this system. It is never left
silently blank in `design-direction.md`.

## Output shape
Answers (asked, inferred, or assumption-tagged) feed directly into the
matching sections of `templates/design-direction.md` — this file does not
define a separate intermediate document; the questionnaire's answers *are*
`design-direction.md`'s Visual style / Layout / Typography / Color /
Components / Interaction / Responsive / Accessibility / Brand sections.

## Explicitly not here
- Extracting answers from a provided reference in the first place →
  `reference-analysis.md`.
- Classifying the overall design-reference decision once answers are
  collected → `reference-selection.md`.
- The final document's complete field list → `design-direction.md`,
  `templates/design-direction.md`.
