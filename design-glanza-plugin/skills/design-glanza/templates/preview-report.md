# Template: Preview Report

## Purpose
The record that implementation was actually launched and verified locally
— satisfying `config/quality-gates.md`'s **B14 (Preview & Run
Verification)** gate. Distinct from `workflows/implementation-notes.md`
(what was built and its build-order status): this file is whether what was
built actually *runs*.

## Required inputs
- `output/*` — the built artifact Implement produced.
- `workflows/preview-run.md`'s 8-step procedure (framework detection through
  the final report).
- `workflows/implementation-notes.md`'s status, to know which screen(s) were
  actually implemented this pass and are expected to be previewable.

## Output structure
- **Header** — per `config/output-contract.md`.
- **Project path** — the root the dev server was started from.
- **Framework** — detected framework/stack (e.g. "Vite + React", "Next.js").
- **Start command** — the exact command used to start the dev server.
- **Local URL** — e.g. `http://localhost:5173`.
- **Port** — the detected port, stated even though it's part of the URL, so
  a port conflict is checkable at a glance.
- **Build status** — success / failed, with the specific error if failed.
- **Runtime status** — clean / errors-present, with the specific error(s) if
  present — a build that succeeds but throws at runtime is **not** a clean
  runtime status.
- **Implemented screen(s)** — which screen(s)/route(s) from this pass were
  actually checked in the browser, by name (cross-reference
  `templates/screen-specification.md` IDs).
- **Preview status** — pass / fail, and if fail, what specifically blocked
  it and what fix was applied (per Rule 19, a failure here is fixed before
  continuing, not shipped as a known issue).
- **Public preview** *(optional section, only when the user explicitly
  requested one)* — ngrok availability check result, the exposed port, and
  the generated public URL. Omitted entirely (not "not applicable" —
  genuinely absent) when no public preview was requested; its absence never
  fails B14.

## Quality criteria
- Checked against `config/quality-gates.md`'s **B14 (Preview & Run
  Verification)** gate — every required field filled, build succeeded,
  runtime clean, local URL/port actually detected (not assumed from a
  framework default).
- A failed build or runtime error is fixed before this report is considered
  final — a report documenting a known-broken preview does not satisfy B14,
  it documents why the gate isn't passed yet.
- The public-preview section, if present, never substitutes for the local
  one — a working ngrok tunnel over a broken local server still fails B14.

## Example structure
_Illustrative, domain-neutral — not real product content._

```
Project path: products/acme-app/output/
Framework: Vite + React
Start command: npm run dev
Local URL: http://localhost:5173
Port: 5173
Build status: success
Runtime status: clean — no console errors on load
Implemented screen(s): SCREEN-004 (Dashboard)
Preview status: pass

Public preview: not requested
```

## Traceability fields
Cited by `workflows/audit-product.md` (Audit folds in preview status
alongside Test's own findings) and by `methodology/test.md` dimension 1
(task completion) as the confirmation a screen is actually reachable before
walking its flow.

## Explicitly not here
- The step-by-step detection/start/verify procedure itself →
  `workflows/preview-run.md`.
- What was built and its build-order/status →
  `workflows/implementation-notes.md`.
- The 9-dimension design validation Test itself performs → `methodology/test.md`.
