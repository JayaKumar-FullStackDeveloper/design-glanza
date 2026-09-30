# Consultation Rule

## Responsibility
The mandatory "check Product Memory first" step — generalizing the
pattern every prior system already established for its own artifact type
(`design-direction.md` as mandatory input, `RF-NNN` findings as mandatory
input, `component-registry/*` checked before inventing a component) into
one explicit rule that applies to *every* decision-making step, not just
the ones a specific engine already covers.

## When this runs
Before any of the following, the acting agent scans
`product-builder/memory/product-memory.md` (and, for a decision in its own
domain, `memory/decision-records.md`'s `ADR-NNN` entries) for an existing,
`active`-status decision on the same subject:

| About to… | Check first |
|---|---|
| Name a structural/interaction-model choice (`agents/ux-architect.md`) | Prior UX-decision ADRs on this flow/screen |
| Apply a visual register/token/component (`agents/ui-designer.md`) | Prior UI/design-system/component ADRs |
| Establish or extend the token set / component inventory (`agents/design-system-expert.md`) | Prior design-system, component, and token-override ADRs |
| Confirm domain/module boundaries (`agents/product-architect.md`) | Prior architecture ADRs |
| Propose a new component (`component-registry/registry-integration.md`'s registry-first check) | Prior component ADRs, in the same lookup, not a separate one |

## What "check first" actually means
Not a formality — the check has exactly three possible outcomes, and the
acting agent states which one applies before proceeding:
1. **No prior decision on this subject** — proceed normally; the new
   decision may itself become an ADR per `auto-recording.md`.
2. **A prior decision exists and this pass agrees with it** — proceed,
   citing the existing `ADR-NNN` (or artifact) rather than re-deriving the
   reasoning from scratch.
3. **A prior decision exists and this pass would contradict it** — stop;
   this is `contradiction-prevention.md`'s supersession protocol, not a
   silent override.

Skipping the check entirely (proceeding without stating which of the
three applied) is itself the failure mode Rule 26 exists to prevent —
the same "artifacts, not conversation" discipline
`workflows/execute-product-builder.md` already requires elsewhere, applied
here to a check instead of an output.

## Scope proportionality
A trivial, narrowly-scoped change (per `design-research/research-
engine.md`'s own full-vs-lightweight threshold, reused here rather than
re-derived) may check only the specific relevant `ADR-NNN` entries its
own scope touches, not the whole memory index — a full-product memory
scan is not required to change one button's label. A genuinely new
module/flow/screen, or anything touching an existing `active` ADR's
subject, checks the relevant memory in full.

## Explicitly not here
- What happens when the check finds a genuine conflict →
  `contradiction-prevention.md`.
- The index's own shape → `memory-model.md`.
- When a new decision itself gets recorded → `auto-recording.md`.
