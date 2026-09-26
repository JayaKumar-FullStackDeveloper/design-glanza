# Business Logic

## Responsibility
Derive the rules, validation, triggers, status/lifecycle logic, decision points,
operational workflow, and success/failure conditions that govern how the domain
actually behaves — the "what happens when" behind every requirement. This is the
single largest concentration of the intake-analysis checklist
(`brd-analysis.md`'s items 6, 8, 9, 10, 11, 13, 14, 15, 16) because these items
are all facets of the same underlying thing: the rules of the system.

## Business rule ID scheme
Every derived rule gets a unique ID: **`BR-NNN`**, zero-padded, sequential.
Requirements (`requirement-engine.md`) cite a rule by this ID in their Business
Rule field rather than restating its content — one rule, cited from every
requirement it governs, so a rule change updates in one place.

## 1. Business rules (item 6)
**Derivation technique:** infer an implied rule from a stated requirement only
when the inference is load-bearing and specific — e.g. a requirement mentioning
"requires approval" implies an approval rule with at least: who can approve,
what triggers the need for approval, and what happens pending it. State the rule
as a condition → consequence pair: *"IF [condition] THEN [consequence]."*
Never infer a rule the source doesn't support just to fill a perceived gap —
an unsupported inference is an assumption (see §8 below), not a rule.

## 2. Validation (item 9)
For every Data-type requirement (`requirement-engine.md`) and every user-entered
field, derive: the condition that makes a value valid, and the resulting
behavior when it's not (block submission / warn but allow / auto-correct).
Distinguish **field-level** validation (this value, alone, must satisfy X) from
**cross-field** validation (this value must be consistent with that other
value — e.g. an end date after a start date). Cross-field rules are more often
missed by inspection alone — check every pair of fields that could plausibly
constrain each other before declaring validation complete.

## 3. Trigger conditions (item 10)
For every rule and every workflow step, name what causes it to fire. Distinguish
**explicit triggers** (the source states "when X happens, Y occurs") from
**inferred triggers** (implied by a described sequence but not named outright).
Common trigger types worth checking for even when not stated: user-initiated
action, scheduled/time-based, incoming event from another system
(`dependency-analysis.md`'s integration assumptions), and state-change-initiated
(one entity's transition triggers a rule on another).

## 4. Status logic (item 11)
Capture every entity's lifecycle as an explicit state machine:

| State | Entry trigger | Exit trigger(s) → next state(s) | Invalid-transition handling |
|---|---|---|---|
| e.g. `draft` | entity created | submitted → `pending`; deleted → *(terminal)* | — |
| e.g. `pending` | submitted from `draft` | approved → `active`; rejected → `rejected` | attempted `pending → active` without approval is invalid — routed to `edge-case-engine.md` |

Every state needs at least one documented exit; a state with no way out is
either genuinely terminal (mark it so explicitly) or a gap. Every *invalid*
transition a determined or careless actor could attempt is handed to
`edge-case-engine.md` for enumeration — this file names the valid graph, that
file enumerates what happens off of it.

## 5. Decision points (item 13)
For every described process, identify every point where the outcome branches on
a condition — every implicit "if approved… if rejected…" moment. For each: name
the condition precisely, name every branch's outcome, and confirm every branch
actually goes somewhere (a decision point with a branch that silently leads
nowhere is a gap, not an edge case — it means the process itself is incomplete).

## 6. Operational workflow (item 14)
Connect the decision points (5) and state transitions (4) for a given process
into one coherent, ordered narrative — start condition through terminal
state(s), naming every actor (`user-roles.md`) involved at each step. This is
what makes the rules legible as a *process*, not just a scattered rule list, and
is what `ux-engine/user-flow-engine.md` will later structure into an actual user
flow.

## 7. Success conditions (item 15)
For every requirement/action, state explicitly what "this worked" means: the
resulting system response and the resulting status (per §4). A success
condition that isn't specific enough to check mechanically
(`methodology/test.md`'s task-completion dimension) is not yet complete.

## 8. Failure conditions (item 16)
For every requirement/action, state explicitly what "this didn't work" means —
paired directly with its success condition (7), not treated as an afterthought.
A failure condition names the failure *category* (validation failure,
permission denial, external-dependency failure, conflict, timeout); the specific
*scenarios* that produce each category are enumerated one level down, in
`edge-case-engine.md`, which consumes this section directly.

## Backend assumption derivation (item 8)
When `brd-analysis.md` flags a gap — a stated action with no described backend
behavior — this file is where the reasonable default gets proposed: e.g. "the
input implies emails must be unique; assume this is enforced at the data layer,
not just the form." State the assumption using
`config/output-contract.md`'s tag format, including impact ("if not actually
enforced at the data layer, duplicate accounts become possible under
concurrent signups"). Never let an inferred backend behavior travel downstream
without its tag — a requirement or rule built on an untagged backend assumption
is the exact failure mode Rule 10 (`config/operating-rules.md`) exists to
prevent.

## The explicit-vs-assumed boundary
Every rule, validation condition, trigger, status, decision point, and
success/failure condition above is tagged **Explicit** (directly stated),
**Inferred** (a specific, load-bearing reading of stated content), or
**Assumed** (no signal at all — filled per Rule 2's lower tiers). This is the
same three-way tag `brd-analysis.md` uses; it travels forward with the rule (by
`BR-NNN` ID) into every requirement that cites it.

## Loop position
Consumes `brd-analysis.md`'s raw facts (items 6, 8–11, 13–16) at the
feature-level loop, and is **re-invoked directly** whenever
`methodology/test.md` reports a business-rule-incorrectness finding — per
`methodology/design-thinking.md`'s routing table, that finding routes to Define
*and* this file, because it means a rule was derived wrong, not just built
wrong.

## Explicitly not here
- The assumption tag format/protocol itself → `config/output-contract.md`.
- Enumerating the specific edge-case scenarios a failure condition or invalid
  transition produces → `edge-case-engine.md`.
- Representing a state transition as a UI state → `ux-engine/state-design.md`.
- Role-based access to a given rule/workflow → `user-roles.md`.
- Turning a workflow into a structured user flow → `ux-engine/user-flow-engine.md`.
