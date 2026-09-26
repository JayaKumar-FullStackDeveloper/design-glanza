# Design-Glanza

**Design-Glanza** is a master Claude Code skill that acts as a **Product-Builder Skill Factory and Orchestrator**.

It does not build one product. It builds the *builders*.

```
ONE MASTER SKILL  →  UNLIMITED PRODUCT BUILDERS  →  UNLIMITED DOMAINS
```

## What it does

Design-Glanza takes any product requirement — a BRD, PRD, SOW, user story collection,
acceptance criteria set, existing application, screenshot set, design reference, or a
plain-language product idea — and generates a **product-specific Product Builder Skill**.

That generated Product Builder Skill is then responsible for designing, architecting,
setting up its visual direction, implementing, previewing, testing, auditing, and
iterating on that specific product.

Design-Glanza itself stays domain-agnostic. It is the reasoning engine that produces
domain-specific builders on demand — for SaaS, admin panels, ERP, CRM, e-commerce,
healthcare, dental PMS, HRMS, logistics, fintech, marketplaces, landing pages, education,
internal enterprise tools, consumer apps, or any custom domain — without ever hardcoding
a domain into its own core logic.

## Status

**Fully implemented**, version **1.0.9**. Every folder in the architecture has real,
load-bearing content; one full product (`products/projectflow`) has been generated
through Prototype as a worked example; the skill has been extended repeatedly with
external design knowledge, a Domain Standards Library, a Design Setup phase, a
Preview & Run phase, and a mandatory design-research/visual-benchmark-and-audit
system — see `config/master-config.md`'s changelog inside the skill for the
complete version history.

## The 12-phase lifecycle

```
INTAKE → EMPATHIZE → DEFINE → IDEATE → ARCHITECT → DESIGN SETUP →
PROTOTYPE → IMPLEMENT → PREVIEW & RUN → TEST → AUDIT → ITERATE
```

A continuous loop, not a one-time checklist — Test findings route backward to
whichever earlier phase actually owns the defect, and a phase never auto-advances
without a completion report. Full detail: [`docs/WORKFLOW.md`](docs/WORKFLOW.md).

## Structure

```
Design-Glanza/
├── .claude/
│   ├── CLAUDE.md                         # project-level instructions for Claude Code
│   └── skills/design-glanza/             # the master orchestrator skill (project-local)
│       ├── SKILL.md                      # entry point, 20 numbered topics
│       ├── config/                       # 20 rules, 15 quality gates, output contract
│       ├── methodology/                  # the 5-phase design-thinking loop + design-judgment
│       ├── product-intelligence/         # BRD/requirement analysis + domain classification/standards
│       ├── ux-engine/ · ui-engine/       # UX and UI technique
│       ├── product-types/                # 12 domain packs + the Domain Pack Contract
│       │   └── domain-standards/         # 122-entry external UI/UX standards registry
│       ├── design-reference-engine/      # reference analysis, questionnaire, selection, direction
│       ├── design-samples/               # default visual-direction library, per domain + platform
│       ├── agents/ · workflows/ · templates/ · scripts/ · use-cases/ · evals/
│       └── ...
├── design-glanza-plugin/                 # the same skill, packaged as a distributable Claude Code plugin
├── products/                             # generated, product-specific Product Builder skills land here
├── docs/                                 # architecture, plugin, installation, workflow, design-reference docs
├── DESIGN-GLANZA-ARCHITECTURE-SPEC.html  # full visual architecture specification (open in a browser)
└── README.md                             # this file
```

## Documentation

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — the four-layer architecture, folder structure, governance mechanisms
- [`docs/PLUGIN.md`](docs/PLUGIN.md) — the three ways this skill can be installed and run
- [`docs/INSTALLATION.md`](docs/INSTALLATION.md) — step-by-step install/usage for each of those three ways
- [`docs/WORKFLOW.md`](docs/WORKFLOW.md) — the 12-phase lifecycle and the full action-by-action pipeline
- [`docs/DESIGN-REFERENCE.md`](docs/DESIGN-REFERENCE.md) — the Design Setup phase, reference engine, and default sample library
- [`DESIGN-GLANZA-ARCHITECTURE-SPEC.html`](DESIGN-GLANZA-ARCHITECTURE-SPEC.html) — a complete, diagram-illustrated technical specification

## Core principles

Five design-thinking principles stay central to every generated Product Builder:

- Empathize
- Define
- Ideate
- Prototype
- Test

Seven production-readiness phases wrap around them:

- Intake
- Architect
- Design Setup
- Implement
- Preview & Run
- Audit
- Iterate

## Ground rules

- Design-Glanza must not invent business rules absent from the source material —
  assumptions are marked explicitly, never silently assumed.
- Design-Glanza must not jump straight to UI generation. Understanding and analysis
  come first, and — since v1.0.7 — a deliberate Design Setup pass, now opening with
  its own design-research step (v1.0.9), establishes the visual/interaction
  direction before any screen is drawn.
- Implementation is not complete because the code was written — since v1.0.8, the
  built output must actually launch and be previewed locally before Test evaluates it.
- A generated screen is a draft, not a final answer — since v1.0.9, every screen
  goes through a mandatory audit against an 11-category UI Audit Framework and a
  three-way Reference/Direction/Generated-UI benchmark, with at least one
  refinement cycle recorded even when nothing was wrong.
- The core reasoning engine must remain domain-agnostic; new domains are added by
  authoring a new domain pack or generating new Product Builder skills under
  `products/`, never by modifying Design-Glanza's core logic.

## License

MIT — see [`LICENSE`](LICENSE).
