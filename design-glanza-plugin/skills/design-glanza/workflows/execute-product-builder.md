# Workflow: Execute Product Builder

## Responsibility
The concrete, artifact-producing procedure a **generated Product Builder**
(`products/<slug>/product-builder/`) itself executes, action by action, for
one product. This is one level more concrete than `create-product.md` (which
orchestrates Design-Glanza's *decision* to build a product and scaffold it) —
this file is the runbook the Product Builder follows once it exists, mapping
every required action to the master technique it uses and the exact file it
must write. It is reusable, generic procedure (Rule 15, Product Isolation) —
referenced by every generated `product-builder/SKILL.md`, never copied into
one.

## Artifacts, not conversation
Every action below is only done once its artifact file is written under
`product-builder/` (or `output/` for Implement) — reasoning that stays only in
conversation context does not count as complete, and no downstream action may
consume an upstream action's output until that file exists. This is the
mandatory, concrete form of `config/output-contract.md`'s phase-completion
report requirement ("what was produced — files/artifacts touched or
created"): here, "what was produced" always resolves to a specific path.

## The lifecycle
Matches `config/master-config.md`'s phase registry exactly — restated only as
an index, not redefined:

```
INTAKE -> EMPATHIZE -> DEFINE -> IDEATE -> ARCHITECT -> DESIGN SETUP -> PROTOTYPE -> IMPLEMENT -> PREVIEW & RUN -> TEST -> AUDIT -> ITERATE
```

## The pipeline actions, mapped to phase, technique, and artifact
41 total rows in the table below — 24 correspond to the originally-requested
numbered list (`#` column), 17 were added since (Design Setup's 8 —
v1.0.10's restructured Design Research actions (3 rows, replacing v1.0.9's
single folded-in action — Research Brief, Evidence gathering, Insight/
Principle synthesis) plus the original 5, Preview & Run's 2, v1.0.11's 2 new
UX scenario-testing actions (spec-level derivation at the end of
Prototype-UX, walked audit at the Test->Audit bridge), plus 4 the engine's
own dependency chain always required — Build empathy model, Select a
solution approach, Confirm domain(s), Build visual hierarchy/UI rules —
plus v1.0.9's new mandatory Visual Benchmark & Audit Cycle action — each
marked `-` in the `#` column rather than renumbering or displacing the
original 24).

Two actions the source material implies but doesn't separately number —
building the Empathy Model (Empathize) and selecting a solution approach
(Ideate) — are included below because the lifecycle cannot skip a phase; they
sit between the numbered actions that depend on them. **Execution order
follows the master engine's own dependency chain, not raw numeric order**:
e.g. `ux-engine/user-flow-engine.md` states that `information-architecture.md`
consumes its flows, and that file states `navigation-system.md` consumes its
hierarchy — so flows (requested #11) are built before IA (#9) and navigation
(#10), even though they're listed later. The requested number is kept in the
table for traceability back to this requirement; the **Order** column is the
actual sequence.

| Order | # | Action | Phase | Master technique | Artifact |
|---|---|---|---|---|---|
| 1 | 1 | Read all available product requirements | INTAKE | `product-intelligence/brd-analysis.md` (input-type recognition) | reads `BRD/*` |
| 2 | 2 | Analyze the complete BRD | INTAKE | `brd-analysis.md`'s full 20-point checklist — business logic is never optional, even for UI-only input | `requirements/brd-analysis-notes.md` |
| 3 | 4 | Extract requirements | INTAKE | `product-intelligence/requirement-engine.md` (`REQ-NNN`) | `requirements/requirement-matrix.md` |
| 4 | 5 | Identify business rules | INTAKE | `product-intelligence/business-logic.md` (`BR-NNN`) | `requirements/business-logic.md` |
| 5 | 6 | Identify users and permissions | INTAKE | `product-intelligence/user-roles.md` (`ROLE-NNN`) | `requirements/user-roles.md` |
| 6 | 7 | Identify dependencies (initial pass) | INTAKE | `product-intelligence/dependency-analysis.md` (`DEP-NNN`) | `requirements/dependency-analysis.md` |
| 7 | 8 | Identify edge cases | INTAKE | `product-intelligence/edge-case-engine.md` (`EDGE-NNN`) | `requirements/edge-cases.md` |
| 8 | - | Build the empathy model | EMPATHIZE | `methodology/empathize.md` (11 dimensions, per role from step 5) | `product/product-definition.md` (Empathy section) |
| 9 | 3 | Build the product definition | DEFINE | `methodology/define.md` (8 outputs) | `product/product-definition.md` |
| 10 | - | Select a solution approach; check Product Memory first, record as ADR | IDEATE | `methodology/ideate.md` (8-point evidence-based selection), `product-memory/{consultation-rule,auto-recording}.md` | `product/product-definition.md` (Chosen Approach section); `memory/decision-records.md` (ADR-NNN, always significant) |
| 11 | - | Confirm domain(s), sequence dependencies; check Product Memory first, record as ADR | ARCHITECT | `product-intelligence/domain-classifier.md` + `domain-standards.md`, `dependency-analysis.md` (refined), `product-memory/{consultation-rule,auto-recording}.md` | `domain/domain-application-notes.md`; `requirements/dependency-analysis.md` (updated); `memory/decision-records.md` (ADR-NNN where significant) |
| 12 | - | Write the Research Brief; classify full vs. lightweight research | DESIGN SETUP | `design-research/research-engine.md`, `design-research/templates/research-brief.md` | `research/research-brief.md` |
| 13 | - | Gather research evidence — Domain, Interaction, Visual, Competitor/Pattern | DESIGN SETUP | `design-research/{domain-analysis,interaction-analysis,visual-analysis,competitor-analysis,pattern-analysis}.md` | `research/research-findings.md` (`RF-NNN` records, Evidence/Observation fields) |
| 14 | - | Derive insights and design principles; map every Critical/High finding to a design implication; apply the Anti-Generic Design challenge | DESIGN SETUP | `design-research/{insight-model,research-to-design}.md` | `research/research-findings.md` (Insight/Confidence/Priority/Design principle fields complete); `research/research-summary.md` |
| 15 | - | Detect and analyze design references, if any | DESIGN SETUP | `design-reference-engine/reference-analysis.md` | `ui/design-direction.md` (Reference analysis section) |
| 16 | - | Run the design questionnaire | DESIGN SETUP | `design-reference-engine/design-questionnaire.md` | `ui/design-direction.md` (Visual style/Layout/Typography/Color/Components/Interaction/Responsive/Accessibility/Brand sections) |
| 17 | - | Classify the design-reference decision, select a default sample if needed | DESIGN SETUP | `design-reference-engine/reference-selection.md`, `design-samples/` | `ui/design-direction.md` (Reference classification, Design inspiration sections) |
| 18 | - | Write the complete Design Direction document, citing every Critical/High `RF-NNN` finding's design principle | DESIGN SETUP | `design-reference-engine/design-direction.md` + `templates/design-direction.md` | `ui/design-direction.md` (complete) |
| 19 | - | Present the Design Direction Summary and gate on approval | DESIGN SETUP | `workflows/design-setup.md` Step 5 — B13 + B16 (findings/insight/principle stage) gates | `ui/design-direction.md` (Approval status recorded) |
| 20 | 11 | Build user flows | PROTOTYPE (UX) | `ux-engine/user-flow-engine.md` (`FLOW-NNN`, recovery paths) | `ux/user-flows.md` |
| 21 | 9 | Build information architecture | PROTOTYPE (UX) | `ux-engine/information-architecture.md` | `ux/sitemap.md` |
| 22 | 10 | Build navigation architecture | PROTOTYPE (UX) | `ux-engine/navigation-system.md` (13 concerns; breadcrumbs never default) | `ux/navigation.md` |
| 23 | 12 | Build screen architecture | PROTOTYPE (UX) | `templates/screen-architecture.md` region map + `ui-engine/layout-system.md` composition pattern | `ux/screen-architecture.md` |
| 24 | 13 | Build interaction architecture | PROTOTYPE (UX) | `ux-engine/interaction-design.md` + `form-design.md` | `ux/ux-rules.md` |
| 25 | 16 | Build state matrix | PROTOTYPE (UX) | `ux-engine/state-design.md` (13 mandatory states) | `ux/state-matrix.md` |
| 26 | 18 | Build accessibility rules | PROTOTYPE (UX+UI) | `ux-engine/accessibility.md` (structural) + `ui-engine/color-system.md` (perceptual) | `ux/accessibility.md` |
| 27 | - | Derive UX scenarios per flow across the 8 mandatory types, build the UX Coverage Matrix, run the spec-level gap-detection check | PROTOTYPE (UX) | `ux-scenario-testing/{scenario-model,scenario-types,gap-detection,coverage-matrix}.md` — B17 (spec-level checkpoint) gate | `ux/scenarios.md` (`SCENARIO-NNN` records); `ux/ux-coverage-matrix.md` |
| 28 | 14 | Build design system | PROTOTYPE (UI) | `ui-engine/design-system.md` + `typography.md`/`color-system.md`/`layout-system.md`, per the approved `ui/design-direction.md` | `ui/design-system.md` |
| 29 | 15 | Build component architecture | PROTOTYPE (UI) | `ui-engine/component-system.md` (8-point framework, iconography) | `ui/components.md` |
| 30 | - | Build visual hierarchy / UI rules | PROTOTYPE (UI) | `ui-engine/visual-hierarchy.md`, `visual-trends.md` (register selection, consistent with `ui/design-direction.md`) | `ui/ui-rules.md` |
| 31 | 17 | Build responsive rules | PROTOTYPE (UI) | `ui-engine/responsive-system.md` | `ui/responsive-rules.md` |
| 32 | - | Run the mandatory critique-and-iteration loop (visual-benchmark-and-audit cycle); where a baseline exists, diff current vs. baseline first; cite every Critical/High `RF-NNN` finding applied in a screen's UI pattern | PROTOTYPE (UI) | `ui-engine/ui-audit-framework.md` (11 A-K categories) + `visual-benchmark.md` (three-way comparison, mandatory refinement, Priority classification) + `visual-regression/*` (baseline diff) — B15 + B16 (decision/pattern stage) + B20 (structural checkpoint) gates | `ui/visual-gap-analysis.md` (one `templates/visual-gap-analysis.md` instance per screen, including Initial/Final score); `research/research-findings.md` (Status updated to `applied`/`deferred`); `ui/baselines/<SCREEN-NNN>.json` (captured/updated) |
| 33 | 19 | Build implementation plan | ARCHITECT->IMPLEMENT bridge | build order from step 11's dependency graph, gated by `config/quality-gates.md` B12 | `workflows/implementation-notes.md` |
| 34 | 20 | Implement the product, where applicable | IMPLEMENT | `workflows/build-product.md` | `output/*`; `workflows/implementation-notes.md` updated with status |
| 35 | - | Detect framework, verify build, start local dev server, detect URL/port | PREVIEW & RUN | `workflows/preview-run.md` steps 1-4 | `workflows/preview-report.md` (project path, framework, start command, build status, local URL, port) |
| 36 | - | Verify runtime, fix build/runtime issues, finalize the Preview & Run report | PREVIEW & RUN | `workflows/preview-run.md` steps 5-8 — B14 gate | `workflows/preview-report.md` (complete) |
| 37 | 21 | Validate the implementation, including Validation for every `applied` Critical/High `RF-NNN` finding | TEST | `methodology/test.md` — all 9 dimensions, not just task completion; `design-research/research-to-design.md`'s Validation step | `qa/qa-report.md` (Test section); `research/research-findings.md` (Validation field recorded) |
| 38 | - | Walk every `covered` UX scenario against the built (or spec) result; run the continuity/gap audit; finalize the UX Coverage Matrix | TEST->AUDIT bridge | `ux-scenario-testing/continuity-audit.md`, `gap-detection.md` (re-run) — B17 (walked checkpoint) gate | `ux/ux-coverage-matrix.md` (Checkpoint status updated) |
| 39 | 22 | Audit the product | AUDIT | `workflows/audit-product.md`, `scripts/validate-*.py`, `config/quality-gates.md` Section B | `qa/qa-report.md`, `qa/traceability.md` |
| 40 | 23 | Fix identified issues | ITERATE | routed per `methodology/design-thinking.md`'s feedback-routing table to whichever phase/file actually owns the defect | whichever artifact above owns the fix |
| 41 | 24 | Revalidate | ITERATE -> back to TEST/AUDIT | re-run only the specific failed gate(s), not the whole pipeline from scratch | `qa/qa-report.md` updated |

**Actions 12–19 (Design Setup, now including v1.0.10's restructured
Research Brief/Evidence/Insight actions in place of v1.0.9's single folded-in
Design Research action), 27 (v1.0.11's new spec-level UX scenario-testing
action), 32 (v1.0.9's mandatory Visual Benchmark & Audit Cycle), 35–36
(Preview & Run), and 38 (v1.0.11's new walked UX scenario-testing action)
are new** — not part of the original 24-action numbering, hence `-` in the
`#` column, the same convention already used for the other
originally-unnumbered actions (Build the empathy model, Select a solution
approach, Confirm domain(s), Build visual hierarchy/UI rules).

**"Where applicable" (action 24):** some engagements stop at a complete,
gated specification with no code output (a planning-only pass) — in that
case `output/` legitimately stays empty, but every gate up through Prototype
(B1-B9) must still pass; "where applicable" is not license to skip Test/Audit
for whatever *was* built.

## Completion criteria — the happy path is not enough
A product (or the specific scope under an Iterate pass) is complete only when
**all** of the following hold, per Rule 12/13 (`config/operating-rules.md`)
and `methodology/design-thinking.md`'s loop-termination rule:

- `methodology/test.md`'s **all nine** evaluation dimensions pass — task
  completion passing while usability, error prevention, edge cases,
  accessibility, responsiveness, or business-rule correctness fail is **not**
  complete, it's one dimension out of nine.
- `config/quality-gates.md`'s Audit -> Iterate gate passes: B10
  (Traceability) and B11 (QA) both green, with every earlier gate (B1-B9,
  B12, B13, B14, B15, B16, B17, B18, B19, B20, B21) still holding — a
  later fix that silently regresses an earlier gate reopens the scope, it
  doesn't get a pass by association with the fix.
- **B15 (Visual Benchmark & Audit Cycle Completeness)** passed before
  Implement began — a screen whose generated UI was never checked against
  its reference/design direction, or whose first pass was simply accepted
  with no recorded refinement cycle, is not complete regardless of how the
  screen looks (Rule 20).
- **B16 (Research-to-Design Traceability)** passed at every one of its
  three checkpoints — every Critical/High research finding has a recorded
  Design Principle, a cited UX Decision/UI Pattern (or an explicit,
  reasoned deferral), and a Validation result — a product whose research
  exists only as a document next to a design made some other way is not
  complete regardless of how thorough that document looks (Rule 21).
- **B17 (UX Scenario Coverage)** passed at both checkpoints — every
  `FLOW-NNN` has a fully populated coverage-matrix row and every `covered`
  scenario has actually been walked with no unresolved dead end, missing
  screen/transition/action/validation/feedback, ambiguous CTA, or
  inconsistent pattern — a product validated only screen by screen, never
  walked as a complete journey, is not complete regardless of how well
  each individual screen tests (Rule 22).
- **B20 (Visual Regression Integrity)** passed at both checkpoints —
  every screen with an existing baseline has been diffed against it, with
  every Critical/High/Medium finding either fixed or an approved,
  reasoned Baseline Update — a product where a later pass silently broke
  an earlier, already-confirmed screen is not complete regardless of how
  clean that pass's own new work looks (Rule 25).
- **B21 (Product Memory Integrity)** passed at both checkpoints — every
  significant decision has a recorded `ADR-NNN`, and every flagged
  potential contradiction has been reviewed and resolved (a supersession
  recorded, or confirmed genuinely non-conflicting) — a product that
  re-derives or silently contradicts its own prior decisions is not
  complete regardless of how correct any single pass looks in isolation
  (Rule 26).
- **B13 (Design Direction Completeness)** passed before Prototype's UI pass
  began — a product whose screens were built with no established, approved
  direction (or an explicitly-waived one) is not complete regardless of how
  polished the result looks.
- **B14 (Preview & Run Verification)** passed before Test began — a product
  whose implementation was never actually launched and previewed locally
  (Rule 19) is not complete regardless of how correct the code looks; a
  build or runtime failure discovered only here is fixed before Test, not
  carried into it as a known issue.
- B7 (State Coverage) means **every** mandatory state is designed or
  explicitly marked not-applicable/deferred with a reason — a screen with
  only its success state built is not state-complete.
- B8 (Accessibility) and B9 (Responsive Behavior) are checked as
  thoroughly as B1 (Requirement Completeness) — a beautiful, working happy
  path that fails contrast or breaks at a mandatory breakpoint is not
  complete.
- Any Blocker or un-waived Major finding anywhere (`config/output-contract.md`
  severity vocabulary) keeps the scope open regardless of whether the
  primary flow works end-to-end.

## Explicitly not here
- *How* each cited master technique works → the file named in the table.
- Design-Glanza's own decision to scaffold a product and the master-level
  phase sequence → `create-product.md`.
- The Design Setup procedure itself → `design-setup.md`.
- The Design Research Engine's own technique → `design-research/*`.
- The UX Scenario Testing engine's own technique → `ux-scenario-testing/*`.
- The visual regression/baseline-diffing technique itself →
  `visual-regression/*`.
- The Product Memory/ADR technique itself → `product-memory/*`.
- The visual-benchmark-and-audit cycle's own technique → `ui-engine/
  {ui-audit-framework,visual-benchmark}.md`, `templates/visual-gap-analysis.md`.
- The Implement-phase build-sequencing procedure itself → `build-product.md`.
- The Preview & Run procedure itself → `preview-run.md`.
- The Audit-phase procedure itself → `audit-product.md`.
- The Product Builder Factory that creates the directories this file writes
  into → `scripts/create-product-builder.py`.
