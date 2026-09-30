# Diff Detection

## Responsibility
The 9 categories a baseline-vs-current diff checks, each precisely defined
against the structured facts `baseline-model.md` captures, and each
reconciled explicitly against `ui-engine/visual-benchmark.md`'s existing 9
gap types — some are the same concept viewed temporally, some are
genuinely new because point-in-time comparison can't see them by
construction.

## The 9 categories

| Category | What changed, structurally | Relationship to `visual-benchmark.md`'s gap types |
|---|---|---|
| **Layout shifts** | A region's order, presence, or composition-pattern assignment differs from baseline (`ui-engine/layout-system.md`) | **Genuinely new** — a point-in-time check has nothing to compare the region order *to* |
| **Spacing changes** | A component/region's spacing token path differs from baseline | Temporal form of **Weak spacing** — same underlying concern, now diffable against a concrete prior value instead of judged against a written rule |
| **Typography changes** | A text role's type-scale token path (`typography.size/weight/lineHeight`) differs from baseline | **Genuinely new** — no existing gap type addresses typography drift specifically |
| **Color deviations** | A component's color token path resolves differently than baseline, **or** the same token path's underlying value changed (a token-scale edit) | **Genuinely new**, though it composes with `design-tokens/token-audit.md`'s raw-value scan — a color deviation here is always *token-to-token*, a raw-value violation is a separate, always-Critical concern (`tolerance-thresholds.md`) |
| **Component inconsistencies** | A component's Registry base or variant differs from baseline with no recorded reason | Temporal form of **Inconsistent components** |
| **Alignment problems** | A region/component's grid-column span or alignment exception (`layout-system.md`'s Alignment rules) differs from baseline | **Genuinely new** — closest existing relative is **Incorrect hierarchy**, but alignment is a structural/grid concern, hierarchy is an emphasis concern; kept distinct |
| **Missing elements** | A component present in baseline is absent from current | Temporal form of **Missing pattern** — but diffed against a *prior generated state*, not just against Design Direction's stated intent |
| **Unexpected elements** | A component present in current was not in baseline, with no corresponding Design Direction change | The **inverse** of Missing pattern — genuinely new; nothing in the existing 9 catches an *addition* nobody asked for (closest relative is **Excessive decoration**, which is composition-craft-level, not structural) |
| **Responsive regressions** | A breakpoint's reflow behavior differs from baseline for the same composition pattern | Temporal form of category J of `ui-audit-framework.md`, now diffed against a prior *working* state rather than judged fresh each time |

## Procedure
For a screen with an existing baseline, before this pass's
`visual-benchmark.md` cycle re-runs:
1. Capture the screen's **current** structured state in the same shape
   `baseline-model.md` defines.
2. Run `scripts/validate-visual-regression.py` — a structural, field-by-
   field diff between the baseline JSON and the current JSON, per the 9
   categories above.
3. Classify every diff found against `tolerance-thresholds.md` (is it
   within tolerance, and if not, how severe) and
   `severity-classification.md` (Critical/High/Medium/Low).
4. Record every diff — even a within-tolerance one — in
   `templates/visual-diff-report.md`; "within tolerance" is a recorded
   judgment, not a silent pass.

## A diff is not automatically a defect
Per `tolerance-thresholds.md` and `baseline-updates.md`: a diff that's
within the configured tolerance, or one that traces to an explicit,
approved Baseline Update (an intentional redesign), is recorded as
**reviewed — accepted**, not as a finding requiring a fix. Only a diff
that's out-of-tolerance **and** has no approved Baseline Update is an
actual regression finding.

## Explicitly not here
- What a baseline captures → `baseline-model.md`.
- Tolerance and severity → `tolerance-thresholds.md`,
  `severity-classification.md`.
- The report shape → `templates/visual-diff-report.md`.
- The script's own implementation → `scripts/validate-visual-regression.py`.
