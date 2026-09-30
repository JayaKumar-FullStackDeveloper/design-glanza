# Severity Classification

## Responsibility
The Critical/High/Medium/Low classification for a regression finding —
and its explicit, fixed mapping onto `config/output-contract.md`'s one
shared Blocker/Major/Minor/Note vocabulary, so this is a domain-specific
refinement of that scale, never a second, competing one (the same
reconciliation `design-research/research-to-design.md` already
established for CRITICAL/HIGH/MEDIUM/LOW research-finding priority, and
`ui-engine/craft-critique.md` already established for its own
pass/minor-issue/major-issue rating).

## The mapping

| This system's label | Maps to (`output-contract.md`) | When it applies |
|---|---|---|
| **Critical** | Blocker | A missing element on a core-workflow screen (`ux-scenario-testing/scenario-types.md`'s Primary/Recovery scenarios); any diff resolving to a non-token raw value; a color deviation that breaks the contrast rule where baseline passed |
| **High** | Major | An unexpected element with no Design Direction justification; a component-inconsistency with no stated reason; a responsive regression on any breakpoint |
| **Medium** | Minor | An in-tolerance-adjacent (1 step) spacing/typography change with no recorded Baseline Update yet; an alignment problem on a non-primary region |
| **Low** | Note | A recorded, still-pending-review diff that's plausibly intentional (e.g. likely part of an in-progress rebrand) but not yet confirmed via `baseline-updates.md` |

## Why a finer scale here specifically
The shared four-level scale is calibrated for "does this block the gate."
A regression finding additionally needs to communicate **how far** from
baseline something drifted, because that's what determines whether a
human reviewer should treat it as an obvious bug (Critical — a missing
button) or a plausible intentional evolution worth a quick confirmation
(Low — a slightly bolder heading). Collapsing that distinction into just
Blocker/Major/Minor/Note would either over-block minor drift or
under-flag real regressions; the finer label is what
`templates/visual-diff-report.md` actually shows a reviewer, while the
mapped Blocker/Major/Minor/Note value is what `config/quality-gates.md`
actually gates on — one finding, two labels, never two independent
severities that could disagree.

## Escalation and de-escalation
A Medium/Low finding that recurs across multiple consecutive passes with
no Baseline Update escalates to High — an unresolved "maybe intentional"
drift left hanging for several passes is itself a process failure, not a
permanently-tolerable state. A Critical/High finding that gets an
approved Baseline Update (`baseline-updates.md`) is reclassified
**reviewed — accepted** and drops out of the active findings list
entirely, not merely down-graded to Low.

## Explicitly not here
- The severity vocabulary itself → `config/output-contract.md`.
- The 9 diff categories this classifies → `diff-detection.md`.
- The tolerance thresholds that decide whether a diff needs classifying at
  all → `tolerance-thresholds.md`.
