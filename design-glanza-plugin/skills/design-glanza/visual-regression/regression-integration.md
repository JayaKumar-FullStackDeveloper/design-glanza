# Regression Integration

## Responsibility
How visual regression findings actually reach the Quality Engine and
trigger refinement — reusing the existing feedback-routing table and
Iterate loop rather than inventing a parallel one, and preserving the
existing architecture (no new phase, no new agent, no new action row).

## Where this runs, relative to the existing cycle
```
Screen already has a baseline (prior pass confirmed clean)?
  NO  → visual-benchmark.md's 3-way comparison + refinement cycle runs
        as it always has (B15) → this system captures the baseline.
  YES → THIS SYSTEM diffs current vs. baseline FIRST
        → Critical/High findings routed and fixed (or explicitly
          approved via baseline-updates.md) before the pass proceeds
        → visual-benchmark.md's cycle still runs afterward, checking the
          (now regression-clean) state against Reference/Direction
        → baseline updated to the new confirmed-clean state.
```
Folded into the **existing** "Run the mandatory visual-benchmark-and-audit
cycle" action (`workflows/execute-product-builder.md`'s Order 32, per
`ui-engine/visual-benchmark.md`) — no new action row, the same restrained
choice `design-tokens/*` and `component-registry/*` both made for their
own generation-time checks.

## Routing a regression finding
Reuses `methodology/design-thinking.md`'s existing feedback-routing table
— every category maps to the agent/file that already owns the underlying
concern, per Rule 13 (fix and revalidate):

| Diff category | Routes to |
|---|---|
| Layout shifts, Alignment problems | `agents/ux-architect.md` (`ui-engine/layout-system.md`) |
| Spacing changes, Typography changes, Color deviations | `agents/ui-designer.md` (the relevant `ui-engine/*` file) |
| Component inconsistencies | `agents/design-system-expert.md` (the same drift-review mechanism `component-registry/registry-integration.md` already routes to) |
| Missing elements, Unexpected elements | `agents/ux-architect.md` if the flow/screen-architecture itself changed; `agents/ui-designer.md` if only the visual realization did |
| Responsive regressions | `agents/ui-designer.md` (`ui-engine/responsive-system.md`) |

A Critical finding on a core-workflow screen additionally re-triggers the
specific `ux-scenario-testing/*` scenario that screen serves — a visual
regression can turn a previously-`covered` scenario into a `gap` (e.g. a
missing element is also a missing action, per `ux-scenario-testing/
gap-detection.md`), so the two systems' findings are cross-checked, not
independently tracked.

## Integration with the Quality Engine
- **`config/quality-gates.md`**'s new **B20 (Visual Regression
  Integrity)** — every screen with an existing baseline has been diffed
  since its last change, with 0 unresolved Critical/High findings (either
  fixed or explicitly approved via `baseline-updates.md`).
- **`templates/qa-report.md`** — the concise visual-difference report
  (`templates/visual-diff-report.md`) folds into the existing Findings
  list and Traceability summary, using the same severity vocabulary,
  never a parallel report.
- **`evals/evaluation-rubric.md`** gains a matching Tier B dimension.

## Preserving existing architecture
No new lifecycle phase, no new agent (`agents/qa-expert.md` runs the
baseline diff at Audit, alongside its existing scenario-walk and
research-validation checks — the same agent, one more check in its
existing procedure); no new ID scheme (a baseline is addressed by
`SCREEN-NNN`, not a new sequential ID, matching `component-registry/*`'s
own name-addressed precedent rather than `RF-NNN`/`SCENARIO-NNN`'s, since
a baseline is a snapshot of an existing ID's state, not a new governing
fact requiring forward citation).

## Explicitly not here
- The baseline/diff mechanics themselves → `baseline-model.md`,
  `diff-detection.md`.
- B20's exact pass criterion → `config/quality-gates.md`.
- Rule 25's full statement → `config/operating-rules.md`.
