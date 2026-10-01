# Template: Modern UI Benchmark Report

## Purpose
The required, human-readable scorecard produced at **FINALIZE**
(`ui-engine/visual-benchmark.md`'s "When to stop") for every screen —
whether generated inside a full Product Builder pass or as a standalone
screen/benchmark request. Distinct from `templates/visual-gap-analysis.md`
(the detailed, pipeline-step-by-step audit record, scored 1-5 on
`evaluation-rubric.md` dimension 21): this file is the *summary* view —
three parts, in order, none of them a new check — every category below
cites an existing engine mechanism rather than inventing one.

## Part A — Design-system validation (internal, before finalizing)
Run silently, before a screen is considered finalized — not itself the
report's visible output, but what the rest of this file summarizes:

| Check | Validates | Owning mechanism |
|---|---|---|
| **Typography** | Hierarchy, readability, consistency | `ui-engine/typography.md`, Category E |
| **Color** | Semantic usage, contrast, hierarchy | `ui-engine/color-system.md`, Category F, **B8.1** |
| **Spacing** | Consistent spacing scale and rhythm | `ui-engine/layout-system.md`, Category D |
| **Grid** | Alignment and responsive structure | `layout-system.md`'s grid, Category D, **B9** |
| **Components** | Reusable and consistent patterns | `ui-engine/component-system.md`, `component-registry/*`, Category G, **B19** |
| **Data visualization** | Appropriate chart selection and readable presentation | `visual-benchmark.md`'s Chart verification pipeline |
| **Interaction** | Clear states and affordances | Category H (state-completeness + interaction-quality halves) |
| **Accessibility** | Contrast, readability, focus/interaction | `ux-engine/accessibility.md`'s pipeline, **B8**/**B8.1** |

## Part B — Final Visual QA (the 15-point audit)
Run after generation, before the scorecard in Part C is produced. Each
item below is already owned by an existing file — this list is a
reconciliation for the report's purposes, the same discipline
`ui-audit-framework.md`'s own "Reconciling the 15-point critique
checklist" table already established (overlapping but not identical —
this list adds Information density, Production readiness, Responsive
readiness, and Overall visual polish as explicit report-level items):

1. **Visual hierarchy** → Category C
2. **Layout quality** → Category D (structural/alignment half)
3. **Typography** → Category E
4. **Spacing** → Category D (spacing half)
5. **Grid consistency** → Category D (grid half), pixel pipeline's Structure step
6. **Component consistency** → Category G
7. **Color system** → Category F, **B8.1**
8. **Data visualization** → `visual-benchmark.md`'s Chart verification pipeline
9. **Information density** → `visual-hierarchy.md`'s density/grouping rules, `layout-system.md`
10. **Interaction clarity** → Category H
11. **Accessibility** → Category I, `accessibility.md`'s full pipeline
12. **Modern visual quality** → `craft-critique.md`'s anti-cliché catalog + `ui-audit-framework.md`'s Final Visual QA closing question + the **Generic/templated** gap type
13. **Production readiness** → `component-system.md`'s Production-readiness pipeline, **B19**
14. **Responsive readiness** → `responsive-system.md`'s verification pipeline, **B9**, including the Alternative-component accessibility contract
15. **Overall visual polish** → the pixel pipeline's Micro-polish step + the Final Visual QA closing question taken as a whole

A finding against any of these 15 is recorded the same way every other
finding in this engine is: Observation → Problem → Fix, a gap type from
`visual-benchmark.md`'s table, and a P0-P3 priority — not a separate
vocabulary invented for this report.

## Part C — Scored summary (the required output)
Ten rows, each **consolidating** specific items from Part B's 15 (stated
explicitly so the consolidation is reproducible, not ad hoc):

