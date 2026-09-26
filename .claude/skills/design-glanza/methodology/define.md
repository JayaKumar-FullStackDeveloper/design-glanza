# Define

## Responsibility
Converge Empathize's findings into a sharp, falsifiable definition of the problem
being solved. This is the reasoning technique; the document that holds the result
is `templates/product-definition.md`. Define produces exactly eight outputs —
each below is a distinct thing, not a rephrasing of another.

## The 8 outputs

### 1. Problem statement
Synthesized from Empathize's pain points (dimension 5) and jobs-to-be-done
(dimension 4). Form: *"How can we help [user] achieve [goal] despite
[pain point/constraint]?"* Must name a specific user and a specific obstacle —
"make the product better" is not a problem statement, it's the absence of one.

### 2. Business objective
The measurable business outcome driving the initiative (revenue, retention, cost
reduction, compliance, risk reduction). Sourced from BRD/PRD/SOW (Rule 2 tier 1)
whenever stated explicitly; when the source is silent on *why* the business wants
this built, that silence is itself flagged as a gap and the inferred objective is
assumption-tagged, never presented as if it were stated.

### 3. User objective
The user's own definition of success — from Empathize's goals (dimension 3) and
JTBD (dimension 4) — stated independently of the business objective, because the
two do not automatically agree. Where they conflict (e.g. business wants higher
conversion friction for verification, user wants zero friction), the conflict is
named explicitly here, with the resolution technique below, not silently merged
into one objective that quietly favors one side.

### 4. Product objective
The bridge statement: what capability the product must actually deliver to move
the user objective and business objective forward together. This is "what we are
building," stated as a capability, not yet as a solution approach (that's
Ideate's job) — e.g. "let a user resolve a billing dispute without contacting
support" is a product objective; a specific flow or UI is not.

### 5. Constraints
Product/technical/business limits on the *build* — budget, timeline, technology
stack, regulatory regime, integration limits with existing systems. Distinct from
Empathize's constraints (dimension 9), which limit the *person*, not the project.
Sourced per Rule 2; a constraint invented without a source is an assumption and
must be tagged as such.

### 6. Assumptions
The consolidation point: every assumption raised anywhere in Empathize or Define
so far is aggregated here in full (per `config/output-contract.md`'s assumption
tag format), so a reviewer sees the complete set of open bets in one place rather
than scattered across upstream artifacts.

### 7. Dependencies
High-level dependencies this problem's solution will rely on — other systems,
teams, or data that must exist or be available. This is coarse and directional at
Define; the detailed dependency graph and build sequencing is
`product-intelligence/dependency-analysis.md`'s job at Architect, not this file's.

### 8. Success criteria
Falsifiable, measurable statements of "solved," each traceable to the business
objective (2) or user objective (3) it validates. This is the single most
load-bearing output of Define: it is what `test.md` measures the built result
against later — a success criterion that isn't falsifiable makes Test
unfalsifiable too.

## Conflict resolution technique
When a stakeholder need surfaced in Empathize contradicts another (two roles want
opposing things from the same flow), or the business/user objectives (outputs 2
and 3) conflict: state both sides explicitly, identify what's actually at stake
for each, and resolve toward whichever better serves the problem statement (1) —
never resolve silently by just picking one side without recording that a
trade-off was made.

## Scope-boundary technique
Distinguish "the problem we are solving now" from adjacent problems the source
material raises but that this pass isn't addressing. Deferred items are logged
(not dropped) so they resurface at the next product-level loop pass rather than
being permanently forgotten.

## Loop position
- **Entered from:** `empathize.md`'s handoff, or re-entered when a Test finding
  routes here per `methodology/design-thinking.md`'s routing table — a
  task-completion failure that isn't explained by Empathize being wrong, or a
  business-rule incorrectness that traces to a misunderstood business objective
  (output 2), or Ideate reporting no feasible direction fits the stated
  constraints (output 5).
- **Hands off to:** `ideate.md`, which generates solution directions against the
  product objective (4) and constraints (5) — Define does not itself propose a
  solution.

## Explicitly not here
- The document structure for the definition output → `templates/product-definition.md`.
- Deriving atomic testable requirements → `product-intelligence/requirement-engine.md`.
- Generating solution options → `ideate.md`.
- The detailed dependency graph → `product-intelligence/dependency-analysis.md`.
