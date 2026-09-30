# Template: Product Memory

## Purpose
The unified index over all 11 decision categories `product-memory/
README.md` maps — one row per decision-bearing artifact, never a
duplicate of the artifact's own content, per `product-memory/
memory-model.md`.

## Required inputs
- Every artifact `README.md`'s table names as already holding a decision
  category (`product/product-definition.md`, `ux/*.md`, `ui/*.md`,
  `domain/domain-application-notes.md`, `research/research-findings.md`,
  `qa/qa-report.md`, `design-tokens/token-inheritance.md`'s override
  records, `component-registry/*`'s Registry base citations,
  `visual-regression/baseline-updates.md`'s records).
- `product-builder/memory/decision-records.md`'s `ADR-NNN` entries.

## Output structure
- **Header** — per `config/output-contract.md`.
- **Index table** — per `memory-model.md`'s shape: Category, Summary
  (one line), Full record (real path/anchor), Status
  (active/superseded/deferred).
- **ADR cross-reference** — every `ADR-NNN` id, its one-line Decision,
  and its Status, so a scan of this file alone surfaces every persisted
  decision without opening `decision-records.md`.
- **Known constraints** — a rolled-up list citing `methodology/
  define.md` output 5 and `product-intelligence/dependency-analysis.md`,
  not re-derived here.

## Quality criteria
- Every row's Full record is a real, existing path — a row pointing at
  nothing is itself a **B21** finding.
- Every `superseded` row names the `ADR-NNN` that superseded it.
- Checked against `config/quality-gates.md`'s **B21 (Product Memory
  Integrity)** gate.

## Example structure
_Illustrative, domain-neutral — not real product content._

```
Index:
| Category | Summary | Full record | Status |
|---|---|---|---|
| UI decision | Dense Enterprise register | ui/design-direction.md | active |
| Component decision | Table = registry `table`, selectable variant | ui/components.md#COMPONENT-004 | active |
| Architecture decision | Billing split from Invoicing | domain/domain-application-notes.md | active |

ADR cross-reference:
| ADR | Decision | Status |
|---|---|---|
| ADR-004 | Rejected optimistic-UI for payment submission | active |
| ADR-007 | Modal (not Drawer) for one-off delete confirmation | active |
| ADR-011 | Superseded ADR-003's inline-edit choice for the audit-log table (read-only, no edit needed) | active (supersedes ADR-003) |

Known constraints: payment provider requires synchronous confirmation
(dependency-analysis.md, DEP-006); no offline support required per BRD.
```

## Traceability fields
Cross-references every ID scheme already in play (`REQ`, `FLOW`,
`SCREEN`, `COMPONENT`, `RF`, `SCENARIO`, `ADR`) without owning any of
them itself.

## Explicitly not here
- The ADR record's own full shape → `templates/decision-record.md`.
- The index's own model/rules → `product-memory/memory-model.md`.
