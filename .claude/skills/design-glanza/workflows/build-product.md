# Workflow: Build Product

## Responsibility
The Implement-phase procedure: turning validated, gated UX+UI specs into an
actual built artifact (code, or whatever the target deliverable is), in
dependency-safe order.

## Executing agent — a deliberate gap
No single reasoning specialist among the 8 `agents/*.md` files owns
"Implement" (see `config/master-config.md`'s Role registry — every phase but
this one has a named owner). This is intentional: Implement is where an
already-fully-specified design gets executed faithfully, not where new
design reasoning happens. It's carried out by whatever build capability is
actually invoking this workflow (the calling session/agent), constrained
entirely by the spec the 8 specialists already produced — it does not
improvise UX, UI, or business logic decisions the spec doesn't already
cover. A gap discovered mid-build is escalated per the rule below, never
silently resolved by the builder's own judgment.

## Step order
Matches `workflows/execute-product-builder.md`'s actions 33-34 (Order
column — shifted from 32-33 when v1.0.11's new spec-level UX
scenario-testing action was inserted earlier in the table; before that,
30-31 after v1.0.10's restructured Design Research actions (3 rows
replacing 1), 28-29 after v1.0.9's new Design Research and Visual
Benchmark & Audit Cycle actions, and originally 23-24 before Design
Setup's actions were inserted):

1. **Build the implementation plan** (`agents/product-architect.md`'s
   build-order output, `product-builder/requirements/dependency-analysis.md`)
   → `product-builder/workflows/implementation-notes.md`. Confirm
   **B12 (Implementation Readiness)** passes before writing any code:
   every screen has a complete `screen-specification.md`, every component a
   complete `component-spec.md`, no unresolved circular dependency.
2. **Sequence the build** by critical path — auth/roles and any
   shared component three or more features depend on first, per
   `product-intelligence/dependency-analysis.md`'s graph.
3. **Per unit** (screen or component): confirm its spec is gate-passed,
   build it into `output/`, then run `scripts/validate-screens.py` /
   `validate-states.py` against it before moving to the next unit.
4. **Escalate spec gaps** — if implementation surfaces something the spec
   didn't cover, route back to the owning file/agent (per
   `methodology/design-thinking.md`'s routing table) rather than inventing
   behavior on the spot (Rule 10, `config/operating-rules.md`).
5. Update `product-builder/workflows/implementation-notes.md` with status
   as units complete — "where applicable" (per
   `workflows/execute-product-builder.md`): a planning-only engagement
   legitimately stops here with `output/` empty, but every gate through
   Prototype must still have passed. Where `output/` is **not** empty
   (something was actually built), hand off to `workflows/preview-run.md`
   next — Implement finishing does not itself mean the product is ready
   for Test (Rule 19).

## Gate
Must pass `config/quality-gates.md`'s **Implement → Preview & Run** gate
(Implementation Readiness, B12, still holding) before
`workflows/preview-run.md` begins. Reaching `methodology/test.md`
validation additionally requires **Preview & Run → Test** (B14) to pass —
this workflow does not itself satisfy that gate, `preview-run.md` does.

## Explicitly not here
- What order things depend on → `product-intelligence/dependency-analysis.md`
  (this workflow consumes that graph, doesn't compute it).
- The spec being implemented → `templates/screen-specification.md` /
  `templates/component-spec.md`.
- Verifying the built output actually launches and runs →
  `workflows/preview-run.md`.
- Post-build correctness audit → `audit-product.md`.
- The build-order/implementation-readiness sign-off itself →
  `agents/product-architect.md`.
