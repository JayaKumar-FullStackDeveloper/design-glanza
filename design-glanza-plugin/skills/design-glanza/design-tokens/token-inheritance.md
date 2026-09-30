# Token Inheritance

## Responsibility
The exact override/extension contract between the **Master Token Set**
(the domain-agnostic scales in `ui-engine/*`, Rule 14) and one product's
**Product Token Set** (`product-builder/ui/design-tokens.json`, Rule 15) —
operationalizing Product Isolation and Extensibility for this specific
artifact, not restating either rule.

## Two layers, one direction of flow
```
MASTER TOKEN SET (ui-engine/*)  ──inherited by──▶  PRODUCT TOKEN SET (product-builder/ui/design-tokens.json)
```
A product's token file is generated **from** the master scales
(`scripts/create-product-builder.py`, per `design-tokens.schema.json`'s
`$inherits` field naming the master skill version it was generated
against — the same field `product.json`'s `master_skill_version` already
tracks for the product as a whole). Nothing ever flows the other
direction: a product-specific value discovered while building one product
never gets written back into `ui-engine/*` as a special case — that's
Rule 15's existing prohibition, applied here to token values specifically
the same way it already applies to requirements/flows/rules.

## What a product may override
| Layer | May a product override it? | Why |
|---|---|---|
| `color.primary.*`, `color.secondary.*` (the brand ramps) | **Yes** — this is the one thing that must differ per product | Every product has its own brand; the *ramp-construction technique* stays fixed, only the seed hue changes |
| `color.semantic.*`'s foreground/background/border **values** | **Yes**, within the fixed triplet *structure* | The structure (triplet, contrast rule, color-blind safety) is closed; the specific hex values derived from the product's own primary/neutral ramps are product-specific by construction |
| `radius.*`, `elevation.*`, `motion.*`, `border.width.*`, `sizing.*`, `zIndex.*` | **No** — closed scales | `design-system.md` explicitly calls these "closed" (radius/elevation/motion) precisely so a product can't quietly invent a 4th motion duration or a 6th radius step; sizing/border-width/z-index join them for the same reason |
| `typography.size.*`/`weight.*`/`lineHeight.*` (the type scale) | **No** — closed scale | Same closed-scale rule, `typography.md` |
| `spacing.*`, `grid.*`, `breakpoint.*` | **No** — closed scales | Same closed-scale rule, `layout-system.md`/`responsive-system.md` |
| A domain-specific addition (e.g. a data-visualization ramp variant `product-types/erp.md` calls for) | **Yes, as an addition, never a replacement** | Lives under a `product.*` namespace (below), not inside the master categories |

The pattern: **seed values within a fixed structure are product-specific;
the structure and the closed scales are not.** This is the same
distinction `design-reference-engine/design-direction.md`'s "binding vs.
soft preference" already draws for the design-direction document, applied
here to the token file specifically.

## The `product.*` namespace
A domain-specific token that has no home in the 14 master categories
(e.g. a healthcare product's patient-status color that isn't one of the
5 core semantics) is added under its own `product.*` top-level key in
`design-tokens.json`, never merged into `color.semantic.*` as a 6th
"core" semantic — this keeps the master schema's own required categories
stable across every product while still letting a product extend it, the
same relationship `product-types/*.md` packs already have to the
domain-agnostic core (Rule 16). A recurring `product.*` addition observed
across multiple products graduates into a proposed master-schema change
the same way a recurring domain pattern graduates into a
`product-types/*.md` pack — reviewed and added upstream deliberately, not
silently promoted.

## Recording a significant override
A product's first departure from a master default (a brand seed hue, a
`product.*` addition) is itself an architecture-level decision — per
`product-memory/auto-recording.md`'s significance threshold, it gets a
persisted `ADR-NNN` the first time, so a later screen's pass finds the
existing decision in `product-builder/memory/product-memory.md` instead
of re-litigating why the override exists.

## Confirming inheritance, not drift
`scripts/validate-tokens.py` (`token-audit.md`) checks that every path in
a product's `design-tokens.json` is either (a) one of the master schema's
required paths with a product-specific *value*, (b) a `product.*`
addition, or (c) absent (falls back to the master default) — a path that
looks like a master category name but isn't ("radius-xl" alongside the
real `radius.*` set) is flagged as an unauthorized scale extension, not
silently accepted as a product preference.

## Explicitly not here
- Rule 15/16 themselves → `config/operating-rules.md`.
- The actual master scale values → `ui-engine/*` (per `token-schema.md`'s
  table).
- The violation-detection mechanics → `token-audit.md`.
- The `$inherits`/versioning field's exact shape → `design-tokens.schema.json`.
