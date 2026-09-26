# User Flow Engine

## Responsibility
Transform analyzed requirements (`REQ-NNN`) and derived workflow logic
(`product-intelligence/business-logic.md`'s triggers, decision points, and
success/failure conditions) into **user journeys** and **task flows** — the
structural realization of `methodology/prototype.md`'s output 1. This file also
owns the canonical flow-step notation and the recovery-path technique every
other flow in the product must follow, and the eight optimization criteria the
whole UX engine is measured against.

## Journeys vs. flows
- **User journey** (macro) — a named sequence of flows spanning time toward one
  overarching goal, built from `methodology/empathize.md`'s jobs-to-be-done and
  goals dimensions (e.g. an "Onboarding Journey" = signup flow → first-project-
  setup flow → invite-teammate flow). Journeys are what make cross-flow
  continuity intentional instead of accidental.
- **Task flow** (micro) — one discrete, single-sitting task: one entry
  condition, one completion condition. Most of this file's technique operates at
  this grain.

## FLOW ID scheme
Every task flow gets a `FLOW-NNN` ID, per the scheme owned by
`product-intelligence/traceability.md`. A journey is recorded as an ordered list
of `FLOW-NNN` references, not a separate ID space.

## The UX Engine optimization criteria
Every decision made anywhere in `ux-engine/*` is checked against these nine
criteria. They are defined once, here, because this is the first file that
structures raw requirements into anything a person experiences — every sibling
file in this folder cites these by name rather than restating them.

1. **Cognitive-load reduction** — minimize how many decisions and information
   sources the user must hold in mind at once at any single step (the same
   estimate technique as `methodology/ideate.md`, now applied per flow step
   rather than per approach).
2. **Fast decision-making** — minimize the time/effort a step demands to choose
   the next action; surface a default or recommended path wherever a business
   rule permits one, rather than presenting an undifferentiated list of equal
   options.
3. **Information prioritization** — show only what's needed for the *current*
   decision; defer secondary information via progressive disclosure instead of
   surfacing everything at once "just in case."
4. **Minimal user effort** — minimize step count and never require re-entry of
   information the system already has (context should pre-fill, not be
   re-asked). Effort here means **extraneous** complexity only — steps that
   exist because of how the flow was built, not because the underlying task
   genuinely requires them. **Inherent** complexity (a task that is
   irreducibly multi-step, e.g. reconciling a multi-line invoice) cannot be
   wished away by this criterion; it can only be deliberately assigned —
   handled by the system where the system has the information to do so, left
   to the user where only they can supply the judgment or authority a step
   requires. Naming which kind of complexity a step actually is prevents
   cutting a step that was never removable in the first place.
5. **Error prevention** — a flow should make an invalid action unavailable
   rather than allow it and then reject it after the fact (concretized further
   in `interaction-design.md` and `form-design.md`).
6. **Accessibility** — every flow must have a complete non-visual,
   keyboard-operable equivalent path (concretized in `accessibility.md`).
7. **Scalability** — a flow must not degrade as data, users, or roles grow; a
   flow assuming "a handful of items" that breaks at real scale is a design
   defect caught here, at the flow level, not discovered later in Test.
8. **Operational clarity** — at every step, the user must be able to answer
   "what state am I in, and what happens next" (concretized in
   `state-design.md` and `interaction-design.md`'s feedback rules).
9. **Emotional arc** — a flow is remembered disproportionately by its peak
   moment (the point of highest stakes or highest delight) and its ending, not
   by its average step — independent of how operationally sound every
   individual step is. Two concrete consequences: never let a flow's last step
   be an error, an administrative confirmation, or a dead-end screen — route
   to a genuine completion/success state (`state-design.md`'s `completed`)
   even when the underlying transaction finished a step earlier; and invest
   disproportionate design attention in whichever single step is this flow's
   peak (the moment of highest risk, effort, or payoff), since a flawless
   surrounding flow doesn't offset a badly-handled peak. This criterion
   evaluates the flow's *shape as remembered*, which criteria 1–8 (each
   evaluating operational soundness) do not capture on their own.

## The canonical flow-step notation
Every important workflow is written in exactly this form — six named parts, in
order, looped as needed:

```
ENTRY → ACTION → DECISION → SYSTEM RESPONSE → NEXT ACTION → COMPLETION
```

- **Entry** — the condition/trigger that puts the user at the start of this
  flow (cite the `BR-NNN` trigger from `business-logic.md` §3 that applies).
- **Action** — what the user does.
- **Decision** — any branch point, whether it's the user choosing between
  options or a business rule being evaluated (`business-logic.md` §5's decision
  points, item 13) — name the condition and every branch's outcome; a branch
  with no named outcome is an incomplete flow, not an acceptable ambiguity.
- **System response** — the immediate, observable result (this is exactly the
  System Response field on the `REQ-NNN` this step realizes).
- **Next action** — what the user does following that response — typically
  loops back into another Action/Decision pair until Completion.
- **Completion** — the terminal state, matching a Success Condition
  (`business-logic.md` §7) and traceable to a `methodology/define.md` success
  criterion.

A flow with steps that don't fit this notation cleanly is usually a sign the
requirement backing it wasn't atomic (`product-intelligence/requirement-engine.md`'s
decomposition rule) — split it rather than forcing an awkward fit.

## Recovery paths
For every Decision or System Response capable of producing a Failure Condition
(`business-logic.md` §8) or an enumerated edge case (`EDGE-NNN`,
`product-intelligence/edge-case-engine.md`), the flow must define an explicit
recovery path — never leave a failure as a dead end:

```
FAILURE POINT → RECOVERY ACTION(S) AVAILABLE → RESULTING STATE
```

Every recovery path resolves to exactly one of: **retry** (return to the same
Action with the failure's cause addressed), **abandon-safely** (return to a
known-good prior state with no data loss beyond what the user chose to
discard), or **escalate** (hand off to another actor/role per
`product-intelligence/user-roles.md`, e.g. a system error routes to support).
A recovery path that leaves the user with no path forward and no path back is
a Blocker-severity defect (`config/output-contract.md`), not an acceptable edge
case.

## Branch handling for role variation
The same requirement can produce structurally different flows per role
(`product-intelligence/user-roles.md`) — do not force one flow to serve every
role through conditional steps if the roles' paths genuinely diverge; produce
separate `FLOW-NNN` instances instead, each still traceable to the same
`REQ-NNN` (per `product-intelligence/traceability.md`'s REQ×USER trace rows).

## Handoff shape
Flows fill `templates/user-flow.md` and are consumed by
`information-architecture.md` (to determine what screens/sections must exist)
and `navigation-system.md` (to determine how a user reaches and moves between
them).

## Loop position
Entered from `methodology/ideate.md`'s chosen approach at the feature-level
loop. Re-entered when a Test finding routes here per
`methodology/design-thinking.md`'s routing table — task-completion failures
(if Define's problem framing still holds, meaning the flow itself needs
rework) and any finding revealing a missing recovery path.

## Explicitly not here
- The document structure for a flow deliverable → `templates/user-flow.md`.
- Grouping flows into a navigable hierarchy → `information-architecture.md`.
- Which nav pattern exposes a flow's entry point → `navigation-system.md`.
- Micro-interaction/feedback timing within a step → `interaction-design.md`.
- The states a step's screen can be in → `state-design.md`.
