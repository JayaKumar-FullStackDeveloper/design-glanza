# Workflow: Design Setup

## Responsibility
The operational, step-by-step procedure for the **Design Setup** phase —
between Architect and Prototype. Applies
`design-reference-engine/*`'s techniques to one real product and produces
one approved `product-builder/ui/design-direction.md` before
`workflows/create-ux.md`/`create-ui.md` may begin. This is "how to actually
run it"; the extraction/classification/authoring methods themselves are
owned by the `design-reference-engine/*` files this workflow sequences.

## Executing agent
`agents/design-setup-specialist.md`, invoked once per product, immediately
after Architect (`agents/product-architect.md`) confirms the domain
classification and dependency graph, and before `agents/ux-architect.md`
begins Prototype's UX pass. Re-entered only when a Test/Audit finding
routes back here per `methodology/design-thinking.md`'s feedback-routing
table (the finding traces to the *direction itself*, not its execution).

## Step order
Matches `agents/design-setup-specialist.md`'s analysis procedure and
`workflows/execute-product-builder.md`'s Design Setup actions, in this
order:

0. **Design Research** — before touching any reference, research current
   product-design patterns relevant to this product: modern SaaS/admin
   conventions, this product's own domain conventions (per the confirmed
   `product-types/*.md`/`domain-standards` match), information density,
   navigation/dataviz/form-table/interaction/accessibility/responsive
   patterns, and current visual trends — checked against
   `ui-engine/visual-trends.md`'s adoption gate, never adopted just because
   they're current (`design-reference-engine/design-research.md`). Folds
   directly into the direction below; produces no separate artifact.
1. **Detect references** — scan `products/<slug>/BRD/*` for any of the 13
   recognized reference forms (`design-reference-engine/
   reference-analysis.md`).
2. **Analyze references, if present** — extract visual/interaction/
   design-system/component/layout/typography/color/spacing/radius-
   elevation/navigation/responsive patterns, each confidence-tagged, tagged
   as design direction and never as a business requirement.
3. **Run the design questionnaire** — the 9-category question set
   (`design-reference-engine/design-questionnaire.md`), asked directly
   where a user is present and no reference/guideline already answers a
   question with real confidence, otherwise answered by inference or
   assumption-tagged.
4. **Classify the design-reference decision** — Reference-Driven /
   Guideline-Driven / Custom Design / Default Design-Glanza
   (`design-reference-engine/reference-selection.md`), selecting a
   `design-samples/` entry only for Default mode, matched against Product
   Architect's confirmed domain — never one generic style regardless of
   domain (Admin Panel ≠ E-commerce ≠ Healthcare ≠ ERP ≠ Fintech ≠ CRM).
5. **Write `product-builder/ui/design-direction.md`** — every field
   `templates/design-direction.md` requires, filled per
   `design-reference-engine/design-direction.md`'s synthesis discipline.
6. **Present the Design Direction Summary and gate on approval** — a
   concise summary (not the full document), asking *"Does this design
   direction match your expectations?"* A requested change loops back to
   step 3 or 4 and re-presents; no user available records an explicit
   waiver instead of a fabricated confirmation.

## Gate
Must pass `config/quality-gates.md`'s **Design Setup → Prototype**
phase-transition gate — which resolves to **B13 (Design Direction
Completeness)** passing — before `workflows/create-ux.md` may begin. This
operationalizes Rule 18 (`config/operating-rules.md`): design direction is
established and, where possible, confirmed before any screen or token is
built against it.

## Relationship to Prototype's ordering (Rule 4/5 still governs)
Design Setup establishes visual/interaction **intent** — it does not move
`ui-engine/design-system.md`'s actual token establishment earlier than its
existing position inside `workflows/create-ui.md`. Rule 4 (UX before UI)
and Rule 5 (system before screen) are unchanged: `create-ux.md` still runs
before `create-ui.md`, and `agents/design-system-expert.md` still
establishes the governed token set before `agents/ui-designer.md` applies
it to screens. Design Setup's output is consumed as an *input* at each of
those existing points, not a reordering of them.

## Explicitly not here
- The extraction/questionnaire/classification/authoring techniques
  themselves → `design-reference-engine/*`.
- The design-research technique itself → `design-reference-engine/
  design-research.md`.
- Comparing the eventual generated screen back against this direction →
  `ui-engine/visual-benchmark.md`, `ui-engine/ui-audit-framework.md`.
- The default sample library's own content → `design-samples/`.
- The document's exact field list → `templates/design-direction.md`.
- What happens once the direction is approved → `create-ux.md`,
  `create-ui.md`.
- The agent's own scope boundaries → `agents/design-setup-specialist.md`.
