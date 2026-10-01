# Operating Rules

## Responsibility
The constitution: 26 behavioral rules that apply to every phase, every domain, and
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
This isolation is physical as well as logical: every generated Product
Builder is written to the external workspace (`scripts/_common.py`'s
`PRODUCTS_DIR`, defaulting to `~/Design-Glanza-Workspace/products/`,
overridable via `DESIGN_GLANZA_WORKSPACE_ROOT`) — never inside this
repository, and a mandatory safety check refuses to proceed if that
resolution ever lands inside it. Design-Glanza never runs `git add`/
`commit`/`push` for generated output, and never initializes a repository
for one — a user wanting a generated product under version control
creates and manages a separate repository for it themselves.
- **Enforced by:** `scripts/_common.py`'s `_assert_workspace_outside_repo`
  safety check, and root `.gitignore`'s defense-in-depth `/products/` rule.
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

### RULE 20 — Design Research & Visual Quality Assurance
Design-Glanza reasons like a senior product designer, not a UI template
generator. Before any screen is drawn, research current product-design,
navigation, data-visualization, form/table, interaction, accessibility, and
responsive patterns for this specific domain/user/density combination —
never adopted blindly, always checked against whether it actually fits
(Rule 11's anti-fashion discipline applies equally to a researched pattern).
Where a reference exists, extract its full visual language, not a shallow
subset. Where none exists, select a domain-matched default — never one
generic style applied to every product regardless of domain. After a
screen is generated, it is a draft, never the final UI: run the fixed
critique-and-iteration loop — GENERATE → CRITIQUE → IDENTIFY DEFECTS →
PRIORITIZE DEFECTS → FIX → RECHECK → FINALIZE (`ui-engine/
visual-benchmark.md`) — across the full UI Audit Framework and the
three-way Reference/Direction/Generated-UI comparison, **at least once**,
before declaring the UI complete. Every defect found is classified P0-P3
and every P0 and un-waived P1 is fixed automatically, never left for a user
to notice; a screen only reaches FINALIZE once that file's own "When to
stop" conditions all hold, never earlier, and never by relaxing them to
get there sooner. Even a clean first draft records that the check ran,
rather than skipping it.
- **Enforced by:** the new **B15 (Visual Benchmark & Audit Cycle
  Completeness)** measurable gate, checked as part of the existing
  Prototype → Implement transition.
- **Executed via:** `design-reference-engine/design-research.md` (Design
  Setup's new Step 0), `ui-engine/ui-audit-framework.md` (the 11-category
  A–K audit), `ui-engine/visual-benchmark.md` (the three-way comparison and
  mandatory refinement cycle), and `ui-engine/ui-design-principles.md` (the
  22 named senior-design principles those checks draw on) —
  `templates/visual-gap-analysis.md` is the required artifact.

### RULE 21 — Evidence-Based Design (Research-to-Design Traceability)
Research is an active input to design, never documentation generated
alongside it. Before any non-trivial screen or pattern is generated, run
the full chain — Research → Evidence → Insight → Design Principle → UX
Decision → UI Pattern → Validation — and never accept a common/default
pattern without applying the Anti-Generic Design challenge (why is this
pattern appropriate, what user problem does it solve, what evidence
supports it, is there a better pattern for this domain, is it consistent
with this product's information architecture). Every research finding is
labeled Known, Assumed, Inferred, or Unknown — never presented as more
certain than its actual evidence supports — and classified CRITICAL, HIGH,
MEDIUM, or LOW. **Every CRITICAL finding, and every HIGH finding affecting a
core workflow, must produce a recorded Design Principle and a cited UX
Decision and/or UI Pattern** — or an explicit, reasoned deferral; it is
never silently dropped. A small, already-well-understood, non-core change
may use lightweight research (citing this product's own prior findings)
rather than running the full chain from scratch — but a genuinely new
screen or structural pattern is never generated with zero research behind
it and zero prior research to cite.
- **Enforced by:** `config/quality-gates.md`'s new **B16 (Research-to-Design
  Traceability)** measurable gate, checked across the Design Setup →
  Prototype, Prototype → Implement, and Audit → Iterate transitions.
- **Executed via:** `design-research/*` (the full engine — `research-
  engine.md`'s mechanics and complexity threshold, `research-methodology.md`'s
  inputs and confidence model, `evidence-model.md`, `insight-model.md`,
  `domain-analysis.md`, `interaction-analysis.md`, `visual-analysis.md`,
  `pattern-analysis.md`'s Anti-Generic Design challenge,
  `competitor-analysis.md`, and `research-to-design.md`'s mandatory-mapping
  mechanism and priority classification), run by
  `agents/design-setup-specialist.md` as Design Setup's Step 0
  (`workflows/design-setup.md`), producing
  `product-builder/research/research-findings.md` and `research-summary.md`
  — real, `RF-NNN`-tagged artifacts, never folded silently into
  `design-direction.md` with nothing else surviving. `RF-NNN` is a sideways
  reference in `product-intelligence/traceability.md`'s model (Product
  Memory), the same category as `BR-NNN`/`EDGE-NNN`/`DEP-NNN`.

### RULE 22 — UX Scenario Testing
A product is validated as a complete end-to-end user journey, not a
collection of individually-attractive screens. Every important flow is
walked as a named scenario across the mandatory 8-type taxonomy (primary,
alternate, error, empty, loading, permission, offline, recovery) —
applicable or explicitly not-applicable with a reason, never silently
skipped. Every scenario walk checks both structural completeness (no
missing screen, transition, action, validation, or feedback rule against
the spec) and experiential continuity (no dead end, unnecessary step,
ambiguous CTA, missing feedback, inconsistent interaction pattern, or
broken contextual consistency across the screens it actually visits).
Every scenario traces to the `FLOW-NNN`, and transitively the `REQ-NNN`,
it instantiates.
- **Enforced by:** `config/quality-gates.md`'s new **B17 (UX Scenario
  Coverage)** measurable gate, checked at the Prototype → Implement
  (spec-level) and Audit → Iterate (walked) transitions.
