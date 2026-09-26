# Prototype

## Responsibility
Realize Ideate's chosen approach as concrete structure — at the *lowest fidelity
that can still be tested*, per the fidelity ladder below. Prototype defines six
specific outputs; each is produced by inhabiting the relevant `ux-engine/*` or
`ui-engine/*` technique at prototype fidelity, not by re-deriving that technique
here. This is the mechanical enforcement point of Rule 4 (UX before UI) and
Rule 5 (System before screen) in `config/operating-rules.md`.

## Fidelity ladder
- **Low** — structure only: flow steps, IA hierarchy, screen regions. No real
  visual system, placeholder content acceptable.
- **Mid** — layout + real content, still no final visual system (`ui-engine/*`
  not yet applied at high fidelity).
- **High** — full `ui-engine/*` visual system applied.

Not every output below needs to reach High fidelity before Test runs — see the
per-output fidelity note. Rule 4 specifically means: information architecture and
interaction problems are diagnosed and fixed at Low/Mid fidelity; do not reach for
`ui-engine/*` to paper over a structural problem still visible at Low fidelity.

## The 6 outputs

### 1. User flow
Produced by `ux-engine/user-flow-engine.md`'s technique, applied to Ideate's
chosen approach for this feature, filled into `templates/user-flow.md`.
**Fidelity: Low.** A flow is testable as soon as its steps and branches are
named — no screen needs to exist yet to validate that the sequence itself makes
sense against Define's success criteria.

### 2. Information architecture
Produced by `ux-engine/information-architecture.md`, filled into
`templates/sitemap.md`. **Fidelity: Low.** Grouping and hierarchy are validated
by asking whether a user could find a given item by its label alone — no visual
treatment required to test this.

### 3. Screen architecture
Produced via `templates/screen-architecture.md`'s region map — which zones exist
on a screen and what job each does, referencing `ui-engine/layout-system.md`'s
named composition patterns only by name (e.g. "list+detail"), not by applying
their spacing/grid values yet. **Fidelity: Low → Mid.** This is the point where
"how many screens, and what's the shape of each" gets fixed before content and
components multiply across them (Rule 5: system before screen).

### 4. Interaction model
The interaction model chosen at Ideate is concretized into actual per-action
behavior specs for this feature's real screens, using `ux-engine/
interaction-design.md` (general behavior) and `ux-engine/form-design.md` (if the
feature involves data entry). **Fidelity: Mid.** Needs real content/fields to be
concrete, but not a final visual system — a feedback rule can be validated as
"user sees a confirmation within 200ms" before that confirmation has its final
visual design.

### 5. State model
Every state Rule 6 requires (`config/operating-rules.md`: initial, loading,
success, empty, validation error, system error, permission denied, processing,
completed, cancelled, conflict, timeout where applicable) is enumerated for this
feature's screens using `ux-engine/state-design.md`, consuming
`product-intelligence/edge-case-engine.md`'s output for this feature, filled into
`templates/state-matrix.md`. **Fidelity: Low is sufficient to enumerate; Mid to
specify each state's behavior.** This is the direct enforcement point of Rule 6 —
a screen architecture (output 3) is not complete until its state model exists
alongside it, not as an afterthought once the screen "looks done."

### 6. Component requirements
Identify which components this feature needs — existing reusable ones from
`ui-engine/component-system.md`'s current inventory, versus genuinely new ones —
without designing the new ones' final visuals yet. **Fidelity: Low.** This is a
requirements list, not a component spec; `agents/design-system-expert.md`'s
reuse-vs-new-variant rule is applied here to catch avoidable component
proliferation before high-fidelity work invests in it.

## Evaluating at realistic scale
When a prototype output is reviewed against `test.md` (at any fidelity),
judge it at the scale/context it will actually be used in — full viewport,
realistic content volume, actual device class where relevant — never at
thumbnail/postage-stamp scale. A hierarchy or density problem that's invisible
zoomed out is exactly the kind of defect Rule 4/5 exist to catch before
Implement, and it is only visible at real scale.

## Sequencing rule
Within a feature, prototype the screen/flow carrying the *riskiest, least-proven
assumption* first — not necessarily the screen a user sees first. Validating the
risky part early means a Test failure there is caught before the rest of the
feature is built around a wrong premise.

## Stop condition
A given output above stops iterating at Prototype once it has done its job:
validated the assumption it existed to test, per `methodology/test.md`'s
evaluation. Continuing to polish past that point is Implement's job (moving
toward High fidelity and real build), not Prototype's.

## Redesign variant
For an existing product (`workflows/redesign-product.md`), the current live
product often **is** the Low-fidelity baseline for outputs 1–3 already — Prototype
here starts by evaluating that baseline against `test.md` directly, rather than
building a new Low-fidelity pass from nothing.

## Loop position
- **Entered from:** `ideate.md`'s handoff (chosen approach), or re-entered when a
  Test finding routes here per `methodology/design-thinking.md`'s routing table —
  usability, discoverability, error-prevention, feedback, responsiveness, or
  edge-case findings that are about *this feature's structure/interaction/state*,
  not about the underlying approach.
- **Hands off to:** `test.md` for evaluation, and — once a screen/component is
  Test-clean — to Implement (`workflows/build-product.md`) for the High-fidelity,
  built version.

## Explicitly not here
- The reasoning technique for any of the six outputs → the `ux-engine/*` or
  `ui-engine/*` file named above for that output.
- The visual system itself → `ui-engine/*` (applied at High fidelity, in
  Implement, not authored here).
- Evaluating the prototype → `test.md`.
