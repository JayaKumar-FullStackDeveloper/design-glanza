# Template: Screen Architecture

## Purpose
A single screen's structural blueprint — named regions and what job each
does — before any content, copy, or visual treatment exists. The bridge
between the whole-product `sitemap.md` and the fully-detailed
`screen-specification.md`. Reusable across every domain: a region map is a
layout concept, never a business rule.

## Required inputs
- The `sitemap.md` node this screen formalizes.
- `ui-engine/layout-system.md`'s named composition patterns (list+detail,
  dashboard-grid, single-column-form, master-detail, wizard).
- The `FLOW-NNN` step(s) that land on this screen.

## Output structure
- **Header** — per `config/output-contract.md`, with the sitemap node
  reference.
- **Composition pattern** — cited by name from `layout-system.md`, not
  redefined.
- **Region map** — named layout zones (e.g. header, primary content, side
  panel, footer actions).
- **Per-region purpose** — what job each region does, tied to the flow
  step(s) that land here.
- **Primary action** — the one dominant action this screen exists to enable.

## Quality criteria
- Exactly **one** primary action — two "primary-looking" actions on one
  screen is a hierarchy failure caught here, before visual work even starts
  (`ui-engine/visual-hierarchy.md`'s rule, enforced structurally at this
  stage).
- Every region traces to a specific flow step — a region with no
  originating flow step is unexplained scope.
- The composition pattern is named, not invented ad hoc per screen (Rule 5,
  `config/operating-rules.md`: system before screen).
- Checked against `config/quality-gates.md`'s **B5 — Screen Architecture**
  gate.

## Example structure
_Illustrative only — placeholders, not a real screen._

```
Sitemap node: <Sub-section A.1>
Composition pattern: list + detail

Regions:
  header          - product/section identity, primary action slot
  primary content - the list (source: FLOW-003 step 1)
  detail panel    - selected-record detail (source: FLOW-003 step 2)
  footer actions  - secondary actions only (no primary action here)

Primary action: <Create new record> (in header region)
```

## Traceability fields
Owns the `SCREEN-NNN` scheme (registered via
`product-intelligence/traceability.md`). Cites the `sitemap.md` node and
`FLOW-NNN` step(s) it formalizes.

## Explicitly not here
- Full content/copy/interaction detail per element →
  `templates/screen-specification.md`.
- The layout pattern's own definition → `ui-engine/layout-system.md`.
- Hierarchy/emphasis rules that justify the primary-action choice →
  `ui-engine/visual-hierarchy.md`.