- **Executed via:** `ux-scenario-testing/*` — `scenario-model.md`'s
  `SCENARIO-NNN` scheme and field mapping onto `ux-engine/
  user-flow-engine.md`'s existing canonical notation, `scenario-types.md`'s
  8-type taxonomy, `gap-detection.md`'s structural check,
  `continuity-audit.md`'s cross-screen experiential walk, and
  `coverage-matrix.md`'s roll-up artifact and Quality Engine integration —
  run by `agents/ux-architect.md` and `agents/interaction-designer.md`
  jointly (checkpoint 1) and `agents/qa-expert.md` (checkpoint 2), per
  `ux-scenario-testing/README.md`'s explicit account of what's newly added
  versus what's cited from already-existing technique. `SCENARIO-NNN` is a
  sideways reference in `product-intelligence/traceability.md`'s model,
  the same category as `BR-NNN`/`EDGE-NNN`/`DEP-NNN`/`RF-NNN`.

### RULE 23 — Design Token Intelligence
No generated screen invents an arbitrary color, type size/weight/line-
height, spacing value, grid measure, radius, border, shadow, component
dimension, breakpoint, motion duration, or z-index. Every value a
component/screen uses resolves to a path in the product's machine-readable
`design-tokens.json` — never a raw value silently introduced. A value with
no fitting token is logged as a system gap (`ui-engine/design-system.md`'s
existing Consistency rule) and either absorbed into the token set or
rejected, never left unlogged. Semantic tokens (`primary`, `secondary`,
`surface`, `background`, `text`, `muted`, `success`, `warning`, `error`,
`info`) are named consistently across the whole product, theme-mapped
(light/dark) where theming applies. A product's token set inherits the
master scales (`ui-engine/*`) and may extend them with product-specific
seed values and a `product.*` namespace — it never redefines a closed
scale, and nothing product-specific is ever written back into the master
engine (Rule 15).
- **Enforced by:** `config/quality-gates.md`'s sharpened **B6 (Design
  System)** pass criterion and new **B18 (Token Inheritance Integrity)**
  gate, both checked at the Prototype → Implement transition.
- **Executed via:** `design-tokens/*` — `token-schema.md`'s 14-category
  structure (citing, not restating, each scale's actual values),
  `semantic-tokens.md`'s canonical naming, `theming.md`'s light/dark data
  shape, `token-inheritance.md`'s master/product override contract, and
  `token-audit.md`'s violation-detection technique — checked by
  `agents/design-system-expert.md` and enforced deterministically by
  `scripts/validate-tokens.py`. `product-builder/ui/design-tokens.json`
  (`design-tokens/templates/design-tokens.json`) is the required artifact.

### RULE 24 — Component Intelligence
No component is designed from a blank page when a professionally-reasoned
answer already exists. Before specifying a new component, the master
Component Registry is checked first, then the product's own inventory —
only when both come back negative, and the proposed component's purpose
doesn't match anything already registered, is a genuinely new component
justified. Common components combine into named, pre-reasoned patterns
(a Data Table is Search + Filters + Sorting + Pagination + Selection +
Bulk actions + Empty/Loading/Error states, not four independently-
invented pieces); a product never re-derives a composition the registry
already specifies. Every component instantiated from the registry
inherits its token discipline (Rule 23) automatically. A product-specific
component need is added to the product's own inventory, never written
back into the master registry (Rule 15) — a recurring need graduates
upstream deliberately, the same way a recurring domain pattern graduates
into a `product-types/*.md` pack.
- **Enforced by:** `config/quality-gates.md`'s sharpened **B6 (Design
  System)** pass criterion and new **B19 (Component Registry
  Conformance)** gate, both checked at the Prototype → Implement
  transition.
