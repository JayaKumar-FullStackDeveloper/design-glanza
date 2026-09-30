# Template: Research Finding

## Purpose
One `RF-NNN` record — the atomic unit this entire engine produces, per
`design-research/research.schema.json`'s machine-checkable shape. Every
research pass produces zero or more of these, stored in
`product-builder/research/research-findings.md`.

## Required inputs
- `design-research/evidence-model.md`'s Evidence record shape.
- `design-research/insight-model.md`'s Insight production technique.
- `design-research/research-to-design.md`'s priority classification and
  mandatory-influence rule.

## Output structure
Per finding:

```
ID: RF-NNN
Source: <input/reference/competitor this was derived from>
Area: <user | domain | interaction | visual | competitor | pattern>

Evidence:
  - Evidence: <what was directly observed/read/measured>
    Source: <input name>
    Tier: <1-8>
    Label: <Known | Assumed | Inferred | Unknown>
  [repeat per evidence item]

Observation: <the shallow, factual observation, before interpretation>
Insight: <the falsifiable claim about user behavior/need>
Confidence: <HIGH | MEDIUM | LOW>

Priority: <CRITICAL | HIGH | MEDIUM | LOW>
Design principle: <the generalized rule, if priority is CRITICAL/HIGH>
Design implication: <what this changes or confirms about the design>

Affected flow(s): <FLOW-NNN, or none yet>
Affected screen(s): <SCREEN-NNN, or none yet>
Affected component(s): <COMPONENT-NNN, or none yet>

UX decision: <citation to the artifact recording it, once made>
UI pattern: <citation to the artifact recording it, once made>
Validation: <how/when methodology/test.md will check this>

Anti-Generic Design check (only if this proposes a common/default pattern):
  Why appropriate: ...
  User problem: ...
  Evidence cited: ...
  Better pattern considered: ...
  IA consistency: ...
  Outcome: <researched-and-adopted | researched-and-rejected>

Status: <open | applied | deferred | rejected>
```

## Quality criteria
- Every field the schema marks required is filled — no blank Evidence,
  Insight, Confidence, or Priority.
- A CRITICAL or HIGH priority finding has a non-empty Design principle, and
  either a UX decision/UI pattern citation or an explicit, reasoned
  `deferred`/`rejected` status — never left `open` indefinitely once
  Prototype has run (B16, `config/quality-gates.md`).
- Confidence and Priority are independent judgments, never conflated (a
  LOW-confidence finding can still be CRITICAL priority).

## Example structure
_Illustrative, domain-neutral — not real product content._

```
ID: RF-014
Source: Competitor reference (named fintech dashboard, supplied by user)
Area: pattern

Evidence:
  - Evidence: Reference dashboard uses a status column with color+icon badge
    Source: reference screenshot, account-list screen
    Tier: 6
    Label: Known

Observation: The reference renders account status as a colored badge, first
column, every row.
Insight: Users scan for outlier accounts across many rows before reading
any single row's full detail — status has to be recognizable without
opening a row.
Confidence: HIGH

Priority: CRITICAL
Design principle: Expose status as a visually scannable attribute, never a
value requiring a click or a read of prose to discover.
Design implication: Account list screen must use a dedicated status column,
positioned early (not appended last), with badge + non-color signal.

Affected flow(s): FLOW-006
Affected screen(s): SCREEN-011
Affected component(s): (pending — Design System Expert to specify the badge
component)

UX decision: ux/screen-architecture.md, SCREEN-011 region map
UI pattern: (pending Prototype's UI pass)
Validation: methodology/test.md Test phase — task: identify 3 accounts
needing attention without opening any row.

Anti-Generic Design check:
  Why appropriate: status badges are a well-understood scanning affordance,
    not chosen merely because they're common.
  User problem: rapid outlier detection across many rows.
  Evidence cited: RF-014's own Evidence entry above.
  Better pattern considered: a sortable status column with text only —
    rejected, fails color-blind-safe scanning speed per
    ui-engine/color-system.md.
  IA consistency: consistent with the account-list IA already defined.
  Outcome: researched-and-adopted

Status: open (awaiting UX Architect's screen-architecture pass)
```

## Traceability fields
`RF-NNN` is a sideways reference (`product-intelligence/traceability.md`),
cited from `FLOW-NNN`/`SCREEN-NNN`/`COMPONENT-NNN` artifacts and from
`ui/design-direction.md` wherever this finding's Design principle applies —
never a standalone document nobody else points back to.

## Explicitly not here
- How Evidence/Insight are actually produced → `evidence-model.md`,
  `insight-model.md`.
- The priority classification's own rule and the mandatory-influence
  mechanism → `research-to-design.md`.
- The roll-up across all findings in a pass → `templates/research-summary.md`.
