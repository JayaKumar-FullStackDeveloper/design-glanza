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
2. **Run structural validation on `output/*`** —
   `scripts/validate-generated-artifact.py`, gate **B14**'s new
   structural-validation layer, added this version. This runs *before*
   the build/runtime steps below because a file can be structurally
   invalid (unbalanced CSS braces, a malformed selector list, a duplicate
   custom-property declaration, unbalanced HTML tags, a missing `alt`, a
   broken same-document reference, a missing local asset, unbalanced JS
   brackets) in ways that don't actually break the build or throw a
   visible runtime error — catching it here, deterministically, is
   cheaper than discovering it as an unexplained visual glitch later. A
   Blocker/Major finding here is fixed before continuing to step 3, the
   same non-negotiable treatment a build failure already gets.
3. **Start the appropriate local development server**, using the detected
   project's own declared start command (e.g. its `package.json` `scripts`
   entry) — never a guessed or generic command that happens to differ from
   what the project itself declares.
4. **Verify the application builds successfully.** A build failure is
   itself a finding, not a reason to skip to the next step — proceed to
   step 8 immediately when this fails.
5. **Detect the actual local URL and port** the dev server bound to —
   read it from the server's own output/logs, never assume a framework's
   documented default port is actually the one in use (a taken port, an
   explicit config override, etc. routinely differ from the default).
6. **Open/verify the implemented UI in the browser** at the detected URL —
   confirm the specific screen(s) this pass implemented actually render.
7. **Check for runtime errors** — console errors, unhandled exceptions, a
   blank/broken render — distinct from a build failure (step 4): a build
   can succeed and still fail at runtime. This is the one check in this
   workflow that genuinely requires execution/observation — distinct from
   step 2's static structural check, neither standing in for the other.
7a. **Render-and-measure the implemented screen(s)**, wherever Playwright
    is available in the current environment (degrades to a disclosed Note
    otherwise, never a crash — see `scripts/validate-product.py`'s own
    docstring): `scripts/capture-render.py` against the step-5 detected
    local URL (a full Product Builder pass) or directly against the
    standalone HTML file (no dev server involved), at every required
    breakpoint/theme, then `scripts/validate-rendered-layout.py` against
    the resulting manifests. This is a **separate pass from step 2** —
    step 2 is fast, dependency-free, structural/code-only and always
    runs; this step is rendering-dependent and catches what step 2
    cannot by design (a syntactically clean file that overflows,
    misaligns, or overlaps when actually rendered). A Blocker finding
    here is fixed before continuing, the same non-negotiable treatment
    a build failure already gets — per `ui-engine/visual-benchmark.md`'s
    Render-and-measure evidence section and gate **B14**.

    Within this same render pass, wherever Playwright is actually
    available (the identical degrade-to-a-disclosed-Note posture, never
    a second failure mode to handle):
    - **Automated accessibility scan** — `capture-render.py` injects
      axe-core into the page and runs it once settled, recording any
      violation into the manifest's `axe_violations` field (severity
      preserved as axe reports it: `critical`/`serious`/`moderate`/
      `minor`); `validate-rendered-layout.py` turns `critical`/`serious`
      violations into Blocker/Major findings, the automated, deterministic
      counterpart to `ux-engine/accessibility.md`'s structural rules —
      catching what a structural read alone misses (a real contrast
      failure, a missing accessible name) without re-litigating what B8
      already checked at the spec level.
    - **Performance budget** — the same render captures LCP/CLS/INP via
      the browser's own Performance API into `web_vitals`;
      `validate-rendered-layout.py` flags a value over a pragmatic budget
      (LCP > 4.0s, CLS > 0.25, INP > 500ms — well above "broken," well
      below a marketing-page-strict Core Web Vitals target, since this
      runs against ordinary app screens, not just landing pages) as a
      finding, not a block on anything already passing.
    - **Breakpoint-transition sweep** — `capture-render.py --sweep`
      captures additional widths beyond the 3 mandatory breakpoints
      (desktop/tablet/mobile) to locate the actual width where a layout
      transitions (a nav mode switch, a column-count change, a sidebar
      appearing/disappearing) and flags one that doesn't degrade
      cleanly; this is rendered *evidence* for B9's already-required
      per-breakpoint reflow check, not a new requirement on top of it —
      B9 still passes or fails on its existing criteria.
8. **Fix build/runtime/structural/rendered-layout issues before
   continuing.** Per Rule 19, a broken build, a runtime error blocking
   the implemented screen(s), an unresolved structural finding from step
   2, or an unresolved rendered-layout finding from step 7a is resolved
   now, at this phase — never carried forward to Test as a known issue,
   and never silently reported as passing. A fix to a rendered-layout
   finding is only confirmed by re-running step 7a against the changed
   output, never by re-reading the changed source and assuming it's
   fixed.
9. **Produce the Preview & Run report** (`templates/preview-report.md`) →
   `product-builder/workflows/preview-report.md`, with the local preview
   URL as the primary, headline output (e.g. `http://localhost:5173`).
   Where this pass's own render-capture screenshots exist, an end-user
   guide can now be generated by reusing them — `workflows/
   project-documentation.md`'s end-user guide section — rather than a
   fresh screenshotting pass; skipped when no such reader is needed yet.

## Optional public preview
Only when the user **explicitly** requests an external/public preview:
- Check whether `ngrok` is actually available in the environment — never
  install or configure it automatically; if it isn't available, report that
  plainly rather than silently substituting something else.
- Reuse the already-running local server from steps 3–7 — never start a
  second, separate server for the public preview.
- Expose the detected port (step 5) through ngrok, and return the generated
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
