# State Design

## Responsibility
Enumerate and behaviorally design every state a screen/component can be in —
the state *architecture* behind Rule 6's mandatory set
(`config/operating-rules.md`) — consuming
`product-intelligence/edge-case-engine.md`'s `EDGE-NNN` scenarios and
`product-intelligence/business-logic.md`'s state machines and failure
conditions. Visual treatment of a state is `ui-engine/*`'s concern.

## The mandatory states, defined precisely
Rule 6 names 13 states; each is distinct from its neighbors, and mixing two up
is a common design defect this file exists to prevent:

| State | Definition | Distinct from |
|---|---|---|
| **Initial** | First view before any user action — the default, blank starting point | `empty` (see below) |
| **Loading** | Existing data is being fetched, not yet available | `processing` (an action in progress, not a fetch) |
| **Success** | An action just completed and produced its expected result (usually transient) | `completed` (the persistent terminal state that follows) |
| **Empty** | A query/list legitimately has zero results after actually being checked | `initial` (never yet queried at all) |
| **Validation error** | User input failed a rule the user can see and correct | `system error` (nothing the user did wrong) |
| **System error** | Something failed outside the user's control (network, dependency) | `validation error`; cite `product-intelligence/dependency-analysis.md`'s failure-mode assumptions when the cause is an integration |
| **Permission denied** | Action blocked by `product-intelligence/user-roles.md`'s permission matrix (a **Deny**) | `system error` — this must communicate *why*, not fail silently or look like a bug |
| **Processing** | A longer-running action is being executed (a submission, a background job) | `loading` (fetching vs. acting) |
| **Completed** | The terminal success state of a workflow, matching `business-logic.md` §7's success condition and the flow's Completion step (`user-flow-engine.md`) | `success` (transient) |
| **Cancelled** | The user or system intentionally aborted before completion | `system error`/failure (intentional stop, not a fault) |
| **Conflict** | A concurrent-edit or concurrent-action collision (`edge-case-engine.md`'s concurrency category) | `system error` (this has a specific resolution path, not a generic failure) |
| **Timeout** | An action didn't resolve within its expected window — applicable specifically to actions that are network-, external-, or approval-dependent (per `business-logic.md`'s trigger analysis); not every action needs a timeout state | — |
| **Offline** | The client has no network connectivity, detected before (or independent of) any specific request — applicable specifically to actions that are network-dependent; not every product runs in a context where connectivity can be absent | `system error` (offline is a known, locally-detected precondition; system error is a failure reported *back* from a request that was actually sent); `timeout` (offline is usually detected before a request is even attempted, not after sending one and waiting) |

## State-priority rule
When more than one state could apply at once, resolve to whichever demands the
most urgent action from the user, roughly in this order (most urgent first):
**permission denied** → **system error** → **offline** → **conflict** →
**timeout** → **validation error** → **processing/loading** → **empty** →
**initial** → transient **success** → terminal **completed**/**cancelled**. A
screen showing a spinner (`loading`) over content the user has no permission
to see is wrong — permission denied wins.

## Recovery-path integration
Every state that can result from a failure (`validation error`, `system
error`, `permission denied`, `conflict`, `timeout`, `offline`) must specify which of
`user-flow-engine.md`'s three recovery resolutions it leads to — **retry**,
**abandon-safely**, or **escalate** — as part of this file's own output, not
left for `interaction-design.md` to improvise later. A `system error` state
with no stated recovery resolution is an incomplete state design, not an
acceptable stopping point.

## State enumeration rule
For every screen/component, run the full mandatory-state checklist above plus
any state added by the active `product-types/*.md` domain overlay, and mark
each cell: **designed** (behavior specified), **not-applicable** (with the
reason — e.g. `timeout` doesn't apply to an action with no external
dependency), or **deferred** (with the reason and the severity of leaving it
undesigned, per `config/output-contract.md`'s vocabulary). A blank cell is
never an acceptable final answer.

## Modeling technique: transitions and guards
Where a component's state count and interdependency make the priority rule
above easy to violate by omission (a complex multi-state workflow, not a
simple 3-state toggle), model it as an explicit state machine — named states,
named transitions between them, and a guard condition per transition (the
condition that must hold for that transition to fire) — rather than leaving
the priority rule to be honored by convention. Modeled this way, an invalid
combination (e.g. `loading` and `permission denied` simultaneously) becomes
structurally unrepresentable instead of merely undesirable, which is a
stronger guarantee than a documented rule a future screen might not
re-check. This is an implementation technique for enforcing this file's
existing state set and priority rule — it does not change which states exist
or their priority order.

## Handoff shape
This file's enumeration fills `templates/state-matrix.md` and is what
`scripts/validate-states.py` checks completeness against (the State Coverage
gate, `config/quality-gates.md` B7).

## Loop position
Consumes `edge-case-engine.md`'s `EDGE-NNN` scenarios and `business-logic.md`'s
state machines at the feature-level loop. Re-entered when a Test finding on
edge cases (dimension 8) or error prevention (dimension 4) traces to a missing
or wrongly-designed state, per `methodology/design-thinking.md`'s routing
table.

## Explicitly not here
- Identifying *what* edge cases exist in the first place →
  `product-intelligence/edge-case-engine.md`.
- Visual appearance of a given state → `ui-engine/*`.
- The state-matrix document structure → `templates/state-matrix.md`.
- The underlying entity lifecycle a state reflects →
  `product-intelligence/business-logic.md`.
