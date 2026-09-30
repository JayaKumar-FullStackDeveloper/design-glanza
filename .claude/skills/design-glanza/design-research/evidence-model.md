# Evidence Model

## Responsibility
What counts as evidence, ranked by the same source-of-truth discipline every
other Design-Glanza fact already uses, and the record shape one piece of
evidence takes before it can become an Insight (`insight-model.md`).

## Evidence, ranked
Reuses Rule 2's existing 8-tier order (`config/operating-rules.md`) rather
than inventing a second, competing priority system — the same reconciliation
`product-intelligence/domain-standards.md` already chose for its own tier-6
placement:

| Tier | Evidence source | Example |
|---|---|---|
| 1-2 | Explicit BRD/PRD/acceptance criteria | "The BRD states managers must approve requests over $500" |
| 3 | Existing product behavior (redesign) | "The current app already uses a status column with color badges" |
| 4 | Existing design system | "The current token set already has a `warning` semantic color" |
| 5 | Existing code | "The codebase's validation logic caps the approval threshold at $500" |
| 6 | Domain conventions (`product-types/*.md`, `domain-standards/`) | "Fintech transaction lists conventionally show status as the first scannable column" |
| 7 | Design best practice (`ux-engine/*`, `ui-engine/*`) | "Tables with >7 columns conventionally support column visibility toggling" |
| 8 | Reasonable assumption, last resort | "Assumed most users triage by status first, since no analytics were supplied" |

A competitor/reference analysis (`competitor-analysis.md`) sits at tier 6 or
7 depending on whether it's evidencing a *domain* convention or a general
*best-practice* pattern — stated explicitly per finding, never left
ambiguous which tier a piece of evidence actually occupies.

## What is not evidence
- A personal design preference with no cited source — that's tier 8 at
  best, and must be labeled **Assumed**, never presented as Known.
- "Everyone does it this way" with no named source — this is exactly the
  weak-signal case `design-reference-engine/reference-analysis.md` already
  treats cautiously ("a reference to an unrelated product with no stated
  reason to emulate it"); noted, not acted on alone.
- A pattern that's merely currently fashionable — `ui-engine/visual-
  trends.md`'s adoption gate and Rule 11 govern this separately; evidence
  that a pattern is *trending* is not evidence that it's *appropriate* for
  this product (see `pattern-analysis.md`'s Anti-Generic Design challenge).

## Reading behavioral/analytics data
Existing-product behavioral data (tier 3, "existing product behavior") is
evidence, not proof, on its own — before treating a number as a finding,
check: the event actually measures what its name implies (not a proxy that
drifted from the label over time); the denominator hasn't silently moved
(a rate whose base changed mid-period reads as a trend that isn't real);
the "step" in a funnel is a genuine user action, not an implementation
artifact (a page-load event isn't the same as task intent); a release or
date-range change isn't confounded with the metric's own movement; and a
platform/segment split isn't masking two opposite trends that average out
to a flat-looking aggregate. Read the data's actual *shape* (a cliff, a
gradual slope, a bimodal split) before summarizing it as one number — a
median or mean can misrepresent a bimodal distribution entirely. None of
this replaces `research-methodology.md`'s Known/Assumed/Inferred/Unknown
labels — a number that passes all five checks is still labeled per that
model, not treated as automatically Known.

## Reconciling qualitative and quantitative sources
Beyond Rule 2's tier order (a higher tier wins when two sources conflict):
behavioral/analytics data (tier 3) and interview/qualitative research
(tier 6–8, domain convention or direct empathy findings) usually answer
*different questions*, not competing versions of the same one —
quantitative data is strongest for **what** is happening and **how
often**; qualitative research is strongest for **why**; and neither alone
answers whether a feature is worth building at all (that needs both,
triangulated, plus Define's own success-criteria framing). Treat a
qual/quant "conflict" as a signal to check which question each source
was actually answering before assuming one must be wrong.

## Multi-source synthesis (cite, don't restate)
Where a finding is built from more than one source of the same kind
(several interview transcripts, several stakeholder documents),
`methodology/empathize.md`'s own "Synthesizing across multiple sources"
rule already governs this — tag every observation by source, verify every
source is actually represented before finalizing, and flag a
single-source pattern as such rather than letting an early, heavily-read
source dominate by default. This file's own research passes follow that
same rule; it is not restated here as a second, separately-worded version.

## Evidence record shape
One entry per piece of evidence, nested inside the `RF-NNN` finding it
supports (`research.schema.json`, `templates/research-finding.md`):

```
Evidence: <what was directly observed/read/measured>
Source: <input name/file/reference, or the domain-standard/convention cited>
Tier: <1-8, per the table above>
Label: <Known | Assumed | Inferred | Unknown>
```

A finding can cite more than one piece of evidence — where two pieces of
evidence at different tiers conflict, the higher tier wins per Rule 2,
stated explicitly rather than silently averaged (the same reconciliation
posture `design-reference-engine/reference-analysis.md` already applies to
conflicting references).

## Explicitly not here
- How evidence becomes an Insight → `insight-model.md`.
- Where evidence comes from, area by area → `research-methodology.md`,
  `domain-analysis.md`, `interaction-analysis.md`, `visual-analysis.md`.
- The assumption-tag literal format → `config/output-contract.md`.
- The trend-adoption gate → `ui-engine/visual-trends.md`.
