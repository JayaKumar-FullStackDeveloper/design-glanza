# Product Memory & Decision Records

## Responsibility
A persistent, queryable index over decisions the Product Builder has
already made — so a later pass consults what was decided before touching
UI again, and a contradiction is only ever introduced via an explicit,
recorded supersession, never silently. This is the elaboration of Rule 26
(`config/operating-rules.md`) and gate **B21** (`config/quality-gates.md`).

## Read this first: almost none of the 11 requested categories are new
Every prior engine built this session already produces most of what
"Product Memory" was asked to contain. This file's actual job is
**indexing and cross-referencing what already exists**, plus owning the
one genuinely new artifact type — the persisted Architecture/Design
Decision Record (`ADR-NNN`).

| Requested category | Already lives here — cited, never duplicated |
|---|---|
| Product decisions | `product/product-definition.md` (Ideate's Chosen Approach) |
| UX decisions | `ux/user-flows.md`, `sitemap.md`, `navigation.md`, `screen-architecture.md` |
| UI decisions | `ui/design-direction.md`, `ui/ui-rules.md` |
| Design-system decisions | `ui/design-system.md`, `ui/design-tokens.json`, `design-tokens/token-inheritance.md`'s override records |
| Component decisions | `ui/components.md`, `component-registry/*`'s Registry base citations |
| Architecture decisions | `domain/domain-application-notes.md` (module/entity boundaries, dependency graph) |
| Research findings | `research/research-findings.md`, `research/research-summary.md` (`RF-NNN`, already ID-tagged) |
| Audit findings | `qa/qa-report.md`, `ui/visual-gap-analysis.md`, `ui/baselines/*` diff reports |
| Accepted exceptions | `ui-engine/design-system.md`'s "logged system gap" pattern — already reused three times: `design-tokens/token-audit.md`'s Token gap log, `visual-regression/baseline-updates.md`'s Baseline Update record |
| Rejected approaches | `methodology/ideate.md` step 8's existing rejected-approaches register, `design-research/pattern-analysis.md`'s researched-and-rejected register |
| Known constraints | `methodology/define.md` output 5, `product-intelligence/dependency-analysis.md`, Rule 10's assumption-tag `IMPACT` field |

**What's genuinely new:**

| Genuinely new | Already exists — cited, never restated |
|---|---|
| `ADR-NNN` — a persisted, ID-tagged, status-tracked decision record | `methodology/design-thinking.md`'s existing 9-step design decision framework (Problem→Context→...→Validation) — that framework was explicitly *not* a stored artifact before this ("use the phase files directly for doing the actual work"); an ADR is that same chain, finally persisted |
| One unified index (`product-builder/memory/product-memory.md`) pointing at all 11 categories above | The categories' own content, wherever it already lives (table above) |
| The explicit consultation rule (check before generating/modifying UI) | The individual "cite as mandatory input" rules each agent already has for its own domain (design-direction.md, RF-NNN, etc.) — this file generalizes the *pattern*, not the specific citations |
| The explicit supersession protocol (a contradiction is only valid via a new ADR that names what it supersedes) | Every prior system's own "logged, not silent" exception mechanism (table above) |
| `scripts/validate-memory.py` | `scripts/validate-requirements.py` (the sibling-file cross-check pattern this one extends to `ADR-NNN`) |

## File map

| File | Owns |
|---|---|
| `memory-model.md` | What the Product Memory index catalogs, isolation guarantee (Rule 15), what it deliberately does not duplicate |
| `adr-schema.md` | The `ADR-NNN` record shape and status lifecycle, reconciled against `design-thinking.md`'s existing decision framework |
| `consultation-rule.md` | The mandatory "check Product Memory first" step, folded into each agent's existing procedure |
| `contradiction-prevention.md` | The supersession protocol — the one mechanism every prior system's exception pattern now composes under |
| `auto-recording.md` | What counts as a "significant" decision, and which existing phase-completion points already trigger an ADR write |
| `memory-integration.md` | Wiring into the Quality Engine, Component Registry, Design Tokens, and UX Scenario Testing |
| `templates/{product-memory,decision-record}.md` | The index and one ADR's shape |

## Explicitly not here
- Any of the 11 categories' own content-producing technique → wherever
  the table above says it already lives.
- The design decision framework's own steps → `methodology/
  design-thinking.md` (this folder persists it, doesn't redefine it).
- Master↔Product inheritance for tokens/components specifically →
  `design-tokens/token-inheritance.md`, `component-registry/
  registry-integration.md` (this folder's isolation guarantee generalizes
  the same Rule 15 pattern, it doesn't compete with those two).
