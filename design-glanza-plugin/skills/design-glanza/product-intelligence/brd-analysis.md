# BRD Analysis

## Responsibility
The extraction method for turning *any* raw input into structured facts — before
any requirement, rule, or design decision exists. This file owns recognition and
extraction; it does not decompose facts into requirements
(`requirement-engine.md`), derive rules (`business-logic.md`), model roles
(`user-roles.md`), or enumerate edge cases (`edge-case-engine.md`) — it hands
each of those a labeled category of raw fact to work from.

## Input-type recognition
Every accepted input form needs a different extraction posture. Recognize which
one you have before extracting:

| Input | Extraction posture | Confidence default |
|---|---|---|
| BRD / PRD / SOW | Direct text parse against the fact categories below | High — explicit statements are ground truth |
| User stories | Already semi-structured: `As a <role>, I want <action>, so that <goal>` maps directly to Actor/Action/Goal | High for the three named fields; the rest (rules, validation) is usually still implicit and must be inferred |
| Acceptance criteria | `Given/When/Then` maps directly to Trigger condition / Action / System response + Validation | High — but scope is narrow (one scenario), don't over-generalize a rule from one example |
| Specifications / documents / PDFs | Same technique as BRD/PRD; check for tables/appendices holding data schemas or business rules that prose sections omit | High for stated content; watch for stale sections that contradict newer ones |
| Screenshots | Structure is implied, not stated — infer IA, roles, and states from what's visible, but treat every business-logic conclusion drawn from a screenshot as inference, not fact | Medium at best; never High |
| Figma reference (a design file or link, not a written spec) | Same posture as Screenshots when only viewed visually — infer IA, components, and states from what's shown. If the file's own structure is actually inspectable (named layers, components, variants, auto-layout), that structural metadata is a stronger signal than a flat image and may be treated as Explicit for *what exists visually* (e.g. "a component named `Empty State` exists") — but any *business-logic* conclusion drawn from either form remains inference, never fact, exactly as for Screenshots | Medium when viewed as an image; Medium-High for structural facts (layer/component names, variants) when the file's own structure is inspectable — never High for business logic |
| Existing product (live/interactive) | Behavioral inference through interaction — click paths, error messages, and state changes are directly observable and outrank screenshot-only inference | Medium-High for observed behavior, Low for anything not actually exercised |
| Existing code | Reverse-engineer actual implemented rules directly from source — this is the *as-built* truth, which may differ from *intended* behavior; flag divergence between code behavior and any stated spec rather than silently trusting one over the other | High for what the code does, explicitly separate from what it was supposed to do |
| Plain-language requirement | The sparsest input — heaviest reliance on Rule 2 tiers 6–8 (domain conventions, best practices, assumptions). Extract what's said, then rely on `domain-classifier.md` and the relevant `product-types/*.md` overlay to fill structural gaps, tagged as assumptions | Low-Medium; expect most fields to carry an assumption tag |

Mixed inputs (e.g. a PRD plus screenshots of an existing product) are analyzed
with each input's own posture, then reconciled — where they agree, confidence
rises; where they conflict, the conflict is surfaced, not silently resolved by
picking one.

