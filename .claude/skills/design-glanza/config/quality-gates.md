# Quality Gates

## Responsibility
Binary/checklist criteria that must be satisfied before work proceeds — both
between phases (Section A) and across the 21 measurable quality dimensions
(Section B) that those phase gates actually check. This file answers "can we move
forward?" — it does not assign a graded score (see `evals/evaluation-rubric.md`)
and it does not define output structure (see `output-contract.md`).

## Section A — Phase-transition gates

| Transition | Must be true before proceeding |
|---|---|
| Intake → Empathize | Requirement Completeness gate (B1) passes |
| Empathize → Define | Personas/stakeholders identified with sourced-or-assumption-tagged findings |
| Define → Ideate | `templates/product-definition.md` complete with falsifiable success criteria |
| Ideate → Architect | A direction is chosen with documented rationale; Business Logic Completeness gate (B2) passes |
| Architect → Design Setup | Domain classification confirmed; dependency graph has no unresolved circular dependency |
| Design Setup → Prototype | Design Direction Completeness gate (B13) passes — `product-builder/ui/design-direction.md` complete per template, its reference classification (Reference-Driven/Guideline-Driven/Custom/Default) stated with rationale, and user confirmation obtained or explicitly waived; Research-to-Design Traceability gate (B16, findings/insight/principle stage) passes |
| Prototype → Implement | User-Flow (B3), Information Architecture (B4), Screen Architecture (B5), Design System (B6), State Coverage (B7), Accessibility (B8, structural), Responsive Behavior (B9), Visual Benchmark & Audit Cycle (B15), Research-to-Design Traceability (B16, decision/pattern stage), UX Scenario Coverage (B17, spec-level checkpoint), Token Inheritance Integrity (B18), Component Registry Conformance (B19), Visual Regression Integrity (B20), Product Memory Integrity (B21, consultation checkpoint) gates all pass |
| Implement → Preview & Run | Implementation Readiness gate (B12) still holds; `output/*` is non-empty for any screen marked implemented this pass |
| Preview & Run → Test | Preview & Run Verification gate (B14) passes |
| Test → Audit | `methodology/test.md` validation against Define's success criteria passes with no Blocker findings |
| Audit → Iterate | Traceability (B10), QA (B11), Accessibility (B8, conformance), Research-to-Design Traceability (B16, validation stage), UX Scenario Coverage (B17, walked checkpoint), Visual Regression Integrity (B20, final re-check), Product Memory Integrity (B21, consistency checkpoint) gates all pass |
| Iterate → (re-entry) | Every finding routed to its owning phase/file; re-entry starts at that phase, not Intake, unless the finding invalidates upstream work |

