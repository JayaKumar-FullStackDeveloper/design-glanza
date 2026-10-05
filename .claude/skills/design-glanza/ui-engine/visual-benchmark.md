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

## Render-and-measure evidence (mandatory wherever rendering is available)
"Generated UI" in the table above is the **actually rendered result**, not
the source markup read by the same agent that wrote it. Wherever
`scripts/capture-render.py` is available in the current environment (it
degrades to a disclosed Note, never a silent skip, if Playwright isn't
installed — see that script's and `scripts/validate-product.py`'s own
docstrings), this comparison runs against real evidence, not prose:

1. **Render the Generated UI** — `scripts/capture-render.py` against the
   actual output file, at every breakpoint `ui-engine/responsive-system.md`
   requires (desktop/tablet/mobile) and both themes, producing real
   screenshots plus a geometric DOM manifest.
2. **Measure it** — `scripts/validate-rendered-layout.py` against that
   manifest: real overflow, alignment, spacing, sizing, and overlap
   findings computed from actual rendered pixels/geometry, never inferred
   by reading the HTML/CSS. Every finding this step produces is logged as
   a **Rendered-layout defect** gap (below) — not folded silently into
   Weak spacing/Incorrect hierarchy, because it carries a specific
   measured number (e.g. "15px top-edge drift") the qualitative gap types
   don't.
3. **Compare against the Reference, where one exists** —
   `scripts/compare-reference-visual.py` against the reference image and
   the matching rendered screenshot, producing a numeric color/layout
   similarity report. This step's output is **mandatory evidence**, not an
   optional nicety: "Reference considered" or "Visual comparison
   completed" is never written as this step's result without this
   script's actual numbers attached (color_similarity, layout_similarity,
   meaningful_mismatch) — a prose-only claim of comparison, with no
   numbers behind it, does not satisfy this step. Where Reference-Driven/
   Guideline-Driven mode applies with no single supplied asset (several
   `design-samples/` entries informed the direction instead), run this
   against the closest-matching sample and record which one; where
   Custom Design truly has no visual reference at all, this step is
   marked not-applicable, not silently skipped without a reason. **Level A
   — visual reference comparison, Figma case:** where `figma-context.json`
   (`design-reference-engine/figma-reference.md`) names a matching
   exported frame for this screen's role (`screens[].role`), that export
   is the Reference asset fed to this script — same script, same
   mechanism as any other supplied reference image, nothing new to wire
   up. **Composition-intent interpretation (added v1.0.32, made
   mandatory-not-advisory in v1.0.33):** a low `layout_similarity` from
   this script is not automatically a gap — a genuinely new screen's
   composition can legitimately differ from its closest-matching
   reference frame's (a dense data list vs. a near-empty panel, say). But
   a real benchmark run (the PerkyPet root-cause audit) found this had
   been misread as "low score, therefore automatically fine" — a missing
   section can itself produce a low-but-not-floor-crossing score, which
   is indistinguishable from a legitimate new composition by this number
   alone. So: whenever `layout_similarity` sits above the hard floor but
   well below a near-identical score, `compare-reference-visual.py`'s
   advisory `Note:`-prefixed flag (never counted toward
   `meaningful_mismatch`) is a **required trigger**, not an optional
   prompt, for the following sequence before the gap can be closed either
   way:
   ```
   Low layout_similarity (Note flagged)
           ↓
   Open the reference image and the generated screenshot side by side
   (not just read the number)
           ↓
   Run ui-audit-framework.md's Category A/G structure/component check
   against figma-context.json's composedFrom/recurrence entries
           ↓
   Determine: legitimate new composition (record why) vs. missing
   fidelity (log the specific Missing pattern gap)
   ```
   Never record "Note: expected, this is a new screen" as the finding
   itself — that sentence is only valid *after* the side-by-side
   comparison above actually ran, and the comparison's outcome (not the
   Note alone) is what gets recorded.
