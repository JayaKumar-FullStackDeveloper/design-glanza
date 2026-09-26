# Form Design

## Responsibility
Behavioral structuring of data-entry: field grouping, step sequencing, and
validation/error behavior — the specialization of `interaction-design.md` for
the highest-stakes interaction type in most products. Visual field styling is
`ui-engine/*`'s concern.

## Data-requirement linkage
Every field in a form must trace back to a Data-type requirement
(`REQ-NNN`, `product-intelligence/requirement-engine.md`). A field with no
backing data requirement is scope creep — the same traceability discipline
`product-intelligence/traceability.md` applies to screens and components
applies at the field level too.

## Field-grouping rule
Related fields cluster by the user's mental model of the task
(`user-flow-engine.md`'s Action step this form realizes), never by database
schema/table order. Group boundaries should be nameable — if a group of fields
can't be given a short, meaningful label, the grouping is probably wrong.

## Single-page vs. multi-step decision rule
Use a multi-step form when **either**: the field count exceeds roughly 7–9
fields with natural groupings that can each stand as a step, **or** the
business logic (`product-intelligence/business-logic.md`) requires sequential,
dependent decisions (a later field's options depend on an earlier field's
value in a way that can't be resolved by simple conditional reveal). Otherwise,
use a single page — splitting a short, ungrouped form into steps only adds
navigation overhead (`user-flow-engine.md` criterion 4) without a matching
benefit. When multi-step is chosen, it uses `navigation-system.md` item 11's
stepper pattern.

## Validation-timing rule
Prefer **inline** validation (checked as the user types or on blur) over
**on-submit-only** wherever the check is cheap and doesn't need a
network round-trip — this is `user-flow-engine.md` criterion 5 (error
prevention) applied to forms directly: catching a problem before submission is
strictly better than catching it after. Reserve on-submit validation for
checks that are inherently only knowable at submission (e.g. a uniqueness
check requiring a server round-trip, or a cross-field rule spanning fields the
user hasn't reached yet in a multi-step form).

Distinguish the two validation shapes from `business-logic.md`:
- **Field-level** — checked inline, immediately, against that field alone.
- **Cross-field** — checked once both fields involved have values (not before,
  which would produce a false error while the user is still mid-entry).

## Error-messaging behavior
An error surfaces immediately adjacent to the field it concerns, not
aggregated only at the top of the form (a top-of-form summary is a supplement
for scanability, never a replacement for the inline message). An error clears
the moment its condition is resolved — it must never persist after the user
has already fixed the problem, which would contradict the system's own
feedback rules (`interaction-design.md`). Multiple simultaneous errors are all
shown at once, not one-at-a-time-on-resubmit — making the user resubmit
repeatedly to discover each new error violates minimal-user-effort
(`user-flow-engine.md` criterion 4). The message's own wording follows
`ux-writing.md`'s error-message formula — this file governs *where and
when* an error appears, not what it says.

## Required vs. optional and conditional fields
Required/optional status comes directly from the Data-type requirement's own
specification, never inferred from convention. Conditional fields (a field
that only applies given another field's value) are derived from
`business-logic.md`'s decision points and `product-intelligence/edge-case-engine.md`'s
enumerated scenarios — every condition under which a field should
appear/disappear must be named, not left to "seems like it should show up
here." Labeling convention: when most fields in a group are required, mark
the few **optional** ones explicitly instead of marking every required
field — the reverse (marking every required field when most already are)
adds visual noise without adding information.

## Loop position
Consumes flows and their Data-type requirements at the feature-level loop.
Re-entered when a Test error-prevention or usability finding (dimensions 2, 4)
traces to a form's structure or validation timing specifically, per
`methodology/design-thinking.md`'s routing table.

## Explicitly not here
- Visual field styling (borders, spacing, input component anatomy) →
  `ui-engine/component-system.md`.
- The resulting error/empty/loading state visuals → `state-design.md`
  (behavior of state) and `ui-engine/*` (visual of state).
- Underlying validation *rules themselves* → `product-intelligence/business-logic.md`.
- General (non-form) interaction behavior → `interaction-design.md`.
