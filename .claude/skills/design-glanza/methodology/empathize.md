# Empathize

## Responsibility
Build an accurate model of the people the product is for — not a features list
restated as a persona. This is the *technique* for building that model, generic
across input types; extracting the raw facts from a specific input artifact (a
BRD, a screenshot set) is `product-intelligence/brd-analysis.md`'s job. Every
dimension below must be filled for every actor identified in
`product-intelligence/user-roles.md`, or explicitly marked not-applicable — an
empty dimension is a gap, not a skip.

## The 11 dimensions

Each dimension is analyzed per actor, tagged per `config/output-contract.md`'s
source-vs-assumption rule (Rule 2 in `config/operating-rules.md`: explicit source
first, assumption only as last resort with impact stated).

### 1. Users
Who literally operates the product — distinct from **role** (below), which is the
permission/authority position. Two users can share a role and still differ:
segment by *usage pattern* (first-time vs. experienced, casual vs. power) because
that distinction, not the role label, is what later drives Ideate's
efficiency-vs-learnability tradeoff.

### 2. Roles
Cross-reference `product-intelligence/user-roles.md` for the RBAC structure —
Empathize does not re-derive permissions, it derives the *lived experience* of
holding the role: what the role is accountable for, what pressure it's under, and
what it risks by acting (e.g. an approver isn't just clicking a button, they're
accountable for the budget it releases).

### 3. Goals
The outcome the user is actually trying to reach. Technique: **goal laddering** —
start from a stated task ("submit an expense report") and ask "why" repeatedly
until reaching the underlying business/personal outcome ("get reimbursed without
having to follow up"). Distinguish the *stated* goal (what the source material
says) from the *underlying* goal (what laddering reveals) — both are recorded,
never silently collapsed into one.

### 4. Jobs-to-be-done
One JTBD statement per user × goal pair, in the form: *"When [situation], I want
to [motivation], so I can [expected outcome]."* This is what the product is
actually hired to do — it must name a situation and an outcome, not a feature.
Where a single job spans a longer arc, an optional finer lens is the job's own
lifecycle (define the need → locate a way to meet it → prepare → confirm →
execute → monitor → modify → conclude) — useful when "get reimbursed" turns
out to actually be several distinct moments the product should treat
differently, not one atomic action.

### 5. Pain points
Friction in the current process (an existing product, a manual workaround, or a
described absence). Distinguish **stated pain** (explicitly named in the source)
from **inferred pain** (implied by a workaround the source mentions in passing —
e.g. "users currently export to a spreadsheet to..." implies an unmet in-product
need even though no one called it a pain point).

### 6. Context
What else is happening around this interaction: is the user mid-multitask, being
interrupted, referencing another tool or document at the same time? Context
determines how much attention the interaction can assume it has.

### 7. Frequency
How often this user performs this action: daily, weekly, or rarely. This is not
a minor detail — it is the single strongest input to Ideate's
efficiency-vs-learnability tradeoff (a frequent action is designed for speed; a
rare action is designed for guidance, because the user won't have built muscle
memory for it).

### 8. Environment
The physical/technical surround: device class, network reliability, ambient
conditions (noise, lighting, being on the move), and any regulatory environment
that constrains what can even be shown or captured here. Feeds
`ui-engine/responsive-system.md` and `ux-engine/interaction-design.md`'s
input-modality rules later. Include the user's **language/script and
locale(s)** here explicitly when they involve anything beyond a single
Latin-script locale (the default `ui-engine/typography.md` and this file's
other techniques are written from) — flag it now, so a non-Latin or
multi-locale product routes to `typography.md`'s Non-Latin script typography
section and `ux-engine/localization.md` from the start, rather than needing a
correction pass after the type scale and layout are already applied.

### 9. Constraints
Real-world limits *on the user themselves* — time pressure, inability to receive
training, obligation to follow a fixed script or procedure, limited authority to
deviate from policy. This is distinct from Define's constraints (product/
technical/business limits) — this dimension is what limits the *person*, not the
*build*.

### 10. Decision-making
How this user decides, and with what authority: can they act alone, or must they
escalate? What information do they need in hand before deciding? What is their
tolerance for risk or ambiguity in that decision? This determines whether a flow
needs a confirmation step, an approval hand-off, or can proceed unattended.

### 11. Operational reality
The messy, often-undocumented actual condition of the work: the exceptions that
happen constantly (not the rare edge case — the *routine* deviation from the
happy path), current workarounds, and informal processes no BRD ever wrote down.
This dimension is the richest source for
`product-intelligence/edge-case-engine.md` later — a workaround mentioned here is
frequently tomorrow's edge case there.

## Synthesizing across multiple sources
When an actor's model is built from several sources at once (multiple
interview transcripts, multiple stakeholder documents), tag every observation
by which source it came from, and before finalizing the model check that
every source is actually represented in it — a pattern drawn from one
early, heavily-read source can otherwise dominate the model by default, not
because it's genuinely the most common finding. A pattern appearing in only
one source isn't discarded, but it's flagged as single-source rather than
corroborated, per Rule 2's source-hierarchy discipline.

## Output
One Empathy Model per actor, covering all 11 dimensions with source/assumption
tags, feeding `templates/user-persona.md` and handed to `define.md`.

## Loop position
- **Entered from:** the product-level or feature-level start of the loop
  (`methodology/design-thinking.md`), or re-entered when a Test finding is routed
  here — specifically an edge case that was never surfaced (dimension 11 was
  incomplete) or a task-completion failure traced back to a wrong understanding
  of the user's actual goal (dimension 3/4 was wrong, not just dimension-8's
  execution).
- **Hands off to:** `define.md`, which consumes the Empathy Model to synthesize a
  problem statement — Empathize does not itself state the problem.

## Explicitly not here
- Parsing a BRD/PRD/SOW into structured facts → `product-intelligence/brd-analysis.md`.
- Formal persona document structure → `templates/user-persona.md`.
- Formal role/permission modeling → `product-intelligence/user-roles.md`.
- Turning empathy findings into a problem statement → `define.md`.
