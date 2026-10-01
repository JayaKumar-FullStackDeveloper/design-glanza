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
  text, and a structural path for identifying it in a report.

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
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

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
      parentPath: e.parentElement ? cssPath(e.parentElement) : null
    });
  }
  return out;
}
"""


def capture(source: str, out_dir: Path, viewports: dict, themes: list[str]) -> list[dict]:
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
                manifest = {
                    "source_file": source,
                    "viewport_name": vp_name,
                    "viewport": vp_size,
                    "theme": theme,
                    "screenshot_full": str(full_path),
                    "screenshot_viewport": str(viewport_path),
                    "element_count": len(elements),
                    "elements": elements,
                }
                manifest_path = out_dir / f"{stem}.json"
                manifest_path.write_text(json.dumps(manifest, indent=1), encoding="utf-8")
                manifests.append({"manifest": str(manifest_path), **{k: manifest[k] for k in ("viewport_name", "theme", "screenshot_full", "screenshot_viewport", "element_count")}})
                page.close()
        browser.close()
    return manifests


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source", help="Path to a generated HTML file (standalone file or output/*.html), OR an http(s):// URL of an already-running dev server (preview-run.md step 6's detected local URL).")
    parser.add_argument("out_dir", help="Directory to write screenshots and DOM-measurement JSON manifests into.")
    parser.add_argument("--viewports", default="desktop,tablet,mobile", help="Comma-separated subset of desktop,tablet,mobile.")
    parser.add_argument("--themes", default="light,dark", help="Comma-separated subset of light,dark.")
    args = parser.parse_args(argv)

    is_url = args.source.startswith("http://") or args.source.startswith("https://")
    if not is_url and not Path(args.source).is_file():
        print(f"error: {args.source} does not exist", file=sys.stderr)
        return 2

    viewports = {k: DEFAULT_VIEWPORTS[k] for k in args.viewports.split(",") if k in DEFAULT_VIEWPORTS}
    themes = [t for t in args.themes.split(",") if t in ("light", "dark")]

    try:
        manifests = capture(args.source, Path(args.out_dir), viewports, themes)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 3

    for m in manifests:
        print(f"[{m['viewport_name']}/{m['theme']}] {m['element_count']} elements -> {m['manifest']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
