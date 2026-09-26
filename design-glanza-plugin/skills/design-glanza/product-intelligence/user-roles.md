# User Roles

## Responsibility
Identify the actors in the system (item 2 of `brd-analysis.md`'s checklist) and
model their access (item 12) — who exists, what each can see/do, and how roles
relate to each other. This is the permission/authority model; the *lived
experience* of holding a role (pressure, accountability, decision-making style)
is a different concern owned by `methodology/empathize.md`, which consumes this
file's role list but does not duplicate its permission structure.

## Role ID scheme
Every distinct role gets a unique ID: **`ROLE-NNN`**, sequential. Requirements
(`requirement-engine.md`) cite a role by this ID in their Actor field.
Non-human initiators (a scheduled job, an external system, an automatic rule)
use the literal Actor value `SYSTEM` rather than a `ROLE-NNN` — they are not
part of the human role model but must still be trackable as the initiator of a
requirement.

## Actor identification technique
Extract explicit actors named in the source directly. Then extract **implicit**
actors: a mentioned action often implies an unstated actor (e.g. "invoices are
approved" implies an approver role that may never be named outright) — every
passive-voice action statement in source material is a prompt to ask "by whom?"
and "who has that authority?"

## Role/permission modeling
For every `ROLE-NNN`, build a permission matrix entry:

| Role | Resource/Action | Access | Condition (if conditional) |
|---|---|---|---|
| `ROLE-002` (Manager) | Approve expense report | Allow | only for reports from their own direct reports |
| `ROLE-003` (Employee) | Approve expense report | Deny | — |
| `ROLE-001` (Admin) | View all expense reports | Allow | — |

Every permission is one of: **Allow**, **Deny**, or **Conditional** (with the
condition stated explicitly — an unstated condition is a gap, not an implicit
"figure it out later").

## Role hierarchy and delegation
Capture whether roles relate hierarchically (a manager inherits visibility into
a report's data), and whether any role can delegate or act on another's behalf
(admin impersonation, an out-of-office approval delegate). A delegation
relationship is itself a permission entry with a condition ("only while
delegated, only for the delegating role's own scope"), not a separate,
undocumented backdoor.

## Multi-tenancy implications
Where relevant, every role is additionally scoped: is this role's authority
global, or bound to one account/organization/workspace? A role that looks
identical in two tenants can still not see each other's data — state the scope
boundary explicitly per role rather than assuming it.

## System / non-human actors
Not every action in `requirement-engine.md` has a human actor. Scheduled jobs,
incoming webhooks, and automatic rule-triggered transitions (from
`business-logic.md`'s trigger conditions) use `SYSTEM` as their Actor. These
still need a documented "permission" in the sense of: what is this automation
allowed to do unattended, and does it bypass any check a human actor would
otherwise face (and if so, is that intentional)?

## Handoff shape
This file's role list and permission matrix feed:
- `requirement-engine.md`'s Actor field (by `ROLE-NNN` or `SYSTEM`).
- `ux-engine/navigation-system.md`'s role-based nav visibility.
- `product-types/*.md`'s "typical roles" sections, which this file's output is
  checked against for a plausibility sanity-check, not overridden by.

## Loop position
Consumes `brd-analysis.md`'s extracted actors at the feature-level loop; is
re-invoked when a Test finding traces to a missing or wrong permission (a
business-rule-incorrectness finding specifically about who was allowed to act),
per `methodology/design-thinking.md`'s routing table (routes to Define +
`business-logic.md`, which in turn may reveal this file's role model was
incomplete).

## Explicitly not here
- The business rules a role's actions trigger → `business-logic.md`.
- How role-based visibility is expressed in navigation →
  `ux-engine/navigation-system.md`.
- Domain-typical role sets (e.g. "ERP usually has Approver, Requester...") →
  the relevant `product-types/*.md` file.
- The lived experience of holding a role (pressure, accountability) →
  `methodology/empathize.md`.
