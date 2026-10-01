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
| **Generic/templated** | `ui-audit-framework.md`'s Final Visual QA closing question came back "generic" — the screen could plausibly be handed to an unrelated SaaS product with no rework, even if every individual pipeline step and category above passed. Distinct from Domain mismatch (that's specifically category K's product-types conventions check) and from Excessive decoration (that's specifically added elements) — this gap type covers the aggregate judgment those two don't individually catch. |

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
   this step, regardless of how correct that one width looks.
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
| **Data Realism** | Rule 10 applied to every value on the chart, not just its axis labels (already required by `component-system.md`'s chart-label-realism note): realistic ranges, dates, currency, and domain terminology for *this* product — a revenue chart with suspiciously round numbers, or a SaaS metric with e-commerce terminology, fails here even if the chart type and axes are otherwise correct. |
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
