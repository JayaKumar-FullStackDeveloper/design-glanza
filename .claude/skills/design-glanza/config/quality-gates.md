# Quality Gates

## Responsibility
Binary/checklist criteria that must be satisfied before work proceeds — both
between phases (Section A) and across the 14 measurable quality dimensions
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
| Design Setup → Prototype | Design Direction Completeness gate (B13) passes — `product-builder/ui/design-direction.md` complete per template, its reference classification (Reference-Driven/Guideline-Driven/Custom/Default) stated with rationale, and user confirmation obtained or explicitly waived |
| Prototype → Implement | User-Flow (B3), Information Architecture (B4), Screen Architecture (B5), Design System (B6), State Coverage (B7), Accessibility (B8, structural), Responsive Behavior (B9) gates all pass |
| Implement → Preview & Run | Implementation Readiness gate (B12) still holds; `output/*` is non-empty for any screen marked implemented this pass |
| Preview & Run → Test | Preview & Run Verification gate (B14) passes |
| Test → Audit | `methodology/test.md` validation against Define's success criteria passes with no Blocker findings |
| Audit → Iterate | Traceability (B10), QA (B11), Accessibility (B8, conformance) gates all pass |
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

## Section B — The 14 measurable quality gates

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
- **Measures:** completeness and consistency of `templates/design-system.md`.
- **Pass criterion:** every token category required by `ui-engine/design-system.md`
  is defined (no missing category); 100% of generated components use system
  tokens (0 undocumented one-off values, per `agents/design-system-expert.md`
  drift check); every semantic color pairing meets the contrast rule in
  `ui-engine/color-system.md`.
- **Checked by:** `agents/design-system-expert.md`.

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

## Explicitly not here
- *How* to produce the artifact being gated → owned by the relevant
  `methodology/`, `product-intelligence/`, `ux-engine/`, `ui-engine/`, or
  `design-reference-engine/` file.
- Scored/graded quality assessment beyond pass/fail → `evals/evaluation-rubric.md`.
- Step-by-step execution order within a phase → `workflows/*.md`.
- The severity vocabulary and report shapes referenced above → `output-contract.md`.
