"""
compare-reference-visual.py

Responsibility
--------------
The COMPARE step of the REFERENCE -> EXTRACT -> DESIGN DIRECTION ->
GENERATE -> RENDER -> COMPARE REFERENCE vs GENERATED -> IDENTIFY DELTAS ->
FIX flow (this version's quality-engine upgrade to `ui-engine/
visual-benchmark.md`). Takes a reference design-sample image (already
living under `design-samples/*/`) and a generated screenshot
(`capture-render.py`'s `*-full.png` or `*-viewport.png` output) and
produces a deterministic, numeric similarity report — never "Reference
considered" or "Visual comparison completed" with no evidence behind it.

This is deliberately a COARSE structural/tonal comparison, not a claim of
pixel-perfect matching — `ui-engine/visual-benchmark.md` and the
design-samples READMEs are explicit that a reference is design language,
not a pixel target a generated screen must clone. What this script
measures:

1. Color-relationship similarity — a coarse color histogram (quantized
   to a small bucket count per channel) compared via histogram
   intersection, catching a generated screen that drifted to a wildly
   different palette/tonal register than its stated reference (e.g.
   reference is a dark, saturated dashboard and the generated screen is
   flat light-gray) without demanding identical pixels.
2. Luminance/density layout similarity — both images downsampled to a
   small fixed grid (e.g. 24x16 cells) of mean luminance, then compared
   cell-by-cell. This is a coarse proxy for "does the overall
   light/dark rhythm and content density distribution resemble the
   reference's layout" (e.g. a reference with a dark left nav rail and
   light content area vs. a generated screen with no visible rail at
   all) — again never claiming exact layout matching, only flagging a
   gross structural mismatch.
3. Aspect-ratio / proportion note — reported for context (resized to a
   common canvas before comparison so this never fails the run, but a
   large source aspect-ratio difference is surfaced since it affects how
   much the other two numbers mean).

Uses Pillow (PIL) — the second and only other non-stdlib dependency in
this folder (`capture-render.py` carries the first, Playwright), for
exactly the same reason: no stdlib substitute exists for real image
decoding/resampling. Degrades with a clear, actionable error (never a
silent false pass) if Pillow isn't installed.

What this deliberately does NOT do
------------------------------------
Judge whether a mismatch is *bad* — thresholds here flag "meaningfully
different from the stated reference," and a human/agent still decides
whether that's an intended departure (the design-direction phase may
have deliberately diverged on a specific attribute) or a real gap to
fix, same as every other Finding in this skill. Does not do semantic
object matching (it cannot tell you "the KPI row moved from top to
bottom") — that level of comparison is what
`validate-rendered-layout.py`'s own sibling-set geometry plus a human/
agent's side-by-side look is for; this script is the fast, deterministic
first pass that makes "did anyone actually compare this" answerable
with numbers instead of prose.
"""

from __future__ import annotations

import argparse
import json
import sys
import warnings
from pathlib import Path

try:
    from PIL import Image
except ImportError:  # pragma: no cover - environment without the optional dependency
    Image = None

warnings.filterwarnings("ignore", category=DeprecationWarning, module="PIL")

GRID_COLS = 24
GRID_ROWS = 16
COLOR_BUCKETS_PER_CHANNEL = 4  # 4^3 = 64-bin coarse histogram

# Below this, flag a likely-meaningful palette/tonal drift from the stated
# reference. Intersection of two identical histograms is 1.0; two
# completely disjoint palettes is 0.0. 0.35 is deliberately forgiving —
# this only catches a gross register change, not a refined palette swap
# within the same family.
COLOR_SIMILARITY_FLOOR = 0.35
# A real benchmark run found layout_similarity can legitimately sit well
# above LAYOUT_SIMILARITY_FLOOR (never a meaningful_mismatch) yet still
# have dropped sharply from a near-identical-composition score with no
# explanation attached — e.g. a genuinely new screen's composition
# differing on purpose from its reference frame. This soft, non-blocking
# floor flags that zone with an advisory Note (never counted toward
# meaningful_mismatch, same "Note:"-prefixed convention as the
# aspect-ratio note below) pointing at the judgment call that already
# exists for this (`ui-engine/visual-benchmark.md`'s Direction-vs-
# Generated principle) rather than inventing a new one here.
COMPOSITION_INTENT_ADVISORY_FLOOR = 0.75

# Mean-grid luminance correlation floor, same reasoning as above applied
# to layout/density rhythm instead of color.
LAYOUT_SIMILARITY_FLOOR = 0.30

ASPECT_RATIO_NOTE_THRESHOLD = 0.25  # relative difference worth surfacing


def _require_pillow():
    if Image is None:
        raise RuntimeError(
            "compare-reference-visual.py requires the optional 'Pillow' "
            "package (pip install Pillow) - not installed in this "
            "environment. This and capture-render.py are the only two "
            "scripts in this folder with a non-stdlib dependency, by "
            "deliberate design (see this file's own docstring)."
        )


