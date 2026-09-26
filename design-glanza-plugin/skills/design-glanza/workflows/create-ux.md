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
Two agents run in sequence, each handing off to the next — neither redoes
the other's decision (see each agent's "must not do" section):

1. **`agents/ux-architect.md`** — structure: flows, IA, navigation, screen
   architecture, and the *named* interaction-model choice per screen (not
   its detailed behavior).
2. **`agents/interaction-designer.md`** — detail: exact feedback timing,
   confirmation rules, form behavior, and the full state matrix, built on
   step 1's named choices.
3. **`agents/accessibility-expert.md`** — structural/behavioral pass over
   both of the above (perceptual/contrast review happens later, in
   `create-ui.md`, once color exists to check).

## Step order
Matches `workflows/execute-product-builder.md`'s actions 12-18:

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

## Gate
Must pass `config/quality-gates.md`'s **B3 (User-Flow Completeness)**,
**B4 (Information Architecture)**, **B5 (Screen Architecture)**, and
**B7 (State Coverage)** gates — plus the structural half of **B8
(Accessibility)** — before `create-ui.md` may begin. This operationalizes
the Ideate → Architect and Architect → Prototype phase gates
(`config/quality-gates.md` Section A) as they apply to UX completeness.

## Explicitly not here
- Any UX reasoning technique itself → the relevant `ux-engine/*.md` file.
- Turning these UX artifacts into visual design → `create-ui.md`.
- Domain-specific UX conventions → the relevant `product-types/*.md`,
  consulted at each step, not restated here.
- The agents' own scope boundaries → `agents/ux-architect.md`,
  `interaction-designer.md`, `accessibility-expert.md`.
