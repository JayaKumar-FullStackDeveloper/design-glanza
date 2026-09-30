# Competitor Analysis

## Responsibility
Applying `pattern-analysis.md`'s technique to one specific, named
competitor or reference product — used whenever the user names one
("make it work like X"), a reference screenshot is explicitly from a known
product, or the domain has one or two products so dominant that ignoring
them would be a research gap. Distinct from `design-reference-engine/
reference-analysis.md`, which extracts *this product's own direction* from
a *supplied* reference regardless of whether it's named — this file is
specifically about analyzing a **named competitor as research evidence**,
which may or may not be the same artifact as a supplied design reference.

## Classifying the competitor first
Before analyzing what a competitor does, name which of three relationships
it actually has to this product — the classification changes how much
weight its pattern carries as evidence:
- **Direct** — same audience, same core job. Its pattern choices are the
  strongest evidence (tier 6/7), since it's solving the identical problem
  for the identical user.
- **Indirect** — same audience, a different solution or workaround (a
  spreadsheet, a manual process, an adjacent tool repurposed for this
  job). Still real evidence of the underlying need, weaker evidence about
  the *specific pattern* to copy, since it wasn't purpose-built for this job.
- **Aspirational** — a different audience/domain entirely, referenced only
  for a specific pattern executed exceptionally well (a checkout flow, an
  onboarding sequence). Weakest evidence of domain fit — apply
  `pattern-analysis.md`'s Anti-Generic Design challenge especially
  rigorously here, since "it's exemplary elsewhere" is not the same claim
  as "it fits this domain."

## What to analyze, per competitor

| Analyze | Record as |
|---|---|
| What works | The specific pattern(s) that solve a real user problem — never the whole product wholesale, individual patterns |
| Why it works | The mechanism, per `pattern-analysis.md`'s deep form |
| What pattern is being used | Named precisely |
| What user problem it solves | Stated as a user need |
| Whether it's relevant to this product | The Anti-Generic Design challenge's question 4/5, applied specifically: does this product share the audience/task/domain that makes the competitor's choice work for *them*? |

## The "make it modern like X" case
A request to emulate a competitor with no more specific reason than general
admiration ("make it modern like Stripe") is weak signal on its own — per
`design-reference-engine/reference-analysis.md`'s existing treatment of an
unrelated-product reference with no stated reason to emulate it
specifically. Handle it the same way: note it, don't act on it alone: ask
(or infer from context) *which specific pattern* the user actually means,
then apply the four-part analysis to that pattern specifically, not to
"being like X" as an undifferentiated whole.

## Reconciling multiple competitors
Where more than one competitor is relevant:
- Patterns multiple competitors converge on independently are stronger
  domain-convention evidence (tier 6/7, `evidence-model.md`) than one
  competitor's idiosyncratic choice.
- Competitors that diverge on the same problem are not silently averaged —
  name the divergence and evaluate each option against this product's own
  audience/task, the same reconciliation posture `design-reference-
  engine/reference-analysis.md` already uses for conflicting supplied
  references.

## Recording the finding
A competitor-analysis finding is a normal `RF-NNN` entry
(`templates/research-finding.md`) whose Evidence field names the competitor
and the specific pattern observed, tagged at the correct confidence label
(`research-methodology.md`) — direct observation of a competitor's live
product is **Known** for what's visible, never **Known** for *why* they
made that choice (that's always Inferred at best, since the actual design
rationale usually isn't published).

## Explicitly not here
- The four-part analysis technique and the Anti-Generic Design challenge
  themselves → `pattern-analysis.md`.
- Extracting this product's own visual direction from a supplied reference
  → `design-reference-engine/reference-analysis.md`.
- How this finding maps to a Design Principle/UX Decision/UI Pattern →
  `research-to-design.md`.