def _color_histogram(img) -> dict:
    img = img.convert("RGB").resize((160, 120))
    hist: dict = {}
    step = 256 // COLOR_BUCKETS_PER_CHANNEL
    pixels = img.getdata()
    for r, g, b in pixels:
        key = (r // step, g // step, b // step)
        hist[key] = hist.get(key, 0) + 1
    total = sum(hist.values()) or 1
    return {k: v / total for k, v in hist.items()}


def _histogram_intersection(a: dict, b: dict) -> float:
    keys = set(a) | set(b)
    return sum(min(a.get(k, 0.0), b.get(k, 0.0)) for k in keys)


def _luminance_grid(img) -> list[float]:
    gray = img.convert("L").resize((GRID_COLS, GRID_ROWS))
    return [p / 255.0 for p in gray.getdata()]


def _grid_correlation(a: list[float], b: list[float]) -> float:
    n = len(a)
    mean_a, mean_b = sum(a) / n, sum(b) / n
    cov = sum((a[i] - mean_a) * (b[i] - mean_b) for i in range(n))
    var_a = sum((x - mean_a) ** 2 for x in a)
    var_b = sum((x - mean_b) ** 2 for x in b)
    denom = (var_a * var_b) ** 0.5
    if denom == 0:
        return 1.0 if var_a == var_b else 0.0
    # Pearson correlation in [-1, 1] -> rescale to [0, 1] similarity.
    return (cov / denom + 1.0) / 2.0


def compare(reference_path: Path, generated_path: Path) -> dict:
    _require_pillow()
    ref_img = Image.open(reference_path)
    gen_img = Image.open(generated_path)

    ref_ratio = ref_img.width / ref_img.height
    gen_ratio = gen_img.width / gen_img.height
    ratio_diff = abs(ref_ratio - gen_ratio) / max(ref_ratio, gen_ratio)

    color_sim = _histogram_intersection(_color_histogram(ref_img), _color_histogram(gen_img))
    layout_sim = _grid_correlation(_luminance_grid(ref_img), _luminance_grid(gen_img))

    flags = []
    if color_sim < COLOR_SIMILARITY_FLOOR:
        flags.append(
            f"Color/tonal register differs meaningfully from reference "
            f"(histogram intersection {color_sim:.2f} < floor {COLOR_SIMILARITY_FLOOR})"
        )
    if layout_sim < LAYOUT_SIMILARITY_FLOOR:
        flags.append(
            f"Layout/density rhythm differs meaningfully from reference "
            f"(luminance-grid correlation {layout_sim:.2f} < floor {LAYOUT_SIMILARITY_FLOOR})"
        )
    elif layout_sim < COMPOSITION_INTENT_ADVISORY_FLOOR:
        flags.append(
            f"Note: layout_similarity ({layout_sim:.2f}) is above the "
            f"meaningful-mismatch floor ({LAYOUT_SIMILARITY_FLOOR}) but well "
            f"below a near-identical composition — this is expected and "
            f"correct for a genuinely new screen whose composition "
            f"legitimately differs from its reference frame (a different "
            f"content shape, not a defect); it is also what a real gap "
            f"would look like before it got bad enough to cross the floor. "
            f"Resolve by checking Direction-vs-Generated, not "
            f"Reference-vs-Generated (`ui-engine/visual-benchmark.md`'s "
            f"existing principle) — never treat this Note alone as "
            f"evidence of a gap, and never suppress it without that check "
            f"having actually been made."
        )
    if ratio_diff > ASPECT_RATIO_NOTE_THRESHOLD:
        flags.append(
            f"Note: reference aspect ratio ({ref_ratio:.2f}) and generated "
            f"screenshot aspect ratio ({gen_ratio:.2f}) differ by "
            f"{ratio_diff * 100:.0f}% - color/layout similarity numbers above "
            f"are weaker evidence at this difference"
        )

    return {
        "reference": str(reference_path),
        "generated": str(generated_path),
        "color_similarity": round(color_sim, 3),
        "layout_similarity": round(layout_sim, 3),
        "aspect_ratio_reference": round(ref_ratio, 3),
        "aspect_ratio_generated": round(gen_ratio, 3),
        "flags": flags,
        "meaningful_mismatch": bool(flags) and any("Note:" not in f for f in flags),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("reference_image", help="Path to the design-samples reference image used as visual inspiration.")
    parser.add_argument("generated_screenshot", help="Path to a capture-render.py screenshot (*-full.png or *-viewport.png).")
    args = parser.parse_args(argv)

    ref_path, gen_path = Path(args.reference_image), Path(args.generated_screenshot)
    for p in (ref_path, gen_path):
        if not p.is_file():
            print(f"error: {p} does not exist", file=sys.stderr)
            return 2

    try:
        result = compare(ref_path, gen_path)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 3

    print(json.dumps(result, indent=2))
    return 1 if result["meaningful_mismatch"] else 0


if __name__ == "__main__":
    sys.exit(main())
