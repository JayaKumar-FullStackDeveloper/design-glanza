# Interaction Analysis

## Responsibility
The Interaction research area: studying which interaction patterns actually
fit this product's task/frequency/density combination before Prototype's UX
pass names a structural choice. A research *technique* — the actual
selection rules for each pattern below are owned by their `ux-engine/*`
file; this file is where research confirms which pattern the evidence
points to, not a second, competing rulebook.

## What to study, per pattern category

| Category | What to establish | Owning technique |
|---|---|---|
| Navigation | Which of the named navigation patterns fits this IA shape and role structure | `ux-engine/navigation-system.md` |
| Search | Whether this product's data volume/structure calls for search over browsing, and what ranking/zero-results behavior fits | `ux-engine/search-ux.md` |
| Filters | Inline vs. panel/drawer, how many exposed by default | Confirmed here from evidence, applied in `ux-engine/interaction-design.md` |
| Sorting | The sort-cycle sequence and its interaction with pagination | `ux-engine/interaction-design.md` |
| Bulk actions | Whether this domain's task volume justifies bulk selection/action at all | `ux-engine/interaction-design.md` |
| Forms | Density, inline-vs-modal editing, validation timing this domain's data-entry volume calls for | `ux-engine/form-design.md` |
| Tables | Row density, which columns are scan-critical vs. secondary | `ui-engine/component-system.md` (Data visualization section), `ui-engine/layout-system.md` |
| Dashboards | Composition (metric-first vs. list-first vs. chart-first) this audience's decision-making style calls for | `ui-engine/component-system.md` |
| Notifications | Which events warrant interruption vs. passive indication, for this task's error cost | `ux-engine/interaction-design.md`'s feedback rules |
| Feedback | Latency/timing conventions this task's frequency calls for | `ux-engine/interaction-design.md` |
| Error recovery | Retry/abandon-safely/escalate conventions for this domain's error cost | `ux-engine/user-flow-engine.md`'s recovery-path technique |

## How research confirms a selection, rather than overriding it
Every one of the owning files above already has its own selection rule
(e.g. `navigation-system.md`'s IA-shape-driven pattern choice). Research's
job is to confirm the rule's *inputs* are actually correct for this
product — frequency, expertise, task complexity — not to substitute a
different pattern based on what "looks current." Where a stated user
expectation (from the questionnaire or a reference) conflicts with what the
owning rule would select, that's a named conflict to resolve
(`agents/ux-architect.md`'s existing conflict-resolution
posture), not a silent override in either direction.

## The frequency/expertise cross-check
Cross-reference `methodology/ideate.md`'s frequency-driven interaction logic
and `methodology/design-judgment.md`'s user-expertise/task-frequency
weighing factors, already run earlier in the lifecycle — Interaction
Analysis's job at Design Setup is to confirm those earlier calls still hold
once real reference/questionnaire evidence exists, the same "confirms, does
not re-derive" relationship `design-reference-engine/design-research.md`
already states for its own trend research.

## Explicitly not here
- Each pattern's own selection rule and full technique → the `ux-engine/*`
  or `ui-engine/*` file named in the table.
- Visual treatment of any of the above (density register, color, spacing) →
  `visual-analysis.md`.
- Domain-specific interaction conventions → `domain-analysis.md`.
