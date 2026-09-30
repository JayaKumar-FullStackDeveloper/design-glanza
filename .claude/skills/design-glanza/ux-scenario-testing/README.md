# UX Scenario Testing

## Responsibility
Validate a product as a complete **end-to-end user journey**, not a
collection of individually-attractive screens. Every important flow
(`FLOW-NNN`, `ux-engine/user-flow-engine.md`) is walked as one or more named
**scenarios** across a mandatory 8-type taxonomy, cross-checked for
structural completeness (missing screens/transitions/actions/validations/
feedback) and experiential continuity (dead ends, ambiguous CTAs,
inconsistent patterns, broken context), and rolled up into one **UX
Coverage Matrix**. This is the elaboration of Rule 22
(`config/operating-rules.md`) and gate **B17**
(`config/quality-gates.md`).

## What is genuinely new here, and what is not
Per the explicit instruction not to duplicate equivalent existing logic —
this engine adds exactly four things the rest of the architecture doesn't
already do, and reuses everything else by citation:

| Genuinely new | Already exists — cited, never restated |
|---|---|
| A mandatory, named 8-type scenario taxonomy walked **per flow**, not left ad hoc | The canonical flow notation and recovery-path technique → `ux-engine/user-flow-engine.md` |
| Structural gap detection cross-checking a flow's steps against the actual screen/navigation/state spec | The 13 mandatory states and their priority rule → `ux-engine/state-design.md` |
| A cross-screen continuity walk (dead ends, ambiguous CTAs, inconsistent interaction patterns, broken context) | Per-screen composition/structural audits → `ui-engine/craft-critique.md`, `ui-engine/ui-audit-framework.md` |
| The UX Coverage Matrix artifact and its own quality gate (B17) | Navigation pattern selection and the four-question wayfinding check → `ux-engine/navigation-system.md` |
| | Task completion/discoverability/error-prevention/edge-case evaluation → `methodology/test.md` |
| | Component/token drift review → `agents/design-system-expert.md` |

`ui-audit-framework.md` and `craft-critique.md` are explicit, by their own
text, about running **at Prototype's UI pass, on one finished screen**.
`methodology/test.md`'s dimensions evaluate a **feature** against user
needs. Neither walks a full scenario's *sequence* of screens end to end
checking whether the sequence itself holds together — that gap is this
folder's entire reason to exist.

## File map

| File | Owns |
|---|---|
| `scenario-model.md` | The `SCENARIO-NNN` ID scheme, and the explicit field-by-field mapping from the user's Goal/Entry/Steps/UI-interactions/System-response/Success/Failure framing onto `user-flow-engine.md`'s existing canonical notation — the same underlying model, relabeled for testing, not a second one |
| `scenario-types.md` | The 8 mandatory scenario types (primary, alternate, error, empty, loading, permission, offline, recovery), each defined against its existing owning technique |
| `gap-detection.md` | Automatically identifying a missing screen, transition, action, validation, or feedback rule for a given scenario, against the spec already produced |
| `continuity-audit.md` | Walking a scenario's actual screen sequence: dead ends, unnecessary steps, ambiguous CTAs, missing feedback, inconsistent interaction patterns, and contextual consistency (does state/filter/selection context survive navigation) |
| `coverage-matrix.md` | The UX Coverage Matrix artifact shape, its two-checkpoint gate (B17), and how a finding routes into the Quality Engine and refinement loop |
| `templates/scenario.md` | One `SCENARIO-NNN` record |
| `templates/ux-coverage-matrix.md` | The full matrix artifact |

## Explicitly not here
- The flow structure and recovery-path technique this engine walks →
  `ux-engine/user-flow-engine.md`.
- The mandatory state set and priority rule →
  `ux-engine/state-design.md`.
- Per-screen visual/structural audit →
  `ui-engine/{craft-critique,ui-audit-framework}.md`.
- Product-level validation against user needs (the 9 test dimensions) →
  `methodology/test.md` (this engine's findings are additional input to
  that evaluation, not a replacement for it).
- Navigation pattern selection itself → `ux-engine/navigation-system.md`.
