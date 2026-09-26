Source: `ui-engine/design-system.md`, `typography.md`, `color-system.md`, `layout-system.md`, `visual-trends.md` | Owning agent: design-system-expert.md | Version: v0.1.0

# ProjectFlow — Design System

## Register selection
**Modern SaaS** (`ui-engine/visual-trends.md`), per `product-types/saas.md`'s
mapping and the Empathize findings (daily-use, efficiency-oriented but not
dense-enterprise — ROLE-002/003 need speed, not maximal density; comfortable
spacing keeps the empty-state-heavy onboarding welcoming for ROLE-001).
Gate: passes the 3-point trend-adoption check (contrast-safe, legible,
register-justified by the audience above, not chosen for fashion).

## Tokens (engine defaults, reused as-is — domain-agnostic, no product-specific override needed)
- Spacing: `4 8 12 16 24 32 48 64 96`
- Radius: `sm(4px)` inputs/buttons, `md(8px)` task cards/panels, `full` for
  avatar/priority-pill components.
- Elevation: level 1 resting task cards, level 2 on hover/drag, level 4 for
  the Invite Member modal.
- Motion: `motion-fast` for card hover/status-pill changes, `motion-base`
  for the Task Detail drawer open/close and toast notifications.
- Type scale: standard engine scale; tabular figures used nowhere in this
  product (no dense numeric columns) except due-date sort in list view,
  where date values align via the same tabular-figures rule.

## Semantic color mapping applied
- `success` → Done status badge.
- `danger` → Blocked status badge (paired with a "blocked" icon + label,
  never color-only) and destructive actions (remove member).
- `warning` → overdue due-date indicator.
- `info` → In Progress status badge.
- `neutral` → To Do, Cancelled.
All pairs checked against the 4.5:1/3:1 contrast rule in both themes
`[ASSUMPTION: light + dark theme both supported | BASIS: tier 7, standard
SaaS expectation | IMPACT: none — default engine behavior]`.

## Component inventory
See `ui/components.md` for the 8 components this product needs — all fit
within the engine's existing atom/molecule/organism taxonomy; none required
inventing a new category.

## Drift check
No undocumented one-off values introduced anywhere in this pass — every
value above cites an existing engine token or semantic mapping.
