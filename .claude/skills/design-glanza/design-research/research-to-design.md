# Research → Design Mapping

## Responsibility
The mandatory mechanism connecting a research finding to an actual design
decision — the part of this engine that makes research an *input* to UI
generation rather than a document sitting beside it. Owns the priority
classification (which findings *must* influence the design), the worked
example, and how this connects into `product-intelligence/traceability.md`
(Product Memory).

## The full chain, worked

**Research Finding:**
Users need rapid comparison of client status across many accounts.

↓

**Insight** (`insight-model.md`):
Users scan rather than read detailed descriptions — status has to be
recognizable at a glance, across a list, without opening any one row.

↓

**Design Principle:**
Expose status as a visually scannable attribute, not a value buried in
prose or requiring a click to see.

↓

**UX Decision** (`agents/ux-architect.md`):
Use a table with a dedicated status column, positioned as the first or
second scannable column (not appended last where it competes with less
important fields for attention).

↓

**UI Pattern** (`agents/ui-designer.md`, `agents/design-system-expert.md`):
Table row + status badge component — badge carries both color and a
non-color signal (icon or label), per `ui-engine/color-system.md`'s
color-blind safety rule.

↓

**Validation** (`methodology/test.md`, Test phase):
Check whether a user can correctly identify a client's status by scanning
the list alone, without opening any row's detail view — a task-completion
and discoverability check, not merely "does the badge render."

Every step names the file/agent that actually owns producing it — this
file is the index connecting them, not a re-implementation of any one
step's technique (the same relationship `methodology/design-thinking.md`'s
design decision framework already has to Empathize/Define/Ideate/Test).

## Research priority
Every `RF-NNN` finding gets exactly one priority, independent of its
confidence label (a HIGH-confidence finding can still be low-priority; a
LOW-confidence finding about a core workflow can still be high-priority —
the two axes are not the same question):

| Priority | Meaning |
|---|---|
| **CRITICAL** | Affects a core workflow (per `methodology/empathize.md`'s frequency dimension or `product-intelligence/requirement-engine.md`'s priority field) — getting this wrong breaks or badly degrades the primary user outcome |
| **HIGH** | Materially affects usability or consistency for a frequently-used surface, short of core-workflow-breaking |
| **MEDIUM** | A real improvement opportunity, not load-bearing |
| **LOW** | A minor refinement or an edge-surface observation |

## The mandatory-influence rule
**Every CRITICAL finding, and every HIGH finding affecting a core workflow,
must produce a recorded Design Principle and a cited UX Decision and/or UI
Pattern** — checked by **B16** (`config/quality-gates.md`). Concretely:

- `agents/ux-architect.md` and/or `agents/ui-designer.md` cite the `RF-NNN`
  id directly in their own artifact wherever that finding's Design
  Principle applies (`ux/user-flows.md`, `ux/screen-architecture.md`,
  `ui/ui-rules.md`, `ui/design-system.md`) — the same way a `REQ-NNN` gets
  cited, not a separate parallel notation.
- A CRITICAL/HIGH finding with **no** cited downstream decision anywhere is
  a defect the moment Audit discovers it — an orphaned finding, the same
  category `product-intelligence/traceability.md` already treats an
  orphaned requirement or artifact as.
- A CRITICAL/HIGH finding may still be **deliberately not applied** — but
  only with an explicit, recorded reason (a conflicting, higher-tier
  requirement; a genuine technical constraint) — never silently dropped.
  This mirrors Rule 10's "explicit assumption, never silent" posture,
  applied here to research influence rather than to unknown facts.
- MEDIUM/LOW findings may inform a decision uncited, or be explicitly
  deferred — they do not trigger B16's pass/fail check, though a Minor/Note
  finding about one may still be logged per `config/quality-gates.md`'s
  persistence rule.

## Traceability — connecting to Product Memory
`RF-NNN` is a sideways reference in `product-intelligence/traceability.md`'s
model (the same category as `BR-NNN`/`EDGE-NNN`/`DEP-NNN`) — a governing
fact a requirement, flow, screen, or design-direction field cites as its
rationale, not a sixth link inserted into the `REQ → USER → FLOW → SCREEN →
COMPONENT → TEST` chain itself. Concretely: `ux/screen-architecture.md` or
`ui/design-direction.md` citing `[RF-014]` alongside a stated decision is
what makes that decision auditable later — a reviewer (or Audit) can look
up why a screen looks the way it does, not just that it was designed by
someone.

## Explicitly not here
- The Evidence/Insight record shapes → `evidence-model.md`,
  `insight-model.md`.
- Recognizing a pattern's purpose in the first place → `pattern-analysis.md`,
  `competitor-analysis.md`.
- The `RF-NNN` ID scheme's ownership and the chain-vs-sideways-reference
  distinction in full → `product-intelligence/traceability.md`.
- The B16 gate's exact pass criterion and checkpoints → `config/quality-
  gates.md`.
- Rule 21's full statement → `config/operating-rules.md`.
