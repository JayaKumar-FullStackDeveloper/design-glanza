# Design Thinking — The Engine

## Responsibility
This is not an index of five phases run once. It is the loop that makes
Design-Glanza reason like a designer instead of a document-to-screen compiler:
**Empathize → Define → Ideate → Prototype → Test**, re-entering earlier phases
whenever Test finds that an earlier phase's understanding — not just its
execution — was wrong. A phase's own technique lives in its own file
(`empathize.md`, `define.md`, `ideate.md`, `prototype.md`, `test.md`); this file
owns the mechanics that make the five connect as a loop instead of a checklist.

## Why a checklist is not enough
A checklist is satisfied once, in order, and stays satisfied. This engine is not:
every "Test" evaluation in `test.md` is a live check against Empathize/Define/
Ideate, run again after every change, at every granularity down to a single
screen. A feature is not "done with design thinking" after one pass through the
five phases — it is done when a Test pass finds nothing left to route backward.
This is the mechanical form of Rule 12 (Self-Critique) and Rule 13 (Iteration) in
`config/operating-rules.md`.

## The loop

```
   ┌─────────────────────────────────────────────────────────────┐
   │                                                               │
   ▼                                                               │
EMPATHIZE ──▶ DEFINE ──▶ IDEATE ──▶ PROTOTYPE ──▶ TEST ────────────┘
   ▲             ▲          ▲           ▲           │
   │             │          │           │           │
   └─────────────┴──────────┴───────────┴───────────┘
         re-entry, routed by WHAT Test found wrong
```

Forward motion (solid arrows, left to right) is the default direction. Backward
motion (the return edges) is not a failure of the process — it *is* the process.
A pass through all five phases with zero backward routing is the exception, not
the expectation, especially on a first pass through a novel feature.

## Granularity: this loop runs at three nested scales

1. **Product-level loop** — runs once, early, to establish the product's overall
   direction (the pass that produces `templates/product-definition.md` and the
   chosen Ideate direction that feeds Architect). Coarse-grained; gets the shape
   of the whole product roughly right.
2. **Feature-level loop** — runs once per feature/flow, independently. Feature A
   can be in Test while feature B is still in Empathize — features do not wait
   for siblings to finish their loop. This is where most of the work happens.
3. **Screen-level micro-loop** — within Prototype/Test, a single screen can cycle
   Prototype → Test → Prototype without re-running Empathize/Define/Ideate, as
   long as the finding is about *execution* (this screen's structure/interaction/
   state) and not about *understanding* (the wrong user, the wrong problem, the
   wrong approach). See the routing table below for how that distinction is made
   mechanically, not by feel.

A change discovered at a finer grain that turns out to invalidate a coarser-grain
decision (e.g. a screen-level Test finding reveals the whole feature's approach is
wrong) escalates outward — it routes to the coarser loop's Ideate or Define, not
just the screen.

## Feedback routing table

Every `test.md` evaluation dimension routes a failure to exactly one primary
phase (occasionally a secondary one), based on *what kind of wrong* was found —
not on which dimension happened to catch it:

| Test finding | Routes to | Why |
|---|---|---|
| Task completion failure | Define (primary), Ideate (if Define holds) | The user couldn't finish the job — either the problem was mis-stated or the chosen approach can't deliver it |
| Business-rule incorrectness | Define + `product-intelligence/business-logic.md` | The design doesn't embody the actual rule — the rule was misunderstood, not just misdrawn |
| Usability heuristic failure | Prototype (primary), Ideate (if the interaction model itself is the cause, not its execution) | Usually an execution problem within the chosen approach |
| Discoverability failure | Prototype (`ux-engine/information-architecture.md`, `navigation-system.md`) | Structural placement problem, not a wrong-approach problem |
| Error prevention gap | Prototype (`ux-engine/state-design.md`) or Define (if the constraint that would have prevented it was never captured) | Usually a missed state; occasionally a missed constraint |
| Feedback gap | Prototype (`ux-engine/interaction-design.md`) | Execution: an interaction rule wasn't actually applied |
| Accessibility failure | Prototype (structural) or `ui-engine/color-system.md` (perceptual) | Almost never an Ideate-level problem unless the interaction model has no accessible equivalent by construction (see `ideate.md`) |
| Responsiveness failure | Prototype (`ui-engine/responsive-system.md`) | Execution problem within the chosen layout pattern |
| Edge case failure | Empathize (if the case was never surfaced) or Prototype (if surfaced but not designed for) | Distinguish "we didn't know" from "we knew and skipped it" |

Routing to Empathize or Define is rare and should be treated as a signal worth
surfacing explicitly in the phase-completion report (`config/output-contract.md`)
— it means earlier work must be revisited, not just patched.

## Loop termination

A loop (at whatever granularity) terminates when `test.md`'s evaluation across
all nine dimensions returns no Blocker or un-waived Major finding (severity
vocabulary in `config/output-contract.md`), which is also the condition
`config/quality-gates.md`'s Test → Audit gate checks. It does not terminate
because a fixed number of cycles has been run.