- **Executed via:** `component-registry/*` — `registry-schema.md`'s
  13-field entry shape (extending, not replacing,
  `ui-engine/component-system.md`'s 8-point framework),
  `components-{actions-inputs,navigation,containers-display,
  feedback-status}.md`'s ~29 pre-populated entries,
  `composition-patterns.md`'s organism-level patterns, and
  `registry-integration.md`'s registry-first enforcement and Quality
  Engine/UX Scenario Testing wiring — checked by
  `agents/design-system-expert.md`, the same agent that already owns the
  reuse-vs-new decision. No new ID scheme: a registry entry is referenced
  by name, and a product's own components still use `COMPONENT-NNN`
  (`product-intelligence/traceability.md`), now citing a Registry base.

### RULE 25 — Visual Regression Integrity
A UI improvement never silently breaks something that already worked.
Once a screen's generated UI has been confirmed clean
(`ui-engine/visual-benchmark.md`'s mandatory cycle, gate B15), its
structural state — regions, components, token paths, breakpoint
behavior — is captured as a baseline. Every later pass touching that
screen is diffed against that baseline **before** being considered
complete: layout shifts, spacing/typography/color changes, component
inconsistencies, alignment problems, missing or unexpected elements, and
responsive regressions are all detected, classified Critical/High/
Medium/Low, and resolved — either fixed, or explicitly approved as an
intentional Baseline Update with a stated reason. A diff with no fix and
no approved update is never silently accepted, and a baseline is never
silently overwritten by an unreviewed pass.
- **Enforced by:** `config/quality-gates.md`'s new **B20 (Visual
  Regression Integrity)** measurable gate, checked at the same
  Prototype → Implement transition B15 already occupies.
- **Executed via:** `visual-regression/*` — `baseline-model.md`'s
  structured (never pixel-based) snapshot, `diff-detection.md`'s 9
  categories, `tolerance-thresholds.md`'s token-step-based tolerance,
  `severity-classification.md`'s Critical/High/Medium/Low labels (mapped
  onto the one shared Blocker/Major/Minor/Note vocabulary, never a
  competing scale), and `baseline-updates.md`'s explicit, logged approval
  mechanism — checked by `agents/qa-expert.md`, enforced deterministically
  by `scripts/validate-visual-regression.py`. Folded into the existing
  visual-benchmark-and-audit cycle action — no new phase, no new agent, no
  new ID scheme.

### RULE 26 — Product Memory & Decision Records
The Product Builder remembers its own significant product, UX, UI,
design-system, component, and architecture decisions throughout the
lifecycle — it does not repeatedly re-derive or contradict them.
Before generating or modifying UI, the acting agent checks
`product-builder/memory/product-memory.md` for a relevant existing
decision; a genuine contradiction is only ever introduced via a new
`ADR-NNN` that explicitly supersedes the one it replaces, never silently.
A significant decision (a real alternative was resolved, it spans more
than one screen/flow, it departs from a domain/token/registry default, or
it supersedes a prior decision) is recorded as it's made, not as a
separate memory-writing pass afterward. Product Memory remains
completely isolated per product (Rule 15, generalized here across every
decision category at once) — a Product Builder inherits the master
engine's standards but never modifies them, and one product's memory is
never read by, or written into, another's.
- **Enforced by:** `config/quality-gates.md`'s new **B21 (Product Memory
  Integrity)** measurable gate, checked at both the Prototype/design-time
  checkpoint (was memory actually consulted) and the Audit checkpoint (is
  it internally consistent).
- **Executed via:** `product-memory/*` — `memory-model.md`'s index (a
  thin cross-reference over content that mostly already exists elsewhere
  in the engine, never a duplicate of it), `adr-schema.md`'s persisted
  form of `methodology/design-thinking.md`'s existing design decision
  framework, `consultation-rule.md`, `contradiction-prevention.md`'s
  supersession protocol, and `auto-recording.md`'s significance
  threshold — checked by the agent owning each decision's domain
  (`agents/{product-architect,ux-architect,ui-designer,design-system-
  expert}.md`) and by `agents/qa-expert.md` at Audit, enforced
  deterministically by `scripts/validate-memory.py`. `ADR-NNN` is a new
  sideways reference in `product-intelligence/traceability.md`'s model,
  the same category as `BR-NNN`/`EDGE-NNN`/`DEP-NNN`/`RF-NNN`/
  `SCENARIO-NNN`.

## Explicitly not here
- Registries/constants (rule numbers are referenced here, but the phase/role/domain
  registries themselves) → `master-config.md`.
- Phase-transition checklists and the 21 measurable quality-gate dimensions →
  `quality-gates.md`.
- Assumption tag syntax, severity vocabulary, report shapes → `output-contract.md`.
