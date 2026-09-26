# QA Report - projectflow

> Generated 2026-09-26T12:17:39+00:00 by `scripts/generate-report.py` (deterministic checks only - see below).

## Findings (deterministic)

- [Minor] No mention of 'component' found - required topic from templates/screen-specification.md may be missing (ux/screen-architecture.md)
- [Minor] No mention of 'responsive' found - required topic from templates/screen-specification.md may be missing (ux/screen-architecture.md)
- [Minor] No mention of 'accessibility' found - required topic from templates/screen-specification.md may be missing (ux/screen-architecture.md)

## Missing artifacts

_None (or not yet expected at this product's current status)._

## Invalid references

_None found._

## Severity summary

| Severity | Count |
|---|---|
| Blocker | 0 |
| Major | 0 |
| Minor | 3 |
| Note | 0 |

## Test dimension summary (methodology/test.md)

_Not evaluated by this script._ All nine dimensions (task completion, usability, discoverability, error prevention, feedback, accessibility, responsiveness, edge cases, business-rule correctness) require reasoning-based evaluation by `agents/qa-expert.md` against `methodology/test.md` - a script cannot judge whether a flow is usable or a business rule is correctly embodied. Do not treat this report as complete until that evaluation has been run and appended here.

## Rubric scores (evals/evaluation-rubric.md)

_Not evaluated by this script._ `evals/evaluation-rubric.md` is still architecture shell as of this report; once implemented, scoring is a reasoning-based judgment, not a script computation.

## Design-system drift notes

_Not evaluated by this script._ Requires `agents/design-system-expert.md`'s reuse-vs-new-variant review, which is a judgment call this toolchain does not automate.

## Accessibility conformance notes

_Not evaluated by this script._ This script checks structural facts only (state-matrix references, requirement mapping); full conformance (contrast values, focus order correctness) requires `agents/accessibility-expert.md`'s review.

## Overall gate status

**PASS** on deterministic checks (B1, B5, B7, B10 partial). This is **not** the same as the Audit -> Iterate gate passing overall - `config/quality-gates.md`'s B2, B3, B4, B6, B8, B9, B11, B12 all require reasoning-based review this script does not perform. Per `workflows/execute-product-builder.md`'s completion criteria: a deterministic PASS here is necessary, never sufficient, for declaring the product complete.
