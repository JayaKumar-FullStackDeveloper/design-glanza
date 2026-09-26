Source: BRD/brief.md + `product-types/saas.md` domain convention | Owning agent: brd-analyst.md | Version: v0.1.0

# ProjectFlow — Requirement Matrix

Fields per `product-intelligence/requirement-engine.md`. Confidence is
**Inferred** unless noted — the brief is a plain-language input with almost
no explicit detail, so nearly everything here is a domain-convention
inference, not a stated fact; genuine **Assumed** items carry the full tag.

| ID | Source | Description | Type | Actor | Action | System response | Business rule | Validation | Dependency | Confidence | Priority | Status | Downstream artifacts |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REQ-001 | BRD/brief.md + saas.md convention | Owner creates a workspace | Behavioral | ROLE-001 | creates workspace | Workspace created; Owner role assigned; empty-state dashboard shown | BR-001 | Workspace name required, non-empty | — | Inferred | Must | validated | FLOW-001, SCREEN-001 |
| REQ-002 | saas.md convention | Owner invites a member by email | Behavioral | ROLE-001 | invites member | Invite record created, pending until accepted | — | Valid email format; not already a member (EDGE-006) | REQ-001 | Inferred | Must | validated | FLOW-001, SCREEN-006, COMPONENT-006 |
| REQ-003 | saas.md convention | Invited user accepts invite and joins workspace | Behavioral | SYSTEM / invitee | accepts invite | Membership created with the invited role | — | Invite token valid, not expired | REQ-002 | Inferred | Must | validated | FLOW-001 |
| REQ-004 | Domain convention | Project Manager creates a project | Behavioral | ROLE-002 | creates project | Project created, empty task list | — | Project name required | REQ-001 | Inferred | Must | validated | FLOW-002, SCREEN-002 |
| REQ-005 | Domain convention | Project Manager adds a task to a project | Behavioral | ROLE-002, ROLE-003 | creates task | Task created in "To Do" status | BR-001 | Task title required | REQ-004 | Inferred | Must | validated | FLOW-002, SCREEN-003 |
| REQ-006 | Domain convention | Project Manager assigns a task to a Team Member | Behavioral | ROLE-002 | assigns task | Task's assignee field set; assignee notified (REQ-009) | BR-002 | Assignee must be a project member | REQ-005 | Inferred | Must | validated | FLOW-002, COMPONENT-001 |
| REQ-007 | Domain convention | Team Member updates a task's status | Behavioral | ROLE-003 | updates status | Status field updated; board column reflects it | BR-001 | Transition must be valid per lifecycle | REQ-005 | Inferred | Must | validated | FLOW-003, COMPONENT-002 |
| REQ-008 | Domain convention | Member adds a comment to a task | Behavioral | ROLE-001/002/003 | comments | Comment appended to task activity log | — | Non-empty comment | REQ-005 | Inferred | Should | draft | SCREEN-005 |
| REQ-009 | Domain convention | System notifies assignee when a task is assigned | Behavioral | SYSTEM | sends notification | In-app notification delivered | BR-007 | — | REQ-006 | Assumed | Must | draft | COMPONENT-008 |
| REQ-010 | Domain convention | System reminds assignee as a due date approaches | Behavioral | SYSTEM | sends reminder | In-app notification delivered | BR-007 | Suppressed if task already Done (EDGE-005) | REQ-013 | Assumed | Should | draft | COMPONENT-008 |
| REQ-011 | Ideate decision | Member views the project board (Kanban) | Behavioral | ROLE-001/002/003/004 | views board | Tasks rendered grouped by status column | — | — | REQ-005 | Inferred | Must | validated | FLOW-002, SCREEN-003 |
| REQ-012 | Ideate decision | Member switches between board and list view | Behavioral | ROLE-001/002/003 | toggles view | Same task set re-rendered in the other layout, filters/sort preserved | — | — | REQ-011 | Inferred | Must | validated | SCREEN-004 |
| REQ-013 | Domain convention | Project Manager sets a task due date | Data | ROLE-002 | sets due date | Due date stored | BR-005 | Not in the past (BR-005) | REQ-005 | Inferred | Must | validated | COMPONENT-001 |
| REQ-014 | Domain convention | Project Manager sets a task priority | Data | ROLE-002 | sets priority | Priority stored (Low/Medium/High) | — | One of the closed set | REQ-005 | Inferred | Should | validated | COMPONENT-001 |
| REQ-015 | Domain convention | Any member views the workspace dashboard | Behavioral | ROLE-001/002/003 | views dashboard | Aggregate status rendered (counts by status, overdue count) | — | — | REQ-005 | Inferred | Must | validated | SCREEN-001 |
| REQ-016 | Domain convention | Owner/PM invites a Guest scoped to one project | Behavioral | ROLE-001/002 | invites guest | Guest membership created, scoped to one project | BR-003 | — | REQ-004 | Inferred | Should | draft | FLOW-004 |
| REQ-017 | Domain convention | Guest views a shared project read-only | Behavioral | ROLE-004 | views board | Board rendered; no action controls exposed | BR-003 | — | REQ-016 | Inferred | Should | draft | FLOW-004, SCREEN-008 |
| REQ-018 | Domain convention | Team Member marks a task Blocked with a reason | Behavioral | ROLE-003 | marks blocked | Task enters Blocked status; reason stored | BR-001 | Reason required | REQ-007 | Inferred | Should | draft | EDGE-003 |
| REQ-019 | Domain convention | A task may depend on another task (blocking) | Data | ROLE-002 | sets dependency | Dependent task cannot move to Done while blocker is open | BR-004 | Blocker task must exist in same project | REQ-005 | Inferred | Could | draft | EDGE-003 |
| REQ-020 | Domain convention | Owner removes a member from the workspace | Behavioral | ROLE-001 | removes member | Member's access revoked; open tasks unassigned (BR-006) | BR-006 | — | REQ-003 | Inferred | Should | draft | EDGE-001 |
| REQ-021 | Rule 5 / operating-rules.md | Every mutating action is permission-checked before executing | Permission | SYSTEM | checks permission | Unauthorized attempts rejected; `permission denied` state shown | — | Actor's role must have Allow for the action | user-roles.md | Explicit | Must | validated | state-matrix.md |
| REQ-022 | Domain convention | Task due date cannot be set in the past | Business-rule | SYSTEM | validates date | `validation error` shown inline if violated | BR-005 | Date ≥ today | REQ-013 | Inferred | Must | validated | state-matrix.md |
| REQ-023 | `product-definition.md`'s explicit scope-boundary log | Owner views workspace billing settings (placeholder — billing itself is explicitly deferred, not built) | Non-functional | ROLE-001 | views billing settings | Placeholder screen rendered; no billing logic wired up | — | — | REQ-001 | Assumed | Could | draft | SCREEN-007 |

**23 requirements total.** Priority distribution: 12 Must, 7 Should, 2
Could, 1 permission/validation-rule (Must). Status: 12 validated (Empathize
through Prototype-UX complete for these), 10 draft (recorded, not yet
carried through Prototype in this pass — see Gaps in the final report).

## Explicitly not here
- Business rule content (only cited by `BR-NNN` here) → `business-logic.md`.
- Role/permission content (only cited by `ROLE-NNN` here) → `user-roles.md`.
- Dependency graph content → `dependency-analysis.md`.
