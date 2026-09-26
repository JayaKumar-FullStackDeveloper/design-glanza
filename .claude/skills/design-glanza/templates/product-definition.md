# Template: Product Definition

## Purpose
The single source of truth for *what problem is being solved and why*,
before any solution, flow, or screen exists. It is the artifact that makes
Define's (and, appended, Ideate's) reasoning checkable later — every
downstream artifact that claims to serve "the product's goals" must trace
back to a specific line in this file, not a vague sense of intent. Reusable
across every domain: it holds no business rule content itself, only the
shape a problem statement takes.

## Required inputs
- An Empathy Model per actor (`methodology/empathize.md`'s 11 dimensions),
  itself built from `product-intelligence/brd-analysis.md`'s extracted facts.
- At minimum a draft problem framing — this template cannot be filled from
  nothing; if Empathize hasn't run, fill what's known and mark the rest
  pending rather than guessing ahead of the evidence.

## Output structure
- **Header** — per `config/output-contract.md`'s artifact-header shape
  (source, owning agent, version).
- **Empathy summary** — condensed Empathy Model findings per actor (full
  detail lives in `templates/user-persona.md`; this is the "why this
  matters" digest that justifies the problem statement below).
- **Problem statement** — `methodology/define.md` output 1.
- **Business objective** — output 2.
- **User objective** — output 3.
- **Product objective** — output 4.
- **Constraints** — output 5 (product/technical/business — distinct from
  Empathize's user-side constraints, which stay in the Empathy summary).
- **Assumptions** — output 6, the consolidation point for every assumption
  raised so far, each in `config/output-contract.md`'s tag format.
- **Dependencies** — output 7 (coarse, directional; the detailed graph is
  `product-intelligence/dependency-analysis.md`'s job).
- **Success criteria** — output 8.
- **In scope / explicitly out of scope** — `define.md`'s scope-boundary
  technique; deferred items logged, not dropped.
- **Chosen approach** — `methodology/ideate.md`'s output: the selected
  solution direction with its rationale and the alternatives rejected and
  why (this file is the natural home for Ideate's decision too, since it's
  still "what are we building," not yet "how it's structured").

## Quality criteria
- Every success criterion is falsifiable — checkable as true/false against
  a built product, not a feeling.
- Business objective and user objective are stated independently, never
  pre-merged into one objective that quietly favors one side; any conflict
  between them is named, not smoothed over.
- Every constraint and assumption carries a source or an
  `[ASSUMPTION: ...]` tag (`config/output-contract.md`) — nothing is stated
  as fact without one.
- The chosen approach records what was rejected and why, not just what was
  picked.
- Checked at the Define → Ideate and Ideate → Architect phase-transition
  gates (`config/quality-gates.md` Section A) before Architect proceeds.

## Example structure
_Illustrative only — placeholders, not a real product._

```
Problem statement: How can we help <actor> achieve <goal> despite <obstacle>?
Business objective: Reduce <business metric> by <target>.
User objective:     Let <actor> accomplish <task> without <friction>.
Product objective:  Provide a capability to <verb phrase>, not yet a UI.
Constraints:        <budget/timeline/tech-stack/regulatory constraint>
Assumptions:        [ASSUMPTION: <text> | BASIS: <tier> | IMPACT: <text>]
Success criteria:   <actor> can <measurable outcome> in <bounded condition>.
Chosen approach:    <approach name> — selected over <alternative(s)> because
                    <evidence per methodology/ideate.md's 8-point framework>.
```

## Traceability fields
No dedicated ID scheme of its own (one instance per product) — it is instead
the **anchor** every `REQ-NNN` cites as its Source when a requirement derives
from a stated objective rather than a direct BRD quote, and what
`product-intelligence/traceability.md` treats as the root of the trace chain
for anything not directly sourced from raw intake material.

## Explicitly not here
- The empathy technique itself → `methodology/empathize.md`.
- The define/ideate reasoning technique itself → `methodology/define.md`,
  `ideate.md`.
- Atomic, testable requirements derived from this definition →
  `templates/requirement-matrix.md`.
- Persona detail per actor → `templates/user-persona.md`.
