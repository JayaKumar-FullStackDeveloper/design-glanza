# Ideate

## Responsibility
Generate genuinely different solution directions and select one using evidence
from Empathize and Define — not designer preference, and not the first idea that
comes to mind. This phase's output is a chosen *approach*, not a screen.

## 1. Identify multiple solution approaches
Divergence technique: generate at least three structurally different directions
per product objective — different *interaction models*, not variations on one
layout. E.g. for "let a user resolve a billing dispute": (a) a guided wizard,
(b) a self-service form with inline account context, (c) a chat-style guided
conversation. Three visually different mockups of the same wizard is not
divergence; three different interaction models is.

**Checkable divergence rule:** name the axis each approach differs on
(interaction model, density, guidance level, synchronous vs. asynchronous,
etc.) and confirm no two approaches share the same position on every named
axis — if two "different" approaches are actually the same interaction model
with a different layout, that is not genuine divergence, it is one direction
presented twice. This is the concrete test for step 8's scoring to be
meaningful: scoring three restatements of one idea against each other cannot
produce a real selection.

## 2. Compare interaction models
For each approach, name its core interaction model explicitly (wizard / single-
page inline-edit / bulk-table-action / conversational / direct-manipulation /
dashboard-drill-down / etc.) and map it against Empathize's findings for the
actor it serves:
- **Frequency** (dimension 7): a rarely-performed task favors a guided model
  (wizard, conversational) that doesn't rely on the user remembering how last
  time; a frequently-performed task favors a fast model (inline-edit, bulk,
  keyboard-driven) that a guided model would slow down.
- **Environment** (dimension 8): a field/mobile/interrupted context favors a
  model tolerant of interruption (savable partial progress) over one requiring
  sustained, uninterrupted attention.
- **Decision-making** (dimension 10): a decision requiring escalation/approval
  favors a model with an explicit hand-off step, not one implying the user acts
  alone.

## 3. Consider efficiency
Count steps-to-completion for each approach against the primary flow. Weight this
count by frequency (dimension 7): an extra step costs more on a daily action than
on a once-a-year one. An approach that's more steps but only used rarely can still
win on other criteria; an approach that adds steps to a high-frequency action
needs a strong justification on another criterion to survive.

## 4. Reduce cognitive load
Estimate the working-memory demand of each approach: how many decisions must the
user hold in mind at once, and how many information sources must they consult
simultaneously to make each one? An approach requiring the user to remember a
value from step 2 while acting on step 5 has higher cognitive load than one that
keeps needed information visible at the point of decision — this is evaluated
before any prototype exists, as a property of the approach itself.

## 5. Consider scalability
Ask how each approach holds up as data or users grow, not just at today's
example scale — a card-grid browsing pattern comfortable at 10 items can be
unusable at 10,000; a flat permission list workable for 5 roles can collapse at
50. Flag approaches with poor scale characteristics at ideation, before
`product-intelligence/dependency-analysis.md` and later screens are built around
a pattern that has to be re-thought.

## 6. Consider accessibility
Ask whether the interaction model has an accessible equivalent *by construction*
— not whether it can be patched later. Drag-and-drop-only reordering has no
keyboard equivalent unless paired with an alternative from the start; a
model that depends entirely on hover-to-reveal has no touch equivalent. An
approach failing this check is flagged now, per Rule 7 in
`config/operating-rules.md` (accessibility is part of the design, not a final
decoration) — this is the ideation-time enforcement of that rule, before
`ux-engine/accessibility.md`'s detailed structural rules even apply.

## 7. Consider implementation complexity
A lightweight build-cost estimate per approach: how many new components, new
states, or new dependencies does it introduce relative to the others? This is a
coarse signal to inform selection, not the detailed graph —
`product-intelligence/dependency-analysis.md` produces that later, at Architect,
for the approach actually selected.

## 8. Select patterns based on evidence and context
Before scoring, sort the criteria in play into two kinds: a **threshold**
criterion is a hard pass/fail (the accessibility check in item 6 is always
one — an approach either has an accessible equivalent by construction or it's
out of contention, never "mostly accessible enough"); a **trade-off**
criterion is genuinely weighed against the others (steps-to-completion,
cognitive load). Mixing the two — letting a should-be-disqualifying failure
get "outweighed" by a strong score elsewhere — is a common, avoidable
failure of this step; keep threshold failures out of the weighing entirely.

Score every remaining approach against criteria 3–7 plus fit to Define's
success criteria and Empathize's operational reality (dimension 11), and
select explicitly — record which approach was chosen, which were rejected,
and *why*, in the same traceable form as any other decision (per Rule 9,
`config/operating-rules.md`). "We went with the wizard because it best fits
infrequent use and the user's decision-making constraint" is a selectable,
falsifiable rationale; "the wizard felt cleaner" is not evidence and does not
satisfy this step.

**Rejected approaches are half of this step's output, not a footnote.** For
each one, record what it was actually testing (which criterion it would have
served best), the specific criterion that broke against it, and what would
have to change for it to become the right call later (e.g. "the self-service
form loses on decision-making support today; if this workflow's approval
requirement is ever removed, it becomes the frontrunner"). A rejected
approach recorded only as "not selected" with no reason is exactly as
incomplete as a selected one recorded without rationale.

**A near-tie is a priority problem, not a design problem.** If two approaches
score close enough that the choice is genuinely ambiguous against the
criteria above, that ambiguity does not average away by picking the
higher-scoring one anyway — it means the criteria themselves haven't been
weighted against this product's actual priorities yet. Escalate for an
explicit priority call (which criterion matters more here, and why) rather
than resolving a tie silently.

## Constraint injection
Before scoring, eliminate any approach that outright violates a constraint from
`define.md` output 5 (product/technical/business) or fails the accessibility
check (item 6 above) — infeasible approaches are removed before scoring, not
scored down and left in contention.

## Output
The chosen approach with its full rationale (what was selected, what was
rejected, and why) — handed to Architect for module/entity shaping and to
`prototype.md` for structural realization. Ideate does not produce screens.

## Loop position
- **Entered from:** `define.md`'s handoff (product objective + constraints), or
  re-entered when a Test finding routes here per
  `methodology/design-thinking.md`'s routing table — specifically a usability or
  scalability failure traced to the interaction model itself (not its execution),
  or an accessibility failure with no accessible equivalent possible within the
  chosen model.
- **Hands off to:** Architect (module/entity shaping,
  `product-intelligence/dependency-analysis.md`) and `prototype.md` (structural
  realization of the chosen approach).

## Explicitly not here
- Turning a chosen direction into system/module architecture →
  `product-intelligence/dependency-analysis.md` + Architect phase.
- Turning a chosen direction into flows/screens → `ux-engine/*`, orchestrated by
  `prototype.md`.
- Fidelity/prototyping decisions → `prototype.md`.
