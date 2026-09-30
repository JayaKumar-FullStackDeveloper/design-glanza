# Template: Visual Baseline

## Purpose
One `SCREEN-NNN`'s captured structural snapshot — the known-good state
every later pass diffs against, per `visual-regression/baseline-model.md`.

## Required inputs
- The screen's confirmed-clean `templates/visual-gap-analysis.md` instance
  (Final status: pass) — a baseline is never captured from an unconfirmed
  draft.
- `templates/screen-architecture.md`'s region map,
  `templates/component-spec.md`'s Registry base + variant per component,
  `design-tokens/token-schema.md` paths actually resolved.

## Output structure (human-readable, `ui/visual-baselines.md`)
- **Header** — per `config/output-contract.md`, plus the pass/date
  captured and the confirming `visual-gap-analysis.md` reference.
- **Regions** — name and order.
- **Components per region** — `COMPONENT-NNN`, Registry base, variant.
- **Token paths** — per component, the resolved paths for spacing,
  radius, color, typography.
- **Design Direction summary** — register, density in effect.
- **Breakpoint behavior** — reflow technique per breakpoint.

## Machine-readable twin
`product-builder/ui/baselines/<SCREEN-NNN>.json`:

```json
{
  "screen": "SCREEN-011",
  "capturedAtPass": 2,
  "capturedDate": "2026-10-XX",
  "confirmedBy": "ui/visual-gap-analysis.md#SCREEN-011-pass2",
  "designDirection": { "register": "Dense Enterprise", "density": "compact" },
  "regions": [
    {
      "name": "primary content",
      "components": [
        {
          "id": "COMPONENT-004",
          "registryBase": "table",
          "variant": "selectable",
          "tokens": {
            "spacing": "spacing.16",
            "radius": "radius.md",
            "color": "color.semantic.surface",
            "typography": "typography.size.body"
          }
        }
      ]
    }
  ],
  "breakpoints": { "mobile": "stacked-cards", "tablet": "stacked-cards", "desktop": "horizontal-scroll-pinned-first-column" }
}
```

## Quality criteria
- Every component in the region map has a token entry for every category
  it actually uses — a component with no token block is itself a gap
  (either the spec is incomplete, or the capture is).
- `confirmedBy` references a real, passing `visual-gap-analysis.md`
  instance — a baseline with no such reference is invalid per
  `baseline-model.md`'s capture rule.

## Explicitly not here
- What a diff against this snapshot looks like →
  `templates/visual-diff-report.md`.
- How this gets replaced → `visual-regression/baseline-updates.md`.
