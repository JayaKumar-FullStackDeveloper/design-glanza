# Workflow: Project Documentation

## Responsibility
Developer-facing and end-user-facing documentation generation, reusing
artifacts already produced earlier in the lifecycle rather than
re-deriving anything — consumed from `workflows/build-product.md` (Order
34, developer docs) and `workflows/preview-run.md` (Order 36, end-user
guide), never a standalone action of its own. Skipped entirely when no
reader exists for a given doc type (no API layer → no API_ENDPOINTS.md;
no database → no DATABASE_SCHEMA.md; a planning-only engagement with no
`output/` → no end-user guide, since there's nothing running to document).

## Developer documentation (ARCHITECTURE / API / DATABASE_SCHEMA)
Generated from what Implement actually produced, never from aspiration:
- **Source material, already produced, never re-derived**:
  `workflows/implementation-notes.md` (what was built, build order,
  status), `domain/domain-application-notes.md` (the applied domain
  pack's module/entity boundaries), the product's own `output/*` source
  (its real `package.json`, route files, schema files).
- **ARCHITECTURE.md**: stack table (runtime/framework/database/ORM/
  frontend/styling, with versions read from the product's own
  dependency file, never from memory), an annotated directory structure
  (top two levels), the key flows `implementation-notes.md` already
  names (e.g. auth, the primary data-processing path), and deployment
  notes where applicable.
- **API_ENDPOINTS.md** (only where the product actually has an API
  layer): base URL, auth method, and one entry per real route — method,
  params, request/response shape copied from the actual
  types/schema in the code, never invented; a route found with no clear
  purpose is flagged (`<!-- TODO: document purpose -->`), not silently
  omitted or silently guessed at.
- **DATABASE_SCHEMA.md** (only where the product actually has a
  database): engine, one table per real schema file (columns, types,
  constraints), relationships/foreign keys, indexes and why they exist,
  migration commands.
- **Updating, never silently overwriting**: when one of these docs
  already exists (a prior Iterate pass), diff against the current
  codebase, show what changed, and preserve any hand-written notes a
  human already added — the same preserve-what's-already-filled-in
  posture `scripts/create-product-builder.py --update` already applies
  to the Product Builder itself.
- **Never duplicate `CLAUDE.md`-equivalent project instructions already
  present** — reference them instead of restating.

## End-user guide (reuses Preview & Run's own screenshots)
Generated only once `workflows/preview-run.md` step 7a has actually
produced render-capture screenshots for this product's real screens
(`qa/render-capture/<screen>/*`) — this is pure artifact reuse, never a
fresh browsing/screenshotting pass of its own:
- One section per documented screen: what it's for (one sentence), the
  reused screenshot, what the user can do, and a numbered how-to for its
  primary action — written from the screen's own
  `templates/screen-specification.md` and `ux/user-flows.md`, not
  improvised.
- Written to `product-builder/qa/user-guide.md` by default; a single
  self-contained HTML version (screenshots as relative paths, not
  inlined base64) only when the product type or an explicit request
  calls for a publishable guide (e.g. a `landing-page.md`-type product
  with an end-customer audience).
- Depth matches what's actually needed — a 2-3 screen planning-only
  engagement earns a short quick-start, not a padded exhaustive manual;
  an engagement that produced render-capture evidence for every screen
  and every mandatory state (per `ui-audit-framework.md`) can support a
  full guide with a getting-started section and a troubleshooting
  section built from the actual defects Test/Audit found and fixed, not
  hypothetical FAQs.

## Explicitly not here
- What Implement actually built, or its current status →
  `workflows/build-product.md`, `workflows/implementation-notes.md`.
- The screenshots this file reuses, and how they were captured →
  `workflows/preview-run.md` step 7a, `scripts/capture-render.py`.
- The product's own functional spec (what a screen does, why) →
  `templates/screen-specification.md`, `ux/user-flows.md`.
- Internal QA reporting (defects, gate status) → `templates/qa-report.md`
  (this file's troubleshooting section only reuses already-resolved
  findings from there, never restates open ones as if fixed).
