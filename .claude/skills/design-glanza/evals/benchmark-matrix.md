# Benchmark Matrix

## Responsibility
Tracks `evaluation-rubric.md` scores across `test-cases.md`'s 10 scenarios
over time, and — critically — turns every failure into a recorded,
traceable improvement to the master skill rather than a one-off note. A
score is only useful if a bad one changes something.

## Matrix structure — two views

### View 1: per-version snapshot
Rows = the 10 scenarios, columns = the 18 dimensions, cells = score (1-5).
One snapshot per skill version (`config/master-config.md`'s version field).

| Scenario | Req. underst. | Bus. logic | Role coverage | ... (18 cols total) |
|---|---|---|---|---|
| 1. SaaS | | | | |
| 2. Admin Panel | | | | |
| ... | | | | |
| 10. Multi-role workflow | | | | |

### View 2: trend per (scenario, dimension) pair
For any single cell above, track its score across consecutive skill
versions — this is what catches a regression a single snapshot can't show:

| Version | Scenario | Dimension | Score | Δ vs. previous |
|---|---|---|---|---|
| 0.14.0 | 2. Admin Panel | Business logic | 4 | — (first measurement) |
| 0.15.0 | 2. Admin Panel | Business logic | 3 | -1 (regression — see Failure Log) |

## Regression-detection rule
A score drop of **≥1 point** (1-5 scale) for any (scenario, dimension) pair
between two consecutive skill versions is a regression. It is investigated
before that version is considered ready — a regression discovered by this
matrix blocks the same way a failed `config/quality-gates.md` gate would,
it just operates at the skill level rather than the product level.

## Failure log — the improvement loop
Every score of **1 or 2** on any dimension, and every failed triggering-
behavior test (`test-cases.md`), is recorded here as a Failure Record. This
is what makes "record failures and use them to improve the skill" a real
mechanism, not a suggestion — mirroring
`product-types/custom-domain.md`'s graduation rule (a recurring gap becomes
a permanent fix, not a repeated patch):

| Field | Meaning |
|---|---|
| Scenario / test | Which of the 10 scenarios or which triggering-behavior test |
| Dimension | Which of the 18 (or "triggering behavior" for should-trigger/etc.) |
| What happened | The concrete observed failure |
| Root cause | Which specific master-skill file's technique was insufficient |
| Fix applied | Which file was edited, and how |
| Re-benchmark result | Score after the fix, confirming resolution |
| Status | Open / Fixed / Fixed-but-regressed (routes back to Root cause) |

**Example record (illustrative):**

```
Scenario:        2. Admin Panel
Dimension:       Business logic
What happened:   A "let staff edit records" request was decomposed into
                 REQ-NNNs without a permission-check business rule — the
                 request's simplicity was mistaken for the absence of
                 underlying logic.
Root cause:      product-intelligence/brd-analysis.md's "business logic
                 is never optional" rule existed but had no concrete
                 worked trigger for the specific "simple-sounding CRUD
                 request" pattern.
Fix applied:     brd-analysis.md's rule section extended with an explicit
                 per-UI-element checklist (already present as of the
                 product-intelligence build) — this record exists to
                 show the *shape* a real failure record takes, not to
                 assert this specific fix is still pending.
Re-benchmark:    Score 4 (up from 2).
Status:          Fixed.
```

A fix is never "fixed" on the strength of the author's confidence alone —
the re-benchmark score is what closes the record.

## Triggering-behavior results tracking
A separate, smaller table for the four triggering-behavior categories
(`test-cases.md`), since these are pass/fail, not scored 1-5:

| Test case | Expected | Actual | Pass/Fail |
|---|---|---|---|
| "Build me a SaaS product for X" | Should trigger | | |
| "Fix this bug in my script" | Should not trigger | | |
| Near-blank product definition | Should ask for missing info | | |
| Scenario 3 (ERP) input | Should route to `product-types/erp.md` | | |

Any Fail here is a Failure Log record with `Dimension: triggering behavior`,
following the same fix → re-benchmark → close cycle as a scored dimension.

## Update cadence
Re-run the full benchmark matrix after any change to a domain-agnostic core
file (`config/`, `methodology/`, `product-intelligence/`, `ux-engine/`,
`ui-engine/`) — those changes can silently affect every scenario at once,
not just the one that motivated the change. A change scoped to a single
`product-types/*.md` pack only requires re-running the scenarios that pack
covers.

## Explicitly not here
- The scoring dimensions themselves → `evaluation-rubric.md`.
- The test scenarios being scored → `test-cases.md`.
- Fixing a recorded failure → whichever master-skill file the Root Cause
  field names; this file tracks the fix, it doesn't perform it.
