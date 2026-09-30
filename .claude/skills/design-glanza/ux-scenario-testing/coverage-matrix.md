# UX Coverage Matrix

## Responsibility
The roll-up artifact — every `FLOW-NNN` × every applicable scenario type
(`scenario-types.md`), each cell a `SCENARIO-NNN` with its status — plus
how a finding from `gap-detection.md`/`continuity-audit.md` actually
reaches the Quality Engine and the refinement loop. This is the artifact
gate **B17** is checked against, the same relationship `templates/
qa-report.md` has to B10/B11 and `research/research-summary.md` has to B16.

## The matrix shape
Rows: every `FLOW-NNN` the product defines. Columns: the 8 scenario types.
Cell: the `SCENARIO-NNN` id and its status — **covered** (walked, no
Blocker/Major finding open), **gap** (a `gap-detection.md` or
`continuity-audit.md` finding is open against it), **deferred** (explicit
reason and severity), or **not-applicable** (explicit reason, per
`scenario-types.md`'s applicability rule). Zero blank cells — the same
discipline `templates/state-matrix.md` already enforces for its own
screen/component × state grid, applied here one level up at the flow ×
scenario-type grid.

```
| FLOW-NNN | Primary | Alternate | Error | Empty | Loading | Permission | Offline | Recovery |
|---|---|---|---|---|---|---|---|---|
| FLOW-006 | SCENARIO-011: covered | SCENARIO-012: covered | SCENARIO-013: gap | N/A (no empty-result state on this flow) | SCENARIO-014: covered | SCENARIO-015: covered | N/A (server-side only, no client offline case) | SCENARIO-016: covered |
```

## Two-checkpoint gate — B17
Mirrors B15/B16's cumulative-checkpoint pattern rather than one all-or-
nothing gate:

1. **Prototype → Implement (spec-level).** Every `FLOW-NNN` has a fully
   populated matrix row — every cell a `SCENARIO-NNN`, `N/A`, or
   `deferred`, never blank — and `gap-detection.md`'s structural check has
   run against the spec with 0 unresolved Blocker findings. This confirms
   the *spec itself* is walkable before Implement begins; it does not yet
   require the built output to exist.
2. **Audit → Iterate (walked).** Every `SCENARIO-NNN` marked `covered` has
   actually been walked (against `output/*` where it exists, against the
   spec where the engagement is planning-only) via
   `continuity-audit.md`, with 0 unresolved Blocker/Major findings across
   dead ends, ambiguous CTAs, missing feedback, inconsistent patterns, and
   contextual consistency.

**Checked by:** `agents/ux-architect.md` and `agents/interaction-designer.md`
jointly (checkpoint 1 — they own the flows/screens/states the matrix is
built from), `agents/qa-expert.md` (checkpoint 2 — the same agent that
already owns Test/Audit) — no new dedicated agent, matching B15/B16's
precedent.

## Integration with the Quality Engine
- **`config/quality-gates.md`** — new **B17 (UX Scenario Coverage)**,
  checked at the Prototype → Implement and Audit → Iterate transitions
  (joining B15/B16 at the same two checkpoints, not a third new
  transition).
- **`product-intelligence/traceability.md`** — `SCENARIO-NNN` is a
  sideways reference (`scenario-model.md`), so every scenario finding is
  already addressable from the same trace record `qa-report.md` reports
  through.
- **`evals/evaluation-rubric.md`** — a new Tier B dimension, "UX scenario
  coverage," mapping directly to B17.

## Integration with Product Memory
A `not-applicable`/`deferred` cell on a core-workflow flow is a
significant decision (`product-memory/auto-recording.md`) — it gets a
persisted `ADR-NNN`, not just a matrix cell, so the reason a scenario type
was deliberately not covered survives independently of the matrix being
regenerated later. A genuinely obvious `not-applicable` (no Offline
scenario on a server-side batch flow) stays in the matrix cell alone, per
that file's own proportionality rule.

## Integration with the refinement loop
A gap-detection or continuity-audit finding is not a new, competing
finding type — it uses `config/output-contract.md`'s existing severity
vocabulary and routes through `methodology/design-thinking.md`'s existing
feedback-routing table exactly as any other Test/Audit finding does:

| Finding | Routes to | Why |
|---|---|---|
| Missing screen/transition/action | `agents/ux-architect.md` | Structural — the flow/IA/navigation model itself is incomplete |
| Missing validation | `agents/interaction-designer.md`, `product-intelligence/business-logic.md` | The rule was never captured or specified |
| Missing feedback (structural or experiential) | `agents/interaction-designer.md` | Execution — a feedback rule wasn't stated or applied |
| Dead end, unnecessary step | `agents/ux-architect.md` | Structural — the flow's own shape, not a visual issue |
| Ambiguous CTA | `agents/ui-designer.md` | Visual hierarchy execution on an otherwise-correct structure |
| Inconsistent interaction pattern | `agents/design-system-expert.md` | Drift, the same category as token/component drift |
| Contextual consistency break | `agents/interaction-designer.md`, `agents/ux-architect.md` (if the navigation model itself doesn't support it) | Usually execution; structural if the pattern genuinely can't preserve context as designed |

A fix is revalidated by re-walking the specific `SCENARIO-NNN` that failed —
not the whole matrix from scratch — per Rule 13 (`config/operating-rules.md`).

## Explicitly not here
- The 8 scenario types and their definitions → `scenario-types.md`.
- The two finding-detection techniques themselves → `gap-detection.md`,
  `continuity-audit.md`.
- The `SCENARIO-NNN` record shape → `scenario-model.md`, `templates/
  scenario.md`.
- The full matrix template → `templates/ux-coverage-matrix.md`.
