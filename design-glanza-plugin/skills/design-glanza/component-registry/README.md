# Component Intelligence Registry

## Responsibility
A **pre-populated, master-level library** of ~29 common production-grade
components and composition patterns — so a Product Builder starts from
professional, evidence-based guidance instead of reasoning every Button,
Table, or Form from a blank page. This is the elaboration of Rule 24
(`config/operating-rules.md`) and gate **B19**
(`config/quality-gates.md`).

## What is genuinely new here, and what is not
`ui-engine/component-system.md` already defines the **framework** — the
8-point analysis every component must satisfy, the atomic-to-composite
taxonomy, iconography, data-viz, and motion-at-the-component-level rules.
This registry does not replace that framework or restate its 8 points; it
supplies **pre-filled instances** of it for the components almost every
product needs, plus the 5 fields the framework doesn't ask for because
they're master-level knowledge, not per-product decisions:

| Genuinely new | Already exists — cited, never restated |
|---|---|
| Pre-populated entries for ~29 named components, each professionally reasoned once at the master level | The 8-point framework itself, atomic-to-composite taxonomy, iconography/data-viz/motion rules → `ui-engine/component-system.md` |
| **When to use / when NOT to use** each component | — |
| **Common UX mistakes** per component (a named anti-pattern catalog at the component-usage grain) | The *visual*-composition anti-cliché catalog → `ui-engine/craft-critique.md` (a different grain — that file catches a generic-looking finished screen; this registry catches choosing the wrong component for the job in the first place) |
| **Composition patterns** — how components combine into organisms (Data Table, Form) | Page-*level* composition (List+detail, Dashboard grid, …) → `ui-engine/layout-system.md` (a different grain — that file composes whole screens from regions; this file composes one organism from atoms/molecules) |
| The Master Component Registry ↔ Product Component Inventory relationship (mirrors `design-tokens/token-inheritance.md`'s model, applied to components) | Rule 15 (Product Isolation) and Rule 16 (Extensibility) themselves |

Interaction behavior, states, accessibility, responsive behavior, and
content rules are **cited from their existing owning file** in every
entry below, never re-derived — `ux-engine/interaction-design.md`,
`state-design.md`, `accessibility.md`, `ui-engine/responsive-system.md`,
`component-system.md` point 6.

## File map

| File | Owns |
|---|---|
| `registry-schema.md` | The 13-field entry shape, mapped onto `component-system.md`'s 8 points plus the 5 new fields |
| `components-actions-inputs.md` | Button, Input, Select, Search, Filter, Date Picker, Upload |
| `components-navigation.md` | Tabs, Navigation, Sidebar, Header, Dropdown, Pagination |
| `components-containers-display.md` | Card, Table, Modal, Drawer, Chart, List, Timeline/Activity Feed |
| `components-feedback-status.md` | Toast, Tooltip, Empty State, Loading State, Error State, Confirmation, Badge, Alert/Banner, Progress Indicator |
| `composition-patterns.md` | Form, Data Table, Record Detail View, and KPI/Stat Card as organisms — which registry entries compose them and how |
| `registry-integration.md` | Registry-first reuse, duplication prevention, token enforcement, and the wiring into the Quality Engine and UX Scenario Testing |

## Explicitly not here
- The 8-point framework, taxonomy, iconography, data-viz chart selection,
  motion-at-component-level → `ui-engine/component-system.md`.
- Per-product component instances → `templates/component-spec.md`
  (which now cites a registry entry as its starting point, per
  `registry-integration.md`).
- Page-level composition → `ui-engine/layout-system.md`.
- Domain-specific UI-pattern conventions → `product-types/*.md` (cited per
  entry where it applies, never restated).
