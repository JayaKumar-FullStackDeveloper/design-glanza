# Scenario Types

## Responsibility
The 8 mandatory scenario types every `FLOW-NNN` is checked against, each
defined against its existing owning technique — never re-derived here. The
genuinely new thing is treating all 8 as a **required checklist per flow**,
the same discipline `ux-engine/state-design.md` already applies to its 13
mandatory states, applied here one level up, at the flow-walkthrough grain.

## The 8 types

| Type | What it walks | Owned by |
|---|---|---|
| **Primary** | The flow's main, no-deviation happy path, ENTRY through COMPLETION | `ux-engine/user-flow-engine.md`'s canonical notation; corresponds to `methodology/test.md` dimension 1 (Task completion) |
| **Alternate** | A named, valid, non-default DECISION branch that still reaches COMPLETION (a different but legitimate path — e.g. a saved-search entry point instead of manual filtering) | `ux-engine/user-flow-engine.md`'s Decision/branch definition |
| **Error** | A DECISION or SYSTEM RESPONSE that produces a Failure Condition | `product-intelligence/business-logic.md` §8, `product-intelligence/edge-case-engine.md`'s `EDGE-NNN`, `ux-engine/user-flow-engine.md`'s recovery paths, `ux-engine/state-design.md`'s `validation error`/`system error` states |
| **Empty** | A step whose data legitimately returns zero results | `ux-engine/state-design.md`'s `empty` state, `ux-engine/search-ux.md`'s zero-results handling |
| **Loading** | A step that fetches data the user is waiting on | `ux-engine/state-design.md`'s `loading` state |
| **Permission** | A step subject to a **Deny** or **Conditional** entry in the current role's permission matrix | `product-intelligence/user-roles.md`, `ux-engine/state-design.md`'s `permission denied` state, `ux-engine/navigation-system.md` item 13 |
| **Offline** | A network-dependent step walked with connectivity absent | `ux-engine/state-design.md`'s `offline` state — same applicability caveat: not every product runs in a context where connectivity can be absent |
| **Recovery** | A FAILURE POINT walked through to its stated resolution (retry / abandon-safely / escalate) to confirm it actually resolves, not just that a resolution is named | `ux-engine/user-flow-engine.md`'s Recovery paths section — this type *is* that section, exercised rather than only designed |

## Applicability rule
Not every type applies to every flow — apply the same zero-blank-cell,
stated-reason discipline `state-design.md` already uses for its own
mandatory-state set: for each flow, mark every type **applicable**
(produces a `SCENARIO-NNN`), **not-applicable** (with the reason — e.g. a
purely server-side batch flow has no Offline scenario because no UI step
is network-dependent in a client sense), or **deferred** (with the reason
and severity). A blank cell in the resulting `coverage-matrix.md` row is
never an acceptable final state.

## Priority interaction with state-design.md
Where a scenario type's applicable state can collide with another (e.g. a
step is both Loading and, once resolved, reveals Permission Denied),
`state-design.md`'s existing state-priority order governs which state
actually renders — this file does not define a second, competing priority
system; a scenario walk that finds the *wrong* state winning (e.g. a
spinner shown over content the user can't see) is a `continuity-audit.md`
finding citing that violation, not a new rule here.

## Explicitly not here
- The mandatory state set and priority order themselves →
  `ux-engine/state-design.md`.
- The recovery-path technique itself → `ux-engine/user-flow-engine.md`.
- How a `SCENARIO-NNN` record is structured →
  `scenario-model.md`, `templates/scenario.md`.
- Detecting that a required type has no flow coverage at all →
  `gap-detection.md`.
