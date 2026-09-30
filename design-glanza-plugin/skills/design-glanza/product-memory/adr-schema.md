# ADR Schema

## Responsibility
The `ADR-NNN` record shape and status lifecycle — the persisted form of
`methodology/design-thinking.md`'s existing 9-step design decision
framework (Problem → Context → User Need → Constraints → Alternatives →
Trade-offs → Selected Approach → Expected Outcome → Validation), which
that file explicitly states is a *review/conversation* walkthrough, not a
stored artifact. An ADR is that same chain, finally given an ID, a
status, and a durable home.

## Field-by-field mapping onto the existing framework
Nothing below is a new reasoning technique — every field is produced by
the phase file the existing framework already cites:

| ADR field | Maps to (`design-thinking.md`'s framework) | Produced by |
|---|---|---|
| ID | — (new: `ADR-NNN`) | This file's own scheme |
| Context | Context (Empathize dimensions 6–8) | `methodology/empathize.md` |
| Problem | Problem (Define output 1) | `methodology/define.md` |
| Decision | Selected Approach (Ideate item 8) | `methodology/ideate.md`, or the owning agent for a narrower-scope decision |
| Reason | Trade-offs (Ideate items 3–7) | `methodology/ideate.md`, `methodology/design-judgment.md` for a pattern-level decision |
| Alternatives considered | Alternatives (Ideate item 1) | `methodology/ideate.md`'s divergence step, including its **rejected-approaches register** — never omitted |
| Impact | Expected Outcome (Define output 8) | `methodology/define.md` |
| Status | — (new: see lifecycle below) | Set and updated by whichever agent owns the decision |
| Related requirements/screens/components | — (new field, the traceability hook) | `REQ-NNN`/`FLOW-NNN`/`SCREEN-NNN`/`COMPONENT-NNN` citations |

**Validation** (the framework's 9th step) is deliberately **not** a field
on the ADR itself — it's `methodology/test.md`'s Test-phase evaluation,
already a separate, re-run-many-times activity; folding it into the ADR
would make the record stale the moment a re-test ran. Instead, an ADR's
Status field is what Test/Audit findings update (see lifecycle below).

## Status lifecycle
| Status | Meaning |
|---|---|
| **proposed** | Decision reasoned through, not yet acted on — rare; most ADRs are recorded once a decision is already being executed, per `auto-recording.md` |
| **accepted** | The decision is in effect — the default status for a recorded, executed decision |
| **superseded** | A later `ADR-NNN` explicitly replaced this one — the record stays, it is never deleted (Rule 13); the new ADR's own **Supersedes** field names this one |
| **rejected** | Considered and explicitly not chosen — the record of a rejected alternative, kept for exactly the reason `ideate.md` step 8 already states: "what would have to change for it to become the right call later" |
| **deprecated** | No longer relevant because the requirement/screen/component it governed was removed, not because it was wrong |

A **superseded** ADR is never edited to look like it agreed with what
replaced it — the original Decision/Reason text stays exactly as
recorded; only the Status field and a new `Superseded by: ADR-NNN`
citation are added.

## Record shape
```
ID: ADR-NNN
Context: <situational facts, per Empathize dimensions 6-8>
Problem: <the problem being decided, per Define output 1>
Decision: <what was decided>
Reason: <why, citing the trade-offs actually weighed>
Alternatives considered: <each alternative + why it wasn't chosen, per
  ideate.md's rejected-approaches register — never omitted>
Impact: <expected outcome, per Define output 8>
Status: <proposed | accepted | superseded | rejected | deprecated>
Supersedes: <ADR-NNN, if applicable>
Superseded by: <ADR-NNN, if applicable>
Related: REQ-NNN [, FLOW-NNN, SCREEN-NNN, COMPONENT-NNN, RF-NNN,
  SCENARIO-NNN...]
Recorded: <pass/date, and which agent recorded it>
```

## ID scheme and traceability
`ADR-NNN` is a new sideways reference in
`product-intelligence/traceability.md`'s model — the same category as
`BR-NNN`/`EDGE-NNN`/`DEP-NNN`/`RF-NNN`/`SCENARIO-NNN` — cited from
whichever artifact the decision governs (a `screen-architecture.md`
entry, a `component-spec.md`, a `design-direction.md` field). An
`ADR-NNN` with no `Related` citation at all is itself a defect (**B21**)
— a decision that governs nothing traceable is either mis-scoped or
belongs in a narrower artifact instead.

## Explicitly not here
- The consultation/supersession *rules* that make this record load-bearing
  rather than decorative → `consultation-rule.md`,
  `contradiction-prevention.md`.
- When an ADR gets written → `auto-recording.md`.
- The document/index this rolls up into → `templates/{decision-record,
  product-memory}.md`.
