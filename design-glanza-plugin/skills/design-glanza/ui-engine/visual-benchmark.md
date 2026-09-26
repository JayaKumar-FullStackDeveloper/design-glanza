# Visual Benchmark

## Responsibility
The three-way comparison run before a UI pass is considered final:
**Reference** (if one exists) vs. **Design Direction**
(`product-builder/ui/design-direction.md`) vs. **Generated UI** (the actual
screen just produced) — producing a named gap analysis, and gating at least
one refinement cycle before completion. This is the mechanism behind Rule
20: the first generated draft is a draft, checked against what it was
supposed to become, never assumed correct because it renders without error.

## The three-way comparison
For each screen audited by `ui-engine/ui-audit-framework.md`:

| Column | Source | What it represents |
|---|---|---|
| **Reference** | The actual supplied reference asset, if Reference-Driven/Guideline-Driven mode applies — otherwise the selected `design-samples/` entry for Default mode, or omitted entirely for Custom Design with no visual reference at all | What the direction was extracted *from* |
| **Design Direction** | `product-builder/ui/design-direction.md` | What was *decided* — the approved intent, which may deliberately depart from the reference in named, recorded ways |
| **Generated UI** | The actual produced screen | What was *built* |

The comparison that matters is Direction-vs-Generated (did the build
actually follow the decision), not Reference-vs-Generated directly — a
generated screen that differs from the raw reference but matches a
*deliberately adapted* design direction is correct, not a gap; a generated
screen that differs from its own design direction with no recorded reason
is always a gap, reference or no reference.

## Gap analysis categories
Run `ui-engine/ui-audit-framework.md`'s A–K categories as the audit, then
classify every finding into one of these gap types so the refinement pass
knows what kind of fix is needed:

| Gap type | What it means |
|---|---|
| **Missing pattern** | Design Direction specified something (a component, a state, an interaction) that the Generated UI simply doesn't have |
| **Incorrect hierarchy** | The relative emphasis in the Generated UI doesn't match what Design Direction (or the reference) established |
| **Excessive decoration** | The Generated UI added visual elements Design Direction never called for — most often traceable to `craft-critique.md`'s anti-cliché catalog |
| **Weak spacing** | Density or the padding/gap relationship departs from what was specified |
| **Poor density** | The comfortable/compact/dense register doesn't match Design Direction's stated preference or the domain's actual need |
| **Inconsistent components** | The same UI need was solved two different ways across screens, or a component departs from the governed inventory |
| **Wrong interaction pattern** | A pattern was used (e.g. a modal where Design Direction called for a drawer) that contradicts the recorded decision |
| **Weak accessibility** | A structural or perceptual accessibility rule was specified but not actually honored in the build |
| **Domain mismatch** | Category K of the audit framework failed — the screen doesn't read as belonging to its actual domain |

A gap is recorded even when it's minor — the point of this file is to make
"looks fine to me" checkable against something concrete, not to filter
findings down to only the ones that feel urgent.

## Mandatory refinement
Per Rule 20 and gate **B15**: at least one refinement cycle is required
before a UI pass is considered complete, regardless of how the first
generated draft looks:
1. Run the three-way comparison and gap analysis above on the first draft.
2. **If gaps were found:** fix them, then re-run the comparison on the
   refined draft — repeat until no new gap is found or a Blocker/Major gap
   remains genuinely unresolvable (escalate the latter per the normal
   feedback-routing table, never ship it silently).
3. **If no gaps were found on the first pass:** still record that the
   comparison ran and found nothing — an unresolvable "we didn't check"
   gap is not an acceptable way to skip this step. A genuinely clean first
   draft is recorded as such, not skipped as unnecessary.

Record the full history — what the first draft's gap analysis found (or
that it found nothing), what changed, and what the re-check confirmed — in
`templates/visual-gap-analysis.md`'s instance for this screen/pass. A
refinement cycle that isn't written down did not happen, per the same
"artifacts, not conversation" discipline `workflows/execute-product-builder.md`
already applies everywhere else.

## Explicitly not here
- The audit categories themselves → `ui-engine/ui-audit-framework.md`.
- The composition-craft numeric checks → `ui-engine/craft-critique.md`.
- The gap-analysis document's exact fields →
  `templates/visual-gap-analysis.md`.
- The gate this enforces → `config/quality-gates.md`'s **B15**.
