Source: BRD/brief.md (plain-language input) | Owning agent: brd-analyst.md (Empathy summary) + product-architect.md (Define/Ideate) | Version: v0.1.0

# ProjectFlow — Product Definition

## Empathy summary
Per `methodology/empathize.md`'s 11 dimensions, applied per role
(`ROLE-NNN`, see `requirements/user-roles.md`). Sourced almost entirely from
`product-types/saas.md`'s domain conventions + general project-management
domain convention (Rule 2 tier 6/7), since the brief itself states no users
— every goal/pain-point below is `[ASSUMPTION: derived from standard PM SaaS
convention | BASIS: tier 6-7 | IMPACT: if this team's actual workflow differs
materially from typical PM tool usage, the flows/screens below may need
rework, not just re-theming]`.

| Role | JTBD | Primary pain point | Frequency | Constraint |
|---|---|---|---|---|
| ROLE-001 Owner | When our team's work is scattered across chat/spreadsheets, I want one shared place to track projects, so I can see if we're on track without chasing updates | No single source of truth for status | Weekly/monthly (billing, settings) | Limited patience for complex admin |
| ROLE-002 Project Manager | When I'm coordinating people across tasks and deadlines, I want to assign work and track status in one view, so I can catch delays early | Unclear ownership of tasks | Daily, high-frequency | Needs speed over hand-holding |
| ROLE-003 Team Member | When I have several tasks assigned, I want a clear list of what's mine and due when, so I can prioritize my day | Hunting for "what's mine" across tools | Daily, high-frequency | Zero tolerance for friction |
| ROLE-004 Guest/Viewer | When a stakeholder wants visibility without being "in" the tool, I want a simple read-only status view, so I don't have to ask for updates manually | Has to manually request status | Rare/occasional | Zero learning curve — first visit must be self-explanatory |

Operational reality (dimension 11): teams routinely have tasks blocked by
other tasks, mid-project scope changes, and members going on leave requiring
reassignment — these feed `requirements/edge-cases.md` directly.

## Problem statement
How can we help small-to-mid-size teams track project work and deadlines in
one shared place, despite work currently being scattered across chat, email,
and spreadsheets with no single source of truth?

## Business objective
`[ASSUMPTION: increase active-usage-driven retention and account expansion,
typical of PM SaaS | BASIS: tier 6, not stated in brief | IMPACT: if the real
objective is different (e.g. pure lead-gen for a larger platform), the
onboarding/pricing-adjacent decisions below may be miscalibrated]`.

## User objective
Let a project manager and their team see, assign, and update work status
without leaving one tool.

## Product objective
Provide shared project/task tracking with role-based visibility and status
reporting — a capability statement, not yet a specific screen or flow.

## Constraints
- Web only. `[ASSUMPTION: no native mobile app in this scope | BASIS: explicit
  "Platform: Web" statement in the brief | IMPACT: if the actual team is
  field-heavy/mobile-first, responsive web may be insufficient]`.
- `[ASSUMPTION: standard MVP scope/budget/timeline | BASIS: tier 8, nothing
  stated | IMPACT: none of the sizing below should be read as a committed
  estimate]`.

## Assumptions (consolidated)
All assumptions above, plus (carried forward into `requirements/*`):
business-rule, dependency, and integration assumptions are tagged at their
point of origin in `business-logic.md` and `dependency-analysis.md` and not
re-listed here — this section aggregates the Empathize/Define-level ones
only, per `config/output-contract.md`'s carry-forward rule.

## Dependencies (coarse)
Workspace & membership must exist before any project feature; project must
exist before any task. Full graph in `requirements/dependency-analysis.md`.

## Success criteria
1. An Owner can create a workspace and their first project within one
   session with no external help.
2. A Project Manager can create a project, add tasks, and assign them to
   team members, and see completion status at a glance.
3. A Team Member can find "what's assigned to me and due when" without
   searching.
4. A Guest can view a shared project's status with zero onboarding.

## In scope / out of scope
**In scope:** workspace/membership, projects, tasks (create/assign/status/
comments/due dates/priority/blocking dependency), board + list views,
dashboard, notifications (assignment + due-date reminder), guest read-only
access.
**Explicitly deferred, not dropped:** Gantt/timeline view, time tracking,
file attachments, third-party integrations (Slack/email sync), mobile native
app. Logged here for the next product-level loop pass, per `methodology/
define.md`'s scope-boundary technique.

## Chosen approach (Ideate)
**Core work view — three alternatives considered:**
1. **Kanban board** (columns = status) — externalizes status visually, low
   cognitive load, strong fit for daily high-frequency use (`ROLE-002`,
   `ROLE-003`), well-matched to users' existing mental model of PM tools.
2. **Flat sortable list/table** — better for dense scanning and bulk
   operations, weaker for at-a-glance visual status.
3. **Calendar/timeline (Gantt)** — best for deadline/dependency
   visualization, but highest implementation complexity, and dependency
   modeling here is intentionally lightweight (single blocking-task links,
   not a full critical-path engine).

**Selected:** Board (1) as the primary view **and** List (2) as a fully
equivalent secondary view of the *same* task data (not a separate feature) —
this simultaneously serves the accessible/keyboard-operable equivalent the
board's drag-and-drop needs (per `methodology/ideate.md`'s accessibility-by-
construction check) and the power-user/bulk-action need, from one decision.
**Rejected:** Gantt/timeline as MVP-primary — implementation complexity
outweighs core value at this scope; logged above as explicitly deferred, not
silently dropped.
