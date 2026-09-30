# Tolerance Thresholds

## Responsibility
Configurable thresholds for when a structural diff is tolerable
(a legitimate, minor evolution) vs. when it's a regression worth
flagging — expressed in **token steps**, never raw pixel deltas, since
every value is already token-addressable (Rule 23,
`design-tokens/token-schema.md`).

## Why token steps, not pixels
A raw-pixel tolerance ("flag anything over 4px") is meaningless once
values are token paths — two adjacent spacing tokens (`spacing.16` →
`spacing.24`) are always exactly 8px apart, and that 8px is either a
deliberate one-step move or it isn't; the question tolerance actually
needs to answer is **"how many scale steps away, and was the move
authorized,"** not a fixed pixel budget.

## Default thresholds, per category

| Category | Tolerable without flagging | Always flagged (Critical, regardless of steps) |
|---|---|---|
| Spacing changes | 0 steps (any token-path change is recorded) | A resolved value that isn't a valid token path at all (`design-tokens/token-audit.md`'s raw-value violation) |
| Typography changes | 0 steps for `body`/data roles (density-sensitive); ±1 step tolerable for `display`/`h1` only if the Design Direction register also changed this pass | A change that drops a numeric column out of tabular figures |
| Color deviations | 0 steps for semantic role changes; a same-role value change is tolerable **only** when it traces to a `design-tokens/token-inheritance.md`-authorized product-level palette update (a rebrand), never an unexplained one-off | A resolved value that fails `color-system.md`'s contrast rule where the baseline value passed |
| Component inconsistencies | 0 — a Registry base or variant change is always recorded | A change with no stated reason and no matching change anywhere else the same task type appears (`ux-scenario-testing/continuity-audit.md`'s inconsistent-pattern check) |
| Alignment problems | 0 steps (grid-column span is a discrete, closed set per `layout-system.md`) | N/A — always flagged when it occurs |
| Layout shifts, Missing/Unexpected elements, Responsive regressions | 0 — presence/order changes are always recorded | Always flagged when found; "tolerable" doesn't apply to a binary presence/absence fact |

**"0 steps tolerable" does not mean 0 diffs are allowed** — it means every
diff in that category is *recorded* (per `diff-detection.md`'s "not
automatically a defect" rule) and then resolved as either an approved
Baseline Update or a genuine finding; nothing in this category is ever
silently ignored as "too small to matter."

## Configuring tolerance per product
A product may tighten (never loosen below the "always flagged" column)
these defaults in `product-builder/ui/design-direction.md`'s Do/Don't
rules section — e.g. a design-system-governance-heavy product may set
Typography changes to 0 steps everywhere, including `display`/`h1`. A
loosened-beyond-default tolerance is itself flagged by
`agents/design-system-expert.md` as a decision requiring a stated reason,
never silently accepted from a product definition file.

## Explicitly not here
- The 9 categories themselves → `diff-detection.md`.
- What happens once a diff is classified out-of-tolerance →
  `severity-classification.md`.
- The approval mechanism for an intentional, tolerance-exceeding change →
  `baseline-updates.md`.
