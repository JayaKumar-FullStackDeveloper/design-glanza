# Use Case: Admin Panel (Greenfield)

## Responsibility
A validated, concrete worked example of Design-Glanza building a greenfield
internal admin/back-office tool, applying the `product-types/admin-panel.md`
overlay.

## Routes through Design-Glanza — not a separate skill
Executed by the same master skill as every other use case here — only the
applied `product-types/*.md` pack and the specific emphases below differ.

## Input
Usually framed around an already-existing customer-facing product: "we need
an internal tool for support staff to view and edit `<records>`." The
customer-facing product itself may or may not already be a Design-Glanza
product.

## Classification
Strong signals almost immediately: "internal," "support agent," "bulk,"
"audit log" → confident match to `product-types/admin-panel.md`.

## Analysis
`brd-analysis.md`'s "business logic is never optional" rule gets exercised
hard here — a request phrased as simply "let staff view/edit `<record>`"
implies a full permission model, an audit trail, and a body of validation
rules that must be extracted explicitly, not left implicit because the
request sounded simple. `edge-case-engine.md`'s concurrency category (two
staff editing the same record) gets full attention from the start.

## Required artifacts
`requirements/user-roles.md`'s permission matrix is built fail-closed from
the first draft (deny by default), per `admin-panel.md`. `requirements/
dependency-analysis.md` typically carries a `DEP-NNN` on the primary
product's own data model — this panel depends on something that already
exists.

## Design-thinking phases
- **Empathize** centers on operational efficiency for trained staff, not
  delight or first-time-user guidance — a materially different Empathize
  emphasis than `new-saas.md`.
- **Ideate** weights the efficiency criterion heavily given how frequently
  this tool is used all day; bulk-action-capable, keyboard-driven
  interaction models are favored over guided/wizard patterns.
- **Prototype** builds the search → filter → bulk-act flow first, since
  that's the dominant workflow shape in this domain, not a single-record
  flow.

## Product Builder generation
`scripts/create-product-builder.py generate`, `product_type: admin-panel`,
`sub_domain` often noting which product this panel is a companion to.

## Implementation
Build order puts the permission model (fail-closed) ahead of any bulk-action
feature — a bulk action shipped before permissions are enforced is exactly
the ordering mistake Rule 5 exists to prevent here.

## QA
Audit specifically checks destructive bulk-action confirmation depth (never
"just a click away") and traceability-chain integrity — `admin-panel.md`
flags a specific naming-collision risk: Design-Glanza's own internal
traceability chain versus the *product's own* audit-log feature being built.
The QA report calls out which is which explicitly.

## Completion criteria
Standard nine-dimension coverage, plus: dense tables still meet the same
contrast and touch-target minimums as any other screen — density is never
an excuse to fall below the accessibility baseline (`admin-panel.md`'s named
accessibility consideration).

## How this differs from other use cases
Unlike `new-saas.md`, Empathize does very little inferential work here
(the audience and their goals are usually explicit and narrow); the harder
work is in extracting the *implicit* business logic behind a
deceptively-simple-sounding request.

## Explicitly not here
- The admin-panel domain reference data itself → `product-types/admin-panel.md`.
- The generic pipeline being demonstrated → `workflows/create-product.md`.
