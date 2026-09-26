# Workflow: Create Product

## Responsibility
The master end-to-end procedure: Intake through Iterate, for a **greenfield**
product. This is the operational form of `methodology/design-thinking.md`'s phase
map — concrete steps, concrete file references, gated by `config/quality-gates.md`.
Sub-procedures for individual phase clusters are delegated to the other
`workflows/*.md` files rather than repeated here.

## Owns
- The phase sequence with, per phase, which files are read/applied and which
  workflow handles its detail:
  1. Intake → `analyze-brd.md`
  2. Empathize/Define/Ideate → applies `methodology/*` directly (no dedicated
     workflow file; light enough to stay here)
  3. Architect → `product-intelligence/dependency-analysis.md` +
     `domain-classifier.md` + `domain-standards.md`, **then scaffold the
     Product Builder** (see below)
  4. Design Setup → `design-setup.md` — establish and, where a user is
     available, get approval on the product's visual/interaction direction
     before any screen or token is built (Rule 18); gates on B13
  5. Prototype → `create-ux.md` then `create-ui.md` at prototype fidelity
     (`methodology/prototype.md` fidelity ladder), consuming Design Setup's
     approved `ui/design-direction.md`
  6. Implement → `build-product.md`
  7. Preview & Run → `preview-run.md` — the built output must actually
     launch and run locally before Test evaluates it (Rule 19); skipped
     only when Implement itself was skipped (a planning-only pass with no
     `output/` content)
  8. Test → `methodology/test.md`
  9. Audit → `audit-product.md`
  10. Iterate → loops back to the appropriate earlier phase per findings
- The gate check-in point between every phase (calls `config/quality-gates.md`) and
  the report shape at each stop (calls `config/output-contract.md`).
- The non-auto-advance behavior itself (per `config/operating-rules.md`): where the
  procedure pauses for user review.

## Scaffolding the Product Builder
Once Architect has a domain classification (`domain-classifier.md`) and Define
has produced at least a problem statement and business/user/product
objectives, invoke `scripts/create-product-builder.py generate` with those
facts as the product definition — this materializes
`products/<product-slug>/` (per the factory's directory contract) with a
product-specific `product-builder/SKILL.md` that references the master
engine rather than copying it.

From that point on, **every phase that produces new product-specific
content re-invokes the generator with `--update`**, supplying only the
newly-completed section(s) (e.g. Prototype supplies `user_flows` and
`information_architecture`; Implement's `build-product.md` supplies
`design_system`; Audit supplies `qa_rules` and `traceability_requirements`).
The generator preserves everything already filled in from a prior run — a
phase never needs to resupply content another phase already recorded. If
`products/<product-slug>/` already exists from an earlier run of this same
workflow (e.g. resuming after a pause), the generator's conflict guard means
`--update` must be used explicitly; a bare `generate` refuses to overwrite it.

## The concrete action sequence
This file orchestrates *at the phase level* ("Prototype → create-ux.md then
create-ui.md"). The concrete, artifact-by-artifact action sequence that
actually executes within a scaffolded Product Builder — 24 required actions,
each mapped to a phase, a master technique, and an exact file it must write —
is `execute-product-builder.md`. That file is also what every generated
`product-builder/SKILL.md` links to directly, so a Product Builder never
needs this master workflow open to know what to do next.

## Explicitly not here
- Redesigning an *existing* product → `redesign-product.md` (different Intake, same
  downstream shape).
- The Intake extraction technique itself → `product-intelligence/brd-analysis.md`.
- Per-phase reasoning technique → `methodology/*.md`.
- The Design Setup procedure itself → `design-setup.md`.
- The Preview & Run procedure itself → `preview-run.md`.
- The generator's own scaffolding/validation logic → `scripts/create-product-builder.py`.
- The concrete, artifact-by-artifact execution sequence →
  `execute-product-builder.md`.