3b. **Level B — Figma design-system conformance (new, only where a Figma
    Design Context exists).** Independently of Level A's image-similarity
    check above, compare the Generated UI's *measured* values — from
    step 2's rendered manifest — directly against `figma-context.json`'s
    `tokens.*` ground truth (spacing, color, radius, sizing, typography):
    a rendered spacing/color/radius/sizing/typography value that
    measurably disagrees with the Figma-sourced token value it was
    supposed to use is logged as a **Figma-spec deviation** gap (below) —
    distinct from Level A, which only checks overall image similarity,
    and distinct from the existing **Rendered-layout defect** gap, which
    only checks the screen's own internal self-consistency against
    itself, never against an external ground truth. Not applicable when
    no Figma Design Context exists for this product. **Level B PASS never
    implies overall visual-fidelity PASS (stated explicitly, added
    v1.0.33):** Level B only measures whether token *values* it can see
    trace correctly and were rendered — a screen can pass Level B
    completely while a whole Figma-derived section or recurring component
    is absent, because Level B has no concept of composition or component
    presence at all. A Level B PASS only ever certifies the token-value
    half of fidelity; the composition/component half is this file's A-K
    audit and step 1's structural comparison above, and both are required
    — a Level B PASS is never, by itself, evidence that this file's
    structure/component checks were satisfied.
4. **Reconcile with Step 1's qualitative audit.** Render-and-measure
   evidence does not replace `ui-audit-framework.md`'s A-K audit or this
   file's existing gap classification — it is additional, objective
   evidence feeding the *same* gap-analysis and priority-classification
   mechanism below, resolved through the same FIX → RECHECK loop. A
   screen is never marked clean on this step purely because the
   qualitative audit passed, and never marked clean on the qualitative
   audit purely because no rendered defect was measured — both run,
   both must pass.

