# Architecture

## Four layers

Design-Glanza is organized as four layers, each with a distinct authority and lifespan:

| Layer | Location | Lifespan | Contains |
|---|---|---|---|
| **1. Master Skill** | `.claude/skills/design-glanza/` | Permanent, versioned (currently **1.0.9**) | The domain-agnostic reasoning engine: rules, gates, methodology, UX/UI technique, agents, workflows, templates, scripts, evals |
| **2. Domain Overlays** | `product-types/*.md` + `product-types/domain-standards/` | Permanent, extended over time | 12 authored domain packs (Domain Pack Contract) *and* a 122-entry externally-sourced UI/UX standards registry — two independent, composable domain-matching systems |
| **3. Portable Plugin** | `design-glanza-plugin/` | Synced snapshot | A Claude Code plugin-packaged mirror of the master skill, for distribution outside this one project |
| **4. Generated Product Builders** | `products/<slug>/` | One per real product, grows over that product's life | Product-specific requirements, UX, UI, QA artifacts — references the master engine by relative path, never copies it |

## The central architectural invariant

A generated Product Builder's own `SKILL.md` literally states: *"Contains
product-specific knowledge only; references the master skill... for all
reusable methodology."* Every technique file is cited by relative link,
never duplicated.

## Governance mechanisms

| Mechanism | Enforces |
|---|---|
| 20 Operating Rules (`config/operating-rules.md`) | The constitution — every phase/agent/domain is bound by the same rules |
| 12 phase-transition gates + 15 measurable gates B1–B15 (`config/quality-gates.md`) | Binary pass/fail checkpoints between phases |
| 21-dimension weighted Evaluation Rubric (`evals/evaluation-rubric.md`) | Graded quality, weighted so visual polish alone cannot mathematically pass (capped under 5% of the 235-point total) |
| Deterministic validator scripts (`scripts/validate-*.py`) | Structural checks only — never fabricate a subjective/reasoning-based verdict |
| Agent "must not do" boundaries (`agents/*.md`) | No specialist can redesign another's scope; problems are routed, not silently fixed in place |

## Folder-by-folder

```
.claude/skills/design-glanza/
├── SKILL.md                       orchestrator: frontmatter + 20 numbered topics
├── config/
│   ├── master-config.md           registries: version, phases, rules, gates, roles, domains
│   ├── operating-rules.md         20 numbered constitutional rules
│   ├── quality-gates.md           12 phase-transition gates + 15 measurable B1–B15
│   └── output-contract.md         assumption-tag format, severity vocabulary, report shapes
├── methodology/
│   ├── design-thinking.md         the 5-phase loop engine + feedback-routing table
│   ├── empathize.md define.md ideate.md prototype.md test.md
│   └── design-judgment.md         9-step / 12-factor applied decision engine
├── product-intelligence/
│   ├── brd-analysis.md            20-point extraction checklist, input-type postures
│   ├── requirement-engine.md · business-logic.md · user-roles.md
│   ├── dependency-analysis.md · edge-case-engine.md
│   ├── domain-classifier.md       matches the 12 product-types/*.md packs
│   ├── domain-standards.md        matches the 122-entry domain-standards registry
│   └── traceability.md            REQ→USER→FLOW→SCREEN→COMPONENT→TEST chain
├── ux-engine/                     flows, IA, navigation, interaction, states, search, i18n, ux-writing
├── ui-engine/                     design tokens, layout, components, craft-critique, UI audit framework, visual benchmark, UI design principles
├── product-types/                 12 domain packs + the Domain Pack Contract
│   └── domain-standards/          122-entry external UI/UX standards registry
├── design-reference-engine/       design research, reference analysis, questionnaire, selection, direction
├── design-samples/                default visual-direction library, per domain + platform
├── agents/                        9 specialist reasoning roles
├── workflows/                     10 operational procedures (one per phase cluster)
├── templates/                     14 fill-in-the-blank artifact shapes
├── scripts/                       7 Python files, stdlib-only, no pip deps
├── use-cases/                     8 worked scenarios
└── evals/                         10 benchmark scenarios, 21-dimension rubric, benchmark matrix
```

## Internal dependency direction (strictly one-way, no cycles)

```
config/ → methodology/ → product-intelligence/ → ux-engine/ + ui-engine/
        → product-types/ → agents/ → workflows/ → templates/ + scripts/ + evals/
```

## External dependencies

- Claude Code's skill mechanism (`SKILL.md` frontmatter, `disable-model-invocation: true`)
- Python 3.x, standard library only — no pip packages
- Claude Code's plugin mechanism (`.claude-plugin/plugin.json`) for the portable/global copies

See [`../DESIGN-GLANZA-ARCHITECTURE-SPEC.html`](../DESIGN-GLANZA-ARCHITECTURE-SPEC.html)
for a fully diagrammed version of this document, including data-flow and
decision-routing diagrams.
