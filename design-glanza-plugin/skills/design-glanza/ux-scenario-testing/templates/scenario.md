# Template: Scenario

## Purpose
One `SCENARIO-NNN` record — one `FLOW-NNN` walked under one scenario type
(`ux-scenario-testing/scenario-types.md`), per the field mapping in
`ux-scenario-testing/scenario-model.md`.

## Required inputs
- The `FLOW-NNN` instance this scenario instantiates
  (`product-builder/ux/user-flows.md`).
- `product-builder/ux/screen-architecture.md`, `navigation.md`,
  `state-matrix.md` — for the UI interactions field and for
  `gap-detection.md`'s cross-checks.

## Output structure

```
ID: SCENARIO-NNN
Flow: FLOW-NNN
Type: <Primary | Alternate | Error | Empty | Loading | Permission | Offline | Recovery>
Requirement(s): REQ-NNN [, REQ-NNN...] (via the flow's own trace record)
Role: ROLE-NNN

User goal: <the flow's own user objective>
Entry point: <ENTRY, per user-flow-engine.md>

Steps:
  1. Action: <what the user does>
     UI interaction: SCREEN-NNN / COMPONENT-NNN
     System response: <SYSTEM RESPONSE>
  2. Decision: <the branch, named>
     UI interaction: SCREEN-NNN / COMPONENT-NNN
     System response: <SYSTEM RESPONSE>
  [repeat per step]

Success state: <COMPLETION, matching the `completed` mandatory state>
Failure state: <the FAILURE POINT this scenario type exercises, if
  applicable — n/a for Primary/Alternate>
Recovery resolution: <retry | abandon-safely | escalate — required for
  Error/Recovery types>

Gap findings: <gap-detection.md findings, or "none"?>
Continuity findings: <continuity-audit.md findings, or "none"?>

Status: <covered | gap | deferred | not-applicable>
```

## Quality criteria
- Every step's UI interaction field is filled — a step with no bound
  `SCREEN-NNN`/`COMPONENT-NNN` is itself a `gap-detection.md` finding, not
  left blank.
- Error/Recovery-type scenarios always state a Recovery resolution; a
  blank one fails `config/quality-gates.md`'s **B17**.
- Status is never silently `covered` while an open Blocker/Major finding
  exists against it.

## Example structure
_Illustrative, domain-neutral — not real product content._

```
ID: SCENARIO-013
Flow: FLOW-006
Type: Error
Requirement(s): REQ-014
Role: ROLE-002 (Manager)

User goal: Approve a pending request without losing track of which ones
still need review.
Entry point: Manager opens the Pending Approvals list.

Steps:
  1. Action: Manager selects a request and clicks Approve.
     UI interaction: SCREEN-011 / COMPONENT-004 (Approve button)
     System response: System validates the request still has status
       "Pending" (concurrent-edit check).
  2. Decision: Has the request already been actioned by another approver?
     UI interaction: SCREEN-011 (inline conflict banner)
     System response: If yes, reject the action with a Conflict state.

Success state: n/a (this scenario exercises the failure branch)
Failure state: Conflict — request was already actioned by another approver.
Recovery resolution: retry (re-fetch the current list; the stale row is
  removed automatically).

Gap findings: none.
Continuity findings: none — conflict banner clearly states what happened
  and offers a single "Refresh list" action (no ambiguous CTA).

Status: covered
```

## Explicitly not here
- The scenario-type definitions → `ux-scenario-testing/scenario-types.md`.
- The matrix these records roll up into → `templates/ux-coverage-matrix.md`.