| Scorecard row | Consolidates Part B items | Deterministic evidence available when rendering is available |
|---|---|---|
| Visual Hierarchy | 1 | None by design — emphasis/weight judgment stays an agent read |
| Layout Quality | 2 | `scripts/validate-rendered-layout.py` (alignment, overlap) |
| Typography | 3 | None by design — no rendered type-scale checker exists yet (disclosed gap, see script's own limitations) |
| Spacing & Grid | 4, 5 | `scripts/validate-rendered-layout.py` (spacing, sizing) |
| Component Quality | 6, 13 | `scripts/validate-rendered-layout.py` (sizing/alignment across a sibling set), `component-system.md`'s Production-readiness record |
| Color System | 7 | `scripts/validate-tokens.py`'s contrast math (already deterministic regardless of rendering), **B8.1** |
| Data Visualization | 8 | `scripts/validate-data-consistency.py` (Data Realism/Cross-Artifact only — Chart Purpose/Storytelling stay agent judgment) |
| Interaction Design | 9, 10 | None by design — state/interaction-quality judgment stays an agent read |
| Accessibility | 11 | `scripts/validate-tokens.py` (contrast/target-size), `scripts/validate-rendered-layout.py` (overlap) |
| Modern UI Quality | 12, 14, 15 | `scripts/validate-rendered-layout.py` (overflow, Not-accepted defect list) for 14/15's pixel-level half; the closing question (12) stays agent judgment by design |

**Scoring.** Each row is **PASS** (full 10 points), **PARTIAL** (5 points —
a real, specific, named gap exists, not merely "could be even better"),
or **FAIL** (0 points — a defect that actually blocks usability or
correctness for that category). No fourth state, no fractional points
within a row — the discrete scale is deliberate, the same way
`visual-benchmark.md`'s Priority classification resists inventing
intermediate severities.

**Evidence Type (mandatory per row, new this version).** Every row's
score is tagged with where it actually came from — never left implicit:

| Tag | Meaning |
|---|---|
| **MEASURED** | This row's score is backed by a deterministic script's actual findings against this specific screen this pass (the table above names which script, per row) — zero Blocker/Major findings from it, or every one fixed, is what earned the PASS. |
| **ASSESSED** | This row's score is an agent's qualitative read with no deterministic backing — either because no deterministic check exists for this row by design (Visual Hierarchy, Interaction Design, the closing-question half of Modern UI Quality), or because rendering was unavailable in the current environment for a row that does have a deterministic check (Layout Quality, Spacing & Grid, etc. when Playwright isn't installed). |
| **MIXED** | Part of this row's consolidated Part B items is MEASURED and part is ASSESSED (e.g. Component Quality: sizing/alignment MEASURED, the broader Production-readiness record ASSESSED). |

Each row additionally states its **Source** — the specific script name and
run (for MEASURED/MIXED) or "agent review, `ui-audit-framework.md`
Category X" (for ASSESSED) — so a reader can trace exactly what produced
the number without re-deriving it.

**Scoring ceiling tied to evidence (new this version) — do not just lower
every score, improve the evidence model instead.** A row that is purely
ASSESSED because rendering *was available this pass and simply wasn't
run* does not get scored PASS at all — per `evals/evaluation-rubric.md`
dimension 13's existing precedent ("a 'passing' score based on visual
inspection where a deterministic check was never actually run" is itself
a failure condition, not a capped pass), that row is FAIL until the
deterministic check is actually run. A row that is ASSESSED because
rendering is genuinely unavailable in the current environment, or because
no deterministic check exists for that row *by design* (see the table
above), may still score PASS/PARTIAL/FAIL on the agent's honest read —
agent judgment is not banned, only required to be disclosed as exactly
what it is. The **STATUS** band is capped by what backs it: a total of
90-100 is only labeled plain **Excellent** when Layout Quality, Spacing &
Grid, and Component Quality are each MEASURED or MIXED (the three rows
rendering evidence can directly speak to); a 90-100 total reached while
any of those three stays purely ASSESSED is instead reported as
**Strong (evidence-limited)** — same number, same section findings,
different band — with one line stating which row(s) capped it and why
(genuinely unavailable rendering vs. a design-level gap), so a future pass
with rendering available can re-earn plain Excellent on actual evidence
rather than this report silently inflating a self-assessment into the top
band.

**Output shape, verbatim** (Evidence/Source columns are the new fields
this version adds — every other line unchanged):

```
DESIGN-GLANZA MODERN UI BENCHMARK

Row                   Score   Evidence   Source
Visual Hierarchy:      XX/10   ASSESSED   agent review, ui-audit-framework.md Category C
Layout Quality:        XX/10   MEASURED   validate-rendered-layout.py (alignment/overlap)
Typography:            XX/10   ASSESSED   agent review, ui-audit-framework.md Category E
Spacing & Grid:        XX/10   MEASURED   validate-rendered-layout.py (spacing/sizing)
Component Quality:     XX/10   MIXED      validate-rendered-layout.py + agent review (Category G)
Color System:          XX/10   MEASURED   validate-tokens.py contrast math (B8.1)
Data Visualization:    XX/10   MIXED      validate-data-consistency.py + agent review (Chart pipeline)
Interaction Design:    XX/10   ASSESSED   agent review, ui-audit-framework.md Category H
Accessibility:         XX/10   MIXED      validate-tokens.py + validate-rendered-layout.py
Modern UI Quality:     XX/10   MIXED      validate-rendered-layout.py + agent closing question

TOTAL: XX/100

STATUS:
90–100 = Excellent              (requires Layout Quality, Spacing & Grid,
                                  and Component Quality each MEASURED or MIXED)
90–100 = Strong (evidence-limited)  (same total, one or more of those three
                                      rows still ASSESSED — state which, and why)
80–89  = Strong
70–79  = Needs Refinement
<70    = Fail
```

The Evidence/Source values above are illustrative of the *typical* case
(rendering available, Data Visualization only partly covered by
deterministic checks, etc.) — the actual tags/sources reported must
reflect what genuinely ran this pass, never copied from this example.

**Critical requirement — do not inflate.** A high score is never awarded
because the screen *looks* attractive. Every row is checked against
whether the screen is genuinely **Functional + Usable + Consistent +
Modern + Scalable + Production-ready** — the same "measured, not assumed"
discipline this engine already applies everywhere else (`scripts/
validate-tokens.py`'s calculated contrast over an eyeballed read; B15's
own "a score adjusted to clear the bar... fails this gate regardless of
the number recorded"). A real defect found during generation — even one
fixed before FINALIZE — is disclosed in the report's findings, not quietly
omitted because it no longer reproduces. **If the total is below 90**,
the report additionally names the specific defects found and what the
owning engine file/rule should tighten to catch the same class of issue
automatically next time — the same self-diagnostic posture the
`validate-*.py` scripts' own "what this deliberately does NOT check"
sections already model.

## When this runs
Required at **FINALIZE** for every screen — a full Product Builder pass
(folded into the existing visual-benchmark-and-audit cycle action,
`workflows/execute-product-builder.md` action 32) and a standalone
screen/benchmark request alike (there is no "lighter" exemption for an
ad hoc generation — Rule 20's "never treat the first generated UI as the
final UI" applies identically either way).

## Where it's recorded
`product-builder/ui/benchmark-reports/<SCREEN-NNN>.md` for a full Product
Builder pass — alongside, never instead of, that screen's `templates/
visual-gap-analysis.md` instance, which still owns the detailed per-step
audit trail this report only summarizes. For a standalone screen request
with no Product Builder scaffold, the report is still produced as real,
written output (chat or an equivalent artifact), per this engine's
"artifacts, not conversation" discipline — a refinement cycle that isn't
written down did not happen.

## Explicitly not here
- The detailed per-pipeline-step findings and the Initial/Final rubric
  score → `templates/visual-gap-analysis.md`.
- The P0-P3 priority definitions and gap-type table → `ui-engine/
  visual-benchmark.md`.
- The 11 lettered audit categories themselves → `ui-engine/
  ui-audit-framework.md`.
- Cross-artifact numeric consistency (a different concern from visual
  quality) → `templates/data-bindings.md`, `scripts/
  validate-data-consistency.py`.
- The rendering/measurement/reference-comparison mechanisms the Evidence
  Type column cites → `scripts/capture-render.py`, `scripts/
  validate-rendered-layout.py`, `scripts/compare-reference-visual.py`;
  the render-and-measure procedure they feed → `ui-engine/
  visual-benchmark.md`'s Render-and-measure evidence section.
