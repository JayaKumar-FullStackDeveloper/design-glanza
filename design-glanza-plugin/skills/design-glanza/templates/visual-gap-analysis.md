# Template: Visual Gap Analysis

## Purpose
The record of `ui-engine/visual-benchmark.md`'s three-way comparison and at
least one mandatory refinement cycle for a given screen/UI pass — satisfying
`config/quality-gates.md`'s **B15 (Visual Benchmark & Audit Cycle
Completeness)** gate. One instance per screen (or per closely-related set of
screens produced in the same UI pass).

## Required inputs
- `ui-engine/ui-audit-framework.md`'s A–K audit run against the generated
  screen, in that file's Pixel-level verification pipeline order
  (Structure → Alignment → Spacing → Sizing → Typography → Component →
  Responsive → Micro-polish → Final Visual QA).
- `product-builder/ui/design-direction.md` (the Design Direction column).
- The original reference asset(s), if Reference-Driven/Guideline-Driven
  mode applies (the Reference column) — otherwise noted as not applicable.
- `ui-engine/craft-critique.md`'s composition-level findings for the same
  screen, folded in rather than re-derived.

## Output structure
- **Header** — per `config/output-contract.md`.
- **Screen(s) covered** — cross-referenced `SCREEN-NNN` IDs.
- **Reference summary** — one line on what the reference/sample was, or
  "not applicable — [mode] with no visual reference."
- **Design Direction summary** — the specific fields from
  `design-direction.md` most relevant to this screen (register, density,
  key components).
- **Initial score** — this screen's `evals/evaluation-rubric.md` dimension
  21 (Visual benchmark & audit cycle) score, 1-5, assessed honestly against
  pass 1's findings below, before any fix is applied.
- **Audit findings (pass 1)** — organized by pipeline step (Structure,
  Alignment, Spacing, Sizing, Typography, Component, Responsive,
  Micro-polish, Final Visual QA), each step listing its owning A–K
  category's findings as Observation → Problem → Fix with a pass/minor/
  major rating — or an explicit "no findings" per step. A step with no
  entry at all (not even "no findings") is treated the same as a skipped
  step, per B15's pass criterion.
- **Gap classification (pass 1)** — each finding tagged with a gap type
  from `visual-benchmark.md`'s list (missing pattern, incorrect hierarchy,
  excessive decoration, weak spacing, poor density, inconsistent
  components, wrong interaction pattern, weak accessibility, domain
  mismatch, generic/templated, data inconsistency), or "none found" — and,
  for every finding, a P0-P3 priority from that same file's Priority
  classification table (reconciled onto the shared Blocker/Major/Minor/Note
  scale).
- **Refinement applied** — the specific change made in response to each
  gap, or "none needed — pass 1 was clean" if genuinely no gaps were found.
- **Audit findings (pass 2 / re-check)** — re-run of the same pipeline
  steps after refinement, confirming the gap is closed (or, for a
  genuinely-clean pass 1, a re-confirmation that nothing changed).
- **Final status** — pass / fail, and if fail, which P0/un-waived-P1
  finding remains and its escalation target. A `pass` status is what
  triggers `visual-regression/baseline-model.md`'s capture/update of this
  screen's baseline (Rule 25) — recorded here as a one-line cross-reference,
  not a duplicate of the baseline's own content.
- **Final score** — the same dimension 21, re-assessed once
  `visual-benchmark.md`'s "When to stop" conditions all hold — showing
  whether this cycle actually moved the score, not just that steps were
  performed.

## Quality criteria
- Checked against **B15** — at least one full pass-1-then-refinement cycle
  is recorded, even when pass 1 found nothing, and every pipeline step
  (Structure/Alignment/Spacing/Sizing/Typography/Component/Responsive/
  Micro-polish) has its own entry — a missing step is treated as a skipped
  step, not an implicit pass.
- Every finding is classified with both a gap type and a P0-P3 priority,
  not left as a bare observation.
- Every P0-priority finding from pass 1 is resolved, and every P1-priority
  finding is either resolved or explicitly waived with a logged reason, by
  Final status — an unresolved P0 or un-waived P1 fails B15 regardless of
  the recorded Final score.
- Initial score and Final score are both recorded, honestly assessed
  against the rubric's existing threshold (no dimension below 3, Tier A
  dimensions never below 4) — never adjusted to make the cycle look like
  it worked.
- A "no gaps found" pass 1 still shows a genuine pass 2 re-check, not a
  skipped step.

## Example structure
_Illustrative, domain-neutral — not real product content._

```
Screen(s): SCREEN-004 (Dashboard)
Reference summary: Reference-Driven — one screenshot of the client's
existing legacy admin tool (dense enterprise register).
Design Direction summary: Dense Enterprise register, compact density,
sidebar navigation, tabular-figure data throughout.

Initial score: 3/5 (cycle ran; one Minor/P2 hierarchy gap found; not yet a
  clean pass).

Audit findings (pass 1):
  Structure — pass.
  Alignment — pass.
  Spacing — pass.
  Sizing — pass.
  Typography — Minor (P2): two KPI cards read as equally primary (C. Visual
    Hierarchy) with no stated reason for parity.
  Component — pass.
  Responsive — pass.
  Micro-polish — pass.

Gap classification (pass 1):
  Typography/C → Incorrect hierarchy (P2).

Refinement applied:
  Reduced the secondary metric card's visual weight one level, per
  visual-hierarchy.md's Contrast-of-weight rule and its Parallel summary
  metrics section.

Audit findings (pass 2 / re-check):
  Typography/C. Visual Hierarchy — pass: primary metric now unambiguous.

Final status: pass.
Final score: 5/5 (gap fixed and re-confirmed; zero unresolved P0/P1/P2
  findings).
```

## Traceability fields
Cited by `agents/qa-expert.md` during Audit (folded in alongside
`craft-critique.md`'s findings) and by `config/quality-gates.md`'s B15 pass
criterion directly.

## Explicitly not here
- The comparison technique and gap-type definitions themselves →
  `ui-engine/visual-benchmark.md`.
- The audit categories → `ui-engine/ui-audit-framework.md`.
- The composition-craft checks → `ui-engine/craft-critique.md`.
