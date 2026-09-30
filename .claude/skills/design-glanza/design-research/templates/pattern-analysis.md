# Template: Pattern Analysis

## Purpose
One UI/UX pattern analysis instance, per
`design-research/pattern-analysis.md`'s technique — used for a general
(not competitor-specific) pattern under consideration, e.g. one surfaced by
`domain-analysis.md`, `interaction-analysis.md`, or `visual-analysis.md`
research rather than tied to one named product. Distinct from
`templates/competitor-analysis.md`, which is always tied to a specific
named competitor/reference.

## Required inputs
- `design-research/pattern-analysis.md`'s four-part analysis technique and
  Anti-Generic Design challenge.
- The research area that surfaced this pattern as a candidate
  (`domain-analysis.md`, `interaction-analysis.md`, or `visual-analysis.md`).

## Output structure
- **Header** — per `config/output-contract.md`.
- **Pattern named** — precisely, not a vague description.
- **Surfaced by** — which research area/file raised this as a candidate.
- **What user problem it solves.**
- **Why it works** — the mechanism (shallow-vs-deep test).
- **Anti-Generic Design challenge**, all five questions answered:
  1. Why is this pattern appropriate for this specific product?
  2. What user problem does it solve, concretely?
  3. What evidence supports it (cite the `RF-NNN` evidence)?
  4. Is there a better pattern for this domain — what alternative was
     actually considered?
  5. Is it consistent with this product's information architecture?
- **Outcome** — researched-and-adopted or researched-and-rejected, with the
  reason either way.
- **Resulting `RF-NNN`.**

## Quality criteria
- All five Anti-Generic Design questions are answered, not just the
  conclusion recorded — a "yes, this is fine" with no stated reasoning
  fails this template's own bar, the same way an unstated domain
  classification fails `domain-classifier.md`'s.
- A rejected pattern's reason is specific enough that a later reviewer
  understands why it was rejected without re-deriving the analysis.

## Example structure
_Illustrative, domain-neutral — not real product content._

```
Pattern: Kanban board for pipeline-stage work items.
Surfaced by: domain-analysis.md (this domain's workflows are pipeline-
shaped: intake -> review -> approved -> closed).

User problem solved: seeing where every item sits in a multi-stage process
at a glance, and moving an item forward without navigating away.
Why it works: spatial position encodes stage, removing the need to read a
status field per item; drag-to-advance matches the mental model of
"physically moving something along."

Anti-Generic Design challenge:
  1. Appropriate?: yes — this domain's workflow is genuinely stage-based,
     not just listable.
  2. User problem: tracking work-item stage across a multi-step process.
  3. Evidence: RF-021 (domain workflow research) confirms a 4-stage
     pipeline is the domain norm.
  4. Better pattern considered: a filterable list grouped by stage —
     rejected, loses the at-a-glance cross-stage view a kanban board gives
     for free.
  5. IA consistency: consistent — the sitemap already groups this module by
     stage, not by another axis.

Outcome: researched-and-adopted.
Resulting finding: RF-021.
```

## Explicitly not here
- The four-part analysis technique and Anti-Generic Design challenge
  themselves → `design-research/pattern-analysis.md`.
- A named-competitor version of this same technique →
  `templates/competitor-analysis.md`.
- The finding record's own full shape → `templates/research-finding.md`.
