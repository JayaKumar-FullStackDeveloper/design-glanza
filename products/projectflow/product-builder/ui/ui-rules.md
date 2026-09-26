Source: `ui-engine/visual-hierarchy.md`, `visual-trends.md` | Owning agent: ui-designer.md | Version: v0.1.0

# ProjectFlow — Visual Hierarchy Application

- **Primary action per screen:** "Create task" (board/list), "Create
  project" (projects list/empty dashboard), "Invite member" (settings) —
  each the highest-contrast, filled-button element on its screen; never two
  competing primary buttons (confirmed against `screen-architecture.md`).
- **Information priority:** on Task Card, status badge and due date (if
  overdue) get the highest visual weight; description/comment count
  recedes. On Dashboard, overdue count is the single most prominent number.
- **Grouping:** board columns are visually separated by whitespace + a
  subtle divider, matching the IA grouping in `ux/sitemap.md` exactly — no
  visual group crosses a status boundary.
- **Scanning pattern:** F-pattern for List view and Dashboard (data-dense,
  scan-for-specific-value screens); board view is inherently column-scanned
  left-to-right, a variant the F-pattern default naturally supports.
- **Density:** Comfortable (per Modern SaaS register) — not Dense
  Enterprise, since ROLE-002/003 use this all day but the audience isn't
  admin-panel-scale data volume (yet); revisit if task-per-project counts
  turn out to be very high (ties to scalability, `ui-engine/design-
  system.md`).
- **Whitespace:** generous margin around the primary "Create" action on
  empty states specifically — reinforcing it as the one thing to do next.
- **Progressive disclosure:** Task Detail's comment thread collapses after
  the first 3 comments with a "show more" control, styled as clearly
  interactive (not plain text), per the progressive-disclosure rule.
- **Emphasis levels used:** 4 (primary action, status badges, secondary
  actions, muted/metadata text) — within the 3-4 level cap.
