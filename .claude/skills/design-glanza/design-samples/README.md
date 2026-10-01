# Design Samples

The **Default Design-Glanza** fallback library —
`design-reference-engine/reference-selection.md`'s mode 4, used only when a
product has no user-supplied references, guidelines, or meaningful
questionnaire answers (modes 1–3 all take priority over this one).

## Folder model
One folder per named product type, matched by
`product-types/<domain>.md`'s slug where one exists, plus two platform
folders and one shared folder:

`saas/` · `admin-panel/` · `erp/` · `crm/` · `ecommerce/` · `healthcare/` ·
`hrms/` · `fintech/` · `logistics/` · `marketplace/` — domain samples.

`mobile/` · `responsive-web/` — **platform** samples, not domain samples —
they apply by platform (a mobile-first or explicitly responsive-web
product) independently of which domain sample also applies, per
`reference-selection.md`'s platform-vs-domain independence note.

`common/` — domain-agnostic patterns (general components, layout,
interaction) — always consulted **alongside** whichever domain/platform
folder is selected, never instead of one. See `common/README.md`.

## Current status
8 of 13 folders now hold real curated reference assets — `fintech`,
`healthcare`, `hrms`, `crm`, `logistics`, `ecommerce`, `common`, and `saas`
— see each folder's own README for exactly what was added, its source, and
its confidence. The remaining folders (`admin-panel`, `erp`, `marketplace`,
`mobile`, `responsive-web`) still hold a placeholder `README.md` only. This
is not an error and does not block a product from proceeding:
`reference-selection.md` uses a placeholder folder as a **named starting
register** (`ui-engine/visual-trends.md`'s Modern SaaS / Dense Enterprise /
Consumer Playful registers, matched per folder — see each folder's own
README for which register it maps to) rather than leaving Default mode
with nothing to select at all.

## Extending this library
Populating a folder means adding real curated reference assets (images,
token files, or a written style brief) under that folder and updating its
`README.md` to describe what was added and its confidence/provenance —
exactly the same "complete" vs. "pending" distinction
`product-types/domain-standards/domain-registry.json` already uses, kept
lightweight here (no JSON registry needed) since selection is a direct
slug match, not a scored classification. Adding a 13th sample folder (a new
domain or platform) requires no core-file change — only a new folder plus
a one-line mention in `reference-selection.md`'s selection list.

## Explicitly not here
- The selection logic that picks a folder → `design-reference-engine/
  reference-selection.md`.
- The register a selected sample actually renders in → `ui-engine/
  visual-trends.md`.
- Product-specific design decisions → `product-builder/ui/
  design-direction.md`, generated per product.
