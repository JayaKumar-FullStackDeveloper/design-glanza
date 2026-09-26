# Design Research

## Responsibility
Design Setup's **first** step (Step 0, before reference detection) —
research current design patterns and conventions relevant to *this*
product's domain, users, workflow, and information density, so the
questions asked in `design-questionnaire.md` and the direction written in
`design-direction.md` are informed by real pattern knowledge, not by
whatever the first idea that comes to mind happens to be. This is where
Design-Glanza reasons like a senior product designer who already knows the
landscape, rather than a template generator with no point of view.

## Why this runs even when a reference already exists
`reference-analysis.md` extracts what *one specific reference* does.
Design Research is broader: it establishes what's currently *conventional*
and *appropriate* for this domain in general, which is what makes it
possible to tell whether a supplied reference is worth following faithfully
or is itself an outlier worth deviating from. Skipping this step and going
straight from a reference (or a blank page) to a screen is exactly the
"functional-looking interface with no design reasoning behind it" failure
mode this file exists to prevent.

## What to research, per category

| Category | What to establish |
|---|---|
| Current product-design patterns | What a well-executed product in this space generally does today — not a specific competitor, the *category* |
| Modern SaaS/admin patterns | Dashboard composition, table-vs-card list defaults, settings organization, workspace/tenant switching where relevant |
| Domain-specific UI conventions | What `product-types/<domain>.md` and any matched `product-types/domain-standards/` entry already state — cite them, don't re-derive |
| Information density | What density this domain/user/task combination actually needs (`ui-engine/visual-hierarchy.md`'s density scale) — a field-ops tool and an executive dashboard have different correct answers, not a universal one |
| Navigation patterns | Which of `ux-engine/navigation-system.md`'s patterns actually fits this product's IA shape — research confirms the selection rule's inputs, it doesn't override the rule |
| Data visualization patterns | Which chart types this domain's data shapes actually call for (`ui-engine/component-system.md`'s Data visualization section) |
| Form/table patterns | Density, inline-vs-modal editing, and validation conventions typical for this domain's data-entry volume |
| Interaction patterns | What interaction model this actor/frequency combination calls for (`methodology/ideate.md` item 2's frequency-driven logic, already run earlier — Design Research confirms it still holds at the UI layer) |
| Accessibility patterns | Any domain-specific accessibility bar beyond the baseline (`product-types/*.md`'s own accessibility point, healthcare/gov-adjacent domains especially) |
| Responsive patterns | Which breakpoints and reflow patterns actually matter for this product's real usage context (desk-bound admin vs. field-mobile) |
| Current visual trends | `ui-engine/visual-trends.md`'s registers — current, not timeless, by that file's own design — checked for staleness per its own Staleness check section |

## The anti-trend-slave rule
Researching current trends is not the same as adopting them. Every pattern
surfaced here still has to clear `ui-engine/visual-trends.md`'s 3-point
trend-adoption gate and `methodology/design-judgment.md`'s anti-fashion
strip-away test before it's used — Design Research's job is to make sure
the *option set* considered is current and complete, not to pre-select the
fashionable option from it. A pattern that's common right now but doesn't
fit this product's density/audience/domain is a researched-and-rejected
option, recorded as such, not silently adopted because "that's what
everyone does now."

## Output
A short, named list of which researched patterns actually apply to this
product and why (one line each is enough — this is a research pass, not a
document unto itself) — feeding directly into `design-questionnaire.md`'s
answers (a researched pattern can pre-answer a question the same way a
reference does) and into `design-direction.md`'s Design principles field.
No separate artifact file — this step's findings are folded into
`product-builder/ui/design-direction.md` alongside everything else Design
Setup produces, not a parallel document.

## Explicitly not here
- Extracting what one specific supplied reference does →
  `reference-analysis.md`.
- The domain's own stated conventions (cited here, not re-derived) →
  `product-types/*.md`, `product-types/domain-standards/`.
- The actual trend-adoption gate and register definitions →
  `ui-engine/visual-trends.md`.
- The anti-fashion reasoning discipline itself →
  `methodology/design-judgment.md`.
