# Traceability

## Responsibility
Maintain the unbroken chain from every requirement to every downstream artifact
that implements it, so nothing gets built without a reason and nothing gets
requested without eventually being built and tested. This is the audit-trail
mechanism every other file relies on rather than inventing its own linkage.

## The chain

```
REQ → USER → FLOW → SCREEN → COMPONENT → TEST
```

| Link | ID scheme (owned here) | Produced by (technique owned there) |
|---|---|---|
| REQ | `REQ-NNN` | `requirement-engine.md` |
| USER | `ROLE-NNN` (or `SYSTEM`) | `user-roles.md` |
| FLOW | `FLOW-NNN` | `ux-engine/user-flow-engine.md` |
| SCREEN | `SCREEN-NNN` | `templates/screen-architecture.md` / `screen-specification.md` |
| COMPONENT | `COMPONENT-NNN` | `ui-engine/component-system.md`, instantiating a `component-registry/*` entry where one exists (Rule 24) |
| TEST | `TEST-NNN` | `methodology/test.md` (design validation) and/or `evals/test-cases.md` (internal QA) |

This file owns the ID *schemes* so every artifact type is uniquely and
consistently addressable across the whole product — the *technique* for
producing a FLOW, SCREEN, COMPONENT, or TEST stays owned by its own file, cited
here only by ID.

**Why USER sits in the chain, not just as a REQ field:** a single requirement
can serve multiple roles differently (the same `REQ-NNN` might produce one
`FLOW-NNN` for an Employee and a materially different one for a Manager). Making
USER an explicit link — not just the Actor field on the requirement — means the
chain can represent "this requirement, for this role, produced this flow,"
rather than collapsing multiple role-specific paths into one ambiguous trace.

## The trace record
One row per `REQ-NNN` × `ROLE-NNN` combination that requirement actually serves:

| REQ | USER | FLOW | SCREEN(s) | COMPONENT(s) | TEST(s) | Status |
|---|---|---|---|---|---|---|
| REQ-014 | ROLE-002 (Manager) | FLOW-006 | SCREEN-011, SCREEN-012 | COMPONENT-004, COMPONENT-009 | TEST-018 | traced |
| REQ-014 | ROLE-003 (Employee) | FLOW-007 | SCREEN-013 | COMPONENT-004 | *(none yet)* | partial |

**Status** per row is one of: `traced` (every link present), `partial` (some
links missing but the requirement is still active/in-progress), or `orphaned`
(see below).

## Sideways references vs. the chain
`BR-NNN` (`business-logic.md`), `EDGE-NNN` (`edge-case-engine.md`),
`DEP-NNN` (`dependency-analysis.md`), `RF-NNN` (`design-research/
research-to-design.md`), `SCENARIO-NNN` (`ux-scenario-testing/
scenario-model.md`), and `ADR-NNN` (`product-memory/adr-schema.md`) are
not links in this chain — they are *governing facts* a requirement, flow,
screen, or design-direction field cites (via a requirement's Business
Rule/Validation/Dependency fields, a `FLOW-NNN`/`SCREEN-NNN`/`ui/
design-direction.md` citation for `RF-NNN`, `ux/scenarios.md`/`ux/
ux-coverage-matrix.md` for `SCENARIO-NNN`, or any artifact's `Related`
field for `ADR-NNN`), not artifacts produced downstream of it. Keep them
out of the trace record above; overloading the chain with every
cross-reference makes orphan detection unreliable.

**`ADR-NNN` specifically:** a persisted decision record (Rule 26) is the
one sideways reference that can itself cite *another* sideways reference
(an ADR's Related field routinely names the `REQ-NNN`/`FLOW-NNN`/
`SCREEN-NNN`/`COMPONENT-NNN` it governs, and may cite an `RF-NNN` or
`SCENARIO-NNN` it resolves) — this is still not a chain link, an ADR
governs several artifacts across one decision, not one artifact per
link. An `ADR-NNN` with no `Related` citation at all is an orphaned
decision — checked by **B21**, the same defect category as an orphaned
requirement under B10.

**`RF-NNN` specifically:** a Research Finding (Rule 21,
`config/operating-rules.md`) is the research-stage evidence behind a design
decision — cited from `ux/user-flows.md`, `ux/screen-architecture.md`,
`ui/ui-rules.md`, or `ui/design-direction.md` wherever that finding's Design
Principle actually applies, the same way a `BR-NNN` rule is cited from the
requirement it governs. A CRITICAL or HIGH priority `RF-NNN` with no
downstream citation anywhere is an orphaned finding — checked by
**B16** (`config/quality-gates.md`), the same defect category as an
orphaned requirement under B10.

**`SCENARIO-NNN` specifically:** a Scenario (Rule 22) is one `FLOW-NNN`
walked under one named scenario type — it does not sit between FLOW and
SCREEN in the chain (a scenario touches *several* screens across one
walk, not one), it sits *beside* the chain, always naming which
`FLOW-NNN` it instantiates and, through it, which `REQ-NNN`/`ROLE-NNN` it
serves. A `FLOW-NNN` with no `SCENARIO-NNN` covering it at all is an
orphaned flow in this same sense — checked by **B17**.

## Orphan detection
- **Orphaned requirement** — a `REQ-NNN` with no downstream link beyond a stated
  point in its lifecycle (e.g. still `draft` past a point where it should have
  progressed), and *not* explicitly marked deferred/out-of-scope
  (`methodology/define.md`'s scope-boundary technique). An orphaned requirement
  is a defect the moment it's discovered outside of an expected in-progress
  state.
- **Orphaned artifact** — a FLOW, SCREEN, COMPONENT, or TEST with no upstream
  `REQ-NNN` (or explicit assumption tag standing in for one). This is scope
  creep made visible: something got built that no requirement asked for.

Both are surfaced in `templates/qa-report.md` via `workflows/audit-product.md`,
not silently tolerated as "probably fine."

## Bidirectional lookup
The trace record must support lookup in both directions — not just "what did
this requirement produce" but "what requirement justifies this artifact." Given
any `SCREEN-NNN` or `COMPONENT-NNN`, it must be possible to find every `REQ-NNN`
that traces to it, and given any `REQ-NNN`, every downstream artifact. A
forward-only log that can't answer "why does this screen exist" defeats the
purpose of traceability at Audit time.

## Handoff shape
This file's trace record is the primary data source for
`workflows/audit-product.md`'s Traceability gate (`config/quality-gates.md`,
B10) and for `templates/qa-report.md`'s traceability summary.

## Loop position
Updated continuously as the feature-level loop
(`methodology/design-thinking.md`) produces each new FLOW/SCREEN/COMPONENT/TEST
— not assembled once at the end. A Test finding that reveals a broken or missing
link (e.g. a screen with no traceable requirement) is itself a Test finding,
routed per that file's evaluation.

## Explicitly not here
- The requirement ID scheme's field content → `requirement-engine.md`.
- The role ID scheme's permission content → `user-roles.md`.
- How a FLOW/SCREEN/COMPONENT/TEST is actually produced → the file named in the
  chain table above, for that link.
- The audit procedure that consumes this data → `workflows/audit-product.md`.
