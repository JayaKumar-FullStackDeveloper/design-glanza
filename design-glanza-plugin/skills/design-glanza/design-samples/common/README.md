# Design Sample: Common (Domain-Agnostic)

Status: **partially populated** — 11 curated reference images added
(source: user-supplied, unattributed third-party dashboard shots — treat
as Inferred-confidence visual reference, not a licensed/attributed asset).
This batch was originally dropped in as one mixed set of 38 images; most
were domain-specific and have been sorted into their matching
`design-samples/<domain>/` folder instead (see each folder's own README) —
only the genuinely domain-agnostic and no-matching-domain ones stayed here.

## Reference assets
| File | What it shows |
|---|---|
| `dashboard-generic-project-timeline.jpg` | Project-management dashboard: progress ring, task-done/in-progress/waiting counts, Gantt-style project timeline, todo list |
| `dashboard-generic-saas-schedule.jpg` | Generic SaaS portal dashboard: weekly schedule grid, upcoming event card, assigned tasks, work-progress bars |
| `dashboard-generic-admin-template.jpg` | Explicitly generic "Admin Dashboard" template: sales/customers/revenue/refunds summary, recent-orders table, top-sellers list |
| `dashboard-generic-task-management.jpg` | Task/project dashboard: active/in-progress/complete task counts, AI task assistant, tasks-activity chart, team insights |
| `dashboard-generic-task-chat.jpg` | Task-management app with embedded team chat: upcoming tasks (drag cards), scheduled meetings, performance chart, chat panel |
| `dashboard-generic-booking-reservation.jpg` | Booking/reservation dashboard (property/hotel-style): total bookings/guests/revenue summary, revenue chart, today's bookings list, occupancy forecast — no dedicated Hospitality/Real-Estate sample folder exists yet, kept here |
| `dashboard-generic-analytics-sustainability.jpg` | Dense analytics/BI dashboard (environmental-metrics use case): KPI summary cards, trend chart, regional data table, choropleth map — a general dense-analytics layout reference, domain incidental |
| `table-generic-sales-orders-bulk-actions-a.jpg` | Generic sales-order data table: status badges, multi-row selection, contextual bulk-action bar (send/print/edit/delete) |
| `table-generic-sales-orders-bulk-actions-b.jpg` | Near-identical to `-a` (same design, different file/export — hashes differ so both were kept rather than assumed redundant; remove one if you confirm they're the same source) |
| `dashboard-education-lms-courses.jpg` | Learning-platform dashboard: course progress, "continue watching" cards, lesson list — no dedicated Education sample folder exists yet, kept here |
| `dashboard-education-management-enrollments.jpg` | Education-management SaaS dashboard: enrollment/revenue/course-sales summary, top-courses list, course-mix donut charts — same no-folder-yet note as above |

## Note on Education
Two images above are clearly Education/LMS-domain but `design-samples/`
has no dedicated `education/` folder (it wasn't part of the original
12-domain list). If Education recurs as a real need, add
`design-samples/education/` (no core-file change required — same
extensibility as any other sample folder) and move these two there.

## Kind
Not a domain sample and not a platform sample — a **shared** sample,
consulted *alongside* whichever domain folder (and platform folder, if any)
`design-reference-engine/reference-selection.md` selects for a given
product, never instead of one. Holds general UI/interaction patterns that
apply regardless of domain: common component compositions (buttons, forms,
cards, tables, modals, navigation shapes), common layout patterns, and
common interaction patterns that aren't specific to SaaS vs. Healthcare vs.
Logistics, etc.

## When it's used
Every time Default Design-Glanza mode (mode 4) applies — this folder is
always part of the starting point, not an alternative to the domain-matched
folder. Rationale: most UI patterns genuinely are domain-agnostic (a table
looks structurally the same in ERP and CRM); putting them here once avoids
duplicating the same reference images across all 12 domain/platform
folders.

## Suggested starting register
No single register — images here should be tagged (in this README, once
populated) with which `ui-engine/visual-trends.md` register(s) they best
illustrate (Modern SaaS / Dense Enterprise / Consumer Playful), since a
domain-agnostic component pattern can still be rendered in any of the three.

## To populate
Add curated reference images or a written style brief for
domain-agnostic UI patterns, then update this README to describe what was
added, its source, and its confidence — same convention as every other
`design-samples/*` folder.

## Explicitly not here
- Domain-specific sample folders → `design-samples/{saas,admin-panel,...}/`.
- Platform-specific sample folders → `design-samples/{mobile,
  responsive-web}/`.
- The selection logic that combines this folder with a domain/platform
  match → `design-reference-engine/reference-selection.md`.