Escalation on failure: a **Blocker** or un-waived **Major** finding (severity
vocabulary in `output-contract.md`) blocks the transition; **Minor**/**Note**
findings are logged and do not block, per Rule 13 (fix and revalidate applies only
to blocking findings by default).

**Logged, non-blocking findings persist across Iterate cycles rather than
disappearing once noted.** A Minor/Note finding stays in `templates/
qa-report.md`'s record, carried forward run over run, until it's actually
fixed or explicitly waived with a reason — not silently dropped because a
later pass didn't re-surface it. Where the backlog of logged findings grows
large enough to need prioritizing, rank by **severity × how often the
affected surface is used**, weighed against the **effort** to fix it — the
same frequency signal `methodology/empathize.md` dimension 7 and
`design-judgment.md`'s task-frequency factor already use elsewhere, applied
here to triaging accumulated debt rather than an individual design decision.

## Section B — The 21 measurable quality gates

Each gate below states: what it measures, the pass criterion, and what checks it.

### B1 — Requirement Completeness
- **Measures:** completeness of `templates/requirement-matrix.md`.
- **Pass criterion:** every row has a unique ID, a type
  (functional/non-functional), a source-or-assumption tag, a priority, and at
  least one owning role where actor-dependent. 0 rows missing a required field.
  Every acceptance criterion in the source input maps to ≥1 requirement row.
- **Checked by:** `scripts/validate-requirements.py`.

### B2 — Business Logic Completeness
- **Measures:** whether Rule 3's 12-point checklist (objective, actors, actions,
  system behavior, validation, status, permissions, dependencies, triggers,
  success, failure, edge cases) has been addressed per feature.
- **Pass criterion:** 12/12 checklist items addressed or explicitly marked
  not-applicable per feature, in `product-intelligence/business-logic.md` output.
  0 features with an unaddressed, unmarked item.
- **Checked by:** `agents/product-architect.md` review; aggregated in audit.

### B3 — User-Flow Completeness
- **Measures:** completeness of `templates/user-flow.md` instances.
- **Pass criterion:** every flow has a defined entry point and exit
  condition/success criteria; every role variant identified in
  `product-intelligence/user-roles.md` that touches the flow has its branch
  covered; every edge case flagged for this flow by
  `product-intelligence/edge-case-engine.md` has a corresponding branch or an
  explicit deferral.
- **Checked by:** `agents/ux-architect.md` review.

### B4 — Information Architecture
- **Measures:** completeness and navigability of `templates/sitemap.md`.
- **Pass criterion:** every node has defined role visibility; no node exceeds the
  max hierarchy depth set in `ux-engine/information-architecture.md`; 0 orphan
  nodes (unreachable from any flow or nav path).
- **Checked by:** `agents/ux-architect.md` review.

### B5 — Screen Architecture
- **Measures:** completeness of `templates/screen-architecture.md` instances.
- **Pass criterion:** every screen in the sitemap has a corresponding
  screen-architecture entry; every entry has a region map and one identified
  primary action; every entry traces to ≥1 flow step.
- **Checked by:** `scripts/validate-screens.py`.

### B6 — Design System
- **Measures:** completeness and consistency of `templates/design-system.md`
  and its machine-readable twin, `product-builder/ui/design-tokens.json`
  (Rule 23, `design-tokens/*`).
- **Pass criterion:** every token category required by
  `design-tokens/design-tokens.schema.json` is present in
  `design-tokens.json` (no missing category, no missing required semantic
  token); 0 raw values flagged by `scripts/validate-tokens.py` with no
  corresponding Token gap log entry (`design-tokens/token-audit.md`) — the
  concrete, checkable form of "0 undocumented one-off values"; every
  semantic color pairing meets the contrast rule in
  `ui-engine/color-system.md`, in every declared theme mode
  (`design-tokens/theming.md`); every component either cites a
  `component-registry/*` entry as its Registry base or is logged as a
  deliberate new component with a stated reason (Rule 24) — the same
  "logged, never silent" treatment as a raw token value.
- **Checked by:** `agents/design-system-expert.md`, enforced deterministically
  by `scripts/validate-tokens.py` for the token half.

### B7 — State Coverage
- **Measures:** completeness of `templates/state-matrix.md` against Rule 6's
  mandatory state set (initial, loading, success, empty, validation error, system
  error, permission denied, processing, completed, cancelled, conflict, timeout,
  offline — both timeout and offline where applicable), plus any states added
  by the active `product-types/*.md` overlay.
- **Pass criterion:** 0 blank cells — every screen/component × state cell is
  marked designed / not-applicable / deferred (with reason if deferred).
- **Checked by:** `scripts/validate-states.py`.

### B8 — Accessibility
- **Measures:** structural (`ux-engine/accessibility.md`) and perceptual
  (`ui-engine/color-system.md`) conformance, run in that file's
  Accessibility verification pipeline order: Keyboard → Focus → Contrast
  → Semantics → ARIA → Forms → Status Communication → Modal/Drawer →
  Charts → Responsive/Touch.
- **Pass criterion:** checked twice — structurally at Prototype (focus order and
  keyboard-equivalence defined for every interaction; semantic roles mapped) and
  for full conformance at Audit (against the stated baseline, or a
  domain-mandated stricter bar from `product-types/*.md`; 0 color-only
  meaning encodings; 100% of interactive elements keyboard-operable). Every
  pipeline step is recorded, not just the ones an agent happened to check —
  a screen that skips a step (most commonly Modal/Drawer or Charts, on a
  screen that doesn't obviously look like it needs them) fails this gate
  the same as one with no accessibility pass recorded at all. Where a step
  has a deterministic, calculable form, it is calculated, not visually
  assumed: `scripts/validate-tokens.py`'s `_check_contrast` (real WCAG
  relative-luminance ratios, not an eyeballed "looks readable") and
  `_check_target_size` (every `sizing.control*` token against the 24px
  WCAG 2.2 minimum) both return 0 findings, or every returned finding is
  fixed or logged as a Token gap. A production-ready accessibility score
  based on visual inspection alone, where a deterministic check was
  available and skipped, does not satisfy this gate.
- **B8.1 — Semantic contrast (tinted-background pairing).** A benchmark
  run found that a semantic hue passing contrast against the plain
  surface does not mean it passes against its own lighter, tinted
  background — the pairing a badge, chip, status pill, delta indicator,
  semantic icon container, or avatar initials/background actually
  renders on. `scripts/validate-tokens.py`'s `_check_contrast` now runs a
  third pass checking every declared `{onSoft, soft}` pair (`design-
  tokens/semantic-tokens.md`'s optional triplet extension) independently
  of whether that same key's plain foreground/background pair already
  passed — 0 findings, or every returned finding fixed or logged as a
  Token gap, in both light and dark mode, same as the existing passes.
- **Checked by:** `agents/accessibility-expert.md`, the Contrast and
  Target Size steps (including B8.1) additionally enforced
  deterministically by `scripts/validate-tokens.py`. Where rendering is
  available (`scripts/capture-render.py` — see B9/B14/B15 below),
  `scripts/validate-rendered-layout.py`'s overlap check additionally
  catches a focus ring, badge, or icon rendered in a way that visually
  collides with adjacent content at an actual breakpoint — a real-render
  signal this gate did not have access to before, feeding the same
  Blocker/Major/Minor/Note handling as every other B8 finding. This does
  not replace `validate-tokens.py`'s contrast/target-size math (no
  rendering-based contrast check exists); it is additional evidence
  where rendering is available, never a required substitute for it.

### B9 — Responsive Behavior
- **Measures:** completeness of `ui-engine/responsive-system.md` application,
  run in that file's Responsive verification pipeline order: Desktop
  baseline → Tablet restructuring → Mobile transformation → Adaptation-
  decision audit → Not-accepted defect scan.
- **Pass criterion:** every screen has defined reflow behavior at every mandatory
  breakpoint, independently verified at each one (not assumed correct at
  Tablet/Mobile because Desktop looked right); every element that changes
  between breakpoints has one of the seven named adaptation decisions
  recorded (stack/collapse/hide/move/become-scrollable/become-alternative-
  component/remain-fixed) — an element that merely "got smaller" with no
  stated decision fails this gate; priority content (per `ui-engine/
  visual-hierarchy.md`) remains reachable at the smallest breakpoint; touch
  targets meet the minimum size rule at touch-relevant breakpoints; zero
  unresolved instances of `responsive-system.md`'s "Not accepted" defect
  list (overflow, clipping, overlapping, accidental horizontal scroll,
  broken alignment, unreadable text, compressed controls, inconsistent
  card sizing, broken charts, inaccessible drawers, hidden critical
  actions) at any supported breakpoint. Every **become-alternative-
  component** decision that produces an interrupting overlay (Sidebar →
  Drawer, Desktop navigation → Mobile drawer) additionally has
  `responsive-system.md`'s Alternative-component accessibility contract
  actually checked, not just the decision recorded: focus entry, focus
  trap, Escape-to-close, focus restoration to the trigger, background
  inertness, functional keyboard navigation, a visible focus indicator,
  correct `dialog`/`complementary` ARIA role, and correct
  `aria-expanded`/`aria-controls` on the trigger — a decision recorded
  with the contract unchecked fails this gate the same as an undecided
  element does.
- **Rendering evidence (where available).** The "Not accepted" defect
  list above (overflow, clipping, overlapping, broken alignment,
  inconsistent card sizing, among others) is exactly what
  `scripts/capture-render.py` + `scripts/validate-rendered-layout.py`
  measure directly from a real render at each mandatory breakpoint
  (desktop/tablet/mobile) and theme (light/dark) — see `ui-engine/
  visual-benchmark.md`'s Render-and-measure evidence section. Wherever
  Playwright is installed in the current environment, this gate's "every
  screen independently verified at each breakpoint" requirement is
  satisfied with measured evidence for these specific defect types, not
  only an agent's visual read of the markup; where it isn't installed,
  the agent-review check below still applies in full and the gap is
  disclosed (`scripts/validate-product.py` emits a Note saying so),
  never silently treated as passed.
- **Checked by:** `agents/ui-designer.md` review, jointly with
  `agents/accessibility-expert.md` for any become-alternative-component
  decision producing an interrupting overlay — the same joint-ownership
  precedent B15/B16/B17 already use.

### B10 — Traceability
- **Measures:** integrity of the REQ → FLOW → SCREEN → COMPONENT → TEST chain
  (Rule 9).
- **Pass criterion:** 0 orphaned requirements (no downstream artifact) unless
  explicitly marked deferred/out-of-scope; 0 orphaned downstream artifacts (no
  traceable upstream requirement or assumption tag).
- **Checked by:** `product-intelligence/traceability.md`'s check, surfaced via
  `scripts/validate-product.py`.

### B11 — QA
- **Measures:** aggregate validator and rubric health.
- **Pass criterion:** `scripts/validate-product.py` (aggregating **B1/B5/B7**
  structural checks, **B6/B8** token checks including **B8.1**'s semantic
  tinted-background contrast pass, **B14**'s generated-artifact structural
  validation, **B15**'s Cross-Artifact Data Realism check, and — wherever
  Playwright is installed in the current environment — **B15**'s rendered-
  layout evidence via `scripts/capture-render.py` +
  `scripts/validate-rendered-layout.py` against every `.html` file under
  `output/`) returns all-pass; `evals/evaluation-rubric.md` score meets or
  exceeds its stated threshold on every dimension; 0 unresolved Blocker or
  un-waived Major findings in `templates/qa-report.md`. Every deterministic
  validator's findings participate in the same Blocker/Major/Minor/Note
  severity handling as every other B11 input — never a second, parallel
  pass/fail scale. (B9's new Alternative-component accessibility contract
  has no deterministic script backing it and is not aggregated here — it
  stays an agent-review check, per B9's own "Checked by.") Where rendering
  isn't available, `validate-product.py` returns a single disclosed Note
  explaining that, and every other aggregated check still runs and still
  gates this result in full — an unavailable optional capability is never
  silently treated as a pass, and never blocks the rest of the gate either.
- **Checked by:** `agents/qa-expert.md`.

### B12 — Implementation Readiness
- **Measures:** whether Implement can start safely.
- **Pass criterion:** every screen has a complete `templates/screen-specification.md`
  (no missing field); every component has a complete
  `templates/component-spec.md`; `product-intelligence/dependency-analysis.md`'s
  graph has a defined build order with no unresolved circular dependency.
- **Checked by:** `agents/product-architect.md` sign-off before
  `workflows/build-product.md` begins.

### B13 — Design Direction Completeness
- **Measures:** completeness of `product-builder/ui/design-direction.md`
  against `templates/design-direction.md`'s required fields, and whether the
  design-reference decision was actually made (not defaulted to silently).
- **Pass criterion:** every required field in the template is filled or
  explicitly marked not-applicable with a reason; the reference-decision
  classification (Reference-Driven / Guideline-Driven / Custom Design /
  Default Design-Glanza, per `design-reference-engine/reference-selection.md`)
  is stated with its rationale; where the user is available to confirm, an
  explicit "does this match your expectations" confirmation is recorded (or
  a stated reason it was waived — e.g. an unattended/batch run). 0 required
  fields blank with no reason.
- **Checked by:** `agents/design-setup-specialist.md`.

### B14 — Preview & Run Verification
- **Measures:** whether the implemented output actually launches and runs
  locally, per `product-builder/workflows/preview-report.md` against
  `templates/preview-report.md`'s required fields — whether that output
  is structurally sound to begin with — and, new this version, whether
  it is also free of overflow/alignment/spacing/sizing/overlap defects
  when actually rendered, wherever rendering is available.
- **Pass criterion:** the build succeeds; a local dev server starts with a
  detected URL/port; no unhandled runtime error blocks the primary
  implemented screen(s); every required field in the preview report is
  filled (project path, framework, start command, local URL, port, build
  status, runtime status, implemented screen(s), preview status). An
  optional public/external preview (e.g. ngrok) is recorded only if the
  user explicitly requested one — its absence never fails this gate.
  **Before** this (`workflows/preview-run.md`'s new structural-validation
  step), `scripts/validate-generated-artifact.py` runs against `output/*`
  and returns 0 Blocker/Major findings — unbalanced CSS braces, a
  malformed selector list mixing a selector with an at-rule, a duplicate
  custom-property declaration, an invalid `@media` condition, unbalanced
  HTML tags, a duplicate `id`, a broken same-document reference, a
  missing `alt`/accessible name, a missing local asset reference, or
  unbalanced JS brackets. This is a structural safety net distinct from
  — and checked before — the build/runtime checks above: a file can be
  structurally invalid in ways that don't actually break the build or
  throw a visible runtime error, which is exactly why the two checks are
  both required, neither standing in for the other. **Rendered-layout
  evidence, layered on top of (not replacing) the above:** a file can
  pass every structural check above — balanced braces, balanced tags, no
  duplicate properties — and still be visually broken when actually
  rendered (overflowing text, misaligned siblings, overlapping elements);
  `scripts/validate-generated-artifact.py` deliberately stays structural/
  code-only and does not try to detect this. Wherever Playwright is
  installed, `scripts/capture-render.py` + `scripts/validate-rendered-layout.py`
  run as a separate, additional pass against the same `output/*.html`
  files and must also return 0 Blocker findings — a screen with clean,
  valid HTML/CSS that nonetheless overflows or misaligns when rendered
  has **not** cleared this gate, even though the structural check above
  passed. This is a deliberately separate validator (not merged into
  `validate-generated-artifact.py`) so the fast, dependency-free
  structural check always runs, and the rendering-dependent check runs
  wherever its one extra dependency is available.
- **Checked by:** the executing session, per `workflows/preview-run.md` —
  no dedicated reasoning agent, the same posture B12/Implement already
  has; the structural-validation step is deterministic
  (`scripts/validate-generated-artifact.py`), not an agent judgment call;
  the rendered-layout step is equally deterministic
  (`scripts/validate-rendered-layout.py`) wherever rendering is available.

### B15 — Visual Benchmark & Audit Cycle Completeness
- **Measures:** whether the generated UI was actually checked against
  `ui-engine/ui-audit-framework.md`'s 11 categories, run in that file's
  Pixel-level verification pipeline order, and
  `ui-engine/visual-benchmark.md`'s three-way (Reference/Design Direction/
  Generated UI) comparison, per `templates/visual-gap-analysis.md`.
- **Pass criterion:** at least one full audit-and-refinement cycle is
  recorded for every screen produced this pass — a first-pass audit
  covering every pipeline step (Structure/Alignment/Spacing/Sizing/
  Typography/Component/Responsive/Micro-polish), a gap classification (or
  an explicit "no gaps found") **per step**, and a re-check after any
  refinement (or an explicit re-confirmation when pass 1 was clean). Zero
  unresolved instances of `ui-audit-framework.md`'s "not accepted" defect
  list (approximate alignment, inconsistent spacing, arbitrary margins,
  arbitrary component dimensions, misaligned icons, inconsistent
  typography, inconsistent card heights, uneven grids, accidental
  whitespace, overlapping elements, clipped content, broken responsive
  layouts) — a screen with one of these still present fails this gate even
  if every category was nominally "checked." The Final Visual QA step's
  closing question ("does this look intentionally designed for this
  product, or could it have been generated for any unrelated SaaS
  product?") must also be answered and recorded — a `generic` verdict is
  the **Generic/templated** gap type (`visual-benchmark.md`'s gap-type
  table) and routes through the same refinement-and-re-check cycle as any
  other gap; it is never passed silently because every pipeline step above
  individually checked out. A modern-looking treatment does not answer
  this question by itself — `visual-trends.md`'s Trend Adoption Gate still
  applies underneath it. Any screen containing at least one chart
  additionally runs `visual-benchmark.md`'s Chart verification pipeline
  (Chart Purpose → Chart Type → Data Realism → Axis → Legend → Tooltip →
  Filter → State → Accessibility → Responsive → Visual Storytelling) —
  a chart that fails Visual Storytelling is rejected and redesigned, the
  same non-negotiable treatment a Blocker/Major pixel-precision finding
  already gets, never passed because it renders without error. A screen
  with no recorded visual-gap-analysis instance, or one that skips a
  pipeline step, the closing question, or (where a chart is present) the
  chart pipeline, fails this gate regardless of how the screen actually
  looks. Every finding recorded during this cycle additionally carries a
  P0-P3 priority (`visual-benchmark.md`'s Priority classification,
  reconciled onto this same Blocker/Major/Minor/Note scale) — a screen with
  an unresolved P0, or an un-waived P1, fails this gate even if every
  category was nominally checked, per that file's "When to stop" list. The
  gate's instance in `templates/visual-gap-analysis.md` additionally
  records an Initial Score and Final Score (evaluation-rubric.md dimension
  21, assessed before and after the refinement cycle) — a cycle that
  doesn't show the score actually holding or improving (or a genuine
  "already clean" explanation) has not demonstrated the refinement did
  anything, and a score adjusted to clear the bar rather than earned by an
  actual fix fails this gate regardless of the number recorded.
- **Cross-Artifact Data Realism.** Where this screen has at least one KPI
  tied to a chart, table, or another KPI, `templates/data-bindings.md`'s
  manifest declares each such relationship and
  `scripts/validate-data-consistency.py` recomputes it: a KPI must equal
  its own chart's latest data point, "today" must correspond to that
  chart's own latest plotted date, a supporting metric (e.g. an average)
  must equal its stated derivation from its parent KPIs, a labeled peak
  must equal the series' actual maximum, and a table total must agree
  with the KPI it restates. A disagreement is logged as a **Data
  inconsistency** gap (`visual-benchmark.md`'s gap-type table) and routes
  through the same refinement-and-re-check cycle as any other gap — a
  screen where every number individually looks plausible but disagrees
  with another number on the same screen has not cleared this gate.
- **Modern UI Benchmark Report.** FINALIZE for this screen additionally
  requires `templates/modern-ui-benchmark-report.md`'s scored summary —
  the "DESIGN-GLANZA MODERN UI BENCHMARK" scorecard (Design-system
  validation, the 15-point Final Visual QA audit, the 10-row scored
  output) — for every screen, whether produced inside a full Product
  Builder pass or as a standalone screen/benchmark request. A score
  adjusted to clear a threshold rather than earned by an actual fix fails
  this gate regardless of the number recorded, the same discipline this
  gate's Priority-classification and Cross-Artifact Data Realism
  sub-criteria above already state.
- **Rendered-evidence evaluation angles (new this version).** The
  qualitative pixel-level pipeline above is necessary but not, by itself,
  proof that the screen is correct when actually rendered — a benchmark
  run found 100%-scored screens with real, measurable UI defects that a
  source-code-only read had missed. Wherever Playwright is installed in
  the current environment, this gate's audit-and-refinement cycle
  additionally covers these 11 angles, each backed by a real render, not
  an agent's reading of the markup:
  1. **Rendered layout** — the screen's actual DOM geometry after
     rendering (`scripts/capture-render.py`'s manifest), not its source
     structure.
  2. **Actual spacing** — `scripts/validate-rendered-layout.py`'s
     measured gap between real sibling elements, against that element
     set's own modal gap.
  3. **Actual alignment** — that same script's measured shared-edge
     drift between real siblings, in real pixels.
  4. **Actual component dimensions** — measured height/width consistency
     across a repeating element set, from real `getBoundingClientRect()`
     data.
  5. **Overflow/clipping** — real `scrollWidth`/`scrollHeight` vs.
     `clientWidth`/`clientHeight`, per `ui-audit-framework.md`'s Text
     overflow sub-list.
  6. **Responsive rendering** — the same capture run at desktop, tablet,
     and mobile viewport sizes, each independently measured (not assumed
     from the desktop measurement).
  7. **Visual reference comparison** — `scripts/compare-reference-visual.py`'s
     numeric color/layout similarity against the stated reference image,
     feeding the **Reference mismatch** gap type
     (`visual-benchmark.md`'s gap-type table) — never "Reference
     considered" with no numbers behind it.
  8. **Component-level visual consistency** — the sibling-set grouping
     `validate-rendered-layout.py` applies (same parent + same leading
     class) checked for navigation, header, KPI cards, forms, buttons,
     filters, tables, charts, badges, alerts, modals, drawers, empty
     states, and loading states specifically, wherever a screen contains
     one of these — not only the generic full-DOM pass.
  9. **Fix/re-render verification** — per `visual-benchmark.md`'s "a fix
     is only verified after re-rendering" rule: a Rendered-layout defect
     or Reference mismatch closed by a source-code change alone, with no
     matching re-capture + re-measure confirming the number actually
     moved, has not been verified — it is still an open finding.
  10. **Visual regression** — this screen's capture feeds **B20**'s
      optional rendered baseline (below), so a later pass can diff
      against *this* pass's real rendered evidence, not only its
      structural baseline.
  11. **Figma-spec conformance** (new, requires rendering AND a Figma
      Design Context — only where both hold) —
      `scripts/validate-rendered-layout.py`'s measured spacing/color/
      radius/sizing/typography values compared against
      `figma-context.json`'s ground-truth token values
      (`ui-engine/visual-benchmark.md`'s Level B), feeding the
      **Figma-spec deviation** gap type. Not applicable, not simply
      absent, when no Figma Design Context exists for this product even
      if rendering is available — the same stated-inapplicability
      treatment the Chart pipeline already gets for a chart-free screen.

  Wherever rendering isn't available, all 11 angles are disclosed as
  not run (the single Note `scripts/validate-product.py` emits) and the
  gate still requires everything else above in full — an unavailable
  optional capability never lowers this gate's bar, and its absence is
  never silently treated as these angles having passed. Angle 11 carries
  one additional applicability condition on top of rendering availability
  (a Figma Design Context must also exist) — the other 10 have no such
  second condition.
- **Checked by:** `agents/ui-designer.md` and
  `agents/design-system-expert.md`, per `ui-engine/visual-benchmark.md`'s
  mandatory-cycle procedure — no new dedicated agent; Cross-Artifact Data
  Realism is deterministic (`scripts/validate-data-consistency.py`), not
  an agent judgment call; the 10 rendered-evidence angles above are
  likewise deterministic (`scripts/capture-render.py`,
  `scripts/validate-rendered-layout.py`,
  `scripts/compare-reference-visual.py`) wherever rendering is available.

### B16 — Research-to-Design Traceability
- **Measures:** whether research findings actually shaped the design,
  rather than existing as documentation beside it — per `design-research/
  research-to-design.md`'s mandatory-influence rule.
- **Pass criterion:** checked at three points, cumulatively, per finding:
  (1) at Design Setup → Prototype, every `RF-NNN` finding has a recorded
  Evidence, Insight, and — for CRITICAL/HIGH priority — a stated Design
  Principle (`product-builder/research/research-findings.md`,
  `research-summary.md`); (2) at Prototype → Implement, every CRITICAL
  finding and every HIGH finding affecting a core workflow has a cited UX
  Decision and/or UI Pattern in `ux/*`/`ui/*`, or an explicit, reasoned
  `deferred`/`rejected` status — 0 such findings left `open`; (3) at Audit →
  Iterate, every `applied` CRITICAL/HIGH finding has a stated Validation
  check result from `methodology/test.md`'s Test phase. A pattern proposed
  from a common/default option has its Anti-Generic Design challenge
  recorded (`design-research/pattern-analysis.md`'s five questions), not
  just its conclusion.
- **Checked by:** `agents/design-setup-specialist.md` (stage 1),
  `agents/ux-architect.md` and `agents/ui-designer.md` jointly (stage 2, the
  same joint-ownership precedent B15 already uses), `agents/qa-expert.md`
  (stage 3) — no new dedicated agent.

### B17 — UX Scenario Coverage
- **Measures:** whether the product was validated as a complete end-to-end
  user journey — every flow walked across the mandatory 8 scenario types,
  structurally complete and experientially continuous — per
  `ux-scenario-testing/coverage-matrix.md`.
- **Pass criterion:** checked at two points, cumulatively: (1) at
  Prototype → Implement, every `FLOW-NNN` has a fully populated
  `ux/ux-coverage-matrix.md` row — 0 blank cells, every gap-detection
  finding at Blocker severity resolved; (2) at Audit → Iterate, every
  `covered`-status `SCENARIO-NNN` has actually been walked via
  `continuity-audit.md` with 0 unresolved Blocker/Major findings (dead
  ends, ambiguous CTAs, missing feedback, inconsistent patterns, broken
  contextual consistency).
- **Checked by:** `agents/ux-architect.md` and `agents/interaction-
  designer.md` jointly (checkpoint 1), `agents/qa-expert.md`
  (checkpoint 2) — no new dedicated agent, the same joint-ownership
  precedent B15/B16 already use.

### B18 — Token Inheritance Integrity
- **Measures:** the structural relationship between the Master Token Set
  (`ui-engine/*`) and this product's Token Set
  (`product-builder/ui/design-tokens.json`), per `design-tokens/
  token-inheritance.md` — distinct from **B6**, which measures whether
  generated screens actually *use* the tokens correctly; this gate
  measures whether the token *set itself* is a valid extension of the
  master, not a fork of it.
- **Pass criterion:** every path in `design-tokens.json` is either (a) a
  required master category/token with a product-specific value, (b) a
  recognized optional extension (`secondary`, `dataViz`), or (c) under the
  `product.*` namespace — 0 unrecognized top-level keys or unauthorized
  scale extensions (`scripts/validate-tokens.py`'s inheritance check); no
  closed scale (radius, elevation, motion, border-width, sizing, z-index,
  the type scale, spacing, grid, breakpoints) has been redefined with an
  extra or altered step; `$inherits.masterSkillVersion` is present and
  names a real `config/master-config.md` version.
- **Checked by:** `agents/design-system-expert.md`, enforced
  deterministically by `scripts/validate-tokens.py` — no new dedicated
  agent.

### B19 — Component Registry Conformance
- **Measures:** the structural relationship between the master
  Component Registry (`component-registry/*`) and this product's
  component inventory (`product-builder/ui/components.md`) — distinct
  from **B6**, which measures whether a component's own spec is complete
  and token-conformant; this gate measures whether the product actually
  *reused* the master registry rather than reinventing what it already
  covers.
- **Pass criterion:** every `COMPONENT-NNN` instance either (a) cites a
  `component-registry/components-*.md` entry as its Registry base, (b) is
  a stated instance of a `composition-patterns.md` organism, or (c) is
  logged as a deliberate new component with a stated reason its purpose
  doesn't match anything in the registry (`registry-integration.md`'s
  registry-first check) — 0 components with none of the three. Citing a
  Registry base is necessary but not sufficient: `ui-engine/
  component-system.md`'s Production-readiness pipeline (Component exists
  → States identified → States designed → Interaction behavior defined →
  Responsive behavior defined → Accessibility behavior defined → Visual
  consistency verified) must be recorded complete for every component
  instance, not just its first two steps — a component whose spec stops
  at "cites Button as its base" with no states-designed/interaction/
  responsive/accessibility record fails this gate the same as one citing
  no base at all. A component is never marked complete because its
  default/resting state alone looks correct.
- **Checked by:** `agents/design-system-expert.md` — no new dedicated
  agent, the same agent that already owns B6 and B18.

### B20 — Visual Regression Integrity
- **Measures:** whether a screen's current state has drifted from its
  last confirmed-clean baseline without review — per `visual-regression/
  {baseline-model,diff-detection}.md`. Checked twice: structurally at
  Prototype → Implement (does this pass's spec regress the prior
  baseline) and again at Audit → Iterate (does the built/final state
  still hold, the same "checked twice" posture B8 already uses).
- **Pass criterion:** every screen with an existing baseline has been
  diffed against it this pass (`scripts/validate-visual-regression.py`);
  every Critical/High/Medium finding is either fixed or has an approved
  `visual-regression/baseline-updates.md` record with a stated reason —
  0 unresolved findings of any of those three severities. A screen with
  no baseline yet (first generation) is not gated by B20 — it's gated by
  B15, whose clean pass is what triggers the first baseline capture.
- **Optional rendered baseline layer (new this version).** Where
  rendering is available, `visual-regression/baseline-model.md`'s second,
  complementary rendered layer (screenshots + DOM-geometry manifest +
  component snapshots, per breakpoint/theme) is also captured/updated at
  the same two checkpoints as the structural baseline, never on its own
  schedule. Diffing against it is additional evidence, not a second
  competing pass/fail path: a meaningful rendered-layer drift
  (re-measured via `scripts/validate-rendered-layout.py` against the
  stored manifest) is logged and resolved the same way a structural B20
  finding is, under the same severity scale — this gate does not grow a
  separate pixel-delta tolerance system of its own. Do not make this
  layer the only regression mechanism: a screen with no rendered baseline
  (rendering unavailable in the current environment) is still fully
  gated by the structural baseline alone, exactly as before.
- **Checked by:** `agents/qa-expert.md`, enforced deterministically by
  `scripts/validate-visual-regression.py` for the structural layer, and
  — wherever rendering is available — `scripts/validate-rendered-layout.py`
  re-run against the stored rendered baseline's manifest for the optional
  second layer; no new dedicated agent either way.

### B21 — Product Memory Integrity
- **Measures:** whether decisions are actually being remembered and
  consulted, rather than re-derived or silently contradicted — per
  `product-memory/{memory-model,consultation-rule,contradiction-
  prevention}.md`.
- **Pass criterion:** checked at two points: (1) Prototype/design-time —
  every significant decision (`product-memory/auto-recording.md`'s
  threshold) has a recorded `ADR-NNN`, and the acting agent states which
  of `consultation-rule.md`'s three outcomes applied before proceeding;
  (2) Audit — `scripts/validate-memory.py` returns 0 Blocker/Major
  findings (no duplicate IDs, no dangling supersession/`Related`
  references, no invalid status), and every flagged *potential*
  contradiction (two `accepted` ADRs with overlapping scope and no
  supersession link) has been reviewed and resolved — either a
  supersession recorded or confirmed as genuinely non-conflicting, never
  left unreviewed.
- **Checked by:** `agents/{product-architect,ux-architect,ui-designer,
  design-system-expert}.md` for the decisions in their own domain
  (design-time checkpoint), `agents/qa-expert.md` (Audit checkpoint),
  enforced deterministically by `scripts/validate-memory.py` — no new
  dedicated agent.

## Explicitly not here
- *How* to produce the artifact being gated → owned by the relevant
  `methodology/`, `product-intelligence/`, `ux-engine/`, `ui-engine/`,
  `design-research/`, `ux-scenario-testing/`, `design-tokens/`,
  `component-registry/`, `visual-regression/`, `product-memory/`, or
  `design-reference-engine/` file.
- Scored/graded quality assessment beyond pass/fail → `evals/evaluation-rubric.md`.
- Step-by-step execution order within a phase → `workflows/*.md`.
- The severity vocabulary and report shapes referenced above → `output-contract.md`.
