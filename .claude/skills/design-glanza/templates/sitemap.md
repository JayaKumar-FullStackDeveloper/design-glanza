# Template: Sitemap

## Purpose
The product's information hierarchy made explicit — every screen/section
node, its depth, and who can see it. Reusable across every domain: it holds
structure only, never domain-specific section names as a requirement (a
product's actual sections come from its own requirements, not from this
template).

## Required inputs
- `ux-engine/information-architecture.md`'s grouping/depth technique.
- The `FLOW-NNN` set (`templates/user-flow.md`) — nodes exist because a flow
  needs them, not by invention.
- `product-intelligence/user-roles.md`'s permission matrix.

## Output structure
- **Header** — per `config/output-contract.md`.
- **Hierarchy tree** — sections/pages nested to the depth
  `information-architecture.md`'s depth rule justifies.
- **Per-node role visibility** — which `ROLE-NNN`(s) can see this node.
- **Per-node source flows** — which `FLOW-NNN`(s) land on this node.
- **Navigation pattern reference** — cross-reference to
  `ux-engine/navigation-system.md`'s chosen pattern for this hierarchy (cited
  by name, not redefined here).

## Quality criteria
- No orphan nodes — every node is reachable from at least one flow or
  navigation path (`product-intelligence/traceability.md`'s orphan-artifact
  check applied to IA nodes specifically).
- Depth beyond 3 levels carries a stated justification
  (`information-architecture.md`'s depth rule), not silent accumulation.
- Every node states its role visibility explicitly — a node with unstated
  visibility is treated as visible to nobody until specified, per
  `information-architecture.md`'s permission-aware-structure rule.
- Checked against `config/quality-gates.md`'s **B4 — Information
  Architecture** gate.

## Example structure
_Illustrative only — placeholders, not a real IA._

```
<Top section A>                    [visible: ROLE-001, ROLE-002]
  <Sub-section A.1>                [visible: ROLE-001, ROLE-002]  <- FLOW-003
  <Sub-section A.2>                [visible: ROLE-001]            <- FLOW-004
<Top section B>                    [visible: ROLE-001]
  <Sub-section B.1>                [visible: ROLE-001]            <- FLOW-005

Navigation pattern: sidebar (per ux-engine/navigation-system.md item 2's rule)
```

## Traceability fields
Nodes are provisionally named here and formalized into `SCREEN-NNN` once
`templates/screen-architecture.md` produces the region map for each — this
file is upstream of that ID assignment, not a replacement for it.

## Explicitly not here
- Grouping/taxonomy technique → `ux-engine/information-architecture.md`.
- Nav pattern selection logic → `ux-engine/navigation-system.md`.
- Per-screen layout/content detail → `templates/screen-architecture.md`.
