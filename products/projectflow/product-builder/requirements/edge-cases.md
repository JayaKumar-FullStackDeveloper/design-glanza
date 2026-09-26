Source: Derived from `business-logic.md`'s failure conditions + `methodology/empathize.md` dimension 11 (operational reality) | Owning agent: brd-analyst.md | Version: v0.1.0

# ProjectFlow — Edge Cases

| ID | Scenario | Category | Severity | Likelihood | Recovery |
|---|---|---|---|---|---|
| EDGE-001 | A member is removed while they still have open (unfinished) tasks assigned | Cross-role / operational | Major | Medium | Tasks become unassigned (BR-006); dashboard flags them "needs reassignment" — retry (PM reassigns) |
| EDGE-002 | Two Project Managers edit the same task's status simultaneously | Concurrency | Major | Low | `conflict` state shown with "updated by X, reload to see latest" — retry |
| EDGE-003 | A task's blocking dependency (REQ-019) is deleted/archived while the blocked task is still pending | Data-format / dangling reference | Major | Low | System clears the block automatically and flags it in the task's activity log — no silent limbo |
| EDGE-004 | A Guest's shared project is deleted while they still hold the link | Permission / lifecycle | Minor | Low | Guest sees an explicit "this project is no longer available" empty-equivalent state, not a broken page |
| EDGE-005 | A due-date reminder (REQ-010) would fire after the task is already Done | Business-rule timing | Minor | Medium | Suppressed — current status checked before sending (business-logic.md BR-007 area) |
| EDGE-006 | An invite (REQ-002) is sent to an email that's already a workspace member | Duplicate submission | Minor | Medium | System detects and informs the inviter rather than creating a confusing duplicate pending invite |
| EDGE-007 | Brand-new workspace with zero projects/tasks | Empty/boundary | Minor | High (every new workspace hits this) | Guided empty state on dashboard and project list — not a blank/broken-looking screen (saas.md's named UX risk) |
| EDGE-008 | A Team Member updates a task's status while offline | Offline | Major | Medium | UI shows the change as pending-sync, not silently lost or falsely confirmed — ties to the just-added `offline` state (`ux-engine/state-design.md`) |
| EDGE-009 | A task is assigned to someone who is not actually a member of that specific project (only of the workspace) | Validation | Minor | Low | Rejected at REQ-006 validation — "assignee must be a project member" |

## Coverage note
Every failure category `business-logic.md` §"Success/failure conditions"
names (permission denial, validation failure, concurrency, dangling
reference, timing) has at least one concrete scenario above — none left at
zero, per `product-intelligence/edge-case-engine.md`'s coverage rule.
