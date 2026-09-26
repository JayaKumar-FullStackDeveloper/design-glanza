# Operating Rules

## Responsibility
The constitution: 19 behavioral rules that apply to every phase, every domain, and
every agent, regardless of product-type. `SKILL.md` and every other file link here
instead of restating these. Each rule below states what it requires, why, and which
file actually executes it — this file is the rule, not the mechanism.

## Rule registry

### RULE 1 — Requirement First
Never begin UI generation immediately after receiving a requirement. Analyze the
business and user problem first.
- **Enforced by:** `config/quality-gates.md`'s Intake → Empathize and
  Ideate → Architect gates, both of which must pass before any `ui-engine/*` file
  may be invoked.
- **Executed via:** `workflows/analyze-brd.md` → `methodology/empathize.md` →
  `methodology/define.md` → `methodology/ideate.md`, in that order, before
  `workflows/create-ui.md` runs.

### RULE 2 — Source of Truth
When facts conflict or a decision needs grounding, prioritize in this order:
1. Explicit BRD/PRD/SOW requirements
2. Acceptance criteria
3. Existing product behavior (for redesigns)
4. Existing design system
5. Existing code
6. Established domain conventions (`product-types/*.md`)
7. Design best practices (`ux-engine/*`, `ui-engine/*`)
8. Reasonable assumptions (lowest priority, always last resort)

Every fact used from tiers 6–8 must be traceable to *why* a higher tier didn't
settle it. Assumptions (tier 8) must be clearly identified per Rule 10.
- **Executed via:** `product-intelligence/brd-analysis.md`'s confidence tagging
  applies this order during extraction.

### RULE 3 — Business Logic
Every feature must be analyzed for all of the following before it is considered
understood:
business objective · actors · actions · system behavior · validation · status ·
permissions · dependencies · triggers · success · failure · edge cases.
- **Enforced by:** `config/quality-gates.md`'s Business Logic Completeness gate.
- **Executed via:** `product-intelligence/business-logic.md` (objective, actions,
  system behavior, validation, status, triggers, success/failure),
  `product-intelligence/user-roles.md` (actors, permissions),
  `product-intelligence/dependency-analysis.md` (dependencies),
  `product-intelligence/edge-case-engine.md` (edge cases).

### RULE 4 — UX Before UI
Do not solve an information architecture problem with visual styling. A confusing
structure stays confusing no matter how well it's styled.
- **Enforced by:** `config/quality-gates.md`'s Prototype → Implement gate, which
  requires `ux-engine/*` artifacts to be gate-passed independent of any visual
  treatment.
- **Executed via:** `workflows/create-ux.md` must fully complete and gate-pass
  before `workflows/create-ui.md` starts.

### RULE 5 — System Before Screen
Establish reusable patterns (layout compositions, component variants, flow
templates) before generating a large number of individual screens.
- **Executed via:** `ui-engine/design-system.md` and `ui-engine/component-system.md`
  must exist and be gate-passed before `workflows/build-product.md` mass-produces
  `templates/screen-specification.md` instances. `agents/design-system-expert.md`
  is the ongoing enforcement mechanism against drift once screens multiply.

### RULE 6 — States Are Mandatory
Every important workflow must consider all applicable states: initial · loading ·
success · empty · validation error · system error · permission denied ·
processing · completed · cancelled · conflict · timeout (where applicable) ·
offline (where applicable).
- **Enforced by:** `config/quality-gates.md`'s State Coverage gate and
  `scripts/validate-states.py`.
- **Executed via:** `ux-engine/state-design.md` enumerates these against
  `product-intelligence/edge-case-engine.md` output, filled into
  `templates/state-matrix.md`.

### RULE 7 — Accessibility
Accessibility is part of the design, not a final decoration applied at the end.
- **Enforced by:** `config/quality-gates.md`'s Accessibility gate, checked at
  Prototype (structural) and again at Audit (conformance), never only at the end.
- **Executed via:** `ux-engine/accessibility.md` (structural/behavioral),
  `ui-engine/color-system.md` (perceptual), applied continuously by
  `agents/accessibility-expert.md`, not as a one-time pass.

### RULE 8 — Responsive Thinking
Every web interface must consider all relevant viewport sizes and interaction
modes (mouse, touch, keyboard) as part of the initial design, not an afterthought
adaptation.
- **Enforced by:** `config/quality-gates.md`'s Responsive Behavior gate.
- **Executed via:** `ui-engine/responsive-system.md`, coordinated with
  `ux-engine/interaction-design.md` for input-modality equivalence.

