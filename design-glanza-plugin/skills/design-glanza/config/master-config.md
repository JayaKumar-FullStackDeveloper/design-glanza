# Master Config

## Responsibility
Single source of truth for constants and registries that every other file
references instead of restating. If a value needs to change once and propagate
everywhere, it belongs here.

## Skill identity & version
- **Name:** design-glanza
- **Version:** 1.0.7 — added a new mandatory **Design Setup / Visual
  Direction** phase between Architect and Prototype (the lifecycle is now
  11 phases, not 10 — nothing existing was removed or reordered, one phase
  was inserted). Before any screen or token is designed, the product's
  visual/interaction direction must be deliberately established: detect and
  analyze any user-supplied design references (screenshots, Figma, brand/
  color/typography guidelines, existing UI, etc. — 13 recognized forms),
  run a structured 9-category design-expectation questionnaire where
  references are absent or incomplete, classify the result as one of
  **Reference-Driven / Guideline-Driven / Custom Design / Default
  Design-Glanza**, write a complete `product-builder/ui/design-direction.md`,
  and gate on user approval ("does this design direction match your
  expectations?") before Prototype's UI pass begins. New **Rule 18 — Design
  Setup / Visual Direction** (18 rules now) and new **B13 — Design Direction
  Completeness** gate (13 measurable dimensions now), inserted into
  `config/quality-gates.md` Section A between Architect→(old Prototype) and
  the renamed Design Setup→Prototype transition. New agent
  `agents/design-setup-specialist.md`; new workflow
  `workflows/design-setup.md`; a new technique library,
  `design-reference-engine/{reference-analysis,design-questionnaire,
  reference-selection,design-direction}.md`, kept deliberately separate from
  `product-intelligence/brd-analysis.md` (which still extracts *business
  logic* from the same reference inputs — the new library extracts *visual
  direction* only, cross-referenced explicitly from `brd-analysis.md` so the
  two extractions are never conflated); a new default-sample library,
  `design-samples/` (12 folders — the 10 domains already matching a
  `product-types/*.md` slug, plus 2 platform samples, Mobile and Responsive
  Web — every folder currently a placeholder README, same disclosed-gap
  posture as `product-types/domain-standards/`'s pending entries); and a new
  template, `templates/design-direction.md`. Wired as mandatory input into
  `agents/ux-architect.md`, `ui-designer.md`, and `design-system-expert.md`
  — explicitly *without* moving Rule 4 (UX before UI) or Rule 5 (system
  before screen)'s actual enforcement points: Design Setup establishes
  *intent*, the design system is still built where it always was, inside
  `create-ui.md`. `workflows/execute-product-builder.md`'s action table
  grew from 24 to 29 actions (5 new Design Setup actions inserted after the
  Architect action, all subsequent Order values shifted by +5, original `#`
  numbering preserved for traceability, `-` used for the new actions per the
  existing convention for unnumbered actions). `SKILL.md` renumbered topics
  8–18 to 9–19 to insert a new topic 8, added a new "How Design-Glanza
  establishes design direction" section header, and updated the core
  lifecycle diagram and routing table. `evals/evaluation-rubric.md` gained a
  19th dimension (Design direction quality, Tier B, mapping to B13; total
  scorable points 205→215) — and, while that file was already open for this
  addition, corrected a pre-existing miscount in its own text (it said "six"
  **new**-marked dimensions when the table itself already had seven).
  `evals/test-cases.md` updated to the new dimension count and given a
  coverage mapping for the new dimension. Deliberately **not** touched:
  `design-glanza-plugin/` (consistent with every prior integration round —
  the plugin remains a manually-synced snapshot, now further behind) and
  `products/projectflow/` (Rule 15, Product Isolation — an already-generated
  product is not retroactively rewritten to match a new phase; a future
  `--update` pass on that product would pick it up).
- **Previously, 1.0.6** — added the **Domain Standards Library**: a new
  `product-types/domain-standards/` folder (a 122-entry `domain-registry.json`
  across 12 categories, 11 complete PDF standards under `01-core-business/`,
  111 reserved `README.md` placeholders) plus a new engine file,
  `product-intelligence/domain-standards.md`, and a new **Rule 17 — Domain
  Standards** (`config/operating-rules.md`, still layered onto the existing
  constitution, not a restructuring of it). This is a second, much
  finer-grained domain-matching system alongside the existing 12
  `product-types/*.md` packs, not a replacement — the two compose (a
  registry entry whose `slug` names an existing pack enriches it; the other
  110+ entries with no corresponding pack still route through
  `custom-domain.md`'s existing fallback, now optionally enriched by a
  loaded standard). Wired as mandatory input, not a rewrite, into
  `agents/product-architect.md` (matches/loads at the same step it already
  applies a `product-types/*.md` overlay), and into `ux-architect.md`,
  `interaction-designer.md`, `ui-designer.md`, `design-system-expert.md`,
  `accessibility-expert.md`, and `qa-expert.md`'s Input sections. Reconciled
  against Rule 2's existing 8-tier source-of-truth order (a loaded standard
  sits at tier 6, the same tier `product-types/*.md` conventions already
  occupy) rather than adopting a second, competing priority list a
  user-provided integration spec had proposed — that spec's own draft
  architecture (a flat `SKILL.md`/`product.json`/`brd/` layout) didn't match
  Design-Glanza's real structure, so its intent was folded into the real
  files above rather than copied in as a second, conflicting document; the
  registry, 11 PDFs, and placeholder READMEs were imported as prepared. A
  `"pending"` registry entry (111 of 122) loads nothing and is not an error —
  never fabricated as a substitute. No existing rule, gate, phase, agent
  boundary, or `products/` content touched; `scripts/create-product-
  builder.py` and its `product.json` schema untouched (the selected
  standard(s) are recorded in Product Architect's own existing output,
  `domain-application-notes.md`, needing no script change).
- **Previously, 1.0.5** — integrated reusable knowledge from a second external
  batch (`tastemaker-main`'s `docs/`+`research/`, `designer-skills-main`'s
  111-skill collection, `ui-ux-pro-max-skill-main`, `frontend-design-pro-
  demo-main`; analyzed, not copied wholesale; all four sources untouched, no
  file under `products/` touched, no new Product Builder created). Roughly
  20 files touched across a large but curated set of additions (most of the
  ~150 substantive files reviewed were duplicates of existing content or
  genuinely out of scope, per the import plan presented before this pass):
  a 12th weighing factor (Convention/familiarity) and an evidence-vs-craft
  labeling requirement in `methodology/design-judgment.md` (now 12 factors,
  citations updated in `design-thinking.md` and `agents/design-system-
  expert.md`); a 9th UX-engine optimization criterion (Emotional arc/
  Peak-End) and inherent-vs-extraneous complexity vocabulary in
  `ux-engine/user-flow-engine.md`; a threshold-vs-trade-off criteria split
  and a mandatory rejected-concepts register in `methodology/ideate.md`'s
  selection step; Optimistic UI, skeleton-vs-spinner selection, and false-/
  missing-affordance vocabulary in `ux-engine/interaction-design.md`; a
  utility-navigation category and serial-position ordering in
  `ux-engine/navigation-system.md`; a state-machine modeling-technique note
  in `ux-engine/state-design.md`; WCAG 2.2 specifics (focus-not-obscured,
  focus appearance, dragging movements, target size, consistent help,
  redundant entry, accessible authentication) and a forced-colors/high-
  contrast check in `ux-engine/accessibility.md`; a contrast "pairing
  contract" concept and data-visualization color ramps in
  `ui-engine/color-system.md`; a chart-selection Data visualization section
  in `ui-engine/component-system.md`; dark-mode elevation-via-lighter-layers,
  a mandatory modal scrim, and motion choreography (stagger/sequence-cap/
  direction-consistency, still inside the closed 3-token scale) in
  `ui-engine/design-system.md`; an explicit density-as-axis note in
  `ui-engine/visual-trends.md`; a full 5-principle Gestalt grouping
  checklist and an isolation-inflation drift caution in `ui-engine/
  visual-hierarchy.md`; a 9th check (cognitive load/scanning fit), a
  sharpened structural-variety check 7, a named/reporting-format section, and
  a corroborated anti-cliché entry in `ui-engine/craft-critique.md`; a
  non-Latin-script typography section in `ui-engine/typography.md`; a
  pivotal-section spacing exception in `ui-engine/layout-system.md` and a
  matching cross-reference in `product-types/landing-page.md`; a locale/
  script flag and a cross-source synthesis-bias caution in
  `methodology/empathize.md`; a non-blocking-findings persistence/
  prioritization note in `config/quality-gates.md`; an optional RICE/Kano
  citation in `product-intelligence/requirement-engine.md`; a re-fired
  color-pairing check and an implementation-fidelity spot-check in
  `agents/qa-expert.md`; and three new files —
  `ux-engine/ux-writing.md` (no microcopy engine existed at all: error-
  message formula, voice-vs-tone, tone-by-state, CTA wording), `ux-engine/
  localization.md` (RTL mirror/no-mirror list, text-expansion planning
  figures, logical-property framing — no localization coverage existed at
  all), and `ux-engine/search-ux.md` (query/ranking/zero-results, composing
  with the existing filter→sort→paginate order — previously referenced by
  `information-architecture.md` but never itself specified) — each cited
  from the responsible `agents/*.md` file and `SKILL.md`'s routing table.
  Explicitly rejected: a competing 0–4 numeric severity scale (kept
  Blocker/Major/Minor/Note as the only vocabulary); an entire 11-aesthetic
  "always commit to one bold style" skill (fails the register fit-condition
  bar the same way a previously-reviewed 67-preset library did); raw CSV
  rows, GSAP snippets, and stack-specific guidance from `ui-ux-pro-max-
  skill-main` (Rule 14 boundary; only paraphrased principles were kept). No
  rule, gate, or phase count changed (still 16 rules, 12 quality-gate
  dimensions, 10 phases) — every addition extended an existing rule/file in
  place or, where genuinely homeless, became one of the three new files
  above.
- **Previously, 1.0.4** — integrated reusable knowledge from an external
  21-skill collection (`Downloads/skills`, analyzed but not copied wholesale;
  originals untouched). Six additions, each cited to its source and checked
  against every existing rule for conflicts before being added: (1) a
  **Motion and animation** section in `ux-engine/interaction-design.md`
  (frequency-based animate/don't-animate gate, purpose-must-be-stated rule,
  interruptibility, spatial-consistency/return-to-origin, asymmetric timing,
  reduced-motion nuance) — cross-checked against `ui-engine/design-system.md`'s
  fixed 3-token motion scale, which stays authoritative and unexpanded, now
  with an explicit closed-scale note; (2) a wayfinding checklist added to
  `ux-engine/navigation-system.md`, and a zoom/text-scaling rule added to
  `ux-engine/accessibility.md`; (3) `methodology/ideate.md`'s divergence
  technique sharpened with a named-axis, no-shared-axis completion rule, and
  `methodology/prototype.md` gained a realistic-scale evaluation note; (4) a
  new 12th domain pack, `product-types/landing-page.md`, for single-page
  conversion surfaces — deliberately excluding the source material's own
  fixed visual/token system, which would have silently overridden
  `ui-engine/visual-trends.md`'s register system; `product-intelligence/
  domain-classifier.md` gained a matching signal row; (5) a new
  `ui-engine/craft-critique.md` — a numeric, checkable finished-composition
  self-critique (hierarchy ratios, hero subtraction, deletion/specificity
  tests, an anti-cliché catalog independently confirmed across three
  unrelated source projects) cited from `agents/ui-designer.md` and
  `agents/qa-expert.md`, deliberately *not* added as a new blocking
  `quality-gates.md` dimension; (6) a Protected-Contracts / redesign-
  classification addition to `workflows/redesign-product.md`. Rule 11
  (`operating-rules.md`) extended to explicitly cover motion, citing the new
  material, without adding a 17th rule. No file under `products/` touched; no
  new Product Builder created; no existing rule, gate, phase, or file
  removed or restructured.
- **Previously, 1.0.3** — added the Design Judgment Engine
  (`methodology/design-judgment.md`) for important UX/UI pattern decisions:
  the same 9-step chain as `design-thinking.md`'s general index, now with
  11 concrete weighing factors, an anti-fashion gate, and a worked
  reasoning-vs-sounding-like-reasoning example. Wired into the 4 agents
  that actually make these calls; see changelog below for the exact list.
- **Previously, 1.0.2** — repaired 4 concrete gaps found by a full master-skill
  validation pass; no architecture redesign, no new files, no Product Builder
  created.
- **Before that, 1.0.1** — every folder in the architecture has real content
  (operating rules, quality gates, output contract, the design-thinking
  methodology engine, the BRD/requirement intelligence engine, the UX
  engine, the UI engine, the domain extensibility architecture
  (`product-types/*`), all 8 `agents/*` files, all 11 `templates/*` files,
  all 7 `workflows/*` files, all 6 `scripts/*.py` files, all 8 `use-cases/*`
  files, all 3 `evals/*` files), and `SKILL.md` was rewritten in full as
  the final, production-oriented orchestrator — valid frontmatter, all 18
  required topics numbered 1-18 exactly, a progressive-disclosure routing
  table, and an explicit Design-Glanza-vs-Product-Builder distinction. That
  rewrite dropped the versioned status banner this section used to be
  cross-referenced from — this changelog is now the only place skill
  history is tracked; `SKILL.md` itself stays clean going forward and does
  not carry a version banner. 1.0.1 then configured the skill for its POC
  phase: `disable-model-invocation: true` (explicit invocation only, via
  `/design-glanza`, which works automatically since a skill is invocable by
  its own name — no separate command file needed), a scoped `allowed-tools`
  list (`Read`/`Write`/`Edit`/`Glob`/`Grep` plus `Bash` narrowed to this
  skill's own `scripts/*.py`, nothing broader), and a "POC invocation &
  safety" section requiring confirmation before any irreversible or
  large-scale action, matching the posture
  `scripts/create-product-builder.py`'s conflict guard already enforces at
  the tooling layer. This marks *specification completeness plus a safe
  invocation posture*, not runtime validation of the whole pipeline against
  a real product.
- **Changelog:**
  - 0.1.0 — architecture shell: directory structure and all file skeletons created.
  - 0.2.0 — `config/operating-rules.md` (16 rules), `config/quality-gates.md`
    (phase-transition gates + 12 measurable dimensions), `config/output-contract.md`
    (assumption tag, severity vocabulary, report shapes) implemented.
  - 0.3.0 — `methodology/*` implemented as a continuous Empathize → Define →
    Ideate → Prototype → Test loop (not a one-time checklist): loop mechanics and
    feedback-routing table in `design-thinking.md`; the 11 Empathize dimensions,
    8 Define outputs, 8 Ideate behaviors, 6 Prototype outputs, and 9 Test
    dimensions each fully specified in their own file.
  - 0.4.0 — `product-intelligence/*` implemented: a 20-point intake-analysis
    checklist owned across `brd-analysis.md` (extraction, input-type
    recognition for BRD/PRD/SOW/user stories/acceptance criteria/specs/PDFs/
    screenshots/existing product/existing code/plain-language input, and the
    "business logic is never optional even for UI-focused input" rule),
    `requirement-engine.md` (the `REQ-NNN` model and full field schema),
    `business-logic.md` (`BR-NNN` rules/validation/triggers/status/decision
    points/workflow/success-failure), `user-roles.md` (`ROLE-NNN` +
    permission matrix), `edge-case-engine.md` (`EDGE-NNN`),
    `dependency-analysis.md` (`DEP-NNN` + integration assumptions),
    `domain-classifier.md` (signal-scored classification), and
    `traceability.md` (the REQ → USER → FLOW → SCREEN → COMPONENT → TEST
    chain and its ID schemes). Rule 9 (`operating-rules.md`) and
    `templates/requirement-matrix.md` updated to match the USER-inclusive
    chain and full field schema.
  - 0.5.0 — `ux-engine/*` implemented: `user-flow-engine.md` (journeys vs.
    flows, the `FLOW-NNN` ID scheme, the 8 UX Engine optimization criteria
    defined once and cited elsewhere, the canonical
    entry→action→decision→system-response→next-action→completion notation,
    and the retry/abandon-safely/escalate recovery-path technique),
    `information-architecture.md` (screen hierarchy depth/breadth rules,
    permission-aware structure, cross-module placement),
    `navigation-system.md` (all 13 navigation concerns — module entry,
    sidebar, primary/secondary/deep nav, back behavior, breadcrumbs-when-
    appropriate with an explicit non-universal selection rule, modals,
    drawers, overlays, multi-step workflows, cross-module nav, role-based
    nav), `interaction-design.md`, `form-design.md` (data-requirement
    linkage per field), `state-design.md` (all 12 mandatory states precisely
    defined and distinguished, plus a state-priority rule and recovery-path
    integration), and `accessibility.md` (structural/behavioral, applied
    concretely to nav, forms, states, and recovery paths).
  - 0.6.0 — `ui-engine/*` implemented: `design-system.md` (radius, elevation,
    motion, and icon-size token scales owned directly since no other file
    claims them; the theming alias layer; "establish before screens" as
    Rule 5's UI-layer enforcement point), `layout-system.md` (4px spacing
    scale, 12-column grid, 5 named composition patterns mapped to IA shape),
    `typography.md` (a density-appropriate 14–16px body type scale, single-
    family pairing rule, tabular-figure rule for numeric data),
    `color-system.md` (9–10 step ramps, semantic foreground/background/border
    triplets, concrete 4.5:1 / 3:1 contrast rule, red/green color-blind
    safety rule), `visual-hierarchy.md` (all 8 required considerations —
    primary/secondary action, information priority, grouping, scanning
    pattern selection, density scale, whitespace-as-priority, progressive
    disclosure — plus a 3–4-level emphasis cap), `component-system.md` (the
    8-point component analysis framework, iconography as its own component
    type, and per-component motion token assignment), `responsive-system.md`
    (4 breakpoints, per-pattern reflow table, the enterprise data-table
    responsive technique), and `visual-trends.md` (3 named registers, a
    3-point trend-adoption gate, and the explicit trend-vs-system boundary
    rule — trends are contextual options, never mandatory).
  - 0.7.0 — `product-types/*` implemented: all 11 packs (SaaS, Admin Panel,
    ERP, CRM, E-commerce, Healthcare, HRMS, Fintech, Logistics, Marketplace,
    Custom Domain) answer the same fixed 12-point Domain Pack Contract
    (defined in `custom-domain.md`) with domain-specific content only,
    citing rather than restating the core engine file each point
    specializes; no company-specific product detail in any pack (Rule 15).
    `custom-domain.md` additionally carries the no-match / partial-match /
    graduation procedure. Rule 16 (`operating-rules.md`) updated to point to
    the contract directly.
  - 0.8.0 — the Product Builder Factory: `scripts/create-product-builder.py`
    fully implemented (not a stub) and verified by running it —
    `generate`/`validate` subcommands, dynamic `product_type` discovery from
    `product-types/*.md` (a new domain pack becomes valid with zero script
    changes), name/slug/required-field/product_type validation,
    `product.json` with all 10 required fields plus timestamps,
    `master_skill_version` read live from `config/master-config.md` rather
    than hardcoded, the full `products/<slug>/{BRD,product-builder/{product,
    requirements,ux,ui,domain,workflows,qa},output}` structure, a generated
    `product-builder/SKILL.md` covering all 20 required sections that
    references the master engine by relative path instead of copying it, a
    conflict guard that refuses to overwrite an existing product without
    `--update`, and content-preserving `--update` (re-parses a prior
    generated `SKILL.md` so a section supplied on one run survives a later
    run that doesn't resupply it). `workflows/create-product.md` and
    `redesign-product.md` updated with a "Scaffolding the Product Builder"
    section describing when/how each phase calls the generator.
  - 0.9.0 — `workflows/execute-product-builder.md` implemented: the concrete
    24-action sequence (per the user's numbered list, reconciled against the
    master engine's actual dependency order — e.g. flows before IA before
    navigation — with the discrepancy stated explicitly rather than silently
    resolved) mapped to phase, master technique, and the exact
    `product-builder/` file each action must write; an explicit
    artifacts-not-conversation mandate; and completion criteria stating
    plainly that a passing happy path is one of nine `methodology/test.md`
    dimensions, not sufficient on its own — full gate compliance
    (`config/quality-gates.md` Section B) is required. `workflows/
    create-product.md` and the generator's `product-builder/SKILL.md`
    template (`scripts/create-product-builder.py`) both updated to link to
    it directly rather than duplicating it — verified by regenerating a test
    product and confirming the relative link resolves on disk.
  - 0.10.0 — all 11 `templates/*` files implemented, each with a fixed
    6-part shape (purpose, required inputs, output structure, quality
    criteria, example structure, traceability fields where applicable):
    `product-definition.md` (now also holding Empathize/Ideate summaries,
    matching `execute-product-builder.md`'s artifact map), the expanded
    `requirement-matrix.md` schema, `user-persona.md`, `user-flow.md` (the
    canonical notation + recovery paths), `sitemap.md`, `screen-architecture.md`,
    `screen-specification.md` (cross-checked against B5/B6/B7/B8/B9
    jointly), `design-system.md`, `component-spec.md` (the 8-point
    framework), `state-matrix.md` (zero-blank-cells rule), and
    `qa-report.md` (explicitly requiring all 9 `methodology/test.md`
    dimensions reported individually — a happy-path-only report is
    rejected on its face). Every quality-criteria section cites its
    `config/quality-gates.md` B-dimension directly. Every example uses
    abstract placeholders or genuinely domain-neutral UI concepts (e.g. a
    Button atom) — no domain-specific business rule appears in any
    template, per Rule 14.
  - 0.11.0 — all 8 `agents/*` files implemented, each with role,
    responsibility, input, analysis procedure, output, quality criteria, and
    "things it must not do." The UX Architect / Interaction Designer
    boundary was drawn explicitly and non-overlappingly: UX Architect owns
    *structural* interaction (which pattern a screen uses); Interaction
    Designer owns its *detailed behavior* (exact timing, confirmation
    rules, the state matrix) — neither may redo the other's decision, each
    file states this in its own "must not do" section. Added an
    **orchestration authority** note to this file's Role registry (above):
    an agent is invoked only by the `workflows/*.md` governing its phase,
    never self-invoking or expanding into another agent's scope — routing a
    problem is always the mechanism, never fixing it in place outside one's
    own artifacts.
  - 0.12.0 — the remaining 5 `workflows/*` files deepened to match the rest
    of the engine: each now names its executing `agents/*.md` file(s) in
    sequence (e.g. `create-ui.md` runs `design-system-expert.md` before
    `ui-designer.md`, enforcing Rule 5 system-before-screen at the
    workflow level, not just in prose), cites exact
    `product-builder/` artifact paths from
    `workflows/execute-product-builder.md`'s action table instead of
    describing them abstractly, and cites the precise `config/
    quality-gates.md` gate ID(s) each step must pass. `build-product.md`
    states explicitly that Implement has no dedicated reasoning specialist
    among the 8 agents (by design — it executes an already-fully-specified
    plan, it doesn't reason about design) rather than silently implying one
    exists.
  - 0.13.0 — the deterministic validation toolchain implemented: a new
    `scripts/_common.py` (shared path resolution, the 9 ID-scheme regexes,
    the 12 mandatory states, and a `Finding` type carrying
    `config/output-contract.md`'s severity vocabulary) so no script
    duplicates another's constants; `create-product-builder.py` refactored
    to import from it (re-verified after the refactor — no behavior
    change). `validate-requirements.py` (duplicate-ID detection, header
    field-presence, blank-cell detection, cross-file `BR-NNN`/`DEP-NNN`/
    `EDGE-NNN` referential integrity), `validate-screens.py` (`SCREEN-NNN`
    existence, required-topic keyword presence, screen-to-requirement
    mapping), `validate-states.py` (mandatory-state column presence, the
    zero-blank-cells rule, `EDGE-NNN` referential integrity), and
    `validate-product.py` (aggregates the above plus
    `create-product-builder.py`'s scaffold check, reused rather than
    duplicated) — every check verified by deliberately constructing test
    content with a duplicate ID, blank cells, a missing mandatory-state
    column, an orphaned screen, and dangling references, confirming each
    fires correctly, then removing the test artifacts.
    `generate-report.py` renders `templates/qa-report.md`'s shape but is
    explicit about the toolchain's central boundary: sections requiring
    reasoning (`methodology/test.md`'s 9 dimensions, rubric scores,
    design-system drift, accessibility conformance) are rendered as
    **"Not evaluated by this script"** with a pointer to the responsible
    agent, never fabricated — per the instruction to prefer deterministic
    validation in scripts and reasoning-based validation in Claude
    instructions.
  - 0.14.0 — all 8 `use-cases/*` files implemented against a fixed 9-stage
    schema (Input → Classification → Analysis → Required artifacts →
    Design-thinking phases → Product Builder generation → Implementation →
    QA → Completion criteria), each closing with a "How this differs from
    other use cases" section that names a concrete contrast (e.g. e-commerce
    splits its two-IA-branch pattern by process stage; HRMS splits the same
    pattern by audience). Added `use-cases/product-redesign.md` (a new
    file) to separate the "already has a Design-Glanza builder, use
    `--update`" case from `existing-product.md`'s "no builder yet, cold
    reverse-engineering" case — the original 7 files conflated these under
    one worked example; `workflows/redesign-product.md`'s cross-reference
    updated to point to both. Every file states explicitly that it routes
    through the one master skill — no separate per-domain skill exists.
  - 1.0.0 — `evals/*` implemented, completing every folder in the
    architecture: `test-cases.md` (the 10 benchmark scenarios — 7 reusing
    `use-cases/*.md` rather than re-describing them, plus 3 new
    format-stress scenarios: Ambiguous Requirement, Large BRD, Multi-role
    Enterprise Workflow — a coverage table showing which scenario stresses
    each of the 18 rubric dimensions, plus the 4 triggering-behavior test
    categories: should/should-not trigger, should-ask-for-missing-info,
    should-use-the-right-pack), `evaluation-rubric.md` (all 18 dimensions —
    12 mapping directly to a named `config/quality-gates.md` B-gate, 6
    genuinely new: user-role coverage, navigation, UX quality, component
    reuse, edge cases, self-critique, iteration quality — grouped into 3
    weighted tiers so visual/presentation dimensions are mathematically
    capped under 5% of the total possible score, directly enforcing
    "do not optimize only for visual output"), and `benchmark-matrix.md`
    (a per-version snapshot view, a per-cell trend view for regression
    detection, and a **Failure Log** — every score of 1-2 or failed
    triggering-behavior test becomes a tracked record with root cause, fix,
    and re-benchmark result, mirroring `custom-domain.md`'s graduation
    rule, making "record failures and use them to improve the skill" a
    real mechanism rather than a suggestion). `SKILL.md` also rewritten in
    full as the final orchestrator (see the Version summary above for what
    changed).
  - 1.0.1 — `SKILL.md` frontmatter reviewed and reconfigured for the POC
    phase: `disable-model-invocation: true` added (explicit invocation
    only — no auto-trigger on a passing mention of UI/UX/SaaS/design;
    `/design-glanza` already works as the entry point since a skill is
    invocable by its own name); `allowed-tools` scoped to
    `Read`/`Write`/`Edit`/`Glob`/`Grep` plus a `Bash` allowlist limited to
    this skill's own `scripts/*.py` (no general shell, no network tools);
    a new "POC invocation & safety" section added requiring confirmation
    before any irreversible or large-scale action. Frontmatter validated
    by actually parsing it as YAML (caught and fixed one real bug in the
    process: an unquoted colon inside the description broke plain-scalar
    parsing).
  - 1.0.2 — repaired the 4 concrete gaps found by the master-skill
    validation pass (a plugin-conversion turn intervened between 1.0.1 and
    this entry; see the `design-glanza-plugin/` deliverable for that,
    unaffected by this repair since it targeted the project-local skill
    only). No architecture redesign; no new files created.
    (1) **Offline state** — added to Rule 6 (`config/operating-rules.md`),
    the mandatory-state table and state-priority order
    (`ux-engine/state-design.md`, now 13 states), `templates/state-matrix.md`,
    `config/quality-gates.md`'s B7 criterion, and — the functional half, not
    just documentation — `scripts/_common.py`'s `MANDATORY_STATES` list and
    `scripts/validate-states.py`'s docstring, verified by re-importing
    `_common` and confirming the list now has 13 entries.
    (2) **Sorting and pagination** — a new section in
    `ux-engine/interaction-design.md` covering the sort-cycle sequence,
    loading behavior during re-sort/repaginate, keyboard/ARIA requirements,
    and the fixed filter→sort→paginate application order (filtering always
    resets to page 1).
    (3) **Figma reference** — added as its own row in
    `product-intelligence/brd-analysis.md`'s input-type table, distinguishing
    visual-only viewing (same posture as Screenshots) from an inspectable
    file's own structural metadata (layer/component names — Medium-High,
    still never High for business logic).
    (4) **The design decision framework** — added to
    `methodology/design-thinking.md` as an explicit, citable
    Problem→Context→User Need→Constraints→Alternatives→Trade-offs→Selected
    Approach→Expected Outcome→Validation chain, mapped to exactly the
    phases/outputs that already produce each step (no new technique) —
    paired with an explicit "the 10-phase lifecycle remains authoritative,
    unchanged" section addressing the fifth requested clarification.
    Deliberately **not** touched: `agents/interaction-designer.md`,
    `workflows/execute-product-builder.md`, `evals/evaluation-rubric.md`,
    and `config/master-config.md`'s own historical changelog entries above
    still say "12 mandatory states" in passing citation — left as a known,
    minor, disclosed residual inconsistency rather than edited, since none
    of those files were part of the named repair scope and editing past
    changelog entries would rewrite history.
  - 1.0.3 — the Design Judgment Engine: a new
    `methodology/design-judgment.md`, the applied counterpart to
    `design-thinking.md`'s general decision-framework index — same 9-step
    chain, now scoped specifically to important UX/UI *pattern* decisions
    with no more specific owning file (explicitly not a replacement for
    `navigation-system.md`'s, `visual-trends.md`'s, or `ideate.md`'s own
    pattern-selection logic — cites those instead of re-deriving them), an
    11-factor weighing table (user expertise, task frequency, task
    complexity, information density, decision speed, error risk,
    accessibility, responsiveness, scalability, maintainability, business
    impact) each with a stated question and a stated effect on the
    decision, an anti-fashion "strip-away test" gate, and a worked
    reasoning-vs-reasoning-*shaped*-prose contrast making the "senior
    reasoning, not senior-sounding language" bar checkable rather than
    aspirational. Cross-referenced from `design-thinking.md` (not
    duplicated) and wired into `agents/ux-architect.md`,
    `ui-designer.md`, `interaction-designer.md`, and
    `design-system-expert.md` with a one-line citation each, plus one new
    row in `SKILL.md`'s progressive-disclosure routing table. While editing
    `agents/interaction-designer.md` for that citation, also closed 2 of the
    3 residual "12 mandatory states" references 1.0.2 had explicitly left
    open (now genuinely in scope, since the file was already open for a
    real edit) — `workflows/execute-product-builder.md` and
    `evals/evaluation-rubric.md` still carry the stale count, still
    deliberately untouched.
  - 1.0.4 — integrated reusable design-judgment knowledge from an external
    21-skill collection under `Downloads/skills` (analyzed, not copied
    wholesale; originals untouched, nothing under `products/` touched, no
    new Product Builder created). See the Version summary above for the full
    list of what changed and why; short form: a Motion and animation section
    in `interaction-design.md` (reconciled against `design-system.md`'s
    fixed 3-token motion scale, kept closed), a wayfinding checklist and a
    zoom/text-scaling rule, a sharpened divergence rule in `ideate.md` and a
    realistic-scale note in `prototype.md`, a new 12th domain pack
    (`product-types/landing-page.md`, explicitly excluding its source's
    fixed visual-token system to avoid overriding `visual-trends.md`), a new
    `ui-engine/craft-critique.md` self-critique checklist (not a new
    blocking gate), and a Protected-Contracts addition to
    `redesign-product.md`. Rule 11 extended in place (still 16 rules) to
    explicitly cover motion; `SKILL.md`'s routing table and domain-count
    references updated to match.
  - 1.0.5 — integrated reusable knowledge from a second external batch
    (`tastemaker-main`'s `docs/`+`research/`, `designer-skills-main`'s
    111-skill collection, `ui-ux-pro-max-skill-main`, `frontend-design-pro-
    demo-main`; analyzed, not copied wholesale, all four sources untouched).
    See the Version summary above for the full list; short form: a 12th
    design-judgment factor and evidence-vs-craft labeling, a 9th flow
    criterion (emotional arc), Optimistic UI and affordance vocabulary in
    `interaction-design.md`, WCAG 2.2 specifics and forced-colors in
    `accessibility.md`, a contrast pairing-contract and data-viz ramps in
    `color-system.md`, dark-mode elevation and a mandatory modal scrim in
    `design-system.md`, a full 5-Gestalt-principle grouping checklist in
    `visual-hierarchy.md`, a 9th craft-critique check plus a sharpened
    structural-variety check, non-Latin typography, a landing-page spacing
    exception, and three new files (`ux-writing.md`, `localization.md`,
    `search-ux.md`) for capabilities that had no home at all. Rejected: a
    competing 0–4 severity scale, and an 11-aesthetic "always commit to one
    style" skill that fails the register fit-condition bar. Still 16 rules,
    12 quality-gate dimensions, 10 phases — no architecture change.
  - 1.0.6 — the Domain Standards Library: a new `product-types/domain-
    standards/` folder (122-entry registry, 11 complete PDFs, 111 reserved
    placeholders) and `product-intelligence/domain-standards.md`, plus a new
    **Rule 17 — Domain Standards** (now 17 rules). A second, finer-grained
    domain-matching system layered onto — not replacing — the existing 12
    `product-types/*.md` packs; matched/loaded by `agents/product-
    architect.md` at the same step it already applies a pack overlay, and
    cited as mandatory input from `ux-architect.md`, `interaction-
    designer.md`, `ui-designer.md`, `design-system-expert.md`,
    `accessibility-expert.md`, and `qa-expert.md`. Reconciled through Rule
    2's existing tier order (tier 6) rather than a second competing
    priority system a source spec had proposed. See the Version summary
    above for the full detail. Still 12 quality-gate dimensions, 10 phases,
    no `products/` content or script touched.
  - 1.0.7 — a new mandatory **Design Setup / Visual Direction** phase
    inserted between Architect and Prototype (11 phases now, nothing
    removed/reordered): reference detection/analysis, a design
    questionnaire, a Reference-Driven/Guideline-Driven/Custom/Default
    classification, a `ui/design-direction.md` artifact, and a user-approval
    gate — new Rule 18 (18 rules), new B13 gate (13 dimensions), a new
    agent (`design-setup-specialist.md`), a new workflow
    (`design-setup.md`), a new `design-reference-engine/` technique library
    (4 files, explicitly cross-referenced from and non-overlapping with
    `brd-analysis.md`'s business-logic extraction), a new `design-samples/`
    default library (12 placeholder folders), and a new template
    (`design-direction.md`). Wired into `ux-architect.md`/`ui-designer.md`/
    `design-system-expert.md` as mandatory input without relocating Rule
    4/5's actual enforcement points. `execute-product-builder.md`'s action
    table grew 24→29; `SKILL.md` renumbered topics 8–18→9–19;
    `evaluation-rubric.md` gained a 19th dimension (205→215 points) and had
    a pre-existing "six vs. seven new-marked rows" miscount corrected while
    open for this change. See the Version summary above for full detail.
    Deliberately not touched: `design-glanza-plugin/`, `products/
    projectflow/`.

## Phase registry
The canonical 11 orchestration phases, in order. Detail lives in
`methodology/design-thinking.md` (relationship map) and `workflows/create-product.md`
(operational sequence) — this is the authoritative list other files point to.

| # | Phase | Core design-thinking phase? |
|---|-------|:---:|
| 1 | Intake | |
| 2 | Empathize | ✓ |
| 3 | Define | ✓ |
| 4 | Ideate | ✓ |
| 5 | Architect | |
| 6 | Design Setup | |
| 7 | Prototype | ✓ |
| 8 | Implement | |
| 9 | Test | ✓ |
| 10 | Audit | |
| 11 | Iterate | |

**Design Setup** (added v1.0.7) sits between Architect and Prototype —
never before Architect (the domain/module shape must exist first) and never
after Prototype has already started (the visual direction must be
established, and where a real user is present, confirmed, before the visual
system and screens are built against it). It is not one of the 5 core
design-thinking phases (it has no Empathize/Define/Ideate/Prototype/Test
counterpart of its own) — same category as Architect/Implement/Audit/Iterate.

## Rule registry
The 18 Operating Rules (full definitions in `config/operating-rules.md`) — listed
here only as an index so any file can cite "Rule N" without restating it:

| # | Rule |
|---|---|
| 1 | Requirement First |
| 2 | Source of Truth |
| 3 | Business Logic |
| 4 | UX Before UI |
| 5 | System Before Screen |
| 6 | States Are Mandatory |
| 7 | Accessibility |
| 8 | Responsive Thinking |
| 9 | Traceability |
| 10 | No Invented Business Rules |
| 11 | Design Trends |
| 12 | Self-Critique |
| 13 | Iteration |
| 14 | Domain-Agnostic Core |
| 15 | Product Isolation |
| 16 | Extensibility |
| 17 | Domain Standards |
| 18 | Design Setup / Visual Direction |

## Quality-gate dimension registry
The 13 measurable quality dimensions (full pass criteria in
`config/quality-gates.md` Section B) — listed here as an index:

| ID | Dimension |
|---|---|
| B1 | Requirement Completeness |
| B2 | Business Logic Completeness |
| B3 | User-Flow Completeness |
| B4 | Information Architecture |
| B5 | Screen Architecture |
| B6 | Design System |
| B7 | State Coverage |
| B8 | Accessibility |
| B9 | Responsive Behavior |
| B10 | Traceability |
| B11 | QA |
| B12 | Implementation Readiness |
| B13 | Design Direction Completeness |

## Role registry
The reasoning personas (full detail in each `agents/*.md` file), mapped to the
phase(s) each owns:

| Agent | Owns phase(s) |
|---|---|
| `agents/brd-analyst.md` | Intake |
| `agents/product-architect.md` | Architect |
| `agents/design-setup-specialist.md` | Design Setup |
| `agents/ux-architect.md` | Prototype (UX) |
| `agents/interaction-designer.md` | Prototype (UX detail) |
| `agents/ui-designer.md` | Prototype (UI) |
| `agents/design-system-expert.md` | Prototype (UI governance) + Audit |
| `agents/accessibility-expert.md` | Prototype + Audit (cross-cutting) |
| `agents/qa-expert.md` | Test, Audit |

**Orchestration authority:** an agent is invoked by the `workflows/*.md` file
governing its assigned phase above; it does not self-invoke, does not expand
its own scope into another agent's phase, and does not independently redesign
work another agent already owns. The master skill (via `workflows/*.md` and
ultimately `SKILL.md`) is what sequences and hands off between specialists —
an agent finding a problem outside its own scope reports it and hands off
(per `methodology/design-thinking.md`'s feedback-routing table), it never
just fixes it in place. Every `agents/*.md` file states this boundary
concretely in its own "Things it must not do" section rather than only here.

## Directory map
See `SKILL.md`'s directory index for the one-line-per-folder summary; this file
does not restate it to avoid two versions drifting apart.

## Domain registry
The recognized `product-types/*.md` overlays: `saas`, `admin-panel`, `erp`, `crm`,
`ecommerce`, `healthcare`, `hrms`, `fintech`, `logistics`, `marketplace`,
`landing-page`. Anything not confidently matched to one of these routes to
`product-types/custom-domain.md` per its no-match/partial-match/graduation
procedure (Rule 16).

**Distinct from the above:** `product-types/domain-standards/domain-
registry.json` is a second, much finer-grained registry (122 named domains
across 12 categories) of externally-sourced UI/UX standard documents,
matched and loaded independently per Rule 17 and `product-intelligence/
domain-standards.md` — it does not replace or extend the 11-pack list above;
the two registries answer different questions and compose (see that file's
relationship table).

## Global toggles
- **Assumption-marking strictness:** strict — every tier-6-or-lower fact (Rule 2)
  must carry an assumption tag; no silent defaults.
- **Phase-completion verbosity:** full — every phase produces the complete report
  shape in `config/output-contract.md`, not an abbreviated version.
- **Auto-advance:** off by default — phases stop for review per Rule 1/12/13
  unless an end-to-end run is explicitly requested.

## Explicitly not here
- The rules themselves → `operating-rules.md`.
- Gate pass criteria themselves → `quality-gates.md`.
- Output formatting rules → `output-contract.md`.
