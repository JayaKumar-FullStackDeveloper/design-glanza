---
name: design-glanza
description: Master product-design and Product Builder factory (POC — explicit invocation only, entry point /design-glanza). Given a product requirement, BRD/PRD/SOW, user stories, acceptance criteria, an existing product (screenshots, a live app, or its codebase), or a plain-language product idea, generates a product-specific Product Builder skill that designs, architects, builds, previews, tests, audits, and iterates that product — across SaaS, enterprise (ERP/CRM/admin panels), consumer, healthcare, e-commerce, HRMS, fintech, logistics, marketplace, landing pages/marketing sites, and arbitrary/custom domains. This is a deliberate, heavyweight, multi-phase workflow, run only when the user explicitly invokes /design-glanza or unambiguously asks to run the Design-Glanza product-building process end to end — never merely because a conversation mentions UI, UX, SaaS, or design in passing, and never for an isolated code fix or a single small change.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(python */scripts/create-product-builder.py *)
  - Bash(python3 */scripts/create-product-builder.py *)
  - Bash(python */scripts/validate-*.py *)
  - Bash(python3 */scripts/validate-*.py *)
  - Bash(python */scripts/generate-report.py *)
  - Bash(python3 */scripts/generate-report.py *)
  # One narrowly scoped exception (v1.0.30): read-only Figma inspection,
  # used only inside Design Setup, only when a Figma reference is
  # detected (design-reference-engine/figma-reference.md). Never a
  # general-purpose grant — no other network/MCP tool is added here, and
  # this one is never used to create/edit/mutate a Figma node.
  - Skill(figma-use)
  - Skill(figma-design-to-code)
  - use_figma
  - get_design_context
---

# Design-Glanza

Design-Glanza is not a product builder. It is the factory that builds product
builders — and it stays domain-agnostic while doing it.

## POC invocation & safety

- **Explicit invocation only.** `disable-model-invocation: true` means Claude
  never auto-loads this skill from a passing mention of UI, UX, SaaS, or
  design — the entry point is the user typing **`/design-glanza`**, or
  unambiguously asking to run the Design-Glanza process by name. If a
  request only loosely touches product/design topics, do the requested work
  directly rather than pulling in this whole lifecycle.
