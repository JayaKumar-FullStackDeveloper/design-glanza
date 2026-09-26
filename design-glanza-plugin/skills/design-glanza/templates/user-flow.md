# Template: User Flow

## Purpose
The document form of one `FLOW-NNN` — a task flow written in the canonical
entry→action→decision→system-response→next-action→completion notation, with
its recovery paths made explicit. Reusable across every domain: the notation
and recovery-resolution vocabulary are fixed regardless of what the flow
actually does.

## Required inputs
- `ux-engine/user-flow-engine.md`'s technique and notation.
- The `REQ-NNN`(s) and `ROLE-NNN` this flow serves.
- `product-intelligence/business-logic.md`'s triggers/decision points and
  `edge-case-engine.md`'s `EDGE-NNN` scenarios for this flow's scope.

## Output structure
- **Header** — per `config/output-contract.md`, plus the owning persona
  (`templates/user-persona.md`).
- **Trigger/entry point** — how the user arrives at this flow.
- **Goal/exit condition** — tied to a `templates/product-definition.md`
  success criterion.
- **Step sequence** — each step as Entry → Action → Decision → System
  response → Next action → Completion, branches named with every outcome.
- **Recovery paths** — one entry per failure point: `FAILURE POINT →
  RECOVERY ACTION(S) → RESULTING STATE` (retry / abandon-safely / escalate).
- **Cross-flow links** — where this flow hands off to/from another flow.

## Quality criteria
- Every decision branch names every outcome — a branch that trails off with
  no stated destination is an incomplete flow, not an acceptable ambiguity.
- Every step capable of producing a Failure Condition
  (`business-logic.md` §8) or a known `EDGE-NNN` has a corresponding recovery
  path — a failure point with no recovery path is a Blocker-severity defect
  (`config/output-contract.md`), not a minor gap.
- The Completion step matches a stated success condition, not an implied one.
- Checked against `config/quality-gates.md`'s **B3 — User-Flow
  Completeness** gate.

## Example structure
_Illustrative only — placeholders, not a real flow._

```
Trigger:    <actor> arrives with <precondition>
Goal:       <actor> has <outcome> when done

1. Action:      <actor> submits <input>
   Decision:    <condition>?
     -> yes:    system responds with <result A> -> Next action: <step>
     -> no:     system responds with <result B> -> Next action: <step>
2. Action:      <actor> confirms
   System response: <record> transitions to <status>
   Completion:  matches success criterion "<criterion>"

Recovery paths:
  <validation failure at step 1> -> retry -> back to step 1 with error shown
  <system error at step 2> -> escalate -> support-visible error state
```

## Traceability fields
Owns the `FLOW-NNN` scheme (assigned by
`product-intelligence/traceability.md`'s registry, produced by
`ux-engine/user-flow-engine.md`). Cites `REQ-NNN`, `ROLE-NNN`, and any
`EDGE-NNN` its recovery paths address.

## Explicitly not here
- Flow-derivation technique → `ux-engine/user-flow-engine.md`.
- Grouping flows into a navigable hierarchy →
  `templates/sitemap.md`.
- Micro-interaction/feedback timing within a step →
  `ux-engine/interaction-design.md`.
