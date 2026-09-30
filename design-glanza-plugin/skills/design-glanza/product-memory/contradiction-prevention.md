# Contradiction Prevention

## Responsibility
The one supersession protocol every prior system's own "logged, not
silent" exception mechanism now composes under — so "prevent
contradictory UI patterns unless a new ADR explicitly supersedes the
previous decision" is a single, checkable rule, not four independently-
worded ones.

## The protocol
A change that contradicts an `active`-status `ADR-NNN` (or an existing
decision recorded only in its own artifact, per `memory-model.md`'s
index) is valid **only** when all three hold:
1. A new `ADR-NNN` is recorded, with a `Supersedes: ADR-<old>` field.
2. The new ADR's Reason field states why the old decision no longer
   holds — not merely that a different choice is preferred now.
3. The old ADR's Status is updated to `superseded` (never deleted, never
   silently left `active` while contradicted in practice).

A contradiction with any of the three missing is a defect
(`config/quality-gates.md`'s **B21**), regardless of whether the new
choice is actually better — the point is that "actually better" has to be
argued and recorded, not asserted by simply building the different thing.

## How this composes with every prior system's own mechanism
None of these are replaced — each already does exactly step 1-3 above for
its own artifact type; this file is what makes that pattern's *name* and
*requirement* explicit and shared:

| Prior mechanism | Is already this protocol, applied to… |
|---|---|
| `ui-engine/design-system.md`'s "logged system gap, absorbed or rejected" | A token/component deviation |
| `design-tokens/token-audit.md`'s Token gap log | A raw-value token deviation specifically |
| `component-registry/registry-integration.md`'s registry-first check | A component choice that departs from the master registry |
| `visual-regression/baseline-updates.md`'s Baseline Update record | A structural diff from a screen's prior confirmed-clean state |
| `methodology/ideate.md`'s rejected-approaches register | A whole-approach reconsideration at the product/feature level |

**A Baseline Update or Token gap that affects the product's overall
direction (not just one screen/token) graduates into a full `ADR-NNN`** —
the two record shapes are already nearly identical (Prior value/New
value/Reason/Approved by vs. Decision/Reason/Status), and this is the one
place they explicitly connect: a narrow, single-artifact exception stays
in its own log; a decision that changes what's true for the *product*
going forward gets the full ADR treatment so later passes elsewhere in
the product see it too, not just the one screen/token file it originated
in.

## What counts as "contradictory," concretely
Two decisions are contradictory when they govern overlapping
`Related` citations (the same `SCREEN-NNN`/`COMPONENT-NNN`/`FLOW-NNN`)
with incompatible Decision fields — e.g. one ADR says "use a Drawer for
record detail" and another, still `active`, says "use a Modal for the
same record detail" with no supersession link between them. Two ADRs
governing genuinely different scope are not contradictory even if their
Decisions differ (a Drawer for the customer module, a Modal for a
one-off confirmation elsewhere) — scope, not surface similarity, is what
determines conflict.

## Explicitly not here
- The ADR record shape itself → `adr-schema.md`.
- Detecting a *structural* (non-semantic) inconsistency automatically →
  `scripts/validate-memory.py` (checks ID/status integrity and flags
  *overlapping-Related, no-supersession* pairs for review — it does not
  itself judge whether two decisions are semantically contradictory).
- The gate this enforces → `config/quality-gates.md`'s **B21**.
