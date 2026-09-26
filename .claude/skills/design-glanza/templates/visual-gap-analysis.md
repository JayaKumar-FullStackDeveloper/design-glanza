# Template: Visual Gap Analysis

## Purpose
The record of `ui-engine/visual-benchmark.md`'s three-way comparison and at
least one mandatory refinement cycle for a given screen/UI pass — satisfying
`config/quality-gates.md`'s **B15 (Visual Benchmark & Audit Cycle
Completeness)** gate. One instance per screen (or per closely-related set of
screens produced in the same UI pass).

## Required inputs
- `ui-engine/ui-audit-framework.md`'s A–K audit run against the generated
  screen.
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
- **Audit findings (pass 1)** — every A–K category from
  `ui-engine/ui-audit-framework.md`, each as Observation → Problem → Fix
  with a pass/minor/major rating — or an explicit "no findings" per
  category.
- **Gap classification (pass 1)** — each finding tagged with a gap type
  from `visual-benchmark.md`'s list (missing pattern, incorrect hierarchy,
  excessive decoration, weak spacing, poor density, inconsistent
  components, wrong interaction pattern, weak accessibility, domain
  mismatch), or "none found."
- **Refinement applied** — the specific change made in response to each
  gap, or "none needed — pass 1 was clean" if genuinely no gaps were found.
- **Audit findings (pass 2 / re-check)** — re-run of the same A–K
  categories after refinement, confirming the gap is closed (or, for a
  genuinely-clean pass 1, a re-confirmation that nothing changed).
- **Final status** — pass / fail, and if fail, which Blocker/Major finding
  remains and its escalation target.

## Quality criteria
- Checked against **B15** — at least one full pass-1-then-refinement cycle
  is recorded, even when pass 1 found nothing.
- Every finding is classified with a gap type, not left as a bare
  observation.
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

Audit findings (pass 1):
  C. Visual Hierarchy — Minor: two elements read as equally primary.
  D. Layout — pass.
  ...(remaining categories)...

Gap classification (pass 1):
  C → Incorrect hierarchy.

Refinement applied:
  Reduced the secondary metric card's visual weight one level, per
  visual-hierarchy.md's Contrast-of-weight rule.

Audit findings (pass 2 / re-check):
  C. Visual Hierarchy — pass: primary action now unambiguous.

Final status: pass.
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
