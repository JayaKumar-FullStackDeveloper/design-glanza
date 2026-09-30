# Visual Regression & Comparison System

## Responsibility
Protect UI consistency **across iterations** — did this pass accidentally
break something that already worked — as distinct from
`ui-engine/visual-benchmark.md`'s existing three-way comparison, which
checks a single point in time (does the just-generated screen match its
Reference/Design Direction). This is the elaboration of Rule 25
(`config/operating-rules.md`) and gate **B20**
(`config/quality-gates.md`).

## What is genuinely new here, and what is not
`visual-benchmark.md` already compares **Reference vs. Design Direction
vs. Generated UI**, produces 9 named gap types, and mandates at least one
refinement cycle (gate **B15**) — but it has no concept of a **prior
version** at all. A screen can cleanly pass B15 on pass 3 while still
being a regression from pass 2 (pass 3's fix for one gap silently broke
something pass 2 had correct) — B15's point-in-time check cannot see
that, by construction, because it never looks backward.

| Genuinely new | Already exists — cited, never restated |
|---|---|
| A **baseline**: a structured snapshot of a screen's visual-relevant facts at a point in time, to diff *future* passes against | The 11-category audit that *produces* those facts each time → `ui-engine/ui-audit-framework.md` |
| Structural diffing between two snapshots (baseline vs. current) | The Reference-vs-Direction-vs-Generated three-way comparison for *one* point in time → `visual-benchmark.md` |
| Configurable tolerance thresholds, expressed in token steps | The closed token scales the thresholds are measured against → `design-tokens/*` |
| A Critical/High/Medium/Low classification for a *regression* specifically | The product's one shared Blocker/Major/Minor/Note severity vocabulary → `config/output-contract.md` (reconciled here, never a competing scale — see `severity-classification.md`) |
| Explicit, logged **baseline updates** for intentional changes | The identical "logged system gap, absorbed or rejected" pattern → `ui-engine/design-system.md`'s Consistency rule (the same discipline, applied here to a temporal diff instead of a token) |
| `scripts/validate-visual-regression.py` — a real, structural diff tool | `scripts/validate-tokens.py` (the sibling script this one is modeled on) |

## The two systems compose, they don't compete
```
FIRST time a screen is produced:
  visual-benchmark.md's 3-way comparison + refinement cycle (B15)
    → screen confirmed clean → THIS SYSTEM captures the baseline.

EVERY SUBSEQUENT pass touching that screen:
  THIS SYSTEM diffs current vs. baseline FIRST (did anything regress)
    → then visual-benchmark.md's cycle still runs as before (does the
      *new* state conform to Reference/Direction) → baseline updated.
```
Neither system substitutes for the other. B15 without this system would
keep re-confirming conformance while silently accumulating regressions
across passes; this system without B15 would have nothing well-defined to
capture as a baseline in the first place.

## File map

| File | Owns |
|---|---|
| `baseline-model.md` | What a baseline snapshot is, what it captures (and doesn't), where it's stored |
| `diff-detection.md` | The 9 detection categories, each reconciled against `visual-benchmark.md`'s existing 9 gap types |
| `tolerance-thresholds.md` | Configurable, token-step-based tolerance — never a raw-pixel-delta system |
| `severity-classification.md` | Critical/High/Medium/Low, mapped onto the one shared severity vocabulary |
| `baseline-updates.md` | The explicit, logged mechanism for preserving an intentional change |
| `regression-integration.md` | Wiring into the Quality Engine, the feedback-routing table, and the existing action sequence — no new phase, no new agent |
| `templates/{visual-baseline,visual-diff-report}.md` | The snapshot record and the concise diff report |
| `scripts/validate-visual-regression.py` | The structural diff implementation |

## Explicitly not here
- The point-in-time three-way comparison and its 9 gap types →
  `ui-engine/visual-benchmark.md`.
- The 11-category audit itself → `ui-engine/ui-audit-framework.md`.
- The composition-craft numeric checks → `ui-engine/craft-critique.md`.
- Token values and their closed scales → `design-tokens/*`.
- Component registry conformance → `component-registry/*`.