A **fix is only verified after re-rendering.** Changing source code in
response to a Rendered-layout defect or a Reference mismatch does not
close that finding — step 2 of the Mandatory refinement cycle below
("re-run validation for the specific category/pipeline step(s) the fix
actually touched") means, for a rendered finding, actually re-running
`capture-render.py` + `validate-rendered-layout.py` (and
`compare-reference-visual.py` where relevant) and confirming the specific
measured number is now within tolerance — not re-reading the changed
source and assuming the number improved.

## Gap analysis categories
Run `ui-engine/ui-audit-framework.md`'s A–K categories as the audit, then
classify every finding into one of these gap types so the refinement pass
knows what kind of fix is needed:

| Gap type | What it means |
|---|---|
| **Missing pattern** | Design Direction specified something (a component, a state, an interaction) that the Generated UI simply doesn't have — including, where a Figma Design Context exists, a `screens[].composedFrom`-named region or a `components[].recurrence`-named component absent with no recorded reason (`ui-engine/ui-audit-framework.md` Category A/G, added v1.0.33) |
| **Incorrect hierarchy** | The relative emphasis in the Generated UI doesn't match what Design Direction (or the reference) established |
| **Excessive decoration** | The Generated UI added visual elements Design Direction never called for — most often traceable to `craft-critique.md`'s anti-cliché catalog |
| **Weak spacing** | Density or the padding/gap relationship departs from what was specified |
| **Poor density** | The comfortable/compact/dense register doesn't match Design Direction's stated preference or the domain's actual need — including, where a Figma Design Context exists, a recorded density note (`figma-reference.md`'s Density extraction, added v1.0.33) the Generated UI's actual content-to-whitespace ratio measurably departs from |
| **Inconsistent components** | The same UI need was solved two different ways across screens, or a component departs from the governed inventory |
| **Wrong interaction pattern** | A pattern was used (e.g. a modal where Design Direction called for a drawer) that contradicts the recorded decision |
| **Weak accessibility** | A structural or perceptual accessibility rule was specified but not actually honored in the build |
| **Domain mismatch** | Category K of the audit framework failed — the screen doesn't read as belonging to its actual domain |
| **Generic/templated** | `ui-audit-framework.md`'s Final Visual QA closing question came back "generic" — the screen could plausibly be handed to an unrelated SaaS product with no rework, even if every individual pipeline step and category above passed. Distinct from Domain mismatch (that's specifically category K's product-types conventions check) and from Excessive decoration (that's specifically added elements) — this gap type covers the aggregate judgment those two don't individually catch. |
| **Data inconsistency** | `scripts/validate-data-consistency.py` (below, Cross-Artifact Data Realism) found a declared relationship between two displayed numbers that doesn't actually hold — a KPI disagreeing with its own chart's latest point, a supporting metric contradicting the KPIs it's computed from, a labeled peak that isn't the series' real maximum, a table total disagreeing with the KPI it restates. Distinct from the Chart pipeline's existing Data Realism step (a value's own plausibility in isolation) — this is two-or-more displayed values disagreeing with each other. |
| **Rendered-layout defect** | `scripts/validate-rendered-layout.py` (above, Render-and-measure evidence) found a real, measured overflow, misalignment, inconsistent spacing/sizing, or overlap in the actually-rendered screen — carries the specific measured number (e.g. "scrollWidth 405 vs clientWidth 80") rather than a qualitative description. Distinct from `ui-audit-framework.md`'s Alignment/Spacing/Sizing/Overflow categories (those are the qualitative audit pass); this gap type is that same defect class, but with rendering evidence behind it where rendering was available. |
| **Reference mismatch** | `scripts/compare-reference-visual.py` reported `meaningful_mismatch: true` against the stated reference with no recorded, deliberate design-direction reason for the departure — a generated screen whose color/tonal register or layout/density rhythm drifted from what the reference established, not merely "didn't copy it pixel-for-pixel" (a reference is design language, not a pixel target; see `design-samples/*/README.md`). |
| **Figma-spec deviation** | Level B (above): a rendered spacing/color/radius/sizing/typography value measurably disagrees with `figma-context.json`'s ground-truth token value for that same need — distinct from **Rendered-layout defect** (internal self-consistency only) and from **Reference mismatch** (overall image similarity only). Only applies when a Figma Design Context exists for this product; otherwise this row is simply inapplicable, the same way the Chart pipeline is inapplicable to a chart-free screen. |

A gap is recorded even when it's minor — the point of this file is to make
"looks fine to me" checkable against something concrete, not to filter
findings down to only the ones that feel urgent.

## Priority classification
Every gap above also gets a priority — not a second competing scale, the
same four-level severity already shared everywhere in the engine
(`config/output-contract.md`'s Blocker/Major/Minor/Note), labeled P0-P3
here because that's the vocabulary this specific critique-and-iteration
loop uses when deciding what gets fixed automatically versus logged:

| Priority | = Severity | Meaning | Action this cycle takes |
|---|---|---|---|
| **P0** | Blocker | Blocks usability, or a major visual defect — any item on `ui-audit-framework.md`'s "not accepted" defect list, a failed Chart Visual Storytelling check, or an Operating Rule violation | Fixed before FINALIZE, unconditionally — never shipped, never waived |
| **P1** | Major | Significant production-quality issue — materially degrades correctness, consistency, or usability without blocking the core outcome | Fixed before FINALIZE, unless explicitly waived with a logged reason — the same waiver discipline every other Major finding in the engine already uses |
| **P2** | Minor | Polish issue — noticeable but doesn't undermine the outcome | Logged; fixed within this cycle where cheap to do alongside a P0/P1 fix already touching the same area, otherwise deferred with the gap recorded — never silently dropped |
| **P3** | Note | Optional refinement — an observation or non-binding suggestion | Logged only; never blocks FINALIZE |

A priority is assigned at the same time as the gap type above, not as a
separate pass — every row of the gap-classification output carries both.

## Mandatory refinement: the critique-and-iteration loop
Per Rule 20 and gate **B15**: at least one refinement cycle is required
before a UI pass is considered complete, regardless of how the first
generated draft looks. The fixed sequence below is that cycle made
explicit — the same steps 0-4 this file has always required, named so the
procedure reads as one deliberate loop rather than a list of checks:

```
GENERATE → CRITIQUE → IDENTIFY DEFECTS → PRIORITIZE DEFECTS → FIX →
RECHECK → FINALIZE
```

| Stage | Is this file's |
|---|---|
| GENERATE | The screen as first produced (or, on a later pass, as a baseline diff already resolved per step 0) |
| CRITIQUE | Step 1 — the three-way comparison and `ui-audit-framework.md` A-K audit |
| IDENTIFY DEFECTS | Step 1's gap classification (above) |
| PRIORITIZE DEFECTS | Step 1's priority classification (above) |
| FIX | Step 2 |
| RECHECK | Step 2's re-run, step 3a's render check |
| FINALIZE | Step 4, gated by "When to stop" below |

0. **If this screen already has a baseline** (`visual-regression/
   baseline-model.md` — i.e. this is not the screen's first pass), diff
   the current draft against it first (`scripts/
   validate-visual-regression.py`, Rule 25) and resolve every Critical/
   High/Medium finding — either fixed or an approved `visual-regression/
   baseline-updates.md` record — before proceeding to step 1. This is
   B20's own check, distinct from and prior to the conformance check
   below.
1. Run the three-way comparison and gap analysis above on the first draft
   — the audit categories it's built from (`ui-audit-framework.md`'s A-K)
   are run in that file's Pixel-level verification pipeline order
   (Structure → Alignment → Spacing → Sizing → Typography → Component →
   Responsive → Micro-polish), not in an arbitrary order, since a later
   step's check (e.g. Alignment) presumes an earlier one (Structure)
   already holds. This pass is where that pipeline's own "not accepted"
   defect list gets actively checked against the actual draft — never
   assumed clear because the draft renders without error. Category I
   (Accessibility) of that same audit is itself
   `ux-engine/accessibility.md`'s own Accessibility verification pipeline
   (Keyboard → Focus → Contrast → Semantics → ARIA → Forms → Status
   Communication → Modal/Drawer → Charts → Responsive/Touch), run here
   the same way the Chart pipeline is (below) — its Contrast and Target
   Size steps are calculated by `scripts/validate-tokens.py`, never
   visually assumed, per gate **B8**. Every screen is additionally checked
   independently at each breakpoint it supports via `ui-engine/
   responsive-system.md`'s own Responsive verification pipeline (Desktop
   baseline → Tablet restructuring → Mobile transformation → Adaptation-
   decision audit → Not-accepted defect scan, gate **B9**) — a screen
   reviewed only at the desktop width it was designed at has not cleared
   this step, regardless of how correct that one width looks. Where this
   screen has at least one KPI tied to a chart, table, or another KPI,
   **Cross-Artifact Data Realism** also runs here, independently of
   whether the screen contains a chart at all: `templates/
   data-bindings.md`'s manifest declares each such relationship, and
   `scripts/validate-data-consistency.py` recomputes it from the
   manifest's own series data — a KPI must equal its own chart's latest
   point, "today" must correspond to that chart's own latest plotted
   date, a supporting metric (e.g. an average) must equal its stated
   derivation from its parent KPIs, a labeled peak must equal the series'
   actual maximum, and a table total must agree with the KPI it restates.
   A disagreement here is never explained away as "each number looked
   fine individually" — individually-plausible numbers that contradict
   each other are exactly what this check exists to catch, and a finding
   is logged as a **Data inconsistency** gap (above), never silently
   reconciled by quietly editing one display to match the other without
   recording which one was actually wrong and why. Wherever rendering is
   available in the current environment, this same step 1 also runs the
   **Render-and-measure evidence** pass above (capture → measure →
   compare-against-reference) — its findings are logged as **Rendered-
   layout defect** and **Reference mismatch** gaps (above) alongside
   whatever this qualitative audit itself found, not as a separate pass
   run some other time.
2. **If gaps were found:** fix every P0 and un-waived P1 first (P2/P3 may
   ride along where cheap, per the Priority classification table above),
   then re-run validation for the specific category/pipeline step(s) the
   fix actually touched — never the full pipeline from scratch on every
   single fix, but never narrower than the fix's actual blast radius either
   (e.g. a spacing fix re-checks Spacing and, since it can shift edges,
   Alignment too). Repeat this FIX → RECHECK pair until no new gap is found
   or a P0/P1 gap remains genuinely unresolvable (escalate the latter per
   the normal feedback-routing table, never ship it silently). This is not
   an endless-redesign loop — see "When to stop" below for the exact
   conditions that close it.
3. **If no gaps were found on the first pass:** still record that the
   comparison ran and found nothing — an unresolvable "we didn't check"
   gap is not an acceptable way to skip this step. A genuinely clean first
   draft is recorded as such, not skipped as unnecessary.
3a. **At least one non-resting state must actually be rendered, not only
    described.** Category H of `ui-audit-framework.md` already requires
    every mandatory state to be *designed*; this step is the render-level
    check that catches the gap between "considered in the spec" and "shown."
    For this screen, produce at least one real mockup/frame of its `empty`,
    `loading`, or `system error` state (`ux-engine/state-design.md`) —
    whichever is most representative of this screen's actual failure/edge
    mode — alongside the resting-state screen already produced. A screen
    whose only rendered evidence is its populated happy-path state fails
    this step, even if the state's *content* was correctly specified
    elsewhere.
4. **Once this screen's Final status is `pass`**, capture (first pass) or
   update (later pass, per any approved Baseline Update from step 0) its
   `visual-regression/baseline-model.md` snapshot — a screen is never left
   confirmed-clean with a stale or absent baseline for the next pass to
   diff against.

### When to stop (FINALIZE)
FINALIZE is reached the first time every one of these holds at once —
never earlier, and this cycle is never extended past this point chasing
further polish once they do:
- Zero unresolved P0 findings.
- Zero unresolved P1 findings — fixed, or explicitly waived with a logged
  reason.
- `ui-audit-framework.md`'s Pixel-level verification pipeline passes: zero
  unresolved items from its "not accepted" defect list (visual QA).
- `ux-engine/accessibility.md`'s Accessibility verification pipeline
  passes, gate **B8** (accessibility QA).
- `ui-engine/responsive-system.md`'s Responsive verification pipeline
  passes, gate **B9** (responsive QA).
- Category H's state coverage shows zero blank cells across the mandatory
  13 states (component-state QA), per **B7**.
- `evals/evaluation-rubric.md`'s score meets its stated threshold on every
  dimension — no dimension below 3, zero Tier A dimensions below 4, per
  gate **B11**.
- Where rendering was available in the current environment: zero
  unresolved **Rendered-layout defect** gaps, and zero unresolved
  **Reference mismatch** gaps without either a fix or a recorded
  deliberate-departure reason. A screen is never marked `pass` on
  this step because "the code looks right" when a render-and-measure
  pass was possible and simply wasn't run — see this file's Render-and-
  measure evidence section above.

A screen clean on its very first CRITIQUE still completes one real RECHECK
confirming that, per step 3 above — "nothing to fix" is not the same as
"never checked." None of the above is satisfied by relaxing a dimension's
bar, re-scoring generously, or narrowing what counts as a defect to reach
the threshold faster: the rubric's existing weighting and this file's
gap/priority definitions are fixed inputs, never adjusted outputs — a
screen that doesn't clear them is fixed, not rescored.

Record the full history — what the first draft's gap analysis found (or
that it found nothing), what changed, and what the re-check confirmed,
including this screen's Initial Score and Final Score
(`templates/visual-gap-analysis.md`'s own fields for exactly this) — in
that file's instance for this screen/pass. A refinement cycle that isn't
written down did not happen, per the same "artifacts, not conversation"
discipline `workflows/execute-product-builder.md` already applies
everywhere else.

**FINALIZE additionally requires `templates/modern-ui-benchmark-report.md`'s
scored summary** — the human-readable "DESIGN-GLANZA MODERN UI BENCHMARK"
scorecard, for every screen this cycle produced, whether generated inside
a full Product Builder pass or as a standalone screen/benchmark request.
This is a required *summary* of findings already recorded above, in that
file's own three-part shape (Design-system validation, the 15-point Final
Visual QA audit, the 10-row scored output) — never a second, independent
audit mechanism, and never an excuse to skip the detailed recording this
section already requires.

