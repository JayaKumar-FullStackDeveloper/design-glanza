# Template: Competitor Analysis

## Purpose
One named-competitor analysis instance, per
`design-research/competitor-analysis.md`'s technique — produced only when a
specific competitor/reference product is actually named or supplied, not a
mandatory artifact for every product.

## Required inputs
- `design-research/pattern-analysis.md`'s four-part analysis technique and
  Anti-Generic Design challenge.
- The competitor's supplied reference (screenshot, link, named product) or
  the user's own naming of it.

## Output structure
- **Header** — per `config/output-contract.md`.
- **Competitor/reference named** — the product, and how it was supplied
  (user-named, screenshot, or inferred from context).
- **Why this competitor is relevant** — the stated reason to analyze this
  one specifically (shares audience/domain/task with this product,
  user explicitly referenced it, or it's domain-dominant enough that
  omitting it would be a research gap) — never analyzed just because it's
  well-known.
- **Per pattern observed** (repeat per pattern, not per screen):
  - **What pattern is being used** — named precisely.
  - **What works** — the specific mechanism, not the whole product.
  - **Why it works** — per the shallow-vs-deep test.
  - **What user problem it solves.**
  - **Relevance to this product** — the Anti-Generic Design challenge's
    questions 4/5, answered concretely.
  - **Resulting `RF-NNN`** — the finding ID this observation was recorded
    as, once written.

## Quality criteria
- No pattern observation stops at naming the pattern (`pattern-analysis.md`'s
  shallow-vs-deep test) — every entry states the mechanism and the user
  problem, not just what was seen.
- Where more than one competitor is analyzed, convergent patterns are
  flagged as stronger evidence; divergent patterns are named as a conflict,
  not silently resolved to one.

## Example structure
_Illustrative, domain-neutral — not real product content._

```
Competitor: [named fintech product], supplied as a screenshot reference by
the user for "the transactions list specifically."

Why relevant: user explicitly referenced this screen; product shares this
product's audience (finance-adjacent professionals reviewing transaction
volume) and task (rapid status triage).

Pattern: status badge, first column, dense table row.
What works: badge is recognizable at a glance across dozens of rows.
Why it works: color+icon combination separates "needs attention" rows from
the rest without requiring the user to read any cell content.
User problem solved: triage-by-status across high row volume.
Relevance: directly relevant — this product's primary user task is the same
triage pattern, at similar or higher row volume.
Resulting finding: RF-014.
```

## Explicitly not here
- The four-part analysis technique and Anti-Generic Design challenge
  themselves → `design-research/pattern-analysis.md`,
  `design-research/competitor-analysis.md`.
- Extracting this product's own visual direction from a supplied reference
  (a distinct, non-overlapping extraction) → `design-reference-engine/
  reference-analysis.md`.
- The finding record's own full shape → `templates/research-finding.md`.
