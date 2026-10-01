# Token Audit

## Responsibility
What counts as a token violation, the justified-exception mechanism (reuse
of `design-system.md`'s existing "logged system gap" rule — not a second,
competing mechanism), and the exact split between what
`scripts/validate-tokens.py` checks deterministically and what still needs
`agents/design-system-expert.md`'s judgment. This is gate **B6**'s
sharpened pass criterion and gate **B18**'s own subject.

## A violation, precisely
Any value in a component spec, screen specification, or generated
`output/*` code that does **not** resolve to a path in the product's
`design-tokens.json` (or its master defaults) — a raw hex color, an
arbitrary pixel value, an ad hoc shadow, a bespoke motion duration — where
`design-system.md`'s Consistency rule already calls this "a one-off value
introduced outside this set." This file gives that existing rule a
checkable shape rather than leaving it to be noticed on review.

## The justified-exception mechanism — reused, not reinvented
`design-system.md`'s Consistency rule already states the resolution path:
*"logged as a system gap and either absorbed into the token set... or
rejected."* A token deviation is recorded exactly that way, in the
product's `product-builder/ui/design-system.md` Usage guidelines section
(or a dedicated Token gap log where the deviation count warrants one):

```
Token gap: <the raw value used>
Location: SCREEN-NNN / COMPONENT-NNN
Reason no existing token fits: <why>
Resolution: absorbed (new token proposed: <name/value>, pending
  agents/design-system-expert.md sign-off) | rejected (reverted to
  <token path> instead)
```

**Never** a value left as a silent one-off with no log entry — that is
the violation `config/quality-gates.md`'s **B6** fails on. A logged,
`absorbed`-resolution deviation is not a failure while pending sign-off;
an unlogged deviation always is.

## What `scripts/validate-tokens.py` checks deterministically
1. `product-builder/ui/design-tokens.json` exists and is valid JSON
   against `design-tokens.schema.json`.
2. Every required semantic token (`semantic-tokens.md`'s 10 names) is
   present.
3. Where a `dark` mode is declared, every `themeable: true` token has both
   `light` and `dark` values — zero partial theme coverage.
4. Scans `product-builder/ui/*.md` and `output/*` source files for
   pattern-detectable raw values — hex colors (`#[0-9a-f]{3,8}`), inline
   `rgb()`/`rgba()`, and numeric pixel values in style-bearing contexts —
   and flags each one not immediately adjacent to a Token gap log entry
   (per the shape above) or a recognized token reference.
5. Cross-checks `token-inheritance.md`'s rule: every path present is
   either a master category with a product-specific value, a `product.*`
   addition, or absent — an unrecognized top-level or scale-extending key
   is flagged.
6. Scans for redundant tokens: two different paths resolving to the exact
   same value, flagged for the reuse-vs-alias review above — never
   auto-merged.
7. Computes a real WCAG contrast ratio (relative luminance, not an
   eyeballed estimate) for every declared `{foreground, background}`
   semantic triplet pair and for `text.primary`/`text.muted` against
   `background`/`surface`, in both light and dark mode, against
   `ui-engine/color-system.md`'s 4.5:1/3:1 thresholds — see Contrast
   validation, below.
8. Computes every `sizing.control*` token's numeric px value against the
   24px WCAG 2.2 Target Size (Minimum) floor (`ux-engine/accessibility.md`'s
   WCAG 2.2-specific rules) — a real dimensional calculation, not a
   visual "looks tappable" read.

Every check above is genuinely mechanical (regex/JSON-structure matching,
or in checks 7-8's case real luminance/ratio and dimensional arithmetic —
still deterministic, still zero judgment) — per the standing instruction
to prefer deterministic validation in scripts, matching every other
`scripts/validate-*.py` file's own stated boundary.

## Contrast validation
`ui-engine/color-system.md`'s Contrast compliance rule states every
semantic triplet's foreground-on-background pairing is checked against
4.5:1/3:1 in both themes — this is that check made real rather than left
as a claim nothing actually computes. Two passes: every declared
`{foreground, background}` triplet (the rule's own named pairs), and
`text.primary`/`text.muted` against `background`/`surface` (the pairings
almost every screen actually uses). A failure below 3:1 (unreadable even
against the lenient bar) is **Major**; a failure that clears 3:1 but
misses the stricter 4.5:1 normal-text bar is **Minor**. Per
color-system.md's own "pairing contract, not a one-time pass" framing,
this check only certifies the pairings above — a new color combination a
later screen improvises (a semantic color reused as a badge fill under
body text, say) is a fresh check, not an assumed pass by association.

## Redundant tokens
Distinct from a raw-value violation: two *different* token paths whose
resolved values are identical (e.g. two semantic color entries that
happen to share the same hex value, or two spacing aliases both resolving
to `16px`) are not individually wrong, but their coexistence is itself a
violation of `design-system.md`'s Consistency rule once discovered — one
should alias the other (or the duplicate should be removed) rather than
leaving two names for one value, which invites the next screen to pick
either one inconsistently. Flagged for review, not auto-merged — which
name is the canonical one is a judgment call (`agents/design-system-
expert.md`'s), never resolved by the script itself.

## What still needs agent judgment
- Whether a *token used in the wrong semantic role* (a value that
  technically matches `color.semantic.warning` but is applied to a
  primary call-to-action) is a defect — this is a semantic-correctness
  question, not a pattern-match, and stays `agents/design-system-
  expert.md`'s call, exactly as it already owns the reuse-vs-new decision.
- Whether a logged Token gap's proposed resolution is actually the right
  one (absorb as a new token vs. reject) — a judgment call, not a script
  output.
- Whether a raw value inside a *third-party library's own internals*
  (vendored code Design-Glanza didn't generate) counts as a violation —
  out of scope by construction; the script only scans Design-Glanza's own
  generated artifacts.

## Gate mapping
- **B6 (Design System)** — sharpened: "0 undocumented one-off values" now
  resolves concretely to "0 raw values flagged by
  `scripts/validate-tokens.py` with no corresponding Token gap log entry."
- **B18 (Token Inheritance Integrity)** — the master↔product relationship
  itself: every path in `design-tokens.json` is a valid override,
  addition, or absence per `token-inheritance.md` — never an
  unauthorized scale extension, and never a value written back into
  `ui-engine/*` (Rule 15).
- **B8 (Accessibility)** — checks 7-8 (contrast, target size) are the
  deterministic half of B8's Contrast and Responsive/Touch pipeline steps
  (`ux-engine/accessibility.md`'s Accessibility verification pipeline);
  every other step in that pipeline (Keyboard, Focus, Semantics, ARIA,
  Forms, Status Communication, Modal/Drawer, Charts) stays
  `agents/accessibility-expert.md`'s structural/behavioral review — this
  script never claims to cover a step it structurally can't calculate
  from a token file alone.

## Explicitly not here
- The Consistency rule itself → `ui-engine/design-system.md`.
- What is/isn't overridable → `token-inheritance.md`.
- The reuse-vs-new decision process → `agents/design-system-expert.md`.
- The script's own CLI/argument shape → `scripts/validate-tokens.py`.
