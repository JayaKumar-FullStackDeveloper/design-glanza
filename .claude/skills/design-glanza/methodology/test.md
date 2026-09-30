# Test

## Responsibility
Evaluate the prototype/implementation against Empathize's users and Define's
success criteria — design validation of the *product being built*, not internal
quality measurement of Design-Glanza's own generated artifacts (that's
`evals/*`), and not post-build correctness auditing of the implementation against
its own spec (that's `workflows/audit-product.md`). Test asks one question nine
ways: *does this actually work for the person it's for, and does it obey the
rules it's supposed to obey?*

## The 9 evaluation dimensions

### 1. Task completion
Walk the primary user flow (`templates/user-flow.md`) step by step for the actor
it was built for, end to end, and check it against Define's success criteria
(output 8). Binary per persona × flow: can they finish, unassisted, or not?
A flow that "mostly works" with an undocumented workaround is a fail, not a pass
with a note.

### 2. Usability
Apply a heuristic evaluation: recognition over recall, consistency with
established patterns, minimal necessary user effort, clear system status,
forgiving of small mistakes, and **flexibility and efficiency of use** — a
frequent-user accelerator (a keyboard shortcut, a bulk action, a saved
filter) that a novice never has to discover but an expert can grow into,
distinct from the interaction model itself being fast by default
(`methodology/ideate.md` criterion 2). Check the actual prototype against
each heuristic, not against the abstract rule in the abstract — a specific
screen either recognizably violates a heuristic or it doesn't.

### 3. Discoverability
Can the actor find the feature/action without being told where it is? Check the
entry point's reachability from the natural IA location a user would look
(`ux-engine/information-architecture.md`, `navigation-system.md`), and whether
the primary action is visually prominent enough to notice
(`ui-engine/visual-hierarchy.md`) — a feature that exists but that no persona
would ever navigate to unprompted is a discoverability failure, not a
non-issue.

### 4. Error prevention
Check whether the design proactively *prevents* the error states enumerated in
`ux-engine/state-design.md` (e.g. disabling submission until input is valid,
confirming before a destructive action) rather than only handling the error
after it occurs. A well-designed error message for a preventable error is still
a partial fail on this dimension.

### 5. Feedback
Every user action defined by `ux-engine/interaction-design.md` must have
confirmed, observable feedback within its stated acceptable latency — check that
this actually holds in the concrete prototype, action by action, not just that
the rule exists in principle.

### 6. Accessibility
Verify, on the concrete artifact, both halves: structural/behavioral
(`ux-engine/accessibility.md` — focus order, keyboard operability, semantics) and
perceptual (`ui-engine/color-system.md` — contrast, color-blind safety). This is
the design-time check; `workflows/audit-product.md` re-checks formal conformance
later at the built artifact, but a failure caught here is cheaper to fix than one
caught at Audit.

### 7. Responsiveness
Verify the concrete screens actually hold up at each mandatory breakpoint
(`ui-engine/responsive-system.md`): priority content (per
`ui-engine/visual-hierarchy.md`) stays reachable at the smallest breakpoint, and
touch targets meet minimum size where the interaction model requires touch.

### 8. Edge cases
For every edge case `product-intelligence/edge-case-engine.md` enumerated for
this feature, verify a designed response exists (cross-referencing
`templates/state-matrix.md`) — not silently ignored, and not silently assumed to
"just not happen." An edge case with no state-matrix entry is a fail on this
dimension by definition.

### 9. Business-rule correctness
Verify the flow's behavior matches `product-intelligence/business-logic.md`'s
stated rules exactly — a calculation matches its formula, a lifecycle's state
transitions match the modeled state machine, a permission check matches the
role model in `product-intelligence/user-roles.md`. This checks that the
*design* embodies the rule correctly; whether the eventual *implementation*
embodies the design correctly is `workflows/audit-product.md`'s job, one phase
later.

## Evaluation output
Per dimension: pass / fail, and if fail, a severity (per
`config/output-contract.md`'s vocabulary) and — critically — which phase the
failure routes to. Routing is not a judgment call made fresh each time; it
follows `methodology/design-thinking.md`'s feedback routing table, keyed to
*what kind of wrong* was found (a wrong understanding routes further back than a
wrong execution of a right understanding).

## Loop position
- **Entered from:** `prototype.md`'s handoff, for every feature/screen as it
  reaches a testable state — not only once at the end of the whole product.
- **Routes back to (per the routing table in `design-thinking.md`):** Define,
  Ideate, or Prototype, depending on the finding — see that file for the full
  table; this file does not restate it dimension-by-dimension to avoid the two
  tables drifting apart.
- **Terminates the loop (this scope) when:** all nine dimensions pass with no
  Blocker or un-waived Major finding — which is also the exact condition
  `config/quality-gates.md`'s Test → Audit gate checks, and hands the feature
  forward to Implement/Audit rather than continuing to cycle.

## Explicitly not here
- Internal artifact-quality scoring of Design-Glanza's own output → `evals/*`.
- Post-implementation correctness/consistency audit → `workflows/audit-product.md`.
- The feedback routing table itself (kept in one place to avoid drift) →
  `methodology/design-thinking.md`.
- Accessibility rule definitions → `ux-engine/accessibility.md`,
  `ui-engine/color-system.md` (this file applies them, doesn't define them).
