# Template: Decision Record (ADR)

## Purpose
One `ADR-NNN` — a significant product/UX/UI/architecture decision,
persisted in the exact shape `product-memory/adr-schema.md` defines.

## Required inputs
- `product-memory/auto-recording.md`'s significance test (confirm this
  decision actually warrants a full ADR before writing one).
- The relevant phase file's own reasoning (`methodology/ideate.md`,
  `design-judgment.md`, or the owning agent's own analysis procedure) —
  this template persists that reasoning, it doesn't redo it.

## Output structure
Exactly `adr-schema.md`'s record shape:
```
ID: ADR-NNN
Context: <situational facts>
Problem: <what's being decided>
Decision: <what was decided>
Reason: <the trade-offs actually weighed>
Alternatives considered: <each alternative + why not, never omitted>
Impact: <expected outcome>
Status: <proposed | accepted | superseded | rejected | deprecated>
Supersedes: <ADR-NNN, if applicable>
Superseded by: <ADR-NNN, if applicable>
Related: <REQ-NNN, FLOW-NNN, SCREEN-NNN, COMPONENT-NNN, ...>
Recorded: <pass/date, agent>
```

## Quality criteria
- Every field filled — "Alternatives considered" is never blank for a
  decision that had a real alternative (per the significance test itself
  requiring one existed).
- At least one `Related` citation — an ADR governing nothing traceable is
  mis-scoped (`adr-schema.md`).
- A `superseded` status always pairs with a `Superseded by` value; a
  `Supersedes` value always points to a real, existing `ADR-NNN` whose own
  Status is updated to `superseded` in the same edit.
- Checked against `config/quality-gates.md`'s **B21**.

## Example structure
_Illustrative, domain-neutral — not real product content._

```
ID: ADR-004
Context: Payment submission is a one-shot, irreversible action; the
  provider's API is synchronous with no reliable partial-success state.
Problem: Should submission use Optimistic UI (interaction-design.md) or
  wait for confirmation?
Decision: Wait for explicit confirmation before showing success.
Reason: interaction-design.md's Optimistic UI section reserves that
  pattern for low-risk, highly-predictable, reversible actions; payment
  submission is high-risk and irreversible, failing the reversibility x
  risk matrix's threshold outright (a threshold criterion, not a
  trade-off one, per ideate.md item 8).
Alternatives considered: Optimistic UI with rollback - rejected; a
  rolled-back "your payment failed" after showing "payment successful"
  is worse than a slightly slower confirmed success, for this specific
  action's stakes.
Impact: Submission has a visible processing state (per interaction-
  design.md's >1s feedback rule) between action and confirmation.
Status: accepted
Related: REQ-041, FLOW-014, SCREEN-022, COMPONENT-004
Recorded: Pass 2, agents/interaction-designer.md
```

## Traceability fields
`ADR-NNN` is a sideways reference in `product-intelligence/
traceability.md`'s model, cited from every `Related` artifact.

## Explicitly not here
- The status lifecycle's own definitions → `product-memory/adr-schema.md`.
- The supersession protocol → `product-memory/contradiction-prevention.md`.
