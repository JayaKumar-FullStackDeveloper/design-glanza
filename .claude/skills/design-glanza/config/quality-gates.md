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
  (`ui-engine/color-system.md`) conformance.
- **Pass criterion:** checked twice — structurally at Prototype (focus order and
  keyboard-equivalence defined for every interaction; semantic roles mapped) and
  for full conformance at Audit (against the stated baseline, or a
  domain-mandated stricter bar from `product-types/*.md`; 0 color-only
  meaning encodings; 100% of interactive elements keyboard-operable).
- **Checked by:** `agents/accessibility-expert.md`.

### B9 — Responsive Behavior
- **Measures:** completeness of `ui-engine/responsive-system.md` application.
- **Pass criterion:** every screen has defined reflow behavior at every mandatory
  breakpoint; priority content (per `ui-engine/visual-hierarchy.md`) remains
  reachable at the smallest breakpoint; touch targets meet the minimum size rule
  at touch-relevant breakpoints.
- **Checked by:** `agents/ui-designer.md` review.

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
- **Pass criterion:** `scripts/validate-product.py` (aggregating B1/B5/B7) returns
  all-pass; `evals/evaluation-rubric.md` score meets or exceeds its stated
  threshold on every dimension; 0 unresolved Blocker or un-waived Major findings
  in `templates/qa-report.md`.
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
  `templates/preview-report.md`'s required fields.
- **Pass criterion:** the build succeeds; a local dev server starts with a
  detected URL/port; no unhandled runtime error blocks the primary
  implemented screen(s); every required field in the preview report is
  filled (project path, framework, start command, local URL, port, build
  status, runtime status, implemented screen(s), preview status). An
  optional public/external preview (e.g. ngrok) is recorded only if the
  user explicitly requested one — its absence never fails this gate.
- **Checked by:** the executing session, per `workflows/preview-run.md` —
  no dedicated reasoning agent, the same posture B12/Implement already has.

### B15 — Visual Benchmark & Audit Cycle Completeness
- **Measures:** whether the generated UI was actually checked against
  `ui-engine/ui-audit-framework.md`'s 11 categories and
  `ui-engine/visual-benchmark.md`'s three-way (Reference/Design Direction/
  Generated UI) comparison, per `templates/visual-gap-analysis.md`.
- **Pass criterion:** at least one full audit-and-refinement cycle is
  recorded for every screen produced this pass — a first-pass audit, a gap
  classification (or an explicit "no gaps found"), and a re-check after any
  refinement (or an explicit re-confirmation when pass 1 was clean). A
  screen with no recorded visual-gap-analysis instance fails this gate
  regardless of how the screen actually looks.
- **Checked by:** `agents/ui-designer.md` and
  `agents/design-system-expert.md`, per `ui-engine/visual-benchmark.md`'s
  mandatory-cycle procedure — no new dedicated agent.

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
  registry-first check) — 0 components with none of the three.
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
- **Checked by:** `agents/qa-expert.md`, enforced deterministically by
  `scripts/validate-visual-regression.py` — no new dedicated agent.

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