### RULE 9 — Traceability
Every important requirement should map forward through the full artifact chain:

```
REQ → USER → FLOW → SCREEN → COMPONENT → TEST
```

An artifact with no upstream requirement, or a requirement with no downstream
artifact, is a defect unless explicitly logged as deferred/out-of-scope.
- **Enforced by:** `config/quality-gates.md`'s Traceability gate.
- **Executed via:** `product-intelligence/traceability.md` maintains the chain;
  `templates/qa-report.md` surfaces breaks in it.

### RULE 10 — No Invented Business Rules
If information is unknown:
1. Mark it as an explicit assumption (format defined in
   `config/output-contract.md`'s assumption tag).
2. Identify its impact (what breaks or changes if the assumption is wrong).
3. Never silently treat an assumption as confirmed behavior downstream — every
   file consuming an assumption-tagged fact must carry the tag forward, not drop
   it once "used."
- **Enforced by:** every `config/quality-gates.md` gate includes an
  assumption-tag-carried-forward check; `evals/evaluation-rubric.md`'s
  assumption-marking-compliance dimension scores this directly.

### RULE 11 — Design Trends
Use current design patterns selectively. Never apply a visual trend simply because
it is fashionable — every trend adopted must serve `ui-engine/visual-hierarchy.md`
or the product's register, not decorate for its own sake. This applies equally to
motion/animation, not only static visual style — an animation is never added
because it's a currently-common flourish, only for a stated purpose.
- **Executed via:** `ui-engine/visual-trends.md`'s register-selection rule, which
  requires a trend's adoption to be justified by audience/domain fit
  (`product-types/*.md`, `methodology/empathize.md`), and its boundary rule that
  trends never override structural rules (contrast, hierarchy);
  `ux-engine/interaction-design.md`'s Motion and animation section (the
  frequency-based animate/don't-animate gate and purpose-must-be-stated rule)
  as the same discipline applied to motion; and `ui-engine/craft-critique.md`'s
  anti-cliché catalog as a finished-composition-level check for both.

### RULE 12 — Self-Critique
Before declaring a feature complete, audit the result against: requirements, UX,
UI, accessibility, states, responsiveness, and edge cases.
- **Enforced by:** `config/quality-gates.md`'s Audit → Iterate gate.
- **Executed via:** `workflows/audit-product.md`, `agents/qa-expert.md`, scored
  against `evals/evaluation-rubric.md`, reported in `templates/qa-report.md`.

### RULE 13 — Iteration
If validation identifies an issue, fix the issue and revalidate — a finding is not
closed until the gate it failed is re-checked and passes.
- **Executed via:** `workflows/audit-product.md`'s Iterate handoff routes each
  finding to its owning file/agent; `config/quality-gates.md` gates are re-run
  after any fix, not assumed fixed.

### RULE 14 — Domain-Agnostic Core
The master engine (`config/`, `methodology/`, `product-intelligence/`,
`ux-engine/`, `ui-engine/`, `workflows/`, `templates/`, `agents/`, `scripts/`,
`evals/`) must remain domain-independent. Domain knowledge belongs in
`product-types/*.md` domain packs only.
- **Enforced by:** a core file must never contain a domain name (SaaS, ERP,
  healthcare, etc.) in its own logic — that's a signal to route the content to
  `product-types/`, per `product-intelligence/domain-classifier.md`.

### RULE 15 — Product Isolation
Every generated Product Builder (`products/<name>/`) must contain
product-specific knowledge without contaminating the master skill. Nothing
learned or decided while building one product may be written back into
`config/`, `methodology/`, `product-intelligence/`, `ux-engine/`, `ui-engine/`,
`workflows/`, `templates/`, or `agents/` as a domain-specific special case.
- **Executed via:** `scripts/create-product-builder.py` scaffolds *from* the core
  outward, never the reverse; a recurring pattern observed across multiple
  products is graduated into a proper `product-types/*.md` file instead
  (per that file's graduation rule), never inlined into the core.

### RULE 16 — Extensibility
Adding a new domain should require adding a domain pack
(`product-types/<domain>.md` + optionally a `use-cases/<domain>.md` example), not
rewriting the master engine.
- **Enforced by:** Rule 14's core-purity check is the mechanical guarantee this
  rule depends on — if the core stays domain-agnostic, a new domain pack is
  always sufficient by construction.
- **Executed via:** `product-types/custom-domain.md`'s **Domain Pack
  Contract** — the fixed 12-point schema (common product characteristics,
  users, workflows, information structures, navigation patterns, UI patterns,
  operational concerns, edge cases, terminology, UX risks, accessibility
  considerations, scalability considerations) every pack answers with
  domain-specific content while citing, never restating, the core engine
  file each point specializes.

### RULE 17 — Domain Standards
Before designing any product, check whether its detected domain(s) have a
matching entry in `product-types/domain-standards/domain-registry.json`. If
one is found and complete, load it and treat it as mandatory domain-specific
guidance for information architecture, user flows, UX patterns, UI
components, the design system, states, data visualization, accessibility,
responsive behavior, domain terminology, and quality gates — layered on top
of the core engine and any matched `product-types/*.md` pack, never
replacing either. Never load an entry that doesn't genuinely match, and
never invent guidance for a `"pending"` entry with no standard yet.
- **Enforced by:** `agents/product-architect.md`'s domain-standards matching
  step (run alongside its existing `product-types/*.md` overlay step), which
  states its match (or deliberate no-match) with confidence exactly as Rule
  2's domain-classification confidence reporting already requires.
- **Executed via:** `product-intelligence/domain-standards.md`, which also
  states the reconciliation rule (Rule 2's existing tier 6, not a separate
  priority system) and the exact agent-by-agent application table.

### RULE 18 — Design Setup / Visual Direction
Before any UI is generated, the product's visual and interaction direction
must be deliberately established — never assumed from generic defaults when
the user has provided real design input, and never generated from silence
when they haven't. Concretely: never treat a screenshot/reference as an
automatic source of business requirements (that's Rule 2/10's job, at
Intake); never blindly copy a reference design pixel-for-pixel instead of
extracting its underlying visual language; never proceed to full UI
generation without the design direction being established and, where a
real user is present to ask, confirmed.
- **Enforced by:** `config/quality-gates.md`'s new Architect → Design Setup
  and Design Setup → Prototype phase-transition gates, and the **B13
  (Design Direction Completeness)** measurable gate.
- **Executed via:** the new **Design Setup** phase between Architect and
  Prototype in the 10→11-phase lifecycle (`config/master-config.md`'s Phase
  registry), run by `agents/design-setup-specialist.md` per
  `workflows/design-setup.md`, using `design-reference-engine/*` (reference
  analysis, the design questionnaire, the reference-vs-default decision) and
  `design-samples/` (the default library, used only when the user has not
  provided sufficient design direction of their own). Its output,
  `product-builder/ui/design-direction.md`, is mandatory input to
  `agents/ui-designer.md` and `agents/design-system-expert.md` from that
  point forward — the approved direction, not fresh preference, governs the
  visual system.

### RULE 19 — Preview & Run
Implementation is not complete because the code was written — it is
complete only once the application actually launches locally and the
implemented screen(s) can be previewed. After Implement, before Test:
detect the framework/dev setup, start the local dev server, verify the
build succeeds, detect the real local URL/port, check for runtime errors,
and fix build/runtime issues before continuing. A public/external preview
(e.g. via ngrok) is never set up unless the user explicitly asks for one,
and ngrok is never required for normal operation.
- **Enforced by:** `config/quality-gates.md`'s new Implement → Preview & Run
  and Preview & Run → Test phase-transition gates, and the **B14 (Preview &
  Run Verification)** measurable gate.
- **Executed via:** the new **Preview & Run** phase between Implement and
  Test in the lifecycle (`config/master-config.md`'s Phase registry), per
  `workflows/preview-run.md` — carried out by whatever capability is
  actually executing the build (the same "no dedicated reasoning
  specialist" posture `workflows/build-product.md` already states for
  Implement, since this is verification-by-execution, not new design
  reasoning). Its output, `product-builder/workflows/preview-report.md`
  (`templates/preview-report.md`), is the required artifact — a local URL
  reported only in conversation, with no file written, does not satisfy
  this rule.

## Explicitly not here
- Registries/constants (rule numbers are referenced here, but the phase/role/domain
  registries themselves) → `master-config.md`.
- Phase-transition checklists and the 12 measurable quality-gate dimensions →
  `quality-gates.md`.
- Assumption tag syntax, severity vocabulary, report shapes → `output-contract.md`.
