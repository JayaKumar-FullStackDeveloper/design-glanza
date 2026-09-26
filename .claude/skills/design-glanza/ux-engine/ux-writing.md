# UX Writing

## Responsibility
What the interface's words say, as distinct from every other `ux-engine/*`
file's concern with structure and behavior — the missing layer between a
correctly-designed state (`state-design.md`) or flow (`user-flow-engine.md`)
and what a user actually reads at that moment. No other file in this folder
owns wording; each cites this one rather than improvising copy inline.

## Error-message formula
Every error message (`state-design.md`'s `validation error`/`system error`
states, `form-design.md`'s field-level errors) states three things, in
order: **what happened** (specific, not "an error occurred"), **why**
(the actual cause, in plain language — not an internal error code standing
alone), and **what to do next** (the concrete recovery action, matching
`user-flow-engine.md`'s retry/abandon-safely/escalate resolution for that
state). A message with only the first part ("Invalid input") and none of the
other two is incomplete regardless of how accurately it names the problem.

## Voice vs. tone
**Voice** is constant across the whole product — the product's underlying
personality, set once. **Tone** shifts by situation while voice stays the
same — the same product sounds measured in a `system error` state and can
sound warmer in a `completed`/celebration state, without becoming a
different product in either. Confusing the two produces either a flat
product (no tone variation ever) or an inconsistent one (voice itself
seems to change state to state).

## Tone by state
A concrete tone posture per state (`state-design.md`), so copy isn't
improvised fresh each time a state is written:

| State | Tone posture |
|---|---|
| `loading` | Neutral, brief — don't editorialize about a wait the user is already experiencing. |
| `empty` | Helpful and forward-looking — state what's missing and what action fills it, never apologetic filler. |
| `validation error` | Direct and specific — the user can fix this themselves right now; don't soften it into vagueness. |
| `system error` | Calm, not alarmed — the user didn't cause this; avoid language that implies blame or catastrophe when the actual impact is minor. |
| `success` | Brief, no exclamation marks by default — reserve stronger affect for a genuinely significant `completed` milestone, not routine confirmations. |
| onboarding / first-run | Encouraging, oriented toward the next concrete step — never a wall of feature description. |

After an error specifically, allow a brief pause (roughly 300–600ms) before
the next prompt/input is offered, rather than immediately re-presenting the
same interaction at full speed — this mirrors `interaction-design.md`'s
asymmetric-timing principle (slow where the user is absorbing something,
fast where the system is merely responding), applied to the *pacing* of
copy delivery rather than a visual transition.

## Call-to-action wording
A CTA is verb-first and specific to what actually happens next ("Save
changes," "Send invite") rather than a generic label ("Submit," "OK",
"Continue") that could belong to any action in any product — this is the
copy-level instance of `ui-engine/craft-critique.md`'s specificity test,
applied to a single button rather than a whole screen. Word the CTA to match
the *user's* intent for taking the action, not the business's internal name
for the process behind it (a user "sends an invite," they don't "trigger the
invitation workflow"). Exactly one CTA per screen reads as primary per
`visual-hierarchy.md`'s rule — this file governs that CTA's wording, not
whether it exists or how prominent it looks.

## Content-realism (cross-reference)
`product-types/landing-page.md`'s content-realism check (no placeholder
content, no fabricated proof, copy grounded in a specific claim) is this
file's discipline applied to persuasion-surface copy specifically — cited
there, not restated here, since it's already scoped to that product type.

## Handoff shape
Consumed inline wherever `state-design.md`, `form-design.md`,
`interaction-design.md`, or `component-system.md`'s Content rules need actual
wording rather than a behavioral description — this file supplies the words,
those files supply where/when/how they appear.

## Loop position
Consumes the state/flow/component structure already decided at the
feature-level loop. Re-entered when a Test finding on feedback or usability
(`methodology/test.md` dimensions 5, 2) traces to unclear or mistoned copy
rather than the underlying state/behavior design, per
`methodology/design-thinking.md`'s routing table.

## Explicitly not here
- Which states exist and when they trigger → `ux-engine/state-design.md`.
- Where an error appears and its timing → `ux-engine/form-design.md`,
  `interaction-design.md`.
- Visual treatment of text (size, weight, color) → `ui-engine/typography.md`,
  `visual-hierarchy.md`.
- Content-truncation and empty-content fallback rules → `ui-engine/
  component-system.md`'s Content rules.
