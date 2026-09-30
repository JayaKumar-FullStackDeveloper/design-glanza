# Auto-Recording

## Responsibility
What counts as a "significant" decision, and which existing phase-
completion points already trigger an ADR write — so "record significant
design decisions automatically" is a concrete trigger list, not a vague
expectation to remember to do it.

## The significance threshold
Reuses `design-research/research-engine.md`'s existing full-vs-
lightweight distinction rather than inventing a second one: a decision is
**significant** (gets a full `ADR-NNN`) when it meets any of:
- It resolves a genuine alternative (more than one structurally different
  option was actually in play) — `methodology/ideate.md`'s divergence
  step, or `methodology/design-judgment.md`'s pattern-level equivalent.
- It affects more than one screen/flow, or a shared component/token.
- It departs from a domain convention, a `component-registry/*` entry, or
  a closed token scale, with a stated reason (`design-tokens/token-
  inheritance.md`, `component-registry/registry-integration.md`).
- It supersedes a prior decision (`contradiction-prevention.md` — always
  significant by definition).
- Audit/Test surfaces a finding that changes an established decision
  rather than just fixing an execution defect (per `methodology/
  design-thinking.md`'s feedback-routing table — a finding that routes to
  Ideate or Define, specifically, per that file's own note that this
  "should be treated as a signal worth surfacing explicitly").

A decision that's none of the above (a single-screen, single-option,
convention-following choice) is **not** significant — it's recorded in
its own artifact as usual (a `screen-architecture.md` entry, a
`component-spec.md`) with no separate ADR, exactly as today. Forcing an
ADR for every micro-decision would make the memory index noise, not
signal — the same "do not optimize only for visual output" discipline
`evals/evaluation-rubric.md` already applies to scoring, applied here to
what's worth remembering.

## Trigger points — no new step, no new agent
An ADR is written at the same point the decision is already being
recorded in its own artifact — "automatically" means *as a byproduct of
existing work*, never a separate memory-writing pass bolted on after:

| Existing point | Agent | What triggers the ADR |
|---|---|---|
| Ideate's approach selection | (Ideate, no dedicated agent — `workflows/create-product.md`'s Empathize/Define/Ideate step) | The Chosen Approach itself, always significant |
| Architect's module/entity boundaries | `agents/product-architect.md` | A boundary decision with a real alternative considered |
| A named interaction-model choice | `agents/ux-architect.md` | Where `methodology/design-judgment.md`'s threshold was actually invoked |
| A token/component/register decision | `agents/design-system-expert.md`, `agents/ui-designer.md` | Per the significance criteria above |
| A registry-first "no match, new component" call | `agents/design-system-expert.md` | Always significant (component-registry/registry-integration.md) |
| A Baseline Update graduating to product-wide scope | Whichever agent approved it | Per `contradiction-prevention.md`'s graduation rule |
| An Audit finding that changes an established decision | `agents/qa-expert.md` | Per the significance criteria above |

## Explicitly not here
- The significance threshold's sibling (research depth) →
  `design-research/research-engine.md`.
- The record shape being written → `adr-schema.md`.
- What happens if a decision *should* have been recorded and wasn't →
  `config/quality-gates.md`'s **B21** (an undocumented significant
  decision surfaces at Audit as a gap, the same way an unlogged token
  deviation already does).
