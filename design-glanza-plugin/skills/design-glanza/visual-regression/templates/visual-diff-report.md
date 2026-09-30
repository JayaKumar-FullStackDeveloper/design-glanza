# Template: Visual Difference Report

## Purpose
The concise, per-pass report of every diff found between a screen's
baseline and its current state — the artifact requested as this system's
output, and what `config/quality-gates.md`'s **B20** is checked against.

## Required inputs
- The prior baseline (`product-builder/ui/baselines/<SCREEN-NNN>.json`).
- The current capture, same shape.
- `scripts/validate-visual-regression.py`'s diff output.

## Output structure
- **Header** — per `config/output-contract.md`.
- **Screen** — `SCREEN-NNN`, baseline pass # vs. current pass #.
- **Diffs found** — one line per diff, in `diff-detection.md`'s category,
  each with its Critical/High/Medium/Low label (`severity-
  classification.md`) and its mapped Blocker/Major/Minor/Note value.
- **Within tolerance** — diffs `tolerance-thresholds.md` accepts without
  further action, still listed, not silently dropped.
- **Baseline updates applied** — any `baseline-updates.md` records written
  this pass, with their Reason.
- **Unresolved findings** — any Critical/High/Medium diff with no fix and
  no approved Baseline Update — this section must be empty for **B20** to
  pass.
- **Overall status** — pass/fail.

## Quality criteria
- Every diff found is listed exactly once, in exactly one of "Within
  tolerance," "Baseline updates applied," or "Unresolved findings" — never
  omitted, never double-counted.
- A "no diffs found" report still states that the comparison ran (the
  same "an unresolvable 'we didn't check' gap is not acceptable" posture
  `visual-benchmark.md` already requires for its own cycle).

## Example structure
_Illustrative, domain-neutral — not real product content._

```
Screen: SCREEN-011 — baseline pass 2 vs. current pass 3

Diffs found:
  Spacing changes — COMPONENT-004's internal padding: spacing.16 → spacing.24
    (Medium / Minor)
  Color deviations — COMPONENT-004's status badge: color.semantic.warning
    → color.semantic.error, no stated reason (High / Major)

Within tolerance:
  (none)

Baseline updates applied:
  SCREEN-011 / Spacing changes — spacing.16 → spacing.24. Reason: table
  density intentionally relaxed per updated Design Direction (register
  unchanged, comfort increased for this screen specifically). Approved by
  agents/design-system-expert.md. Baseline updated.

Unresolved findings:
  SCREEN-011 / Color deviations — reverted to color.semantic.warning
  (the actual intended semantic); COMPONENT-004's status badge fixed, not
  approved as a baseline update.

Overall status: pass (all findings resolved — one accepted, one fixed).
```

## Traceability fields
Cited by `agents/qa-expert.md`, folded into `templates/qa-report.md`'s
Findings list and `config/quality-gates.md`'s **B20** pass criterion
directly.

## Explicitly not here
- The diff categories and their definitions → `visual-regression/
  diff-detection.md`.
- Tolerance/severity rules → `visual-regression/{tolerance-thresholds,
  severity-classification}.md`.
- The baseline's own shape → `templates/visual-baseline.md`.
