# Gap Detection

## Responsibility
Automatically identify a missing workflow screen, transition, action,
validation, or feedback rule for a given scenario — checked against the
spec the product already has (`ux/sitemap.md`, `ux/navigation.md`,
`ux/screen-architecture.md`, `ux/state-matrix.md`, `ux/ux-rules.md`), not a
new source of design content. This file finds absences; it does not fill
them — a gap routes to the agent who owns the missing artifact
(`methodology/design-thinking.md`'s routing table), it is never
improvised here.

## The five gap categories

### Missing screen
A scenario step (`scenario-model.md`'s Steps/UI interactions fields) names
an Action, Decision, or Completion with no corresponding `SCREEN-NNN` in
`templates/screen-architecture.md`. This sharpens **B5**'s existing "every
screen traces to a flow step" check by walking the reverse direction —
every flow *step* traces to a screen — which B5 alone does not guarantee
(a screen-architecture pass can be complete for the screens it has while
still missing one a flow actually requires).

### Missing transition
A scenario's Next Action has no defined navigation path in
`ux/navigation.md` — the target screen exists, but nothing in
`ux-engine/navigation-system.md`'s selected pattern (items 5/6/11/12)
actually gets the user there from the current step. Distinct from a missing
screen: here, both screens exist, but the path between them doesn't.

### Missing action
A DECISION branch (`ux-engine/user-flow-engine.md`) has no corresponding
UI control identified in the target screen's region map or component
inventory (`ui-engine/component-system.md`) — the flow names a choice the
user must make, but the screen gives them no way to make it. Resolving
this checks `component-registry/*` first (Rule 24) — the missing action
is very often exactly a registered pattern (a Data Table's bulk-action
Button, a Form's Cancel) that was never instantiated, not a genuinely
novel control.

### Missing validation
An Action step that collects input has no cited validation rule
(`product-intelligence/business-logic.md` §9, `ux-engine/form-design.md`) —
the same completeness bar `product-intelligence/requirement-engine.md`
already expects per requirement, checked here at the concrete step level
where it's actually exercised.

### Missing feedback
An Action has no stated feedback rule in
`ux-engine/interaction-design.md`'s action-feedback table — a structural,
proactive check; `methodology/test.md` dimension 5 (Feedback) later
confirms this holds on the *concrete* prototype, this check confirms the
*rule was ever stated* in the first place, catching the gap earlier and
cheaper (same "cheaper to fix here than at Audit" relationship
`methodology/test.md`'s Accessibility dimension already states for its own
design-time vs. Audit-time check).

## Procedure
For every `SCENARIO-NNN` (`scenario-model.md`), walk its Steps in order and
check each of the five categories above against the current spec. Record
each finding with:

```
Gap type: <missing screen | missing transition | missing action | missing validation | missing feedback>
Scenario: SCENARIO-NNN
Step: <which step in the walk>
Expected: <what the spec should have>
Found: <what's actually there, or "nothing">
Severity: <per config/output-contract.md>
Routes to: <the owning agent/file, per methodology/design-thinking.md>
```

A **missing screen** or **missing transition** on a scenario's Primary or
Recovery type is a Blocker by default (the scenario cannot be completed at
all) — a gap on an Alternate/Error/Empty/Loading/Permission/Offline type is
at minimum Major, never silently downgraded because the primary path still
works.

## Explicitly not here
- Defining what a scenario/step is → `scenario-model.md`.
- Walking the actual built screen sequence for experiential problems
  (dead ends, ambiguous CTAs, inconsistent patterns) → `continuity-audit.md`.
- The severity vocabulary and routing table themselves →
  `config/output-contract.md`, `methodology/design-thinking.md`.
- Where findings are aggregated → `coverage-matrix.md`.
