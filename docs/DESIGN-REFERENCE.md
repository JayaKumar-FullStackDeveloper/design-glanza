# Design Reference & Sample Documentation

Covers the **Design Setup** phase's supporting library — `design-reference-engine/`
(the technique) and `design-samples/` (the default fallback content) — both
under `.claude/skills/design-glanza/`.

## Why this exists

Before any UI is generated, Design-Glanza must not assume a visual style
when the user has provided real design input, and must not fabricate one
when they haven't. `design-reference-engine/` is the technique that
resolves this; `design-samples/` is what it falls back to as a last resort.

## `design-reference-engine/` — the technique

| File | Responsibility |
|---|---|
| `design-research.md` | **Step 0, runs first (added v1.0.9).** Researches current product-design patterns relevant to this specific product before any reference is even looked at — modern SaaS/admin conventions, this product's own domain conventions, information density, navigation/dataviz/form/table/interaction/accessibility/responsive patterns, and current visual trends — checked against `ui-engine/visual-trends.md`'s adoption gate so a "current" pattern is never adopted just because it's fashionable. Folds into the direction below; produces no separate artifact. |
| `reference-analysis.md` | Extracts **design direction** (visual patterns, layout structure/grid, typography, color, visual hierarchy, border treatment, radius, shadows/elevation, iconography, navigation, tabs, tables, filters, forms, cards, status indicators, spacing/density, responsive behavior) from up to 13 recognized reference forms (screenshots, Figma, brand guidelines, existing UI, etc.) — explicitly never business requirements, which is `product-intelligence/brd-analysis.md`'s job on the same input. |
| `design-questionnaire.md` | The structured, 9-category question set (visual style, layout, typography, color, components, interaction, responsive, accessibility, brand/guidelines) — asked directly, or answered by inference where a reference already covers it. |
| `reference-selection.md` | Classifies the result into one of four modes: **Reference-Driven**, **Guideline-Driven**, **Custom Design**, or **Default Design-Glanza** — the last only when no real direction exists from the other three, and never the same default register regardless of domain (Admin Panel ≠ E-commerce ≠ Healthcare ≠ ERP ≠ Fintech ≠ CRM). |
| `design-direction.md` | The authoring/approval technique: synthesize everything above into `product-builder/ui/design-direction.md`, then gate on user approval before Prototype's UI pass begins. |

## `design-samples/` — the default fallback library

Used only for **Default Design-Glanza** mode. One folder per named product
type, matched by `product-types/<domain>.md`'s slug where one exists, plus
two platform folders and one shared folder:

```
design-samples/
├── saas/  admin-panel/  erp/  crm/  ecommerce/  healthcare/
├── hrms/  fintech/  logistics/  marketplace/      (10 domain folders)
├── mobile/  responsive-web/                        (2 platform folders)
└── common/                                          (domain-agnostic patterns)
```

`common/` is always consulted **alongside** whichever domain/platform
folder applies — never instead of one, since most UI patterns (buttons,
tables, cards, modals) genuinely don't vary by domain.

### Current population status

Several folders (`fintech`, `healthcare`, `hrms`, `crm`, `logistics`,
`ecommerce`, `common`) contain curated reference images with a per-file
description in that folder's own `README.md`. The rest currently hold only
a placeholder `README.md` — this is a disclosed, non-blocking gap: a
placeholder folder is still used as a **named starting register**
(mapped to `ui-engine/visual-trends.md`'s Modern SaaS / Dense Enterprise /
Consumer Playful registers) rather than leaving Default mode with nothing
to select.

### Attribution note on the sample images

The curated reference images under `design-samples/*/` (and the sample
`standard.pdf` files under `product-types/domain-standards/01-core-business/`)
are **unattributed, third-party design-inspiration assets** — screenshots
collected from general design-reference sources, not originals authored for
this project. They are included here as visual/structural reference
material only (the same way a mood board or a competitor screenshot is used
in any design process), not as licensed, redistributable assets in their
own right. The MIT license in this repository's [`LICENSE`](../LICENSE)
file covers Design-Glanza's own original methodology and code — it does not
purport to grant rights to these third-party images.

## Closing the loop — checking the generated screen against this direction

Establishing a direction here is only half the discipline (added v1.0.9):
once a screen is actually generated, `ui-engine/ui-audit-framework.md` (an
11-category A–K audit) and `ui-engine/visual-benchmark.md` (a three-way
Reference/Design-Direction/Generated-UI comparison) check it back against
whatever was decided in this phase, and require at least one
audit-and-refinement cycle — recorded in `templates/visual-gap-analysis.md`
— before a screen is treated as final, even when nothing was wrong on the
first pass. See `docs/WORKFLOW.md`'s quality-gates section for **B15**.

## Extending either library

- **A new domain-standard entry**: add one JSON object to
  `product-types/domain-standards/domain-registry.json` plus a folder with
  either a real `standard.pdf` or a placeholder `README.md` — zero code
  changes.
- **A new default sample folder**: add a folder under `design-samples/`
  and a one-line mention in `reference-selection.md`'s selection list —
  also zero core-file changes, per the same extensibility principle that
  governs adding a new `product-types/*.md` pack.
