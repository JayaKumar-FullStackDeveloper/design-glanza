# Template: Data Bindings

## Purpose
The machine-readable declaration of a screen's cross-artifact numeric
relationships — which KPI claims to equal which chart's latest point,
which supporting metric is derived from which other KPIs, which
annotation claims to be a series' peak, which table total restates which
KPI — satisfying `config/quality-gates.md`'s **B15** Cross-Artifact Data
Realism requirement. One instance per screen that has at least one KPI
tied to a chart, table, or another KPI (`ui-engine/visual-benchmark.md`'s
Chart verification pipeline, Data Realism step). A screen with no such
relationship (e.g. a single static KPI with nothing else to agree with)
needs no instance — this is not a universal per-screen requirement the
way `templates/visual-gap-analysis.md` is.

## Why this exists
A benchmark run found three real defects a purely visual audit never
catches, because each individual number renders without error: a KPI
tile's total disagreed with its own supporting chart's latest point, a
displayed average mathematically contradicted the two KPIs it was
computed from, and a chart's labeled "peak" didn't equal the series'
actual maximum. Representing these relationships in a machine-readable
form (`scripts/validate-data-consistency.py` recomputes each one from the
manifest's own `series` data) catches this class of defect the same
deterministic way `scripts/validate-tokens.py` catches a contrast failure
— by calculating, not by an agent eyeballing two numbers on the same
screen and trusting they agree.

## Required fields

```json
{
  "screen": "SCREEN-NNN",
  "today": "Mar 11",
  "series": {
    "<seriesId>": { "dates": ["...", "..."], "values": [0, 0] }
  },
  "kpis": [
    {
      "id": "<kpiId>",
      "value": 0,
      "deltaPct": 0.0,
      "derivedFrom": { "kind": "latestInSeries", "series": "<seriesId>" }
    }
  ],
  "annotations": [
    { "series": "<seriesId>", "kind": "peak", "claimedValue": 0 }
  ],
  "tableTotals": [
    { "label": "...", "claimedValue": 0, "matchesKpi": "<kpiId>" }
  ],
  "subtotals": [
    { "parts": [0, 0], "claimedTotal": 0 }
  ]
}
```

| Field | Required | Meaning |
|---|---|---|
| `screen` | Yes | The `SCREEN-NNN` this manifest describes. |
| `today` | Where any KPI uses `latestInSeries` | The date the screen claims is "today"/"current" — checked against every cited series' own last plotted date. |
| `series.<id>.dates` / `.values` | Yes, per series a KPI or annotation cites | The actual plotted data, in the same order the chart renders it. |
| `kpis[].derivedFrom.kind = "latestInSeries"` | — | This KPI claims to equal `series.values[-1]`; if it also states `deltaPct`, that's checked against the series' own last-two-points delta too. |
| `kpis[].derivedFrom.kind = "ratio"` | — | This KPI claims to equal `numeratorKpi.value / denominatorKpi.value` (e.g. Average Order Value = Revenue / Total Orders). |
| `kpis[]` with no `derivedFrom` | — | A KPI with no declared relationship is not checked — per the "pairing contract, not a one-time pass" discipline this script shares with `validate-tokens.py`, an undeclared relationship is a fresh check for whoever introduces one, not a gap here. |
| `annotations[].kind = "peak"` | — | Claims to equal `max(series.values)` for the cited series. |
| `tableTotals[].matchesKpi` | — | Claims to equal the cited KPI's own `value` — a table footer restating a KPI headline. |
| `subtotals[].claimedTotal` | — | Claims to equal `sum(parts)`. |

## Quality criteria
- Checked against **B15**'s Cross-Artifact Data Realism requirement —
  `scripts/validate-data-consistency.py` recomputes every declared
  relationship above from the manifest's own `series` data; any disagreement
  with the stated `value`/`claimedValue`/`deltaPct` is a Major finding,
  routed the same way a Chart pipeline Data Realism finding already is.
- Only declared relationships are checked — this file does not require
  every number on a screen to have one; it requires that whichever ones
  *are* declared stay arithmetically honest.
- A tolerance applies (absolute $0.02 / 0.5% relative, whichever a check
  uses) to absorb legitimate rounding — never to mask a genuine
  disagreement; a benchmark-scale mismatch (a wrong AOV off by a factor of
  ~4) clears either tolerance by a wide margin.

## Example structure
_Illustrative, domain-neutral — not real product content._

```json
{
  "screen": "SCREEN-001",
  "today": "Mar 11",
  "series": {
    "orders": { "dates": ["Mar 10", "Mar 11"], "values": [22918, 24386] },
    "revenue": { "dates": ["Mar 10", "Mar 11"], "values": [610988.70, 679418.20] }
  },
  "kpis": [
    { "id": "totalOrders", "value": 24386, "deltaPct": 6.4,
      "derivedFrom": { "kind": "latestInSeries", "series": "orders" } },
    { "id": "revenue", "value": 679418.20, "deltaPct": 11.2,
      "derivedFrom": { "kind": "latestInSeries", "series": "revenue" } },
    { "id": "avgOrderValue", "value": 27.86,
      "derivedFrom": { "kind": "ratio", "numeratorKpi": "revenue", "denominatorKpi": "totalOrders" } }
  ],
  "annotations": [
    { "series": "revenue", "kind": "peak", "claimedValue": 748920 }
  ]
}
```

## Explicitly not here
- Whether a value is independently *realistic* (plausible ranges, non-round
  figures, correct currency/date formatting) → `ui-engine/
  visual-benchmark.md`'s Chart verification pipeline's Data Realism step —
  this template's check is relational (do these numbers agree with each
  other), not absolute (is this number itself believable).
- The chart/KPI/table components themselves → `templates/
  screen-specification.md`, `templates/component-spec.md`.
- The gap-type/priority classification a failure here routes through →
  `ui-engine/visual-benchmark.md`'s gap-type table (**Data inconsistency**).
