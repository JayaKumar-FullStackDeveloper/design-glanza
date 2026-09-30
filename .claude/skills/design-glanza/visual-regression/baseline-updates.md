# Baseline Updates

## Responsibility
The explicit mechanism for preserving an **intentional** design change —
so a genuine improvement is never fought as a false regression on every
subsequent pass, and so a baseline is never silently overwritten by an
unreviewed change either. Reuses `ui-engine/design-system.md`'s existing
"logged system gap, absorbed or rejected" pattern (already reused, in
turn, by `design-tokens/token-audit.md`'s Token gap log) — the same
discipline, applied here to a temporal diff instead of a token.

## The record
Every Critical/High/Medium finding that a reviewer judges intentional
gets exactly this record, in `product-builder/ui/visual-baselines.md`,
before the baseline is touched:

```
Baseline update: SCREEN-NNN
Diff category: <one of diff-detection.md's 9>
Prior value: <the baseline's value/path>
New value: <the current value/path>
Reason: <why this is an intentional improvement, not an accident>
Approved by: agents/design-system-expert.md sign-off (or explicit user
  confirmation, where a user is available to ask — same posture
  design-setup-specialist.md's approval gate already uses)
Date/pass: <when>
```

**Never** a bare "accepted" with no reason — the same "IMPACT must never
be omitted" discipline Rule 10's assumption tag already enforces, applied
here to a different field name (Reason) but the identical requirement:
an approval with no stated reason is not a complete approval record.

## What happens after approval
The screen's baseline (`product-builder/ui/baselines/<SCREEN-NNN>.json`)
is updated to the new value **at the same time** the log entry above is
written — never one without the other, since an update with no log entry
is indistinguishable from a silent overwrite, and a log entry with no
actual baseline update leaves the next pass comparing against stale data.

## Graduating to a full ADR
A Baseline Update record already carries nearly the same shape an
`ADR-NNN` does (Prior value/New value/Reason/Approved by vs. Decision/
Reason/Status) — per `product-memory/contradiction-prevention.md`, one
affecting the product's overall direction (not just one screen/token)
graduates into a full ADR, indexed in `product-builder/memory/
product-memory.md`, so later passes elsewhere in the product see it too.
A narrow, single-screen update stays exactly as described below.

## Batch updates (a deliberate redesign)
Where a pass deliberately touches many screens at once (a rebrand, a
density-register change), each affected screen still gets its own record
above — a single blanket "redesign, ignore all diffs this pass" is not an
acceptable substitute, per the same "artifacts, not conversation"
discipline `workflows/execute-product-builder.md` already applies
everywhere. `workflows/redesign-product.md`'s existing Protected-Contracts
concept governs which screens are in scope for such a pass; this file
governs how each one's baseline is actually updated once the pass
completes.

## What must never happen
- A regression finding silently reclassified as "accepted" with no Reason
  field — this is exactly Rule 10's no-invented-facts discipline, applied
  to approvals instead of assumptions.
- A baseline overwritten by a pass that hasn't yet passed
  `visual-benchmark.md`'s own mandatory refinement cycle for that screen
  — an unconfirmed draft is never captured as the new "known-good" state.
- A Critical finding (a missing element on a core workflow) approved via
  this mechanism without also re-confirming the affected
  `ux-scenario-testing/*` scenario still walks cleanly — a baseline
  update never bypasses B17's own walked checkpoint.

## Explicitly not here
- The severity labels being approved/reclassified →
  `severity-classification.md`.
- The baseline's own stored shape → `baseline-model.md`,
  `templates/visual-baseline.md`.
- The redesign-scope concept this composes with →
  `workflows/redesign-product.md`.
