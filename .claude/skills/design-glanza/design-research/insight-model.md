# Insight Model

## Responsibility
The transformation from Evidence (what was observed) to Insight (what it
means about the user or task) — the step most template-driven research
skips, going straight from "here's what we saw" to "here's what we're
building" with no stated reasoning connecting them.

## An Insight is not a restatement of Evidence
Evidence: "The reference dashboard uses a card grid for client accounts."
That is not yet an insight — it's still just an observation. An Insight
states what the observation implies about the user's actual behavior or
need:

**Insight:** "Users scan for outliers across many accounts before drilling
into one — a card grid supports parallel scanning better than a single
detail view would, for this task."

The test: an Insight must be falsifiable against user behavior, not just a
description of the UI. "Users need X" or "users do Y" — something that
could, in principle, turn out to be wrong and be caught by
`methodology/test.md`'s Validation step. "The design uses cards" is a fact
about a screen, not an insight about a person.

## Producing an Insight
1. State the Evidence plainly (`evidence-model.md`'s record).
2. Ask **why** that evidence would be true — what does it suggest about
   frequency, expertise, context, or goal (cite the matching
   `methodology/empathize.md` dimension where one applies directly)?
3. State the Insight as a claim about user behavior/need, not about the
   interface.
4. Note the Insight's own confidence: **HIGH** (multiple evidence sources
   agree, or a tier 1-3 source states the underlying need directly),
   **MEDIUM** (one credible source, reasonable inference), or **LOW**
   (a single tier 6-8 source, or evidence that only weakly supports the
   claim) — carried forward as the finding's own confidence field, per
   Rule 21.

## Insight record shape
Nested inside the `RF-NNN` finding, immediately after its Evidence
(`research.schema.json`, `templates/research-finding.md`):

```
Insight: <the falsifiable claim about user behavior/need>
Confidence: <HIGH | MEDIUM | LOW>
Derived from: <the Evidence entry/entries this reasons from>
```

## Where an Insight goes next
An Insight on its own is still not a design instruction — it becomes a
**Design Principle** only once generalized beyond this one observation
(`research-to-design.md`). Do not skip straight from Insight to a specific
UI Pattern ("so we'll use a card grid") without stating the Design
Principle in between — the principle is what makes the reasoning
reusable and auditable for the *next* screen that needs the same judgment
call, not just this one.

## Explicitly not here
- How Evidence itself is recorded → `evidence-model.md`.
- How an Insight becomes a Design Principle, then a UX Decision, then a UI
  Pattern, then gets Validated → `research-to-design.md`.
- The priority classification (Critical/High/Medium/Low) that determines
  whether a finding *must* influence the design → `research-to-design.md`.
