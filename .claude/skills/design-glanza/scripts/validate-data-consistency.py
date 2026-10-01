"""
validate-data-consistency.py

Responsibility
--------------
Deterministic, structural cross-artifact data-realism check — gate **B15**'s
Chart verification pipeline's Data Realism step, extended. A benchmark run
found three real, user-visible defects a purely visual audit never catches
because each number individually renders without error: a KPI tile's total
didn't match its own supporting chart's latest point, a displayed average
("Average Order Value: $31.60") mathematically contradicted the two KPIs it
was computed from (Revenue/Orders actually implied $7.65), and a chart's
labeled "Peak" value didn't correspond to the series' actual maximum.

This script validates `product-builder/ui/data-bindings/<SCREEN-NNN>.json`
— one manifest per screen that has at least one KPI tied to a chart or
table, per `templates/data-bindings.md`. The manifest is the *declared*
relationship between a screen's displayed numbers (a KPI must equal its
chart's latest point, a KPI must equal a stated ratio of two other KPIs,
an annotation must equal its series' actual max, a table total must match
the KPI it restates) — this script recomputes each declared relationship
from the manifest's own `series` data and flags where the *displayed*
value disagrees with what the relationship actually computes to.

What this deliberately does NOT check
--------------------------------------
Whether the manifest itself was built correctly from the real generated
screen (an agent's job — the manifest is a machine-readable restatement of
what the screen displays, not a re-derivation from pixels); whether a
number is "realistic" in the Rule 10/chart-label-realism sense (plausible
ranges, non-round figures, correct currency/date formatting) — that's
`ui-engine/visual-benchmark.md`'s existing Chart pipeline Data Realism
step, which this script extends rather than replaces; arithmetic the
manifest doesn't declare a relationship for at all (an unrelated KPI with
no `derivedFrom` is not flagged as "unchecked," per the same "pairing
contract, not a one-time pass" discipline `scripts/validate-tokens.py`
already applies to contrast — a declared relationship is checked, an
undeclared one is a fresh check for whoever introduces it later, not a
gap here).

Status: implemented.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import _common
from _common import Finding, read_text

# Absolute tolerance for a currency/count comparison — guards against
# legitimate floating-point/rounding noise (e.g. $679,418.20 stored as
# 679418.199999) without masking a genuine mismatch; a real data-realism
# defect is never this close (the benchmark's own example was off by a
# factor of ~4, not a cent).
ABS_TOLERANCE = 0.02
# Relative tolerance (as a fraction) for a ratio/percentage comparison,
# where an absolute cent-level tolerance doesn't make sense (e.g. a delta
# percentage) — generous enough to absorb a manifest author rounding a
# displayed "+6.4%" from a true 6.405%, tight enough to still catch the
# benchmark's own ~4x AOV mismatch by a wide margin.
REL_TOLERANCE = 0.005


def _approx_equal(a: float, b: float) -> bool:
    if abs(a - b) <= ABS_TOLERANCE:
        return True
    denom = max(abs(a), abs(b), 1e-9)
    return abs(a - b) / denom <= REL_TOLERANCE


def _load_manifest(path: Path) -> tuple[dict | None, str | None]:
    text = read_text(path)
    if text is None:
        return None, "missing-file"
    try:
        return json.loads(text), None
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON: {exc}"


def _kpi_by_id(manifest: dict) -> dict:
    return {k.get("id"): k for k in manifest.get("kpis", []) if isinstance(k, dict) and k.get("id")}


def _check_latest_in_series(manifest: dict, kpi: dict, rel: str) -> list[Finding]:
    findings: list[Finding] = []
    derived = kpi.get("derivedFrom") or {}
    series_id = derived.get("series")
    series = (manifest.get("series") or {}).get(series_id)
    if not isinstance(series, dict):
        findings.append(Finding(
            "Major",
            f"KPI '{kpi.get('id')}' cites series '{series_id}' via "
            "derivedFrom.kind=latestInSeries, but that series doesn't exist "
            "in this manifest",
            rel, "data-consistency-missing-series",
        ))
        return findings
    values = series.get("values") or []
    dates = series.get("dates") or []
    if not values:
        return findings
    latest = values[-1]
    kpi_value = kpi.get("value")
    if isinstance(kpi_value, (int, float)) and not _approx_equal(float(kpi_value), float(latest)):
        findings.append(Finding(
            "Major",
            f"KPI '{kpi.get('id')}' displays {kpi_value}, but its own chart "
            f"('{series_id}') latest data point is {latest} — a KPI claiming "
            "to represent the current/today value must equal that chart's "
            "own last point",
            rel, "data-consistency-kpi-chart-mismatch",
        ))

    # "Today" consistency — the manifest's stated `today` must be the
    # series' actual last plotted date, not an earlier/later one.
    today = manifest.get("today")
    if today is not None and dates and dates[-1] != today:
        findings.append(Finding(
            "Major",
            f"Manifest states today='{today}', but series '{series_id}' "
            f"ends at '{dates[-1]}' — 'today' must correspond to the latest "
            "plotted data point, not a different date in (or past the end "
            "of) the displayed range",
            rel, "data-consistency-today-mismatch",
        ))

    # Delta-percentage consistency, where the KPI also states one.
    delta_pct = kpi.get("deltaPct")
    if isinstance(delta_pct, (int, float)) and len(values) >= 2 and values[-2]:
        actual_pct = (values[-1] - values[-2]) / values[-2] * 100.0
        if not _approx_equal(float(delta_pct), actual_pct) and abs(actual_pct - delta_pct) > 0.15:
            findings.append(Finding(
                "Major",
                f"KPI '{kpi.get('id')}' displays a {delta_pct:+.1f}% delta, "
                f"but series '{series_id}'s own last two points imply "
                f"{actual_pct:+.2f}% — the displayed percentage does not "
                "correspond to the underlying values",
                rel, "data-consistency-percentage-mismatch",
            ))
    return findings


def _check_ratio(manifest: dict, kpi: dict, by_id: dict, rel: str) -> list[Finding]:
    findings: list[Finding] = []
    derived = kpi["derivedFrom"]
    num_id, den_id = derived.get("numeratorKpi"), derived.get("denominatorKpi")
    num_kpi, den_kpi = by_id.get(num_id), by_id.get(den_id)
    if num_kpi is None or den_kpi is None:
        findings.append(Finding(
            "Major",
            f"KPI '{kpi.get('id')}' declares a ratio derivedFrom citing "
            f"'{num_id}'/'{den_id}', but one or both aren't defined KPIs in "
            "this manifest",
            rel, "data-consistency-missing-kpi",
        ))
        return findings
    num_val, den_val = num_kpi.get("value"), den_kpi.get("value")
    if not (isinstance(num_val, (int, float)) and isinstance(den_val, (int, float))) or den_val == 0:
        return findings
    actual = num_val / den_val
    kpi_value = kpi.get("value")
    if isinstance(kpi_value, (int, float)) and not _approx_equal(float(kpi_value), actual):
        findings.append(Finding(
            "Major",
            f"KPI '{kpi.get('id')}' displays {kpi_value}, but "
            f"'{num_id}' ({num_val}) / '{den_id}' ({den_val}) actually "
            f"computes to {actual:.2f} — a supporting metric must equal "
            "its own stated derivation from its parent KPIs, not an "
            "unrelated figure",
            rel, "data-consistency-ratio-mismatch",
        ))
    return findings


def _check_annotations(manifest: dict, rel: str) -> list[Finding]:
    findings: list[Finding] = []
    for ann in manifest.get("annotations", []):
        if not isinstance(ann, dict) or ann.get("kind") != "peak":
            continue
        series = (manifest.get("series") or {}).get(ann.get("series"))
        if not isinstance(series, dict):
            continue
        values = series.get("values") or []
        if not values:
            continue
        actual_max = max(values)
        claimed = ann.get("claimedValue")
        if isinstance(claimed, (int, float)) and not _approx_equal(float(claimed), float(actual_max)):
            findings.append(Finding(
                "Major",
                f"Annotation claims a peak of {claimed} on series "
                f"'{ann.get('series')}', but that series' actual maximum is "
                f"{actual_max} — a labeled peak must correspond to the "
                "series' real highest value",
                rel, "data-consistency-peak-mismatch",
            ))
    return findings


def _check_table_totals(manifest: dict, by_id: dict, rel: str) -> list[Finding]:
    findings: list[Finding] = []
    for entry in manifest.get("tableTotals", []):
        if not isinstance(entry, dict):
            continue
        kpi_id = entry.get("matchesKpi")
        kpi = by_id.get(kpi_id)
        if kpi is None:
            continue
        claimed, kpi_value = entry.get("claimedValue"), kpi.get("value")
        if isinstance(claimed, (int, float)) and isinstance(kpi_value, (int, float)) \
                and not _approx_equal(float(claimed), float(kpi_value)):
            findings.append(Finding(
                "Major",
                f"Table total '{entry.get('label', kpi_id)}' displays "
                f"{claimed}, but the KPI it restates ('{kpi_id}') displays "
                f"{kpi_value} — a table total must agree with the KPI "
                "headline claiming the same figure",
                rel, "data-consistency-table-kpi-mismatch",
            ))
    return findings


def _check_subtotals(manifest: dict, rel: str) -> list[Finding]:
    findings: list[Finding] = []
    for entry in manifest.get("subtotals", []):
        if not isinstance(entry, dict):
            continue
        parts, claimed_total = entry.get("parts"), entry.get("claimedTotal")
        if not isinstance(parts, list) or not all(isinstance(p, (int, float)) for p in parts):
            continue
        actual_total = sum(parts)
        if isinstance(claimed_total, (int, float)) and not _approx_equal(float(claimed_total), actual_total):
            findings.append(Finding(
                "Major",
                f"Subtotal parts {parts} sum to {actual_total}, but the "
                f"displayed total is {claimed_total} — a subtotal must "
                "equal the sum of its own parts",
                rel, "data-consistency-subtotal-mismatch",
            ))
    return findings


def validate_manifest(manifest: dict, rel: str) -> list[Finding]:
    findings: list[Finding] = []
    by_id = _kpi_by_id(manifest)
    for kpi in manifest.get("kpis", []):
        if not isinstance(kpi, dict):
            continue
        derived = kpi.get("derivedFrom")
        if not isinstance(derived, dict):
            continue  # no declared relationship — nothing to check, not a gap (see docstring)
        kind = derived.get("kind")
        if kind == "latestInSeries":
            findings += _check_latest_in_series(manifest, kpi, rel)
        elif kind == "ratio":
            findings += _check_ratio(manifest, kpi, by_id, rel)
    findings += _check_annotations(manifest, rel)
    findings += _check_table_totals(manifest, by_id, rel)
    findings += _check_subtotals(manifest, rel)
    return findings


def validate(product_builder_dir: Path) -> list[Finding]:
    findings: list[Finding] = []
    bindings_dir = product_builder_dir / "ui" / "data-bindings"
    if not bindings_dir.is_dir():
        return findings  # no manifests declared this pass — not itself a finding, per B15's chart-only trigger
    for manifest_path in sorted(bindings_dir.glob("*.json")):
        rel = f"ui/data-bindings/{manifest_path.name}"
        manifest, err = _load_manifest(manifest_path)
        if err:
            findings.append(Finding("Major", f"data-bindings manifest {err}", rel, "load-error"))
            continue
        findings += validate_manifest(manifest, rel)
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("product_builder_dir", help="Path to a product-builder/ directory, or a single manifest.json file.")
    args = parser.parse_args(argv)

    target = Path(args.product_builder_dir)
    if target.is_file():
        manifest, err = _load_manifest(target)
        findings = [Finding("Major", f"data-bindings manifest {err}", target.name, "load-error")] if err else validate_manifest(manifest, target.name)
    else:
        findings = validate(target)

    if not findings:
        print("validate-data-consistency: no findings.")
        return 0
    for f in findings:
        print(f)
    return 1 if any(f.severity in ("Blocker", "Major") for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
