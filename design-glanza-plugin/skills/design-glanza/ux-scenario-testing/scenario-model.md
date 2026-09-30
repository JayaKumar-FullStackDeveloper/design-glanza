# Scenario Model

## Responsibility
The `SCENARIO-NNN` ID scheme and the exact mapping between the
Goal/Entry/Steps/UI-interactions/System-response/Success/Failure framing
scenario testing is asked for in, and `ux-engine/user-flow-engine.md`'s
existing canonical notation. A Scenario is **not** a second flow-modeling
system — it is one FLOW-NNN, walked under one named scenario type
(`scenario-types.md`), reported in a shape built for testing rather than
for design.

## What a Scenario is
One `SCENARIO-NNN` = one `FLOW-NNN` × one scenario type, e.g. `FLOW-006`
walked as its **primary** scenario is a different `SCENARIO-NNN` than
`FLOW-006` walked as its **offline** scenario, even though both instantiate
the same underlying flow. A flow with three applicable scenario types (per
`scenario-types.md`'s applicability rule) produces three `SCENARIO-NNN`
records, not one record with three sub-cases buried inside it — each is
independently walkable, independently pass/fail, independently
traceable.

## Field-by-field mapping
Every field below is produced by an existing technique — this file
reformats it for a testing report, it does not re-derive it:

| Scenario field | Maps to | Owned by |
|---|---|---|
| User goal | The flow's user objective/JTBD | `methodology/define.md` output 3, `methodology/empathize.md` dimensions 3–4 |
| Entry point | ENTRY | `ux-engine/user-flow-engine.md`'s canonical notation |
| Steps | ACTION + DECISION, looped | `ux-engine/user-flow-engine.md`'s canonical notation |
| UI interactions | The concrete `SCREEN-NNN`/`COMPONENT-NNN` realizing each Action/Decision — **the one field this model adds**, since a flow names *what* the user does without necessarily binding it to *which* control on *which* screen does it | `templates/screen-architecture.md`, `ui-engine/component-system.md`, resolved against `component-registry/*` first (Rule 24) so the binding is to a reasoned, registered control, not an improvised one |
| System response | SYSTEM RESPONSE | `ux-engine/user-flow-engine.md`'s canonical notation |
| Success state | COMPLETION, matching the `completed` mandatory state | `ux-engine/user-flow-engine.md`, `ux-engine/state-design.md` |
| Failure state | A recovery path's FAILURE POINT, matching the relevant failure-branch mandatory state | `ux-engine/user-flow-engine.md`'s Recovery paths section, `ux-engine/state-design.md` |

The **UI interactions** field is the only genuinely new binding this model
introduces: a flow can be perfectly well-formed by
`user-flow-engine.md`'s own standard while still having a step with no
identified UI control realizing it — that gap is exactly what
`gap-detection.md` checks for, using this field as its anchor.

## Deriving scenarios from a BRD requirement
1. Start from the `FLOW-NNN` instance(s) already built for a `REQ-NNN`
   (`ux-engine/user-flow-engine.md`, `agents/ux-architect.md`'s output) —
   never derive a scenario directly from raw BRD text, skipping the flow
   that already models it; a scenario with no underlying `FLOW-NNN` is
   itself a gap (`gap-detection.md`).
2. For each applicable scenario type (`scenario-types.md`'s applicability
   rule), instantiate one `SCENARIO-NNN`, filling every field in the table
   above from the flow's own steps/branches — never inventing a step the
   flow doesn't already have.
3. Where the flow itself doesn't yet cover a scenario type that should
   apply (e.g. no recovery path exists for a step that can fail), that's a
   `gap-detection.md` finding against the flow, routed back to
   `agents/ux-architect.md`/`agents/interaction-designer.md` — the scenario
   is recorded as `open` with the gap named, never silently completed with
   an invented branch.

## Traceability
`SCENARIO-NNN` is a sideways reference in
`product-intelligence/traceability.md`'s model — the same category as
`BR-NNN`/`EDGE-NNN`/`DEP-NNN`/`RF-NNN` — cited from
`product-builder/ux/scenarios.md` and `ux/ux-coverage-matrix.md`, always
naming the `FLOW-NNN` (and therefore, transitively, the `REQ-NNN`/`ROLE-NNN`)
it instantiates. A `SCENARIO-NNN` with no traceable `FLOW-NNN` is invalid by
construction, per step 1 above.

## Explicitly not here
- The flow structure and canonical notation itself →
  `ux-engine/user-flow-engine.md`.
- The 8 scenario types and their applicability rule → `scenario-types.md`.
- Detecting a missing field/step → `gap-detection.md`.
- Walking a scenario's actual screen sequence for continuity →
  `continuity-audit.md`.
- The matrix roll-up and its gate → `coverage-matrix.md`.
