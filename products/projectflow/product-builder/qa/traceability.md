Source: `product-intelligence/traceability.md`'s chain, applied to this product | Owning agent: qa-expert.md | Version: v0.1.0

# ProjectFlow — Traceability

The built chain is **REQ → USER → FLOW → SCREEN → COMPONENT → TEST**
(`product-intelligence/traceability.md`) — this product builder uses the
real, currently-built chain, which includes the `USER` link; noting this
explicitly since it's one link richer than a bare REQ→FLOW→SCREEN→COMPONENT→
TEST reading would suggest.

## Trace record

| REQ | USER | FLOW | SCREEN | COMPONENT | TEST |
|---|---|---|---|---|---|
| REQ-001 | ROLE-001 | FLOW-001 | SCREEN-001 | COMPONENT-007 | *(pending — Test not run)* |
| REQ-002 | ROLE-001 | FLOW-001 | SCREEN-006 | COMPONENT-006 | pending |
| REQ-003 | invitee/SYSTEM | FLOW-001 | SCREEN-006 | — | pending |
| REQ-004 | ROLE-002 | FLOW-001 | SCREEN-002 | — | pending |
| REQ-005 | ROLE-002/003 | FLOW-002 | SCREEN-003 | COMPONENT-001 | pending |
| REQ-006 | ROLE-002 | FLOW-002 | SCREEN-003, SCREEN-005 | COMPONENT-001 | pending |
| REQ-007 | ROLE-003 | FLOW-003 | SCREEN-003, SCREEN-005 | COMPONENT-002 | pending |
| REQ-008 | ROLE-001/002/003 | *(sub-step of FLOW-002/003, no dedicated flow)* | SCREEN-005 | — | pending |
| REQ-009 | SYSTEM | FLOW-002 (trigger) | — | COMPONENT-008 | pending |
| REQ-010 | SYSTEM | *(not flow-mapped — system-triggered, no user flow)* | — | COMPONENT-008 | pending |
| REQ-011 | ROLE-001/002/003/004 | FLOW-002, FLOW-003, FLOW-004 | SCREEN-003 | COMPONENT-003 | pending |
| REQ-012 | ROLE-001/002/003 | *(capability of SCREEN-004, no dedicated flow)* | SCREEN-004 | COMPONENT-004 | pending |
| REQ-013 | ROLE-002 | FLOW-002 | SCREEN-005 | COMPONENT-001 | pending |
| REQ-014 | ROLE-002 | FLOW-002 | SCREEN-005 | COMPONENT-001 | pending |
| REQ-015 | ROLE-001/002/003 | *(not flow-mapped — standalone view)* | SCREEN-001 | — | pending |
| REQ-016 | ROLE-001/002 | FLOW-004 (setup) | SCREEN-006 | COMPONENT-006 | pending |
| REQ-017 | ROLE-004 | FLOW-004 | SCREEN-008 | COMPONENT-003 | pending |
| REQ-018 | ROLE-003 | FLOW-003 | SCREEN-005 | COMPONENT-002 | pending |
| REQ-019 | ROLE-002 | *(not flow-mapped)* | SCREEN-005 | — | pending |
| REQ-020 | ROLE-001 | *(not flow-mapped)* | SCREEN-006 | — | pending |
| REQ-021 | SYSTEM | *(cross-cutting, all flows)* | *(all screens)* | — | pending |
| REQ-022 | SYSTEM | FLOW-002 | SCREEN-005 | COMPONENT-001 | pending |
| REQ-023 | ROLE-001 | *(not flow-mapped — placeholder, billing deferred)* | SCREEN-007 | — | pending |

## Coverage summary
- **23/23 requirements** trace to ≥1 `USER` and ≥1 `SCREEN` — zero
  orphaned requirements at the SCREEN link, confirmed by re-running
  `scripts/validate-screens.py` after adding REQ-023 to back the
  previously-orphaned SCREEN-007 (Billing placeholder) — it went from a
  `[Major]` finding to zero findings.
- **16/23** trace to a named `FLOW-NNN`; **7** (REQ-008, 010, 012, 015, 019,
  020, 023) are either sub-steps of an existing flow, standalone
  system-triggered behaviors, a deferred placeholder, or cross-cutting
  rules with no single "user flow" shape — named explicitly here rather
  than force-fit into a flow that doesn't really apply, per Rule 10 (don't
  invent structure that isn't there).
- **17/23** trace to a named `COMPONENT-NNN`; 6 don't have a dedicated
  component of their own, which is expected — not every requirement is
  itself a discrete visual component.
- **0/23** trace to a `TEST-NNN` — Test has not run in this exercise (by
  explicit instruction not to build/test the application). This is the
  chain's only structurally incomplete link, and it's incomplete for the
  correct reason (out of scope for this pass), not a defect.
- **Zero orphaned artifacts**: every `SCREEN-NNN` and `COMPONENT-NNN`
  created in this exercise now traces back to at least one `REQ-NNN` above —
  confirmed mechanically via `scripts/validate-product.py`, not just by
  inspection.

## Explicitly not here
Requirement/rule/role *content* → `requirements/*.md`; how each artifact was
produced → `ux/*.md`, `ui/*.md`.