- **Minimal tool surface.** Only `Read`/`Write`/`Edit`/`Glob`/`Grep` and a
  narrowly scoped `Bash` limited to this skill's own
  `scripts/{create-product-builder,validate-*,generate-report}.py` — no
  general shell access, nothing beyond what the pipeline itself needs. One
  deliberate, narrowly scoped exception (v1.0.30): the `figma-use`/
  `figma-design-to-code` skills and their `use_figma`/`get_design_context`
  tools, used only inside Design Setup, only when a Figma reference is
  detected, read-only — see `design-reference-engine/figma-reference.md`.
  No other network/MCP tool is granted to Design-Glanza's own
  self-invocation. The optional Gemini capability (v1.0.35,
  `ui-engine/gemini-capability.md`) adds no tool grant here either — like
  the Playwright render-QA scripts and `asset-pipeline.md`'s image
  tooling already in use, it executes only inside Implement/Preview &
  Run/Audit's separate, broader execution boundary
  (`workflows/build-product.md`'s "whatever capability is actually
  invoking this workflow"), never through this restricted surface.
- **No destructive automation by default.** Before any irreversible or
  large-scale action — regenerating/overwriting an existing Product Builder
  outside `--update`, running Implement across many screens/files at once,
  or any bulk delete-like operation — stop and confirm with the user first.
  `scripts/create-product-builder.py`'s conflict guard already refuses a
  silent overwrite at the tooling layer; this is the same posture applied to
  every other large-scale step, not just that one.

## 1. Mission

```
USER REQUIREMENT  →  PRODUCT UNDERSTANDING  →  PRODUCT-SPECIFIC BUILDER  →  COMPLETE PRODUCT
```

Given any input describing a product, Design-Glanza (1) understands it deeply
before touching a screen, (2) generates a **Product Builder** — a separate,
product-specific skill under `products/<slug>/product-builder/` — and (3) that
Product Builder, not Design-Glanza itself, goes on to design, build, preview,
test, audit, and iterate the actual product.

**Design-Glanza ≠ Product Builder — never confuse the two:**

| | Design-Glanza (this file) | A Product Builder (generated) |
|---|---|---|
| What it is | The one master skill, domain-agnostic | One skill per product, product-specific |
| What it knows | Reusable methodology, engines, domain packs | This product's requirements, flows, screens, rules |
| What it does | Orchestrates specialist reasoning and generates builders | Executes the product's own lifecycle |
| Where it lives | `.claude/skills/design-glanza/` | `products/<slug>/product-builder/` |

Design-Glanza creates and orchestrates Product Builders. Product Builders
execute product-specific work. A Product Builder never contains Design-Glanza's
own methodology copied in — it only *references* this skill
(`workflows/execute-product-builder.md`'s pattern) and carries product-specific
content. Editing a Product Builder never changes Design-Glanza; a new domain
means adding a `product-types/*.md` pack here, never forking this file.

## The core lifecycle (enforced, not optional)

```
INTAKE → EMPATHIZE → DEFINE → IDEATE → ARCHITECT → DESIGN SETUP → PROTOTYPE → IMPLEMENT → PREVIEW & RUN → TEST → AUDIT → ITERATE
```

This is a **continuous loop**, not a one-time checklist — Test findings route
backward to whichever earlier phase actually owns the defect
(`methodology/design-thinking.md`'s feedback-routing table), and a phase never
auto-advances without a completion report (`config/output-contract.md`). Full
mechanics: `methodology/design-thinking.md`. Full operational, file-by-file
execution: `workflows/execute-product-builder.md`. **Design Setup** (added
v1.0.7) and **Preview & Run** (added v1.0.8) are not among the 5 core
design-thinking phases below — like Architect/Implement/Audit/Iterate,
they're production-pipeline phases with no Empathize/Define/Ideate/
Prototype/Test counterpart of their own.

## Progressive disclosure — load only what the current step needs

Do not read every supporting file up front. This table is the map; load a row
only when you're actually at that step.

| Doing this | Load |
|---|---|
| Recognizing/extracting from raw input | `product-intelligence/brd-analysis.md` |
| Classifying the domain | `product-intelligence/domain-classifier.md`, the matching `product-types/*.md` |
| Matching/loading an external domain-standard document | `product-intelligence/domain-standards.md`, `product-types/domain-standards/domain-registry.json` |
| Deriving requirements, rules, roles, dependencies, edge cases | `product-intelligence/{requirement-engine,business-logic,user-roles,dependency-analysis,edge-case-engine}.md` |
| Empathize / Define / Ideate reasoning | `methodology/{empathize,define,ideate}.md` |
| Running the full Design Research Engine — evidence, insight, competitor/pattern analysis that must actively shape UX/UI decisions, not just document them | `design-research/*` (entry point cited from Design Setup's Step 0: `design-reference-engine/design-research.md`) |
| Establishing/confirming the visual and interaction direction before any screen exists | `design-reference-engine/*` — including `figma-reference.md` (extraction) and `figma-context-consumption.md` (the precedence rule once extracted) for a Figma reference specifically — `design-samples/`, `workflows/design-setup.md` |
| Structuring flows, IA, navigation, states | `ux-engine/*` |
| Deriving scenarios from flows, checking for missing screens/transitions/actions/validations/feedback, auditing navigation continuity across a scenario's real screen sequence, building the UX Coverage Matrix | `ux-scenario-testing/*` |
| Launching and verifying the built output locally, after Implement | `workflows/preview-run.md`, `templates/preview-report.md` |
| Search/query design, or a non-Latin-script/multi-locale product, or interface wording (errors, CTAs, tone) | `ux-engine/{search-ux,localization,ux-writing}.md` |
| Ideate selected a conversational interaction model, or designing the first-run/onboarding experience | `ux-engine/{conversational-ux,onboarding-design}.md` |
| Visual system, layout, components | `ui-engine/*` |
| Consuming/generating the machine-readable token set (colors, type, spacing, radius, shadows, sizing, breakpoints, motion, z-index), checking a value resolves to a token instead of being invented | `design-tokens/*`, `product-builder/ui/design-tokens.json` |
| Specifying a component (Button, Table, Modal, Form, …) or a composition pattern (Data Table, Form) — checking the master registry before inventing anything new | `component-registry/*` |
| Establishing/diffing a screen's baseline across passes, classifying a visual regression, or deciding whether a diff is an intentional change | `visual-regression/*`, `product-builder/ui/baselines/*.json` |
| Checking what's already been decided before making a new product/UX/UI/architecture decision, or persisting a significant one as an ADR | `product-memory/*`, `product-builder/memory/{product-memory,decision-records}.md` |
| Reasoning through an important UX/UI pattern decision with no obvious owner | `methodology/design-judgment.md` |
| Self-critiquing a finished screen/page's visual composition | `ui-engine/craft-critique.md` |
| Auditing/benchmarking a generated screen against its reference and design direction | `ui-engine/{ui-audit-framework,visual-benchmark}.md`, `templates/visual-gap-analysis.md` |
| Translating general UI-quality principles into an actionable check | `ui-engine/ui-design-principles.md` |
| Applying a stack-specific implementation technique (Tailwind v4, shadcn/ui, React 19, Vitest) during Implement | `ui-engine/frontend-implementation.md` |
| Picking an icon for a screen/component (check before generating anything) | `icon-packages/README.md` (Lucide + Heroicons, 2454 bundled icons) |
| Generating a favicon/app-icon package, processing/optimizing an image, or building a custom SVG icon set (only once the bundled `icon-packages/` has no fitting icon) | `ui-engine/asset-pipeline.md` |
| Generating real photographic/illustrative imagery (native + API dual-path, only when actually needed) | `ui-engine/visual-asset-generation.md` |
| Deciding whether an optional Gemini call (image generation, multimodal reference analysis, an independent visual/QA second opinion, or a content/localization second-pass) is actually warranted right now | `ui-engine/gemini-capability.md` |
| Generating developer docs (ARCHITECTURE/API/DATABASE_SCHEMA) or an end-user guide from already-produced artifacts | `workflows/project-documentation.md` |
| Generating or updating a Product Builder | `scripts/create-product-builder.py`, `workflows/create-product.md` |
| Running the product-builder's own action sequence | `workflows/execute-product-builder.md` |
| Building, testing, auditing | `workflows/{build-product,audit-product}.md`, `methodology/test.md`, `scripts/validate-*.py` |
| Checking a specific specialist's exact scope | `agents/*.md` |
| Filling in an artifact's exact shape | `templates/*.md` |
| A worked, end-to-end example for this kind of request | `use-cases/*.md` |
| Grading quality / running a benchmark | `evals/*` |
| Any rule, gate, or ID scheme by name | `config/*.md` |

This file never restates what's inside those — it only says what each is for
and when to reach for it.

---

## How Design-Glanza understands a request

### 2. Input types
Accepts a BRD, PRD, SOW, user stories, acceptance criteria, specifications,
PDFs/documents, screenshots, an existing product (live app or its codebase), or
a plain-language idea. Each has its own extraction posture and default
confidence — see `product-intelligence/brd-analysis.md`. Business-logic
extraction is never skipped just because the input looks UI-only.

### 3. Product classification
`product-intelligence/domain-classifier.md` scores signals (entity vocabulary,
role names, workflow shape) against the domain registry
(`config/master-config.md`) and states its confidence explicitly — confident
match, hybrid, partial, or no match.

### 4. Domain selection
A confident/partial match applies its `product-types/<domain>.md` pack — 12
exist today (SaaS, Admin Panel, ERP, CRM, E-commerce, Healthcare, HRMS,
Fintech, Logistics, Marketplace, Landing Page, Custom Domain). No match routes
to `product-types/custom-domain.md`'s procedure. Every pack follows the same
12-point Domain Pack Contract, so a new domain is added as a new pack, never a
core-file rewrite (see **Domain extensibility**, below). Independently, at the
same step, Product Architect also matches the product against a second,
much finer-grained registry (`product-types/domain-standards/domain-
registry.json`, 122 named domains) and loads any confidently-matched,
complete external standard as mandatory domain-specific guidance — Rule 17,
`product-intelligence/domain-standards.md`.

## How Design-Glanza reasons about the product

### 5. Design-thinking lifecycle
Empathize → Define → Ideate → Prototype → Test is the design-thinking core of
the 12-phase lifecycle above — real technique, not decoration: Empathize
builds an 11-dimension model per actor; Define produces 8 falsifiable outputs;
Ideate scores real alternatives on evidence, not preference. Detail:
`methodology/{empathize,define,ideate,prototype,test}.md`.

### 6. Requirement analysis
Raw facts become atomic, ID-tagged, source-or-assumption-tagged records:
`REQ-NNN` (requirements), `BR-NNN` (business rules), `ROLE-NNN` (roles/
permissions), `DEP-NNN` (dependencies), `EDGE-NNN` (edge cases) — never
invented, per Rule 10 (`config/operating-rules.md`). Detail:
`product-intelligence/{requirement-engine,business-logic,user-roles,
dependency-analysis,edge-case-engine}.md`.

### 7. Product architecture
Architect confirms the domain classification, applies the pack, defines
module/entity boundaries, and refines the dependency graph and build order —
before any screen exists (Rule 5: system before screen). Owner:
`agents/product-architect.md`.

## How Design-Glanza establishes design direction

### 8. Design Setup / Visual Direction
Between Architect and Prototype (added v1.0.7): first, run the full
**Design Research Engine** (Step 0, restructured v1.0.10 —
`design-research/*`) — a Research Brief classifying full vs. lightweight
research, then evidenced findings across Domain/Interaction/Visual (User
research is Empathize's own output, cited not re-derived) plus Competitor/
Pattern analysis where a reference exists, each finding labeled Known/
Assumed/Inferred/Unknown and CRITICAL/HIGH/MEDIUM/LOW-prioritized, recorded
as a real `RF-NNN` entry — never adopting a common pattern without clearing
the Anti-Generic Design challenge (Rule 21). Every CRITICAL finding, and
every HIGH finding affecting a core workflow, must produce a cited UX
Decision/UI Pattern or an explicit reasoned deferral — checked by **B16**.
Then detect and analyze any user-supplied design references, run a
structured design-expectation questionnaire, classify the result as
Reference-Driven / Guideline-Driven / Custom Design / Default
Design-Glanza — never one generic style regardless of domain (Rule 20) —
and produce one approved `product-builder/ui/design-direction.md`,
citing every Critical/High research finding's design principle —
confirmed with the user where one is available, never assumed from
generic defaults when real direction exists, and never fabricated from
nothing when it doesn't (Rule 18). Screens and tokens are never built
before this exists. A Figma reference whose structure is actually
inspectable (added v1.0.30, `design-reference-engine/figma-reference.md`)
is the highest-fidelity Reference-Driven instance — Explicit rather than
Inferred confidence, never a 5th mode — read via the Figma Skill's
read-only inspection tools, never by image inference alone where
structural data is available. Owner: `agents/design-setup-specialist.md`.
Detail: `design-research/*`, `design-reference-engine/*`, `design-samples/`,
`workflows/design-setup.md`.

## How Design-Glanza designs the product

### 9. UX architecture
Structure: user journeys/flows (`FLOW-NNN`, with recovery paths), information
architecture, navigation (13 concerns — breadcrumbs are never a default),
screen architecture, and the *named* interaction model per screen. Owners:
`agents/ux-architect.md` (structure), `agents/interaction-designer.md` (exact
behavior/states), `agents/accessibility-expert.md` (structural pass). Detail:
`ux-engine/*`. **Once flows/screens/states exist, every flow is walked as a
scenario across 8 mandatory types** (added v1.0.11, Rule 22 — primary,
alternate, error, empty, loading, permission, offline, recovery), checked
for missing screens/transitions/actions/validations/feedback and rolled
into the UX Coverage Matrix (`ux/ux-coverage-matrix.md`) — spec-level
checkpoint, gate **B17**. Owners: `agents/ux-architect.md` and
`agents/interaction-designer.md` jointly. Detail: `ux-scenario-testing/*`.

### 10. UI architecture
Visual realization on top of that structure: tokens, layout, typography,
color, component inventory, visual hierarchy, responsive rules — system
established before screens multiply (Rule 5 again, now at the UI layer),
consuming Design Setup's approved direction rather than re-deciding it.
Owners: `agents/design-system-expert.md` (governs the system),
`agents/ui-designer.md` (applies it). Detail: `ui-engine/*`. **Every token
is machine-readable and addressable by path** (added v1.0.12, Rule 23 —
`product-builder/ui/design-tokens.json`, `design-tokens/*`): 14 categories
including semantic color tokens (`primary`/`secondary`/`surface`/
`background`/`text`/`muted`/`success`/`warning`/`error`/`info`), themed
light/dark where applicable, inheriting the master scales without a
product ever redefining a closed one. A raw value with no fitting token is
logged as a system gap, never left silent — checked by
`scripts/validate-tokens.py`, gates **B6**/**B18**. **Every component
checks the master Component Registry before anything is invented** (added
v1.0.13, Rule 24 — `component-registry/*`): ~29 pre-populated components
(Button, Table, Modal, Card, Badge, …) and composition patterns (Data
Table, Form, Record Detail View, KPI/Stat Card) each with
when-to-use/when-not-to-use,
composition rules, and a named common-mistakes catalog — a component with
no cited registry base (or a stated reason none fit) fails gate **B19**.
Every
CRITICAL/HIGH `RF-NNN` research finding naming a UI pattern is mandatory
input here, cited directly in the artifact it shaped — never a common
pattern accepted without clearing the Anti-Generic Design challenge (Rule
21, gate **B16**). **Every generated screen then goes through a mandatory
visual-benchmark-and-audit cycle** (added v1.0.9, Rule 20): an 11-category
A–K audit (`ui-engine/ui-audit-framework.md`), a three-way Reference/
Design-Direction/Generated-UI comparison (`ui-engine/visual-benchmark.md`),
and at least one refinement pass — recorded in
`templates/visual-gap-analysis.md` even when a screen is clean on first
pass. The first generated UI is never treated as final. Gate: **B15**.
**Once confirmed clean, a screen's structural state is captured as a
baseline** (added v1.0.14, Rule 25 — `visual-regression/*`): every later
pass diffs current against baseline first — layout shifts, spacing/
typography/color changes, component inconsistencies, alignment problems,
missing/unexpected elements, responsive regressions — classified
Critical/High/Medium/Low and either fixed or explicitly approved as an
intentional Baseline Update; an unreviewed regression fails gate **B20**.

## How Design-Glanza builds the product

### 11. Product Builder generation
`scripts/create-product-builder.py generate` materializes
`products/<slug>/` (BRD/, product-builder/{product,requirements,ux,ui,domain,
workflows,qa}/, output/) with a product-specific `SKILL.md` that *references*
this skill's engines by relative path rather than copying them — first
generated once Architect + an initial Define pass exist, then refreshed with
`--update` as each later phase produces new content. `--update` preserves
everything already filled in; a bare `generate` on an existing product refuses
and reports the conflict instead of overwriting it. Full lifecycle mapping:
`workflows/execute-product-builder.md`.

### 12. Implementation
The generated Product Builder executes an already-fully-specified plan into
`output/`, in dependency-safe order; a gap discovered mid-build escalates back
to the owning spec, it is never improvised. Detail: `workflows/build-product.md`.

### 13. Preview & Run
Between Implement and Test (added v1.0.8): detect the framework, start the
local dev server, verify the build succeeds, detect the real local URL/
port, check for runtime errors, and fix any build/runtime issues before
continuing — implementation is not complete until it can actually be
launched and previewed (Rule 19). No dedicated reasoning specialist, same
posture as Implementation (12) — this is verification by execution, not new
design reasoning. An optional public preview (e.g. ngrok) happens only on
explicit request and is never required for normal operation. Detail:
`workflows/preview-run.md`, `templates/preview-report.md`.

## How Design-Glanza verifies the product

### 14. Testing
Nine dimensions, every time, never just task completion: task completion,
usability, discoverability, error prevention, feedback, accessibility,
responsiveness, edge cases, business-rule correctness. Owner:
`agents/qa-expert.md`. Detail: `methodology/test.md`. **Validated as a
product, not only as screens** — every scenario the UX Coverage Matrix
marks `covered` is walked end to end against the built (or spec) result,
checking for dead ends, ambiguous CTAs, missing feedback, and inconsistent
interaction patterns across the real screen sequence it visits (added
v1.0.11, Rule 22, walked checkpoint of gate **B17**). Detail:
`ux-scenario-testing/continuity-audit.md`.

### 15. Audit
Aggregates validator results (`scripts/validate-*.py`), traceability
integrity, design-system drift, and accessibility conformance into one QA
report with an explicit pass/fail gate status. Detail:
`workflows/audit-product.md`, `templates/qa-report.md`.

### 16. Iteration
Every finding routes to whichever phase/agent actually owns it
(`methodology/design-thinking.md`'s routing table); a fix is revalidated, and
a fix that regresses an already-passing gate reopens the scope rather than
passing by association. **A passing happy path never means complete** — see
Quality gates, next.

## Governing principles

### 17. Quality gates
`config/quality-gates.md` defines 12 phase-transition gates and 21 measurable
dimensions (B1-B21: requirement completeness, business logic, user-flow
completeness, IA, screen architecture, design system, state coverage,
accessibility, responsive behavior, traceability, QA, implementation
readiness, design direction completeness, preview & run verification,
visual benchmark & audit cycle completeness, research-to-design
traceability, UX scenario coverage, token inheritance integrity,
component registry conformance, visual regression integrity, product
memory integrity).
Completion requires clearing the relevant gates — not a working demo.
`evals/evaluation-rubric.md` extends this into a scored rubric, weighted so
visual polish alone can never carry a passing score.

### 18. Traceability
Every important requirement maps forward:
`REQ → USER → FLOW → SCREEN → COMPONENT → TEST`
(`product-intelligence/traceability.md`). An artifact with no upstream
requirement, or a requirement with no downstream artifact, is a defect unless
explicitly deferred. `RF-NNN` (Research Finding), `SCENARIO-NNN` (one
flow walked under one scenario type), and `ADR-NNN` (a persisted decision
record) are sideways references in the same model — cited, not chain
links — and a CRITICAL/HIGH research finding, a flow, or a decision with
no downstream artifact/`Related` citation is the same defect category
(Rules 21/22/26).

### 19. Product isolation
A generated Product Builder holds product-specific knowledge only; it never
contaminates this master skill, and this skill never hardcodes one company's
product. (Rule 15, `config/operating-rules.md`.)

### 20. Domain extensibility
A new domain is added by authoring one new `product-types/<domain>.md` pack
against the fixed Domain Pack Contract (`product-types/custom-domain.md`) — the
domain-agnostic core (`config/`, `methodology/`, `product-intelligence/`,
`ux-engine/`, `ui-engine/`) is never edited to accommodate a domain. (Rule 14
and Rule 16, `config/operating-rules.md`.)

### 21. Product Memory
Added v1.0.15 (Rule 26): the Product Builder remembers its own significant
product/UX/UI/design-system/component/architecture decisions across the
whole lifecycle, indexed in `product-builder/memory/product-memory.md` —
mostly a cross-reference over content that already lives in `product/`,
`ux/`, `ui/`, `domain/`, `research/`, `qa/` (`product-memory/README.md`
states exactly where, category by category), plus one genuinely new
persisted artifact: `ADR-NNN`, the storage form of topic 18's design
decision framework. Before generating or modifying UI, the acting agent
checks Product Memory first; a contradiction is only ever introduced via
a new ADR that explicitly supersedes the one it replaces — never
silently. Gate: **B21**. Detail: `product-memory/*`.

---

## Do not

- Do not generate UI before Empathize/Define have run (Rule 1/4).
- Do not invent a business rule, role, or requirement the source doesn't
  support — tag it as an assumption with its impact stated (Rule 10).
- Do not copy this skill's methodology into a generated Product Builder —
  reference it.
- Do not hardcode a domain into a core file — that belongs in a
  `product-types/*.md` pack.
- Do not declare a product complete because its happy path works — clear the
  relevant gates (17) first.
- Do not let Prototype's UI pass begin before Design Setup's approved
  `ui/design-direction.md` exists (8) — never generate UI from generic
  assumption when the user has provided real design direction (Rule 18).
- Do not treat an exact Figma reference as a literal clone target just
  because its data is precise and easy to copy 1:1 — extract the
  underlying design language and generate a new screen, never reproduce
  an existing Figma frame (8, Rule 18, `design-reference-engine/
  figma-context-consumption.md`'s non-negotiable output rule).
- Do not declare Implement complete, or proceed to Test, before the built
  output has actually been launched locally and previewed (13) — a build
  that "should work" is not the same as one that was run (Rule 19).
- Do not treat the first generated UI as final — at least one visual
  audit-and-refinement cycle is mandatory for every screen, even a clean
  one (10, Rule 20).
- Do not select the same default design register/sample for every product
  regardless of its matched domain — Admin Panel ≠ E-commerce ≠ Healthcare
  ≠ ERP ≠ Fintech ≠ CRM (8, Rule 20).
- Do not treat research as documentation generated beside a design decision
  made some other way — a CRITICAL finding, or a HIGH finding affecting a
  core workflow, must produce a cited UX Decision/UI Pattern or an
  explicit, reasoned deferral (8, Rule 21, gate B16).
- Do not accept a common/default UI pattern without applying the
  Anti-Generic Design challenge (why is it appropriate, what user problem
  does it solve, what evidence supports it, is there a better pattern, is
  it IA-consistent) — `design-research/pattern-analysis.md` (8/10, Rule 21).
- Do not declare a product complete because every individual screen passed
  its own audit — every flow must be walked as a scenario end to end, and
  a dead end, missing screen/transition/action/validation/feedback, or
  unresolved recovery path anywhere in that walk keeps the product
  incomplete regardless of how well any single screen tests (9/14, Rule
  22, gate B17).
- Do not invent an arbitrary color, type size, spacing value, radius,
  border, shadow, component dimension, breakpoint, motion duration, or
  z-index — every value resolves to a `design-tokens.json` path or is
  logged as a system gap, never left silent (10, Rule 23, gates B6/B18).
- Do not let a product's token file redefine a closed master scale
  (radius/elevation/motion/border-width/sizing/z-index/type/spacing/grid/
  breakpoints) or write a product-specific value back into `ui-engine/*` —
  extend under `product.*`, never fork the master (10, Rule 23, gate B18).
- Do not specify a new component before checking `component-registry/*`
  first, then the product's own inventory — and never write a
  product-specific component back into that registry (10, Rule 24, gate
  B19).
- Do not let a later pass silently change a screen that already passed
  its visual-benchmark cycle without diffing it against its baseline
  first — an unreviewed regression (a missing element, a drifted token,
  a broken breakpoint) is never accepted just because the pass's own new
  work looks fine (10, Rule 25, gate B20).
- Do not accept a visual diff as "intentional" with no logged Reason and
  approval — the same no-invented-facts discipline Rule 10 already
  requires of an assumption, applied to a Baseline Update (Rule 25).
- Do not generate or modify UI without first checking
  `product-builder/memory/product-memory.md` for a relevant existing
  decision — and do not introduce a contradicting decision without a new
  `ADR-NNN` that explicitly supersedes the one it replaces (21, Rule 26,
  gate B21).
- Do not let a specialist agent self-invoke outside the phase
  `workflows/*.md` assigns it, or redesign work another agent owns — route
  the problem to the owning agent instead (`config/master-config.md`'s Role
  registry).
