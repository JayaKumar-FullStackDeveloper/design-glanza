# Continuity Audit

## Responsibility
Walk a scenario's **actual screen sequence** — not the flow diagram, the
real sequence of screens a user would move through — checking for
experiential breaks that no single-screen audit can see, because a
single-screen audit only ever looks at one screen at a time. This is the
cross-screen sibling to `ui-engine/craft-critique.md` and `ui-engine/
ui-audit-framework.md`, both of which are explicit about running on one
finished screen; this file is what runs *across* the set a scenario visits.

## The five checks

### 1. Dead ends
At every screen the scenario passes through, is there a forward path
(toward Next Action) or a stated Completion/recovery route? A screen with
no exit — no primary action, no back path, no recovery link — is a dead
end. This exercises `ux-engine/navigation-system.md`'s existing "how do I
get out" wayfinding check and `user-flow-engine.md`'s dead-end prohibition
as a systematic walk instead of a one-off design-time reminder — the
difference between a rule existing and a rule being checked.

### 2. Unnecessary steps
Per `ux-engine/user-flow-engine.md` criterion 4 (Minimal user effort,
extraneous vs. inherent complexity): walking the *actual* screen sequence,
does every screen/step visited move the scenario closer to Completion? A
step that exists only because of how the flow happened to be built —
re-entering information the system already has, an intermediate screen
with no decision or action of its own — is flagged, naming which kind of
complexity it is (per that criterion's own distinction) rather than
assumed removable by default.

### 3. Ambiguous CTAs
Does the screen's designated primary action (`ui-engine/visual-hierarchy.md`,
**B5**'s "one identified primary action" criterion) actually match what
*this* scenario's step needs the user to do next? Two failure shapes: more
than one control on the screen could plausibly be "the" next step with no
way to tell which is primary: the CTA exists but its label doesn't name
its outcome (e.g. "Continue" where "Submit for Approval" would remove the
ambiguity). This sharpens B5's structural check (one primary action exists)
into an experiential one (that action is the *right*, *identifiable* one
for the scenario actually being walked).

### 4. Missing feedback
The experiential counterpart to `gap-detection.md`'s structural check:
walking the scenario, was feedback for each action actually observable
within `ux-engine/interaction-design.md`'s stated latency — not just
specified somewhere, but present at the point the scenario needed it.

### 5. Inconsistent interaction patterns
The same task type handled two different ways across the screens this
scenario (or a sibling scenario of the same flow) visits — e.g. "delete a
record" confirmed via a modal on one screen and inline, unconfirmed, on
another — with no stated reason. This is `agents/design-system-expert.md`'s
existing drift-review concept (Rule 5, system before screen), extended
from *token/component* drift to *interaction-pattern* drift; a finding
here is routed to Design System Expert exactly as a token/component drift
finding already is, not handled as a new category of defect. Very often
this finding is itself a registry-first violation
(`component-registry/registry-integration.md`, Rule 24) — two screens
handling "delete a record" differently because only one of them actually
consulted the Confirmation entry before specifying its own interaction.

## Contextual consistency
A sixth, related check, not a numbered defect type on its own: does context
carried from one screen survive into the next and back? Filters, sort
order, scroll position, and in-progress form data must persist across a
back-navigation per `ux-engine/navigation-system.md` item 6's existing
"back returns to the last meaningful state... with entered data intact"
rule — walked here concretely, per scenario, rather than only stated as a
general rule.

## Procedure
For every `SCENARIO-NNN`, walk its actual screen sequence (post-Prototype:
the specified screens; post-Implement: the built `output/*` where it
exists) and check all five, plus contextual consistency, recording each
finding in the same shape `gap-detection.md` uses:

```
Check: <dead end | unnecessary step | ambiguous CTA | missing feedback | inconsistent pattern | contextual consistency>
Scenario: SCENARIO-NNN
Screen(s): SCREEN-NNN [, SCREEN-NNN...]
Observation → Problem → Fix: <per the same triad craft-critique.md/
  ui-audit-framework.md already use>
Severity: <per config/output-contract.md>
Routes to: <the owning agent/file>
```

A dead end on a scenario's Primary or Recovery type is a Blocker by
default, matching `gap-detection.md`'s own severity default for those two
types.

## Explicitly not here
- Structural gaps against the spec (missing screen/transition/action/
  validation) → `gap-detection.md`.
- Single-screen composition/structural audit → `ui-engine/craft-critique.md`,
  `ui-engine/ui-audit-framework.md` (this file's findings are a distinct,
  additional pass — never a restatement of those).
- Token/component drift itself → `agents/design-system-expert.md`.
- Where findings roll up → `coverage-matrix.md`.
