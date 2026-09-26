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
37 total rows in the table below — 24 correspond to the originally-requested
numbered list (`#` column), 13 were added since (Design Setup's 6 —
including v1.0.9's new Design Research action, Preview & Run's 2, plus 4 the
engine's own dependency chain always required — Build empathy model, Select
a solution approach, Confirm domain(s), Build visual hierarchy/UI rules —
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
| 10 | - | Select a solution approach | IDEATE | `methodology/ideate.md` (8-point evidence-based selection) | `product/product-definition.md` (Chosen Approach section) |
| 11 | - | Confirm domain(s), sequence dependencies | ARCHITECT | `product-intelligence/domain-classifier.md` + `domain-standards.md`, `dependency-analysis.md` (refined) | `domain/domain-application-notes.md`; `requirements/dependency-analysis.md` (updated) |
| 12 | - | Research current design patterns relevant to this product | DESIGN SETUP | `design-reference-engine/design-research.md` | `ui/design-direction.md` (folds into the direction; no separate artifact) |
| 13 | - | Detect and analyze design references, if any | DESIGN SETUP | `design-reference-engine/reference-analysis.md` | `ui/design-direction.md` (Reference analysis section) |
| 14 | - | Run the design questionnaire | DESIGN SETUP | `design-reference-engine/design-questionnaire.md` | `ui/design-direction.md` (Visual style/Layout/Typography/Color/Components/Interaction/Responsive/Accessibility/Brand sections) |
| 15 | - | Classify the design-reference decision, select a default sample if needed | DESIGN SETUP | `design-reference-engine/reference-selection.md`, `design-samples/` | `ui/design-direction.md` (Reference classification, Design inspiration sections) |
| 16 | - | Write the complete Design Direction document | DESIGN SETUP | `design-reference-engine/design-direction.md` + `templates/design-direction.md` | `ui/design-direction.md` (complete) |
| 17 | - | Present the Design Direction Summary and gate on approval | DESIGN SETUP | `workflows/design-setup.md` Step 5 — B13 gate | `ui/design-direction.md` (Approval status recorded) |
| 18 | 11 | Build user flows | PROTOTYPE (UX) | `ux-engine/user-flow-engine.md` (`FLOW-NNN`, recovery paths) | `ux/user-flows.md` |
| 19 | 9 | Build information architecture | PROTOTYPE (UX) | `ux-engine/information-architecture.md` | `ux/sitemap.md` |
| 20 | 10 | Build navigation architecture | PROTOTYPE (UX) | `ux-engine/navigation-system.md` (13 concerns; breadcrumbs never default) | `ux/navigation.md` |
| 21 | 12 | Build screen architecture | PROTOTYPE (UX) | `templates/screen-architecture.md` region map + `ui-engine/layout-system.md` composition pattern | `ux/screen-architecture.md` |
| 22 | 13 | Build interaction architecture | PROTOTYPE (UX) | `ux-engine/interaction-design.md` + `form-design.md` | `ux/ux-rules.md` |
| 23 | 16 | Build state matrix | PROTOTYPE (UX) | `ux-engine/state-design.md` (13 mandatory states) | `ux/state-matrix.md` |
| 24 | 18 | Build accessibility rules | PROTOTYPE (UX+UI) | `ux-engine/accessibility.md` (structural) + `ui-engine/color-system.md` (perceptual) | `ux/accessibility.md` |
| 25 | 14 | Build design system | PROTOTYPE (UI) | `ui-engine/design-system.md` + `typography.md`/`color-system.md`/`layout-system.md`, per the approved `ui/design-direction.md` | `ui/design-system.md` |
| 26 | 15 | Build component architecture | PROTOTYPE (UI) | `ui-engine/component-system.md` (8-point framework, iconography) | `ui/components.md` |
| 27 | - | Build visual hierarchy / UI rules | PROTOTYPE (UI) | `ui-engine/visual-hierarchy.md`, `visual-trends.md` (register selection, consistent with `ui/design-direction.md`) | `ui/ui-rules.md` |
| 28 | 17 | Build responsive rules | PROTOTYPE (UI) | `ui-engine/responsive-system.md` | `ui/responsive-rules.md` |
| 29 | - | Run the mandatory visual-benchmark-and-audit cycle | PROTOTYPE (UI) | `ui-engine/ui-audit-framework.md` (11 A-K categories) + `visual-benchmark.md` (three-way comparison, mandatory refinement) — B15 gate | `ui/visual-gap-analysis.md` (one `templates/visual-gap-analysis.md` instance per screen) |
| 30 | 19 | Build implementation plan | ARCHITECT->IMPLEMENT bridge | build order from step 11's dependency graph, gated by `config/quality-gates.md` B12 | `workflows/implementation-notes.md` |
| 31 | 20 | Implement the product, where applicable | IMPLEMENT | `workflows/build-product.md` | `output/*`; `workflows/implementation-notes.md` updated with status |
| 32 | - | Detect framework, verify build, start local dev server, detect URL/port | PREVIEW & RUN | `workflows/preview-run.md` steps 1-4 | `workflows/preview-report.md` (project path, framework, start command, build status, local URL, port) |
| 33 | - | Verify runtime, fix build/runtime issues, finalize the Preview & Run report | PREVIEW & RUN | `workflows/preview-run.md` steps 5-8 — B14 gate | `workflows/preview-report.md` (complete) |
| 34 | 21 | Validate the implementation | TEST | `methodology/test.md` — all 9 dimensions, not just task completion | `qa/qa-report.md` (Test section) |
| 35 | 22 | Audit the product | AUDIT | `workflows/audit-product.md`, `scripts/validate-*.py`, `config/quality-gates.md` Section B | `qa/qa-report.md`, `qa/traceability.md` |
| 36 | 23 | Fix identified issues | ITERATE | routed per `methodology/design-thinking.md`'s feedback-routing table to whichever phase/file actually owns the defect | whichever artifact above owns the fix |
| 37 | 24 | Revalidate | ITERATE -> back to TEST/AUDIT | re-run only the specific failed gate(s), not the whole pipeline from scratch | `qa/qa-report.md` updated |

**Actions 12–17 (Design Setup, now including v1.0.9's new Design Research
action), 29 (v1.0.9's new mandatory Visual Benchmark & Audit Cycle), and
32–33 (Preview & Run) are new** — not part of the original 24-action
numbering, hence `-` in the `#` column, the same convention already used
for the other originally-unnumbered actions (Build the empathy model,
Select a solution approach, Confirm domain(s), Build visual hierarchy/UI
rules).

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
  B12, B13, B14, B15) still holding — a later fix that silently regresses an
  earlier gate reopens the scope, it doesn't get a pass by association with
  the fix.
- **B15 (Visual Benchmark & Audit Cycle Completeness)** passed before
  Implement began — a screen whose generated UI was never checked against
  its reference/design direction, or whose first pass was simply accepted
  with no recorded refinement cycle, is not complete regardless of how the
  screen looks (Rule 20).
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
- The visual-benchmark-and-audit cycle's own technique → `ui-engine/
  {ui-audit-framework,visual-benchmark}.md`, `templates/visual-gap-analysis.md`.
- The Implement-phase build-sequencing procedure itself → `build-product.md`.
- The Preview & Run procedure itself → `preview-run.md`.
- The Audit-phase procedure itself → `audit-product.md`.
- The Product Builder Factory that creates the directories this file writes
  into → `scripts/create-product-builder.py`.
