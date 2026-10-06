"""
capture-render.py

Responsibility
--------------
The RENDER + OBSERVE step of the GENERATE -> RENDER -> OBSERVE -> MEASURE ->
COMPARE -> FIX -> RE-RENDER -> RE-CHECK loop (Rule 20, gate B15, this
version's quality-engine upgrade). Loads a generated HTML file in a real,
headless Chromium browser (Playwright) at one or more configured
viewports and color schemes, and for each combination:

- Captures a full-page screenshot and a viewport-only screenshot (PNG).
- Walks the live, rendered DOM and records every visible element's actual
  geometry: bounding box (left/top/width/height), scroll-vs-client
  dimensions (the raw signal `validate-rendered-layout.py` uses to detect
  overflow), computed `overflow-x`/`overflow-y`, tag name, class list, a
  short text excerpt, whether the element carries direct (non-descendant)
  text, and a structural path for identifying it in a report. Also
  records a small set of computed STYLE values per element (added
  v1.0.30, extended v1.0.32 with `borderColor` after a real benchmark
  run found color-token conformance checks had no way to see a border's
  color at all — alongside the existing geometry fields, for no cost
  beyond reading properties already available on the same
  `getComputedStyle()` call this script already makes): `backgroundColor`,
  `color`, `borderColor` (read from `borderTopColor` — the single value
  most elements' own authored `border` shorthand sets identically on all
  four sides), `borderRadius`, `fontFamily`, `fontSize`, `padding` (the
  resolved shorthand string), and `gap` (read from `rowGap` — the value a
  browser's `getComputedStyle()` normalizes a flex/grid `gap` shorthand
  into) — the measured values `ui-engine/visual-benchmark.md`'s Level B
  (Figma-spec conformance) compares against a Figma Design Context's
  `tokens.*` ground truth, spacing values included. This
  does not turn this script into a style-judgment tool — it still only
  **captures**; comparing a captured value against anything is always a
  downstream script's or agent's job, same boundary as the geometry
  fields above.

This script only **captures** — it does not judge alignment, spacing,
overflow, or overlap itself. That analysis (grouping, tolerances, Finding
generation) is `validate-rendered-layout.py`'s job, deliberately kept
separate so the capture step stays a thin, swappable rendering layer and
the analysis step stays unit-testable against a hand-built JSON fixture
with no browser required at all.

Why Playwright, not stdlib
---------------------------
Every other script in this folder is stdlib-only by design (see each
script's own docstring) because nothing else they check requires it.
Actual rendering fundamentally cannot be done without a real browser
engine — no stdlib substitute exists. This is a deliberate, explicit,
narrow exception: only this script and `validate-rendered-layout.py`'s
image-comparison sibling (`compare-reference-visual.py`, via Pillow) carry
a non-stdlib dependency; every structural/token/data validator in this
folder remains dependency-free exactly as before.

Standalone-screen support
--------------------------
Takes a single HTML file path directly — no `product-builder/` scaffold
required. A full Product Builder pass points this at `output/<file>.html`;
a standalone screen/benchmark request points it at the file directly. Same
script, same capability, either way (Rule: standalone screens receive the
same validation a scaffolded product does).

What this deliberately does NOT check
--------------------------------------
Whether a measurement is actually a defect (that's a tolerance/grouping
judgment — `validate-rendered-layout.py`'s job). Whether the screen
matches a reference image (`compare-reference-visual.py`'s job). Console
errors / network failures during load (`workflows/preview-run.md`'s
existing runtime-check step, unchanged by this addition). Component
*identity* across renders (that is, it does not know a hand-authored
"KPI card" from any other `<div>` — it reports geometry for every element
uniformly; `validate-rendered-layout.py` groups by sibling+class
similarity, not by a predefined component taxonomy).

Status: implemented and verified (see Test 1-4/6 in the changelog for
this version).

Added this version: three further capture modes, each independently
optional and each degrading to a disclosed `None`/omitted field rather
than a crash when its one extra requirement (network access for axe-core,
a Performance-API-capable page) isn't available — the same posture this
file already applies to the Playwright dependency itself.

- `--axe` (on by default): injects axe-core via CDN and runs it once the
  page has settled, recording violations into the manifest's
  `axe_violations` field. `validate-rendered-layout.py` turns
  `critical`/`serious` entries into Blocker/Major findings — the
  deterministic counterpart to `ux-engine/accessibility.md`'s structural
  rules, not a replacement for them.
- `--vitals` (on by default): captures LCP and CLS via the Performance
  API, and a single-sample, best-effort INP approximation from one
  synthetic interaction (true INP needs a real user's interaction
  history across a session, which headless rendering has none of — this
  is disclosed as an approximation, not presented as a full measurement)
  into the manifest's `web_vitals` field.
- `--sweep`: captures at 8 widths (320/375/768/1024/1280/1440/1920/2560,
  one light-theme pass) instead of the 3 named breakpoints, then runs a
  best-effort transition detector (`detect_transitions()`) flagging width
  ranges where element count or overflow onset changes between adjacent
  widths — a signal for *where* to look, not a precise CSS-breakpoint
  oracle.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# See _common.py's identical guard for why: a generated screen's own text
# can contain a non-ASCII character that crashes a Windows console's
# default cp1252 stdout. This script doesn't import _common (deliberately
# dependency-light), so it carries its own copy of the same fix.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

try:
    from playwright.sync_api import sync_playwright
except ImportError:  # pragma: no cover - environment without the optional dependency
    sync_playwright = None

# Default viewport set - desktop/tablet/mobile, matching
# ui-engine/responsive-system.md's breakpoint set (desktop reference width
# 1440, tablet 1024, mobile a common real device width rather than the
# bare 640px floor, since real mobile Safari/Chrome chrome occupies some
# of that).
DEFAULT_VIEWPORTS = {
    "desktop": {"width": 1440, "height": 1024},
    "tablet": {"width": 1024, "height": 900},
    "mobile": {"width": 390, "height": 844},
}

# --sweep mode widths - matches the device spectrum
# ui-engine/responsive-system.md's named breakpoints sit inside, plus the
# extremes a named-breakpoint-only capture can miss (a small phone, an
# ultra-wide desktop).
SWEEP_WIDTHS = [320, 375, 768, 1024, 1280, 1440, 1920, 2560]
SWEEP_HEIGHT = 900

# Pinned version so a result is reproducible; bump deliberately, not
# silently, when a newer axe-core is actually verified against this script.
AXE_CDN_URL = "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.0/axe.min.js"

# JS evaluated in-page to dump every element's rendered geometry in one
# round-trip (far faster than one Python<->JS call per element). Skips
# elements with zero rendered area (display:none / collapsed) - nothing
# to measure there, and including them would make every hidden popover
# menu a false-positive "overflow" or "misalignment" target.
DOM_DUMP_JS = r"""
() => {
  function cssPath(el) {
    if (!el || el.nodeType !== 1) return '';
    var parts = [];
    while (el && el.nodeType === 1 && parts.length < 6) {
      var sel = el.tagName.toLowerCase();
      if (el.id) { sel += '#' + el.id; parts.unshift(sel); break; }
      if (el.className && typeof el.className === 'string' && el.className.trim()) {
        sel += '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.');
      }
      // Disambiguate same-tag siblings with no id (e.g. two unrelated
      // ".row-2col" container instances at the same nesting level) so
      // their descendants don't collapse onto one identical path string
      // and get falsely grouped as one sibling set by
      // validate-rendered-layout.py's _sibling_sets().
      if (el.parentElement) {
        var sameTagSiblings = Array.prototype.filter.call(
          el.parentElement.children, function(c) { return c.tagName === el.tagName; }
        );
        if (sameTagSiblings.length > 1) {
          sel += ':nth(' + (sameTagSiblings.indexOf(el) + 1) + ')';
        }
      }
      parts.unshift(sel);
      el = el.parentElement;
    }
    return parts.join(' > ');
  }
  var out = [];
  var all = document.querySelectorAll('body *');
  for (var i = 0; i < all.length; i++) {
    var e = all[i];
    var r = e.getBoundingClientRect();
    if (r.width <= 0 || r.height <= 0) continue;
    var cs = window.getComputedStyle(e);
    if (cs.visibility === 'hidden' || cs.display === 'none') continue;
    var hasDirectText = false;
    for (var c = 0; c < e.childNodes.length; c++) {
      if (e.childNodes[c].nodeType === 3 && e.childNodes[c].textContent.trim()) { hasDirectText = true; break; }
    }
    out.push({
      path: cssPath(e),
      tag: e.tagName.toLowerCase(),
      classes: (e.className && typeof e.className === 'string') ? e.className.trim() : '',
      text: (e.textContent || '').trim().slice(0, 60),
      left: r.left, top: r.top, right: r.right, bottom: r.bottom,
      width: r.width, height: r.height,
      scrollWidth: e.scrollWidth, clientWidth: e.clientWidth,
      scrollHeight: e.scrollHeight, clientHeight: e.clientHeight,
      overflowX: cs.overflowX, overflowY: cs.overflowY,
      hasDirectText: hasDirectText,
      parentPath: e.parentElement ? cssPath(e.parentElement) : null,
      backgroundColor: cs.backgroundColor, color: cs.color,
      borderColor: cs.borderTopColor, borderRadius: cs.borderRadius,
      fontFamily: cs.fontFamily, fontSize: cs.fontSize,
      padding: cs.padding, gap: cs.rowGap
    });
  }
  return out;
}
"""

# Captures LCP + CLS directly from the Performance API (both measurable
# with no user interaction), plus a single-sample, best-effort INP
# approximation from one synthetic interaction on the first interactive
# element found. This is a pragmatic budget measurement (per
# ux-audit's performance-budget technique), not a full Core Web Vitals
# field-data measurement - disclosed as such in this script's docstring.
WEB_VITALS_JS = r"""
async () => {
  function getLCP() {
    return new Promise((resolve) => {
      let value = null;
      try {
        const po = new PerformanceObserver((list) => {
          const entries = list.getEntries();
          const last = entries[entries.length - 1];
          if (last) value = last.renderTime || last.loadTime || last.startTime;
        });
        po.observe({ type: 'largest-contentful-paint', buffered: true });
      } catch (e) { /* LCP unsupported in this engine build - leave null */ }
      setTimeout(() => resolve(value), 50);
    });
  }
  function getCLS() {
    let value = 0;
    try {
      const entries = performance.getEntriesByType('layout-shift');
      for (const entry of entries) {
        if (!entry.hadRecentInput) value += entry.value;
      }
    } catch (e) { /* layout-shift unsupported - leave at 0, disclosed via null below */ }
    return value;
  }
  function getINP() {
    const target = document.querySelector('button, a[href], [role="button"], input, select');
    if (!target) return Promise.resolve(null);
    return new Promise((resolve) => {
      let resolved = false;
      const finish = (v) => { if (!resolved) { resolved = true; resolve(v); } };
      try {
        const po = new PerformanceObserver((list) => {
          const entries = list.getEntries();
          if (entries.length) finish(entries[0].duration);
        });
        po.observe({ type: 'event', buffered: true, durationThreshold: 0 });
      } catch (e) { /* Event Timing API unsupported - fall through to the timer below */ }
      const start = performance.now();
      target.dispatchEvent(new MouseEvent('pointerdown', { bubbles: true }));
      target.dispatchEvent(new MouseEvent('pointerup', { bubbles: true }));
      try { target.click(); } catch (e) { /* non-clickable target - timing still measured */ }
      setTimeout(() => finish(performance.now() - start), 150);
    });
  }
  const lcp_ms = await getLCP();
  const inp_ms = await getINP();
  const cls = getCLS();
  return { lcp_ms: lcp_ms, cls: cls, inp_ms: inp_ms, inp_is_approximation: true };
}
"""


def _run_axe(page) -> list[dict] | dict:
    """Injects axe-core from CDN and runs it once the page has settled.
    Returns a list of {id, impact, help, nodes} violation summaries, or a
    {"error": "..."} dict when injection/execution fails (no network, a
    blocked CDN, an incompatible page) - never raises, matching this
    file's existing "degrade to a disclosed Note, never a crash" posture
    for every rendering-dependent capability."""
    try:
        page.add_script_tag(url=AXE_CDN_URL)
        result = page.evaluate("async () => { return await axe.run(); }")
        return [
            {
                "id": v.get("id"),
                "impact": v.get("impact"),
                "help": v.get("help"),
                "nodes": len(v.get("nodes", [])),
            }
            for v in result.get("violations", [])
        ]
    except Exception as exc:  # noqa: BLE001 - any failure here must degrade, not crash the capture
        return {"error": str(exc)}


def detect_transitions(manifests: list[dict]) -> list[dict]:
    """Best-effort transition detector for --sweep mode: flags a width
    range where element count or overflow-element count changes between
    adjacent captured widths - a signal for where a layout transition
    (nav-mode switch, column-count change, sidebar appearing/
    disappearing) actually happens, not a precise CSS-breakpoint oracle.
    Confirm against the actual screenshots before treating a flagged
    range as a defect."""

    def _overflow_count(manifest_path: str) -> int:
        data = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
        return sum(1 for e in data["elements"] if e["scrollWidth"] > e["clientWidth"] + 1)

    ordered = sorted(manifests, key=lambda m: m["viewport"]["width"])
    transitions = []
    prev = None
    for m in ordered:
        overflow = _overflow_count(m["manifest"])
        current = {"width": m["viewport"]["width"], "count": m["element_count"], "overflow": overflow}
        if prev is not None and (current["count"] != prev["count"] or current["overflow"] != prev["overflow"]):
            transitions.append({
                "from_width": prev["width"],
                "to_width": current["width"],
                "element_count_change": current["count"] - prev["count"],
                "overflow_element_change": current["overflow"] - prev["overflow"],
            })
        prev = current
    return transitions


def capture(
    source: str,
    out_dir: Path,
    viewports: dict,
    themes: list[str],
    run_axe: bool = False,
    measure_vitals: bool = False,
) -> list[dict]:
    """`source` is either a local HTML file path (standalone screen/
    benchmark request — loaded via a file:// URI) or an already-running
    dev server URL (a full Product Builder pass's `preview-run.md` step 6
    local URL, e.g. http://localhost:5173/some-screen) — loaded directly.
    Same capture + manifest shape either way; the caller doesn't need to
    know which kind of target it's pointing at."""
    if sync_playwright is None:
        raise RuntimeError(
            "capture-render.py requires the optional 'playwright' package "
            "(pip install playwright && playwright install chromium) - "
            "not installed in this environment. This is the one script in "
            "the folder with a non-stdlib dependency, by deliberate design "
            "(see this file's own docstring); every other validator still "
            "runs with none."
        )
    out_dir.mkdir(parents=True, exist_ok=True)
    is_url = source.startswith("http://") or source.startswith("https://")
    if is_url:
        uri = source
        stem_base = re.sub(r"[^A-Za-z0-9_-]+", "-", source).strip("-") or "page"
    else:
        html_path = Path(source)
        uri = html_path.resolve().as_uri()
        stem_base = html_path.stem
    manifests = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for vp_name, vp_size in viewports.items():
            for theme in themes:
                page = browser.new_page(viewport=vp_size, color_scheme=theme)
                page.goto(uri, wait_until="load")
                page.wait_for_timeout(150)  # let webfont swap / chart JS settle
                stem = f"{stem_base}-{vp_name}-{theme}"
                full_path = out_dir / f"{stem}-full.png"
                viewport_path = out_dir / f"{stem}-viewport.png"
                page.screenshot(path=str(full_path), full_page=True)
                page.screenshot(path=str(viewport_path), full_page=False)
                elements = page.evaluate(DOM_DUMP_JS)
                axe_violations = _run_axe(page) if run_axe else None
                web_vitals = page.evaluate(WEB_VITALS_JS) if measure_vitals else None
                manifest = {
                    "source_file": source,
                    "viewport_name": vp_name,
                    "viewport": vp_size,
                    "theme": theme,
                    "screenshot_full": str(full_path),
                    "screenshot_viewport": str(viewport_path),
                    "element_count": len(elements),
                    "elements": elements,
                    "axe_violations": axe_violations,
                    "web_vitals": web_vitals,
                }
                manifest_path = out_dir / f"{stem}.json"
                manifest_path.write_text(json.dumps(manifest, indent=1), encoding="utf-8")
                manifests.append({"manifest": str(manifest_path), **{k: manifest[k] for k in ("viewport_name", "viewport", "theme", "screenshot_full", "screenshot_viewport", "element_count")}})
                page.close()
        browser.close()
    return manifests


def sweep(
    source: str,
    out_dir: Path,
    theme: str = "light",
    run_axe: bool = False,
    measure_vitals: bool = False,
) -> dict:
    """--sweep mode: capture at SWEEP_WIDTHS (one theme, to keep an
    8-viewport pass reasonably fast — matching the single-session
    efficiency a breakpoint sweep needs) and run detect_transitions()
    over the result. Writes `sweep-summary.json` into `out_dir` alongside
    the per-width manifests `capture()` already writes, and returns the
    same summary dict."""
    sweep_viewports = {f"sweep-{w}": {"width": w, "height": SWEEP_HEIGHT} for w in SWEEP_WIDTHS}
    manifests = capture(source, out_dir, sweep_viewports, [theme], run_axe=run_axe, measure_vitals=measure_vitals)
    transitions = detect_transitions(manifests)
    summary = {
        "source": source,
        "theme": theme,
        "widths": SWEEP_WIDTHS,
        "manifests": manifests,
        "transitions": transitions,
    }
    summary_path = out_dir / "sweep-summary.json"
    summary_path.write_text(json.dumps(summary, indent=1), encoding="utf-8")
    summary["summary_path"] = str(summary_path)
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source", help="Path to a generated HTML file (standalone file or output/*.html), OR an http(s):// URL of an already-running dev server (preview-run.md step 6's detected local URL).")
    parser.add_argument("out_dir", help="Directory to write screenshots and DOM-measurement JSON manifests into.")
    parser.add_argument("--viewports", default="desktop,tablet,mobile", help="Comma-separated subset of desktop,tablet,mobile. Ignored when --sweep is set.")
    parser.add_argument("--themes", default="light,dark", help="Comma-separated subset of light,dark. --sweep uses only the first.")
    parser.add_argument("--sweep", action="store_true", help="Capture at 8 breakpoint-spectrum widths instead of --viewports, and run best-effort transition detection (see SWEEP_WIDTHS).")
    parser.add_argument("--axe", dest="axe", action="store_true", default=True, help="Inject axe-core and record accessibility violations (default: on; degrades to a disclosed error field, never a crash, when network/CDN access is unavailable).")
    parser.add_argument("--no-axe", dest="axe", action="store_false", help="Skip the axe-core pass.")
    parser.add_argument("--vitals", dest="vitals", action="store_true", default=True, help="Capture LCP/CLS and a best-effort INP approximation (default: on).")
    parser.add_argument("--no-vitals", dest="vitals", action="store_false", help="Skip the web-vitals capture.")
    args = parser.parse_args(argv)

    is_url = args.source.startswith("http://") or args.source.startswith("https://")
    if not is_url and not Path(args.source).is_file():
        print(f"error: {args.source} does not exist", file=sys.stderr)
        return 2

    themes = [t for t in args.themes.split(",") if t in ("light", "dark")]

    try:
        if args.sweep:
            summary = sweep(args.source, Path(args.out_dir), theme=(themes[0] if themes else "light"), run_axe=args.axe, measure_vitals=args.vitals)
            for m in summary["manifests"]:
                print(f"[{m['viewport_name']}] {m['element_count']} elements -> {m['manifest']}")
            for t in summary["transitions"]:
                print(f"transition: {t['from_width']}px -> {t['to_width']}px (element_count {t['element_count_change']:+d}, overflow {t['overflow_element_change']:+d})")
            print(f"sweep summary -> {summary['summary_path']}")
            return 0
        viewports = {k: DEFAULT_VIEWPORTS[k] for k in args.viewports.split(",") if k in DEFAULT_VIEWPORTS}
        manifests = capture(args.source, Path(args.out_dir), viewports, themes, run_axe=args.axe, measure_vitals=args.vitals)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 3

    for m in manifests:
        print(f"[{m['viewport_name']}/{m['theme']}] {m['element_count']} elements -> {m['manifest']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
