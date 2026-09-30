# Research Engine — The Mandatory Chain

## Responsibility
The mechanics of the chain every other file in this folder feeds:

```
RESEARCH → EVIDENCE → INSIGHT → DESIGN PRINCIPLE → UX DECISION → UI PATTERN → VALIDATION
```

This file states what each link means, what makes the chain *mandatory*
rather than decorative, and where it runs inside the 12-phase lifecycle.
Each link's own production technique is owned by another file, cited below.

## What each link is, concretely

| Link | Question it answers | Produced by |
|---|---|---|
| Research | What did we go look at? | `research-methodology.md` (inputs), `domain-analysis.md`, `interaction-analysis.md`, `visual-analysis.md`, `competitor-analysis.md`, `pattern-analysis.md` |
| Evidence | What did we actually observe, sourced? | `evidence-model.md` |
| Insight | What does the evidence mean about the user/task? | `insight-model.md` |
| Design Principle | What general rule follows from that insight? | `research-to-design.md` |
| UX Decision | What structural choice applies that principle here? | `agents/ux-architect.md`, `agents/interaction-designer.md` |
| UI Pattern | What concrete component/composition realizes that decision? | `agents/ui-designer.md`, `agents/design-system-expert.md` |
| Validation | Did the pattern actually solve the user's problem? | `methodology/test.md` (Test phase) |

The first four links are this folder's own scope, executed once per product
at Design Setup (and re-entered per `methodology/design-thinking.md`'s
feedback-routing table when a later finding traces back to research, not
execution). The last three links are existing pipeline stages — Prototype's
UX/UI passes and Test — now required to consume the first four rather than
reasoning from a blank page. **No new agent and no new lifecycle phase are
added** — this chain runs inside Design Setup (Step 0) through Test, the
same phases that already exist (`config/master-config.md`'s Phase registry
is unchanged).

## Why "mandatory" and not "documentation"
A chain that stops at Insight or Design Principle, with no recorded UX
Decision/UI Pattern the principle actually produced, and no Validation that
checks whether it worked, is not research feeding design — it's a research
report sitting next to a design that was made some other way. Concretely:

- Every Design Principle derived from a **Critical** or **High** priority
  finding (`research-to-design.md`'s priority classification) **must**
  appear as a cited input in the UX Decision and/or UI Pattern it implies —
  `agents/ux-architect.md`/`agents/ui-designer.md` cite the `RF-NNN` id
  directly in their own artifact, the same way they'd cite a `REQ-NNN`.
- A **Medium/Low** finding may inform a decision without being cited, or may
  be explicitly deferred with a stated reason — not every finding has to
  win, but every Critical/High one has to be accounted for, one way or the
  other.
- This is what **B16** (`config/quality-gates.md`) actually checks — not
  "was research written down," but "did a Critical/High finding produce a
  traceable downstream decision, or an explicitly recorded reason it
  didn't."

## The complexity threshold — full vs. lightweight research
Not every change needs the full chain run from scratch. Per Rule 21:

- **Full research** — a new product, a new module/feature area, or any
  screen serving a core workflow (per `methodology/empathize.md`'s frequency
  dimension and `product-intelligence/requirement-engine.md`'s priority
  field). Runs the complete chain: all four research areas
  (`domain-analysis.md`, `interaction-analysis.md`, `visual-analysis.md`,
  plus Empathize's existing User model), competitor/pattern analysis where
  references exist, and the full Finding → Insight → Principle mapping.
- **Lightweight research** — a small, already-well-understood, non-core UI
  change (e.g. "add a filter to this existing table," "restyle this
  already-approved button state"). Cites the *existing* product's own prior
  research/decisions (`product-builder/research/research-findings.md`, if
  it exists) rather than re-running the full chain — a genuinely new
  decision inside that scope still gets a real `RF-NNN` entry, it's just
  scoped narrowly, not skipped.
- **Never skip entirely** for anything Prototype will build a new screen or
  a new structural pattern for — a change with zero research behind it and
  zero prior research to cite is exactly Rule 20/21's "functional-looking
  interface with no design reasoning behind it" failure mode.

This mirrors `SKILL.md`'s own POC-safety framing ("a request that only
loosely touches product/design topics" doesn't need the whole lifecycle) —
applied here at the research-depth level, not the whole-skill-invocation
level.

## Position in the lifecycle
Runs as Design Setup's Step 0 (`workflows/design-setup.md`), before
`design-reference-engine/reference-analysis.md`'s reference detection —
research about what's generally true for this domain/user/density has to
exist before a specific supplied reference can be judged as typical or an
outlier worth deviating from (the same reasoning
`design-reference-engine/design-research.md` already stated; this file is
now that step's actual technique, not a summary of it). Produces
`product-builder/research/research-findings.md` and `research-summary.md`
as real, durable artifacts (not folded silently into `design-direction.md`
with nothing else surviving) — `design-direction.md` still cites the
Critical/High findings' Design Principles in its own Design principles
field, but the full evidence trail lives in `research/`, addressable by
`RF-NNN` from any later artifact.

## Explicitly not here
- Where each research area's own technique lives → `domain-analysis.md`,
  `interaction-analysis.md`, `visual-analysis.md`, `competitor-analysis.md`,
  `pattern-analysis.md`.
- The Evidence and Insight record shapes themselves → `evidence-model.md`,
  `insight-model.md`.
- The exact Finding → Insight → Principle → Decision → Pattern → Validation
  worked example and priority classification → `research-to-design.md`.
- The operational step order this runs inside → `workflows/design-setup.md`.
- The gate that gets checked → `config/quality-gates.md`'s **B16**.
