# Template: State Matrix

## Purpose
The complete enumeration of every screen/component × mandatory-state
combination — proof that "what if it's loading, empty, or wrong" was
actually considered for everything, not just the cases that came to mind.
Reusable across every domain: the 13 mandatory states are fixed by Rule 6
(`config/operating-rules.md`) regardless of what the product does.

## Required inputs
- `ux-engine/state-design.md`'s 13 mandatory-state definitions and
  state-priority rule.
- `product-intelligence/edge-case-engine.md`'s `EDGE-NNN` scenarios for the
  screens/components in scope.
- The `SCREEN-NNN` / `COMPONENT-NNN` set from `screen-architecture.md` /
  `component-spec.md`.

## Output structure
- **Header** — per `config/output-contract.md`.
- **Matrix rows** — one per screen/component.
- **Matrix columns** — initial, loading, success, empty, validation error,
  system error, permission denied, processing, completed, cancelled,
  conflict, timeout (where applicable), offline (where applicable), plus any
  state added by the active `product-types/*.md` overlay.
- **Per-cell status** — designed / not-applicable (with reason) / deferred
  (with reason and severity).
- **Per-cell reference** — link to the `state-design.md`-derived behavior
  spec and the `component-spec.md` entry holding its visual treatment.

## Quality criteria
- **Zero blank cells** — every cell is designed, marked not-applicable with
  a reason, or marked deferred with a reason and severity; a blank cell is
  never an acceptable final answer.
- Every cell traceable to an `EDGE-NNN` where the state represents a
  failure/exception condition, not just asserted as "handled."
- State-priority conflicts (two states that could apply at once) are
  resolved per `state-design.md`'s precedence order, stated explicitly per
  row where it applies.
- This is exactly what `config/quality-gates.md`'s **B7 — State Coverage**
  gate checks, mechanically, via `scripts/validate-states.py`.

## Example structure
_Illustrative only — placeholders, not a real screen's states._

| Screen/Component | initial | loading | empty | validation error | system error | permission denied | success/completed |
|---|---|---|---|---|---|---|---|
| SCREEN-011 | designed | designed | designed (EDGE-002) | N/A (read-only) | designed | designed | designed |
| COMPONENT-004 | N/A (atom, no fetch) | N/A | — | designed | designed | N/A | designed |

## Traceability fields
Rows cite `SCREEN-NNN` / `COMPONENT-NNN`; cells cite `EDGE-NNN` where the
state instantiates an enumerated edge case.

## Explicitly not here
- Which states exist and why → `ux-engine/state-design.md`.
- The visual treatment of a state → `templates/component-spec.md`,
  `ui-engine/*`.
- Completeness validation logic → `scripts/validate-states.py`.
