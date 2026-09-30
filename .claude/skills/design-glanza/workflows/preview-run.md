# Workflow: Preview & Run

## Responsibility
The Preview & Run-phase procedure: verifying that what Implement produced
actually launches and runs locally, before Test evaluates it. Implementation
is not complete because the code was written — Rule 19
(`config/operating-rules.md`) makes running it the completion condition.

## Executing agent — same posture as Implement
No dedicated reasoning specialist owns this phase, for the same reason
`workflows/build-product.md` states for Implement: this is verification by
execution and observation, not new design reasoning. It is carried out by
whatever capability is actually invoking this workflow (the same
session/agent that just ran `build-product.md`), constrained entirely by
what was actually implemented — it does not redesign, re-scope, or silently
skip a screen that fails to load.

## Step order
Matches `workflows/execute-product-builder.md`'s actions 35-36 (Order
column — shifted from 34-35 when v1.0.11's new spec-level UX
scenario-testing action was inserted earlier in the table; before that,
32-33 after v1.0.10's restructured Design Research actions (3 rows
replacing 1), 30-31 after v1.0.9's new Design Research and Visual
Benchmark & Audit Cycle actions):

1. **Detect the framework and existing development setup** — read
   `output/*`'s own project files (e.g. `package.json`, a framework config
   file) rather than assuming one; this is observation of what Implement
   actually produced, not a fresh technology choice.
2. **Start the appropriate local development server**, using the detected
   project's own declared start command (e.g. its `package.json` `scripts`
   entry) — never a guessed or generic command that happens to differ from
   what the project itself declares.
3. **Verify the application builds successfully.** A build failure is
   itself a finding, not a reason to skip to the next step — proceed to
   step 7 immediately when this fails.
4. **Detect the actual local URL and port** the dev server bound to —
   read it from the server's own output/logs, never assume a framework's
   documented default port is actually the one in use (a taken port, an
   explicit config override, etc. routinely differ from the default).
5. **Open/verify the implemented UI in the browser** at the detected URL —
   confirm the specific screen(s) this pass implemented actually render.
6. **Check for runtime errors** — console errors, unhandled exceptions, a
   blank/broken render — distinct from a build failure (step 3): a build
   can succeed and still fail at runtime.
7. **Fix build/runtime issues before continuing.** Per Rule 19, a broken
   build or a runtime error blocking the implemented screen(s) is resolved
   now, at this phase — never carried forward to Test as a known issue, and
   never silently reported as passing.
8. **Produce the Preview & Run report** (`templates/preview-report.md`) →
   `product-builder/workflows/preview-report.md`, with the local preview
   URL as the primary, headline output (e.g. `http://localhost:5173`).

## Optional public preview
Only when the user **explicitly** requests an external/public preview:
- Check whether `ngrok` is actually available in the environment — never
  install or configure it automatically; if it isn't available, report that
  plainly rather than silently substituting something else.
- Reuse the already-running local server from steps 2–7 — never start a
  second, separate server for the public preview.
- Expose the detected port (step 4) through ngrok, and return the generated
  public URL.
- Record this in the Preview Report's optional Public preview section. Its
  absence (when not requested) never affects B14's pass status.

## Gate
Must pass `config/quality-gates.md`'s **Preview & Run → Test** transition,
which resolves to **B14 (Preview & Run Verification)** passing, before
`methodology/test.md` evaluation begins.

## Explicitly not here
- What was implemented and its build-order/status →
  `workflows/build-product.md`, `workflows/implementation-notes.md`.
- The Preview Report's exact required fields → `templates/preview-report.md`.
- The 9-dimension design validation performed once this gate passes →
  `methodology/test.md`.
- Installing or configuring `ngrok` itself, or any tooling setup beyond
  checking availability — out of scope by design (Rule 19: never required
  for normal operation, never auto-installed).