**A visual reference is analyzed twice, for two different things.** This
file extracts *business-logic* signal from a screenshot/Figma/existing-
product input (an implied validation rule, a permission, a status). At the
later Design Setup phase, `design-reference-engine/reference-analysis.md`
extracts *visual/interaction direction* (layout, color, spacing, component
style) from the very same input. Neither extraction substitutes for the
other, and a fact belongs to whichever category it actually is — a button's
label implies a business action (this file's concern); its rounded corners
imply a radius preference (that file's concern, never this one's).

## Fact-extraction categories — the 20-point checklist
Every input, regardless of type, is checked against all 20 items below. An item
with nothing found is a **gap**, recorded as such (see below) — never silently
skipped, and never left implicit because the input "looked like" it was only
about one thing (e.g. a screenshot set is not exempt from business-rule
extraction — see the rule below this table).

| # | Item | Extracted here (raw signal) as… | Deepened by |
|---|---|---|---|
| 1 | Business objective | Any stated or implied "why" behind a feature | `methodology/define.md` (business objective output) |
| 2 | User roles | Named or implied actors | `user-roles.md` |
| 3 | User goals | Stated outcomes a user wants | `methodology/empathize.md` (goals dimension) |
| 4 | Core problems | Stated or implied pain/friction | `methodology/empathize.md` (pain points), `methodology/define.md` (problem statement) |
| 5 | Core actions | Verb-level behaviors ("submit," "approve," "export") | `requirement-engine.md` (Action field) |
| 6 | Business rules | Stated or implied conditional logic | `business-logic.md` |
| 7 | Dependencies | Named prerequisite systems/data/teams | `dependency-analysis.md` |
| 8 | Backend assumptions | Unstated system behavior implied by a stated action (see below) | `business-logic.md` (derivation) |
| 9 | Validation | Stated or implied data-correctness rules | `business-logic.md` |
| 10 | Trigger conditions | Stated or implied "what causes this to happen" | `business-logic.md` |
| 11 | Status logic | Named states or implied lifecycle | `business-logic.md` |
| 12 | Permissions | Stated or implied access restriction | `user-roles.md` |
| 13 | Decision points | Stated or implied branching ("if approved... if rejected...") | `business-logic.md` |
| 14 | Operational workflow | The described end-to-end process | `business-logic.md` |
| 15 | Success conditions | What "worked" looks like per action | `business-logic.md` |
| 16 | Failure conditions | What "didn't work" looks like per action | `business-logic.md` |
| 17 | Edge cases | Boundary/exception scenarios mentioned or implied | `edge-case-engine.md` |
| 18 | Data requirements | Entities, fields, types, required/optional-ness | `requirement-engine.md` (Data-type requirements) |
| 19 | Integration assumptions | Named or implied external systems and their assumed behavior | `dependency-analysis.md` |
| 20 | Cross-module dependencies | Interactions between distinct modules/features | `dependency-analysis.md` |

## Rule: business logic extraction is never optional
A UI-focused input (a screenshot set, a Figma link, a description of "what the
screens should look like") is **not exempt** from items 6, 8, 9, 10, 11, 12, 13,
14, 15, 16. Every visible UI element implies business logic — extract it by
asking, for each element:
- A form field → what validates it (9), and is it required (18)?
- A submit/action button → what business rule permits it to fire (6, 12), what
  system response follows (system response, `requirement-engine.md`), what does
  success vs. failure look like (15, 16)?
- A status badge/label → what states exist, and what causes each transition
  (11, 10)?
- A conditional element (shown only sometimes) → what's the condition, and is it
  a permission (12) or a decision point (13)?

If the input truly contains no signal for one of these, that is a **gap**, not an
exemption — record it as a gap (below), and hand it to `business-logic.md` to
either derive a reasonable default (assumption-tagged) or flag as an open
question, per Rule 10 in `config/operating-rules.md`. Silently rendering a
"clean-looking" screen with no business logic behind it is the single most
common way this rule gets violated — it is explicitly forbidden.

## Gap detection
For every one of the 20 items with no signal in the input, record: which item,
which actor/action it would have applied to, and route it forward per the table
above rather than inventing content to fill it in at this stage — extraction
identifies gaps, it does not close them (closing a gap is
`business-logic.md`'s, `user-roles.md`'s, or `edge-case-engine.md`'s job,
each within its own assumption-tagging discipline).

## Confidence tagging
Every extracted fact carries one of: **Explicit** (a direct quote/observation),
**Inferred** (a reasonable reading of stated content, not a direct quote), or
**Assumed** (no signal at all; filled per Rule 2's lower tiers and tagged per
`config/output-contract.md`'s assumption format). This tag travels with the fact
into whichever downstream file deepens it.

## Loop position
Feeds the Intake phase and, at the feature-level loop
(`methodology/design-thinking.md`), re-runs whenever a Test finding routes back
to Empathize or Define because something was missed at extraction (e.g. an edge
case that was never surfaced, per that file's routing table).

## Explicitly not here
- Decomposing extracted actions into atomic REQ-tagged requirements →
  `requirement-engine.md`.
- Deriving the actual business rule/validation/workflow content →
  `business-logic.md`.
- Role/permission modeling → `user-roles.md`.
- Edge-case enumeration → `edge-case-engine.md`.
- Classifying the product's domain → `domain-classifier.md`.
- Extracting visual/interaction direction from the same reference input →
  `design-reference-engine/reference-analysis.md` (Design Setup phase).