**Escalation, not infinite looping:** if the same finding survives more than two
Prototype → Test cycles at the same scope without resolving, that is a signal the
problem is actually one level up (Ideate's approach, or Define's problem framing)
and must be escalated there rather than iterated on indefinitely at Prototype —
per the question-vs-proceed decision rule in `config/operating-rules.md`, this is
a point to surface to the user rather than keep silently cycling.

## Relationship to the 10-phase production pipeline

This 5-phase loop is not confined to phases 2–4 of the 10-phase pipeline
(`config/master-config.md`'s phase registry). It is the reasoning engine running
*underneath* Architect through Iterate at feature/screen granularity, continuously,
while the 10-phase pipeline is the once-per-product macro sequence
(`workflows/create-product.md`) that the loop operates inside of. Architect
kicks off the product-level pass; Implement and Audit are where feature-level and
screen-level loops are still actively cycling, not where they've already finished.

## The design decision framework

A single, citable chain for walking one decision start-to-finish — synthesized
from Empathize's, Define's, Ideate's, and Test's own techniques, not a
replacement for any of them (each still owns its actual method; this is the
index tying them together, the same relationship this file already has with
the five phases as a whole):

```
Problem → Context → User Need → Constraints → Alternatives → Trade-offs → Selected Approach → Expected Outcome → Validation
```

| Step | Produced by |
|---|---|
| Problem | Define output 1 (`methodology/define.md`) — the problem statement |
| Context | Empathize dimensions 6–8 (`empathize.md`) — context, frequency, environment |
| User Need | Empathize dimensions 3–4 (goals, JTBD) + Define output 3 (user objective) |
| Constraints | Define output 5 (`define.md`) — constraints |
| Alternatives | Ideate's divergence step — at least 3 structurally different approaches (`ideate.md` item 1); for a UX/UI pattern decision specifically, evidenced by `design-research/research-to-design.md`'s Finding → Insight → Design Principle chain rather than reasoned from a blank page (Rule 21) |
| Trade-offs | Ideate's scoring against criteria 3–7 (efficiency, cognitive load, scalability, accessibility, implementation complexity) |
| Selected Approach | Ideate's evidence-based selection (item 8) — including what was rejected and why |
| Expected Outcome | Define output 8 — success criteria, checked against the selected approach |
| Validation | Test's nine-dimension evaluation (`methodology/test.md`) — whether the expected outcome actually occurred; the same step satisfies `design-research/research-to-design.md`'s own Validation link for any research finding this decision applied |

This is a naming/indexing convenience, not a new phase or a new technique —
every step's substance is exactly what its cited file already does. Reach for
this chain when a decision needs to be walked start-to-finish in a review or
audit conversation; use the phase files directly for doing the actual work.

**For a significant decision, this chain is now also persisted, not just
walked in conversation** (added v1.0.15, Rule 26): `product-memory/
adr-schema.md` gives this exact same nine-step reasoning an ID, a status,
and a durable home (`ADR-NNN`) — Problem/Context/Alternatives/Trade-offs/
Selected Approach/Expected Outcome map directly onto an ADR's fields;
Validation stays owned by `methodology/test.md`'s own re-run Test phase,
never frozen into the ADR itself. A decision walked here without ever
being persisted is exactly what `product-memory/auto-recording.md` exists
to prevent for anything meeting its significance threshold.

**For a specific, important UX/UI pattern decision** (not a whole-product
decision), the same 9 steps get applied with concrete teeth — 12 weighing
factors, an anti-fashion gate, and a worked example distinguishing real
reasoning from reasoning-shaped prose: `methodology/design-judgment.md`.
That file is the applied engine; this section remains the general index.

## The 10-phase lifecycle remains authoritative

Nothing above changes the enforced production lifecycle. `config/
master-config.md`'s phase registry — `INTAKE → EMPATHIZE → DEFINE → IDEATE →
ARCHITECT → PROTOTYPE → IMPLEMENT → TEST → AUDIT → ITERATE` — is unchanged and
remains the single authoritative sequence. The design decision framework above
is a cross-phase index describing *how a decision gets made* within that
lifecycle, not a competing or parallel process: Problem/Context/User Need map
into Empathize/Define, Alternatives/Trade-offs/Selected Approach map into
Ideate, Expected Outcome maps into Define, and Validation maps into Test — all
inside the same 10 phases, none of them added to, removed, or reordered.

## Explicitly not here
- Any single phase's analytical technique → its own file in this folder.
- The operational, tool-calling procedure that invokes this engine →
  `workflows/create-ux.md`, `create-ui.md`, `build-product.md`, `audit-product.md`.
- Gate pass/fail criteria → `config/quality-gates.md`.
- The canonical phase registry itself → `config/master-config.md`.
- The applied, factor-weighted engine for a specific important UX/UI pattern
  decision → `methodology/design-judgment.md`.
