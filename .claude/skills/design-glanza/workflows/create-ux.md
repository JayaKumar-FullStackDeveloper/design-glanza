# Workflow: Create UX

## Responsibility
The operational procedure for turning a defined problem/direction
(post-Ideate) into structural and behavioral UX artifacts — gated before any
`ui-engine/*` work is allowed to start (Rule 4, `config/operating-rules.md`:
UX before UI). Entered only after Design Setup's approved
`product-builder/ui/design-direction.md` exists (Rule 18) — its Layout
section (grid/container/sidebar-header preference) is available input here,
though IA and navigation pattern selection remain governed by
`information-architecture.md`'s and `navigation-system.md`'s own
structural rules, not overridden by a stated visual preference.

## Executing agents, in sequence
Three agents run in sequence, each handing off to the next — neither
redoes the other's decision (see each agent's "must not do" section):

1. **`agents/ux-architect.md`** — structure: flows, IA, navigation, screen
   architecture, and the *named* interaction-model choice per screen (not
   its detailed behavior).
2. **`agents/interaction-designer.md`** — detail: exact feedback timing,
   confirmation rules, form behavior, and the full state matrix, built on
   step 1's named choices.
3. **`agents/accessibility-expert.md`** — structural/behavioral pass over
   both of the above (perceptual/contrast review happens later, in
   `create-ui.md`, once color exists to check).
4. **`agents/ux-architect.md`** and **`agents/interaction-designer.md`**
   jointly, once more — derive UX scenarios per flow and run the
   spec-level UX Scenario Coverage check (Rule 22), now that flows, IA,
   navigation, screen architecture, and states all exist to check against.

## Step order
Matches `workflows/execute-product-builder.md`'s actions 20-27 (Order
column — shifted from 20-26 when v1.0.11's new UX scenario-testing action
was inserted at the end of this range; before that, 18-24 after v1.0.10's
restructured Design Research actions, 17-23 after v1.0.9's single
folded-in Design Research action, and originally 12-18 before Design
Setup's actions were inserted):

1. Build user flows (`ux-engine/user-flow-engine.md`, `FLOW-NNN`, recovery
   paths) → `product-builder/ux/user-flows.md`.
2. Build information architecture (`information-architecture.md`) →
   `product-builder/ux/sitemap.md`.
3. Build navigation architecture (`navigation-system.md`'s 13 concerns —
   breadcrumbs never a default inclusion) → `product-builder/ux/navigation.md`.
4. Build screen architecture (region maps, one primary action each) →
   `product-builder/ux/screen-architecture.md`.
5. Specify interaction/form/state detail (`interaction-design.md`,
   `form-design.md`, `state-design.md`) → `product-builder/ux/ux-rules.md`,
   `product-builder/ux/state-matrix.md`.
6. Run the structural/behavioral accessibility pass (`accessibility.md`) →
   `product-builder/ux/accessibility.md`.
7. Derive UX scenarios per flow across the 8 mandatory types, build the UX
   Coverage Matrix, and run the spec-level gap-detection check
   (`ux-scenario-testing/{scenario-model,scenario-types,gap-detection,
   coverage-matrix}.md`) → `product-builder/ux/scenarios.md`,
   `product-builder/ux/ux-coverage-matrix.md`.

## Gate
Must pass `config/quality-gates.md`'s **B3 (User-Flow Completeness)**,
**B4 (Information Architecture)**, **B5 (Screen Architecture)**, and
**B7 (State Coverage)** gates — plus the structural half of **B8
(Accessibility)** and **B17 (UX Scenario Coverage)**'s spec-level
checkpoint — before `create-ui.md` may begin. This operationalizes
the Ideate → Architect and Architect → Prototype phase gates
(`config/quality-gates.md` Section A) as they apply to UX completeness.
Every Critical/High `RF-NNN` finding UX Architect's flows/IA/navigation/
screen-architecture cite contributes to **B16 (Research-to-Design
Traceability)**'s decision/pattern stage, checked at the Prototype →
Implement transition.

## Explicitly not here
- Any UX reasoning technique itself → the relevant `ux-engine/*.md` file.
- Turning these UX artifacts into visual design → `create-ui.md`.
- Domain-specific UX conventions → the relevant `product-types/*.md`,
  consulted at each step, not restated here.
- The UX scenario-testing technique itself → `ux-scenario-testing/*`.
- The agents' own scope boundaries → `agents/ux-architect.md`,
  `interaction-designer.md`, `accessibility-expert.md`.
