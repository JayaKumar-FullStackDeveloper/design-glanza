# Use Case: Figma-Referenced New Screen

## Responsibility
A validated, concrete worked example (and the required end-to-end test,
per the finalized Figma-Integration TODO's Phase 7/Phase 9) of generating a
**new** screen for a product that already has an existing Figma design,
using that Figma design as a high-fidelity reference. This is the single
artifact that proves the capability actually works end to end, rather than
only proving `figma-context.json` can be produced — a generated
`figma-context.json` with no screen ever built from it would not satisfy
this use case.

## Routes through Design-Glanza — not a separate skill
Executed by the same master skill and the same 41-row
`workflows/execute-product-builder.md` pipeline as every other use case
here. A Figma reference changes what two of those rows (15 and 18) cite as
their master technique — it does not add a row, remove a row, reorder a
row, or introduce a second pipeline. See "Full-flow traceability" below for
the row-by-row proof.

## Input
- An existing Figma file with a non-trivial design system: multiple color/
  type/spacing variables, at least one multi-variant component, auto-layout
  frames. (A trivial single-frame mockup with no variables/components
  would not meaningfully exercise `figma-reference.md`'s structured
  extraction — this use case specifically needs a file worth extracting
  from.)
- A new screen requirement that does **not** already exist as a frame in
  that Figma file — chosen deliberately, so the test cannot be satisfied by
  the generator simply reproducing an existing frame.

## The scenario, step by step
```
Existing Figma product/design  +  New screen requirement
        |
        v
Figma Skill inspection (figma-use loaded first, use_figma/
get_design_context called read-only)
        |
        v
Figma Design Context produced (BRD/figma/figma-context.json +
BRD/figma/screens/*.png)
        |
        v
Existing Design Setup (reference detected/analyzed at row 15,
figma-context-consumption.md's precedence rule applied at row 18,
approval gate at row 19)
        |
        v
Existing UI-generation action pipeline (all 41 rows, unchanged order —
rows 20-27 UX, 28-31 UI/tokens/components, 32 benchmark cycle)
        |
        v
New screen generated (row 34, Implement)
        |
        v
Render (rows 35-36, Preview & Run)
        |
        v
Visual comparison — Level A (vs. the closest Figma export)
        |
        v
Figma-spec conformance — Level B (vs. figma-context.json ground truth)
        |
        v
Fix / Iterate (rows 40-41, existing feedback-routing)
```

## Pass criteria (not merely "it ran without error")
1. The new screen uses the **same** color/type/spacing tokens the Figma
   file actually defines, cited by name in `ui/design-tokens.json`/
   `ui/design-direction.md` — not Design-Glanza defaults that happen to
   look similar.
2. At least one multi-variant component from the Figma file is reused via
   its `component-registry/*` match (`figma-context.schema.json`'s
   `matchedRegistryEntry`), with the correct variant selected for the new
   screen's actual need.
3. The new screen is **not** a copy of any single existing Figma frame — a
   reviewer comparing it to the Figma file should recognize "this belongs
   to the same product" without finding it identical to any one existing
   screen (`figma-context-consumption.md`'s non-negotiable output rule).
4. Visual-benchmark Level A and Level B (`ui-engine/visual-benchmark.md`)
   both run and both report a result (pass, or a resolved gap) — "we
   didn't check" is itself a failure here, same as everywhere else in this
   engine.
5. The existing pipeline's gates (B6, B13, B15, B16, B18, B19, B20 at
   minimum) all still pass, proving the new capability didn't quietly
   weaken anything it touches.

## Negative-path run (Figma access unavailable)
Run the same scenario with Figma tool access deliberately unavailable
(simulated auth failure): confirm `figma-reference.md`'s step 4 fallback
engages, `figma-context.json.source.inspectionMode` is recorded as
`"image-fallback"` with a non-empty `fallbackReason`
(`scripts/validate-figma-context.py` fails Blocker if it isn't — this is
mechanically enforced, not left to an agent remembering to record it), and
the pipeline still completes via `reference-analysis.md`'s existing
image-only extraction at its existing Medium confidence. Level B
(Figma-spec conformance) is marked not-applicable in this run, not skipped
silently; Level A still runs if any image export exists. This is the proof
the feature degrades gracefully rather than blocking the whole pipeline
when Figma access fails.

## Full-flow traceability (required documentation, per Phase 9)
Produced against one real run of the scenario above — not a hypothetical
walkthrough. Five items:

**1. Which existing actions execute.** All 41 rows of
`workflows/execute-product-builder.md` run, in the same order, by the same
owning agent, as a non-Figma product. Rows 1-14, 19-27, 33, 35-41 show
zero Figma-specific change in *how* they execute — their inputs may carry
richer citations, their procedure does not change. Rows 15, 18, 28-32 are
the only rows carrying a Figma-specific annotation (confirmed directly in
the live table: row 15's Master technique cell now reads "...or, for a
Figma reference whose structure is inspectable, `figma-reference.md`..."
and row 18's reads "...where `figma-context.json` exists,
`figma-context-consumption.md`'s precedence rule applied here...").

**2. Where Figma analysis is injected.** Exactly two points, both inside
Design Setup, no others: row 15 (Figma Skill invoked, `figma-context.json`
produced) and row 18 (`figma-context-consumption.md`'s precedence rule
folds that context into `design-direction.md`). Rows 19-31 (13 gated
actions) run between Figma analysis and any screen generation (row 34) —
the concrete answer to "never generate immediately after reading Figma."

**3. How BRD requirements flow through.** Rows 1-7 (Intake) and rows 20-27
(Prototype UX) produce `REQ-NNN`/`FLOW-NNN`/`SCREEN-NNN`/`SCENARIO-NNN`
artifacts sourced only from the BRD and `ux-engine/*`'s own extraction
technique. Confirm, by inspecting `ux/user-flows.md`, `ux/sitemap.md`, and
`ux/screen-architecture.md` from the actual test run, that none of the
three cites `figma-context.json` as a source — a Figma citation appearing
in any of them is itself a failure of this check (it would mean Figma
leaked into WHAT, not HOW).

**4. How Figma Context influences UI decisions.** Confirm, from the test
run's `ui/design-system.md`, `ui/design-tokens.json`, `ui/components.md`,
`ui/ui-rules.md`, and `ui/responsive-rules.md`, that each Figma-matched
value/component/pattern cites its source `figma-context.json` entry by
name (`ui-engine/design-system.md`'s Figma token mapping section,
`component-registry/registry-integration.md`'s matching section), and each
non-matched value cites the Design-Glanza default it fell back to, per
`figma-context-consumption.md`'s precedence rule — zero silent/uncited
values either way.

**5. How the final screen reaches QA/Audit/Visual Benchmark/Iterate.**
Confirm `ui/visual-gap-analysis.md` and
`ui/benchmark-reports/<SCREEN-NNN>.md` show both Level A and Level B
results (`ui-engine/visual-benchmark.md`), that `qa/qa-report.md`'s Audit
section aggregates any **Figma-spec deviation** gap through the same
Blocker/Major/Minor/Note handling as every other finding (no separate
report), and that any such gap is actually fixed and revalidated through
rows 40-41 (Iterate), not left open while the screen is still declared
complete.

## Explicitly not here
- The extraction technique itself → `design-reference-engine/
  figma-reference.md`.
- The precedence/consumption contract → `design-reference-engine/
  figma-context-consumption.md`.
- The structured context's exact shape → `design-reference-engine/
  figma-context.schema.json`.
- The deterministic structural check of a produced `figma-context.json` →
  `scripts/validate-figma-context.py`.
- A product with no Design-Glanza builder yet, and no Figma reference
  either → `use-cases/existing-product.md`.
- Redesigning a product that already has a Design-Glanza builder →
  `use-cases/product-redesign.md`.