## Chart verification pipeline
An additional, mandatory pass for any screen containing at least one
chart — run inside the Mandatory refinement cycle above, not a separate
gate, the same way the pixel-level pipeline (`ui-audit-framework.md`) and
the closing question sit inside this same cycle. Every step below cites
its owning rule rather than restating it:

```
Chart Purpose Check → Chart Type Check → Data Realism Check → Axis
Check → Legend Check → Tooltip Check → Filter Check → State Check →
Accessibility Check → Responsive Check → Visual Storytelling Check
```

| Step | What it verifies |
|---|---|
| **Chart Purpose** | This is genuinely the right visualization *class* for the job — a single tracked number with no meaningful trend/comparison uses `composition-patterns.md`'s KPI/Stat Card instead, per `component-system.md`'s Data visualization section; a chart added because "dashboards have charts" without a stated insight fails here first, before any downstream step is even relevant. |
| **Chart Type** | `component-system.md`'s data-shape table (trend→line/area, comparison→bar, composition→stacked/donut only within its slice cap, distribution→histogram/box) — the type matches what relationship the data actually has, never preference. |
| **Data Realism** | Rule 10 applied to every value on the chart, not just its axis labels (already required by `component-system.md`'s chart-label-realism note): realistic ranges, dates, currency, and domain terminology for *this* product — a revenue chart with suspiciously round numbers, or a SaaS metric with e-commerce terminology, fails here even if the chart type and axes are otherwise correct. This step checks a value's own plausibility in isolation; whether this chart's values actually *agree* with a KPI, table, or annotation elsewhere on the same screen is the Mandatory refinement cycle's own Cross-Artifact Data Realism check (above, step 1) — a fresh, separate check, not restated here. |
| **Axis** | Real domain values and real dates (never a `D1`/`D2` index placeholder), correct units stated, meaningful tick intervals (not so sparse the shape is unreadable, not so dense they collide), and the zero-baseline rule for bar/column charts — no truncated or dual-scale axis that visually exaggerates a difference the data doesn't actually show. |
| **Legend** | Present only when more than one series is shown (a single-series chart with a legend is clutter, not clarity); labels match the data's own terminology; each legend entry's color is the same one used on the chart, never a near-miss; legend position/wrapping has a stated responsive behavior at narrow widths, not silent overlap. |
| **Tooltip** | On hover/focus, reveals the exact value, the date/time or category it belongs to, and — where a comparison period is part of the chart's story — the prior-period value alongside it; formatted with the same units/currency/locale convention as the rest of the screen, never a raw unformatted number. |
| **Filter** | Where the screen has dashboard-level filters (date range, category, status, region/vendor), this chart actually responds to them — `ux-engine/search-ux.md`'s Filter facets section now states explicitly that a filter scopes every data-bearing component on the screen, not just an adjacent table; a chart that stays unfiltered while the table beside it narrows is a Filter Check failure. |
| **State** | Loading (skeleton axes), empty (states why), error (with a recovery action), **partial data** (the query succeeded but returned fewer points than the chart type needs to read cleanly — shown as itself, not silently rendered as if complete), and **insufficient data** (fewer than the ~3-point floor `component-system.md`'s chart entry already names — shown as a stated message, e.g. "not enough data yet," never an empty-looking blank chart) are each distinguishable from one another, per `state-design.md`'s own distinctness discipline. |
| **Accessibility** | A text-equivalent summary or data-table alternative exists (already required by the Chart registry entry); color-blind-safe per `color-system.md`'s ramps; keyboard-reachable tooltip-equivalent per `interaction-design.md`'s hover-and-focus rule. |
| **Responsive** | Legend/axis labels reflow or abbreviate rather than overlapping at narrow widths; touch gets tap-to-reveal in place of hover, per the Chart registry entry's existing Responsive field. |
| **Visual Storytelling** | The chart states a meaningful title (names what's being measured, not a generic "Overview"), a subtitle/context line (time period, comparison period where relevant), and — where the data has one — a meaningful highlight (an emphasized endpoint, a labeled peak/dip) that gives the viewer a starting read rather than a bare, uninterpreted plot; a chart that requires the viewer to derive the story entirely themselves from raw marks has not finished this step. |

**A chart that fails Visual Storytelling even after passing every
mechanical step above is rejected and redesigned, not shipped as a
technically-correct but silent plot** — the standard this whole pipeline
exists to check is whether the chart communicates a decision-relevant
insight, not merely whether it renders without error. Rejection routes
through this file's existing gap-analysis mechanism (a **Generic/
templated** or **Incorrect hierarchy** gap type, whichever fits the actual
cause) and the normal fix→re-check cycle above — never a separate
mechanism.

## Explicitly not here
- The audit categories themselves → `ui-engine/ui-audit-framework.md`.
- The composition-craft numeric checks → `ui-engine/craft-critique.md`.
- The gap-analysis document's exact fields →
  `templates/visual-gap-analysis.md`.
- The gate this enforces → `config/quality-gates.md`'s **B15**.
- Diffing this pass against a *prior* pass's confirmed-clean state (a
  temporal concern this file has no notion of by design) →
  `visual-regression/*`, gate **B20**.
- The Cross-Artifact Data Realism manifest's exact fields and the
  relationships it declares → `templates/data-bindings.md`; the
  deterministic recomputation itself → `scripts/
  validate-data-consistency.py`.
- The rendering/screenshot/DOM-geometry capture mechanism itself →
  `scripts/capture-render.py`; the geometric analysis that turns a
  manifest into Rendered-layout defect findings → `scripts/
  validate-rendered-layout.py`; the reference-image numeric similarity
  check → `scripts/compare-reference-visual.py`. This file only requires
  that their evidence feed the gap analysis above — their own thresholds
  and mechanics live in their docstrings, not duplicated here.
