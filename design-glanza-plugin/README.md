# Design-Glanza (Plugin)

A distributable Claude Code plugin packaging of **Design-Glanza** — the master
product-design and Product Builder factory. Given a product requirement, BRD/
PRD/SOW, user stories, acceptance criteria, an existing product, or a
plain-language idea, it generates a product-specific **Product Builder** skill
that designs, architects, builds, tests, audits, and iterates that product —
across SaaS, ERP, CRM, e-commerce, healthcare, HRMS, fintech, logistics,
marketplace, landing pages, and arbitrary/custom domains.

## What this is (and isn't)

This plugin provides exactly one thing: the **master orchestrator skill**
(`skills/design-glanza/`). It never contains product-specific work — a
generated Product Builder always lives in the *host project* you're working
in (`products/<slug>/product-builder/`), never inside this plugin. See
`skills/design-glanza/SKILL.md`'s Mission section for the full
Design-Glanza-vs-Product-Builder distinction, and its "Governing principles"
section for Product Isolation and Domain Extensibility.

## Structure

```
design-glanza-plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── design-glanza/
│       ├── SKILL.md              # the master orchestrator (19 numbered sections)
│       ├── config/                # rules (18), quality gates (13), output contract
│       ├── methodology/           # Empathize->Define->Ideate->Prototype->Test loop + design-judgment
│       ├── product-intelligence/  # BRD/requirement analysis + domain classification/standards
│       ├── ux-engine/             # flows, IA, navigation, interaction, states, search, i18n, ux-writing
│       ├── ui-engine/             # design tokens, layout, components, craft-critique
│       ├── product-types/         # 12 domain packs + the Domain Pack Contract
│       │   └── domain-standards/  # 122-entry external UI/UX standards registry
│       ├── design-reference-engine/ # reference analysis, questionnaire, selection, direction (Design Setup phase)
│       ├── design-samples/        # default visual-direction library, per domain + platform
│       ├── workflows/             # operational, agent-by-agent procedures (incl. design-setup.md)
│       ├── templates/             # output-contract shapes for every artifact
│       ├── agents/                # 9 specialist reasoning roles
│       ├── scripts/                # deterministic scaffolding + validation tooling
│       ├── use-cases/             # 8 validated worked examples
│       └── evals/                 # test scenarios, rubric, benchmark matrix
└── README.md
```

## Invocation

This is a **POC-phase, explicit-invocation-only** skill
(`disable-model-invocation: true` in `SKILL.md`'s frontmatter) — Claude never
auto-loads it from a passing mention of UI, UX, SaaS, or design.

Once this plugin is loaded, invoke it as:

```
/design-glanza:design-glanza
```

(the `<plugin-name>:<skill-name>` form — both happen to be named
`design-glanza` here.)

## Local install / test (no marketplace)

Load the plugin for a single session directly from this folder — no
marketplace, no `marketplace.json`, no install step required:

```bash
claude --plugin-dir ./design-glanza-plugin
```

Validate the manifest first, if you want a standalone check:

```bash
claude plugin validate ./design-glanza-plugin
```

While iterating, `/reload-plugins` inside a running session picks up on-disk
edits without a restart.

## Requirements this plugin satisfies

- Callable from Claude Code as a plugin skill, not a project-local one.
- Remains a **master orchestrator** — it generates Product Builders, it is
  never itself a product-specific builder.
- Supports the full 11-phase lifecycle end to end: BRD/PRD/SOW/user-story/
  acceptance-criteria analysis, product classification, domain detection
  (both the 12 `product-types/*.md` packs and the 122-entry Domain Standards
  Library), Design Setup (visual/interaction direction, established and
  approved before any screen exists), UX architecture, UI architecture,
  design-system generation, Product Builder generation, Product Builder
  validation, implementation, testing, auditing, and iteration — see
  `skills/design-glanza/SKILL.md`'s 19 numbered sections for exactly where
  each lives.
- Product-specific work stays isolated from the plugin: nothing under
  `skills/design-glanza/` is product-specific, and nothing here writes
  outside the host project's own `products/` directory.
- Domain-agnostic and extensible: a new domain is a new
  `product-types/<domain>.md` pack, never a change to this plugin's core.

## Not done yet

Not published to any marketplace — this is a local, filesystem-path plugin
for testing only, per the current phase of work.
