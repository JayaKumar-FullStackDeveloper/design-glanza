# Memory Model

## Responsibility
What the Product Memory index (`product-builder/memory/product-memory.md`)
actually catalogs, how it stays a thin cross-reference layer rather than a
second copy of content that already exists, and the isolation guarantee
every entry inherits.

## The index, not the content
One row per decision-bearing artifact, across all 11 requested categories
(`README.md`'s table), each row stating: **what** was decided (one line),
**where** the full content lives (a real file path, never re-typed),
**when** (pass/date), and **status** (active / superseded / deferred).
The index is what a later agent scans in seconds before starting work — it
is never the thing an agent reads *instead of* the actual artifact when
real detail is needed.

```
| Category | Summary | Full record | Status |
|---|---|---|---|
| UI decision | Dense Enterprise register, sidebar nav | ui/design-direction.md | active |
| Component decision | Table uses component-registry's `table` entry, selectable variant | ui/components.md#COMPONENT-004 | active |
| Architecture decision | Billing module split from Invoicing per user mental model | domain/domain-application-notes.md | active |
| ADR | Rejected optimistic-UI for payment submission (high-risk, irreversible) | memory/decision-records.md#ADR-004 | active |
```

## Isolation (Rule 15, generalized)
Every Product Memory index and every `ADR-NNN` record lives entirely
inside `products/<slug>/product-builder/memory/` — nothing here is ever
written back into the master engine (`config/`, `methodology/`,
`product-intelligence/`, `ux-engine/`, `ui-engine/`, `design-research/`,
`ux-scenario-testing/`, `design-tokens/`, `component-registry/`,
`visual-regression/`), and nothing here is ever read by, or leaked into,
a *different* product's own memory. This is the same guarantee
`design-tokens/token-inheritance.md` and `component-registry/
registry-integration.md` already state for their own artifact types,
generalized here to cover every decision category at once — Product
Memory is where Rule 15's isolation guarantee is stated once, comprehensively,
for the whole Product Builder, rather than once per subsystem.

**The inheritance direction stays one-way**, exactly as those two files
already established:
```
MASTER ENGINE (config/, methodology/, ui-engine/, design-tokens/, etc.)
  ──inherited by──▶  PRODUCT MEMORY (product-builder/memory/*)
```
A recurring pattern observed across *multiple products'* memory graduates
into the master engine deliberately (a new `product-types/*.md` pack, a
new `design-tokens/` category, a new `component-registry/` entry) — the
same graduation discipline every prior system in this engine already
uses, never a silent, one-off promotion.

## What the index deliberately does not do
- It does not re-derive or re-summarize a decision's actual reasoning —
  that's the linked artifact's job (or the ADR's, for a decision with no
  more specific home).
- It is not a chronological log/diary — it's a current-state index; a
  superseded entry's row is marked `superseded`, pointing to the ADR that
  superseded it, not deleted (Rule 13, iteration: a fix is revalidated,
  not erased from the record).
- It does not gate anything by itself — `config/quality-gates.md`'s
  **B21** is what actually checks it's complete and internally consistent.

## Explicitly not here
- The ADR record shape itself → `adr-schema.md`.
- When the index (or an ADR) actually gets written → `auto-recording.md`.
- How a later pass is required to consult it → `consultation-rule.md`.
