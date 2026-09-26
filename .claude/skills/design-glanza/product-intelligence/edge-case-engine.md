# Edge Case Engine

## Responsibility
Systematically enumerate edge cases (item 17 of `brd-analysis.md`'s checklist) —
the specific boundary/exception *scenarios* that instantiate the failure
categories `business-logic.md` names and the invalid transitions its state
machines leave off the valid graph. That file names *what kind* of thing can go
wrong; this file enumerates the *specific scenarios* that do.

## Edge case ID scheme
Every enumerated edge case gets a unique ID: **`EDGE-NNN`**, sequential.
`templates/state-matrix.md` cites edge cases by this ID against the screen/state
cell they apply to.

## Enumeration technique — by category
For every requirement (`requirement-engine.md`) and every entity's state
machine (`business-logic.md` §4), systematically check each category:

- **Boundary values** — zero, one, the maximum, one-past-the-maximum, negative
  where a negative shouldn't be possible, empty string vs. null vs. whitespace.
- **Empty/zero states** — the very first time this screen/list has no data yet,
  distinct from "no results after a filter."
- **Concurrency conflicts** — two actors acting on the same entity at once (two
  approvers, a record being edited while being viewed elsewhere).
- **Permission conflicts** — a role's access changes mid-action (demoted while
  midway through a form), or two roles' permissions collide
  (`user-roles.md`'s permission matrix has an unresolved overlap).
- **External-dependency failures** — an integration (`dependency-analysis.md`)
  is slow, unavailable, or returns something malformed.
- **Partial-completion states** — a multi-step process abandoned partway,
  reopened later, or interrupted by a connectivity loss.
- **Duplicate submission** — the same action submitted twice (double-click,
  retry after a slow response, replay of a queued action).
- **Invalid state transition** — every off-the-valid-graph transition
  `business-logic.md`'s state machine leaves undocumented (§4 of that file
  hands these here directly).
- **Timeout** — an action that doesn't resolve within an expected window, where
  "applicable" is judged by whether the action depends on anything
  network/external/human-approval-based (per Rule 6, `config/operating-rules.md`).
- **Data-format edge cases** — malformed, truncated, or unexpectedly-encoded
  input that passes a naive validation check but breaks a downstream assumption.

## Entity-lifecycle edge cases
Derived directly from `business-logic.md`'s state machines: for every state with
an "invalid-transition handling" note, this file produces the concrete `EDGE-NNN`
scenario(s) — e.g. `business-logic.md` names "attempted `pending → active`
without approval is invalid"; this file produces `EDGE-014`: *"a user with a
stale/cached view attempts to activate a still-pending record via a direct
action, bypassing the approval step visible in their UI."*

## Cross-role edge cases
What happens when two roles' actions collide, per `user-roles.md`'s model — two
approvers acting simultaneously, a delegate and the delegating role both acting
in the same window, a role's scope change mid-session invalidating an
in-progress action.

## Derived directly from failure conditions
For every failure condition `business-logic.md` §8 names (validation failure,
permission denial, external-dependency failure, conflict, timeout), this file
must produce at least one concrete `EDGE-NNN` scenario per category per
requirement it applies to — a failure *category* with zero enumerated scenarios
underneath it is an incomplete edge-case pass, not a "nothing to add" result.

## Severity/likelihood tagging
Every `EDGE-NNN` is tagged with severity (`config/output-contract.md`'s
Blocker/Major/Minor/Note vocabulary — reflecting how bad it is if unhandled) and
likelihood (how often this scenario will actually occur in operational reality,
per `methodology/empathize.md` dimension 11). Prioritization for what gets
designed first, versus logged as a known limitation, is severity × likelihood,
not severity alone — a Blocker-severity case with near-zero likelihood may be
consciously deferred, but only with that reasoning stated explicitly.

## Loop position
Consumes `business-logic.md`'s failure conditions and state machines at the
feature-level loop, feeds `ux-engine/state-design.md`'s state enumeration and
`templates/state-matrix.md` directly. Re-invoked when a Test finding reports an
edge case with no designed response (`methodology/test.md` dimension 8) — per
`methodology/design-thinking.md`'s routing table, this routes to Empathize if
the case was never surfaced at all, or back to this file/`state-design.md` if it
was surfaced but not designed for.

## Explicitly not here
- Deciding how an edge case is visually/behaviorally represented as a UI state →
  `ux-engine/state-design.md` (this file feeds it, doesn't do it).
- The underlying rule/lifecycle an edge case deviates from → `business-logic.md`.
- Test scenarios that verify edge-case *handling* once designed → `evals/test-cases.md`.
