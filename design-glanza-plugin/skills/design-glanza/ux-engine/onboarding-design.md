# Onboarding Design

## Responsibility
The first-run experience for a new user's very first session — distinct from
`user-flow-engine.md`'s general Journey concept (which already names an
"Onboarding Journey" as an example composed of ordinary flows) in that this
file is specifically about **choosing which onboarding pattern fits**, and
the completion/activation criteria that make a chosen pattern checkable
rather than a vague "make it welcoming" goal.

## Choosing the pattern
Four named patterns, chosen by the same evidence this file's siblings use —
never defaulted to a tour/wizard out of habit:

| Pattern | Fits when | Risk if misapplied |
|---|---|---|
| **Progressive/contextual** — teach each feature at the moment it's first needed, in-place | The product's value is visible with real (or realistic) data from the first screen; most features aren't needed in session 1 | None specific — this is the default absent a reason for one of the other three |
| **Wizard** (a fixed guided setup before first real use) | Genuine required setup exists before the product is usable at all (e.g. connecting an account, defining an org's roles) — per `user-flow-engine.md`'s inherent-vs-extraneous complexity distinction, criterion 4: only justified when the setup is inherently required, not merely convenient to front-load | Turns optional configuration into a mandatory gate the user must clear before seeing any value — a common cause of first-session abandonment |
| **Sample/seeded data** | The product's value is only visible with content in it, and a genuinely empty state would show nothing meaningful (a dashboard, a workflow board, an inbox) | Sample data left ambiguous (not clearly marked as sample) is mistaken for real data — always label it and provide an explicit, single-action way to clear it |
| **Product tour** (an overlay walkthrough, not gating real use) | The product's core action is genuinely non-discoverable through its own affordances even after `ui-engine/*`'s visual-hierarchy and `information-architecture.md`'s findability heuristic are applied correctly | A tour used to compensate for an actually-undiscoverable UI is patching a design defect with narration instead of fixing the defect — check the underlying screen first |

More than one pattern can combine (a short wizard for genuinely-required
setup, followed by progressive teaching for everything else) — the table
above is chosen per-need, not as one mutually-exclusive decision for the
whole onboarding.

## Skippability
Every onboarding step beyond an inherently-required one (the Wizard row's
own justification test) must be skippable, and skipping must not block
access to the product's core action — an onboarding flow the user cannot
exit is a dead end, the same Blocker-severity defect
`user-flow-engine.md`'s Recovery paths section already treats a flow with no
path forward and no path back as being.

## Resuming interrupted onboarding
Where onboarding spans more than one session, this reuses
`navigation-system.md` item 11's existing "Resuming an interrupted workflow"
rule directly — resume at the exact uncompleted state, surface only the 1-2
still-open steps, never restart the whole sequence from the top.

## Activation, not completion
A finished onboarding flow ("the user reached the last screen") is not the
same as a successful one — define the product's actual **activation
event**: the first point the user has experienced the product's real value,
not merely clicked through its introduction (e.g. "created their first
project and invited one teammate," not "closed the welcome modal"). Name
this event explicitly during Define (`methodology/define.md`'s Success
criteria output) rather than leaving onboarding's own success condition
implicit — an onboarding flow with no named activation event cannot be
tested against `methodology/test.md`'s task-completion dimension, only
against whether its screens rendered.

## Explicitly not here
- The general Journey concept and how flows compose into one → `ux-engine/
  user-flow-engine.md`.
- Findability/depth/breadth rules a tour might be compensating for →
  `ux-engine/information-architecture.md`.
- Resuming a multi-step workflow generally → `ux-engine/
  navigation-system.md` item 11.
- Where the activation event is recorded as a success criterion →
  `methodology/define.md`.
