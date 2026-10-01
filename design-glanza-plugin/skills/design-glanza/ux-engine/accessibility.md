# Accessibility (UX)

## Responsibility
Structural and behavioral accessibility: how the interface is navigable and
operable without relying on sight or a mouse. Perceptual accessibility (color
contrast, color-blind-safe palettes) is owned by `ui-engine/color-system.md`;
this file owns structure and interaction, applied concretely to every other
`ux-engine/*` output.

## Focus order rule
Focus order follows the **visual-hierarchy reading order**
(`ui-engine/visual-hierarchy.md`), not raw DOM/insertion order — a screen-reader
or keyboard user should encounter content in the same priority order a sighted
user visually scans it in, even if the underlying markup was authored in a
different order for layout convenience. Worked check: if the primary action is
visually first/most prominent, it must also be focus-reachable early, not
buried after secondary content in tab order.

## Keyboard-operability rule
Every interaction defined in `interaction-design.md` and `form-design.md` has a
keyboard equivalent — this file states the equivalence table those files
implement (see `interaction-design.md`'s gesture/input-modality table for the
concrete mapping). No interaction may ship with a mouse/touch path and no
keyboard path, full stop; this is checked at the same point
`methodology/ideate.md` checks accessibility-by-construction, and again here at
structural design time.

**No keyboard traps.** Keyboard focus must always be able to move away from
any component using only the keyboard — Tab/Shift+Tab at minimum, Escape
where the component is an overlay (Modal/Drawer/Dropdown/Tooltip, below).
A custom widget that captures focus and never releases it (an unclosable
overlay, a custom control that swallows Tab) is a Blocker-severity defect,
not a minor polish gap — it doesn't just degrade the experience, it makes
the rest of the product completely unreachable for a keyboard-only user
from that point on.

## Skip navigation
Every screen with a persistent navigation region (primary nav, sidebar,
header) that precedes the main content in reading/DOM order provides a
skip link — the first focusable element on the page, visually hidden until
focused, jumping focus directly to the main content landmark (below). This
is not optional polish: without it, a keyboard/screen-reader user re-tabs
through the entire navigation on every single page load before ever
reaching the content, which `user-flow-engine.md` criterion 4 (minimal
user effort) already prohibits for a sighted user's clicks — the same
principle applies to a keyboard user's tab stops, at a much higher cost
per page.

## Focus management and restoration
General rule, of which Modal/Drawer's own entries (below) are the most
common specific case: **any interaction that moves focus programmatically
(opens an overlay, replaces a region's content, completes a multi-step
action) states where focus goes, and — when the triggering context still
exists afterward — restores it there on close/completion.** Focus is never
silently left on a now-removed/hidden element (which strands a screen-
reader user with no announced context) and never silently reset to the
document body (which loses the user's place entirely). This is the general
form; Modal, Drawer, and Dropdown each state their own specific trigger-
and-return points because an overlay is the case where getting this wrong
is most disruptive.

## Semantic / ARIA-role mapping
Map each structural concept to its semantic role so assistive technology
announces it correctly:

| Concept | Semantic mapping |
|---|---|
| Page structure | Exactly one `main` landmark per screen (the skip link's target, above), one `banner` (Header), one `contentinfo` if a footer carries real content — landmark roles are a small, fixed set; inventing a new one for a region that fits an existing landmark is drift, the same category `agents/design-system-expert.md` already catches for tokens/components. |
| Heading hierarchy | One `h1` per screen (the page/record's own name); every subsequent heading level follows the previous without skipping (an `h2` is never followed directly by an `h4`) — levels encode document structure for screen-reader navigation, not visual size (visual size/weight is `typography.md`'s scale, applied independently of the semantic level). |
| Primary/secondary navigation (`navigation-system.md` items 3–4) | `nav` landmark, labeled distinctly if more than one exists on a screen |
| Modal (`navigation-system.md` item 8) | `dialog` role, with a focus trap and a return-focus target on close |
| Drawer (`navigation-system.md` item 9) | `dialog` or `complementary` role depending on whether it interrupts (dialog) or supplements (complementary) — an interrupting drawer (including an off-canvas mobile navigation panel) gets the same focus trap, Escape-to-close, and return-focus-to-trigger treatment as Modal above; a supplementary drawer the user can still interact past does not |
| Breadcrumbs (`navigation-system.md` item 7, when used) | `nav` with an explicit accessible label (e.g. "breadcrumb"), not a generic list |
| Tabs (`navigation-system.md` item 4) | `tablist` / `tab` / `tabpanel` triad, not a set of unrelated buttons |
| Multi-step workflow (`navigation-system.md` item 11) | progress/step indicator exposed as a status, not decorative-only text |
| Button vs. link (`component-system.md` point 1) | `button` triggers an action on the current page; a link (real `a`/navigation semantics) goes somewhere — never a `div` with a click handler standing in for either. |
| Table (`component-registry`'s Table entry) | `table`/`row`/`columnheader` semantics — never a grid of styled `div`s with no table structure underneath. |
| List/Timeline (`component-registry`'s List, Timeline/Activity Feed entries) | `list`/`listitem` semantics for any genuinely list-shaped collection. |

## ARIA — used only when necessary
Native HTML semantics (a real `button`, `nav`, `table`, `input` with a
programmatically-associated label) satisfy assistive technology with no
ARIA at all, and are preferred over an ARIA-patched generic element in
every case where the native element actually fits — ARIA is a repair
mechanism for a genuinely custom widget, not a default layer applied
everywhere out of habit. Where a custom widget's state has no native HTML
equivalent, these five attributes are the ones this engine's own
components actually need, cited from wherever their owning component
already specifies them rather than restated per-component here:
- **`aria-expanded`** — a disclosure control's (Dropdown, an expandable
  Table row, a collapsible Sidebar section) open/closed state.
- **`aria-selected`** — Tabs' and a selectable List/Table row's `selected`
  state (`component-system.md` point 4), so the persistent choice is
  announced, not just visually indicated.
- **`aria-current`** — the active item in a navigation sequence
  (Navigation's active-section indication, Pagination's current page,
  breadcrumbs' current location) — distinct from `aria-selected`, which is
  for a picked item in a set of options, not a location in a sequence.
- **`aria-describedby`** — associates supplementary text with its control:
  a form field's helper text and/or validation error (`form-design.md`),
  a Tooltip's content, a Progress Indicator's unit/context text.
- **`aria-live`** — announces a dynamic content change with no page
  reload: a Toast's appearance, a Table's row-count after a filter
  change (`search-ux.md`'s own "result count announced... not just
  visually" requirement), an Alert/Banner's appearance, a form's
  submission result.

A component reaching for a sixth attribute or a role outside its own
registry entry's stated semantic mapping is the ARIA-level instance of
drift `agents/design-system-expert.md` already reviews for tokens and
components.

## Screen-reader flow
Reading order for a screen is derived from `ui-engine/visual-hierarchy.md`'s
emphasis structure without assuming the user can visually scan — every
non-text state indicator (a color-only badge, an icon-only action) must have an
accompanying text/label announced alongside it, mirroring the color-only-
encoding prohibition in `ui-engine/color-system.md` at the structural level.

## Recovery-path accessibility
Every recovery path (`user-flow-engine.md`) must be reachable and announced
non-visually — a `system error` state's retry action
(`state-design.md`) must be keyboard-focusable and identified by an accessible
name, not conveyed only through a visual icon or color change.

## Permission-denied accessibility
A `permission denied` state (`state-design.md`) is communicated with an
explicit accessible reason (e.g. `aria-disabled` plus a descriptive label),
never merely grayed out with no announced explanation — a sighted user infers
meaning from visual disabling; a screen-reader user needs the same meaning
stated directly.

## Zoom and text scaling
Pinch-zoom and browser/OS-level text-resize are never disabled to preserve a
fixed layout — a layout that only holds together at one fixed scale has
pushed a visual-polish preference ahead of a user's actual ability to read
the content, which this file's responsibility explicitly ranks above. Where
reflow at a larger text size would break a layout, that is a
`ui-engine/responsive-system.md` gap to fix, not grounds for locking the
zoom/text-scale level itself.

## Conformance target
The baseline standard (stated once here, at the level the product commits to —
e.g. WCAG AA) applies to every product unless a domain
(`product-types/*.md`) requires a stricter bar, in which case that overlay's
stricter target supersedes this default for that product only.

## Accessibility verification pipeline
Gate **B8**'s mandatory, explicitly ordered pass — the same rules above and
in the files they cite, sequenced, not a second accessibility framework:

```
Keyboard → Focus → Contrast → Semantics → ARIA → Forms → Status
Communication → Modal/Drawer → Charts → Responsive/Touch
```

| Step | What it verifies |
|---|---|
| **Keyboard** | Every interaction has a keyboard equivalent (Keyboard-operability rule); no keyboard trap; a skip link is present and functional where persistent navigation precedes content. |
| **Focus** | Focus order matches visual-hierarchy reading order; a visible focus indicator meets the WCAG 2.2 Focus appearance minimum (2px-equivalent, 3:1 contrast); focus is never obscured by a sticky element; focus management/restoration is stated for every interaction that moves it programmatically. |
| **Contrast** | Calculated, not eyeballed — `scripts/validate-tokens.py`'s `_check_contrast` computes real WCAG relative-luminance ratios for every declared semantic triplet and `text.primary`/`text.muted` pairing, in both theme modes, against `color-system.md`'s 4.5:1/3:1 thresholds; a control's own outer size additionally clears the 24px WCAG 2.2 Target Size minimum, calculated by the same script's `_check_target_size`. Disabled-state text/controls are the one stated exemption — WCAG explicitly excludes inactive components from the contrast minimum, so a legitimately dimmed `disabled` treatment is not a Contrast-step finding. |
| **Semantics** | Landmarks (one `main`, one `banner`, labeled `nav`s), heading hierarchy with no skipped levels, button-vs-link correctness, table/list semantics — the Semantic/ARIA-role mapping table above. |
| **ARIA** | Only the five attributes named above, only where no native element already covers the need; a role/attribute outside a component's own registry-stated mapping is flagged as drift. |
| **Forms** | Every field has a programmatically-associated label (`form-design.md`, the Input registry entry); helper text and validation errors are associated via `aria-describedby`, not adjacency alone; required/optional status is programmatically exposed, not conveyed by an asterisk with no accessible text equivalent; every validation-timing and error-messaging rule in `form-design.md` has a stated non-visual announcement path. |
| **Status Communication** | Never color alone (Screen-reader flow, above) — every status (a Badge, an Alert/Banner, a Toast, a chart series) carries a second channel: text, icon, shape, pattern, or an accessible label, per `color-system.md`'s color-blind safety rule and the Badge/Alert registry entries' own stated requirements. |
| **Modal/Drawer** | Focus trap, Escape-to-close, focus restoration to the trigger, background-interaction prevention (the scrim, `design-system.md`'s elevation-4 requirement), and correct `dialog`/`complementary` role — the Modal and Drawer registry entries' own fields, checked as a set here rather than assumed from the role alone. |
| **Charts** | A text-equivalent summary or data-table alternative exists; every data-bearing color carries a non-color channel; tooltip content is keyboard-reachable (hover-and-focus, never hover-only) — `visual-benchmark.md`'s own Chart verification pipeline's Accessibility step, cited not restated. |
| **Responsive/Touch** | Interactive targets meet the 24px general minimum (calculated, above) and the stricter 44×44px touch minimum at touch-relevant breakpoints (`responsive-system.md`); adequate spacing between adjacent targets so a mis-tap on a neighbor is structurally unlikely, not just technically avoidable. |

**A UI does not receive a passing accessibility score from visual
inspection alone.** Every step above that has a deterministic, calculable
form (Contrast, Target Size within Responsive/Touch) is checked by running
`scripts/validate-tokens.py`, not by an agent's visual read of whether text
"looks readable enough" — a step that *can* be calculated and instead was
only eyeballed has not actually cleared this pipeline, per the same
"considered vs. verified" discipline this engine already applies to
rendered UI states (`visual-benchmark.md`'s step 3a).

## Audit-time conformance checklist
`agents/accessibility-expert.md`'s Audit-phase pass checks the rules above
against each of these modalities explicitly, not just "keyboard operable in
principle" — a rule can hold in the abstract and still fail under one
specific modality:
- **Keyboard-only** — every interaction reachable and operable with no
  mouse/touch at all, in the focus order this file already specifies.
- **Screen reader** — content and state changes actually announced, not
  just structurally present (spot-check against a screen reader's actual
  output, not just the markup's semantic correctness on paper).
- **200%–400% text zoom / browser text-resize** — content reflows per
  this file's Zoom and text scaling section, not just "doesn't crash."
- **Forced-colors / high-contrast mode** — per this file's High-contrast
  section, every non-color-only distinction still holds.
- **Reduced-motion preference** — per `ux-engine/interaction-design.md`'s
  Motion section, decorative motion degrades, state-indicating motion
  shortens rather than vanishing.

A conformance pass that only checked one modality (commonly: keyboard-only,
skipping the rest) is not a complete B8 pass, per this checklist.

## WCAG 2.2-specific rules
Concrete, frequently-missed criteria worth stating explicitly rather than
leaving to a generic "meets WCAG AA" target:
- **Focus not obscured.** A focused element must not be hidden behind a
  sticky header, a cookie banner, or another overlay — at minimum partially
  visible (the AA form of this criterion); fully visible is the stricter AAA
  form. Do not treat the AAA wording as the baseline requirement by mistake.
- **Focus appearance.** A visible-focus indicator needs a minimum 2px-
  equivalent perimeter around the focused element with at least 3:1 contrast
  against the adjacent colors — a 1px outline in a similar hue to the
  background does not satisfy this even if "something" is technically
  focused.
- **Dragging movements.** Any drag-based interaction (already required to
  have a non-drag alternative per `interaction-design.md`'s direct-
  manipulation rule) must specifically offer a **single-pointer** alternative
  (e.g. tap-to-select-then-tap-target, not just "use the keyboard") — drag
  can require fine motor control a single-pointer path doesn't.
- **Target size minimum.** 24×24 CSS px minimum for any interactive target,
  with exceptions for inline text links and targets already spaced far enough
  apart that mis-tapping a neighbor is impossible — this is the general web
  minimum; it does not replace platform-specific touch-target minimums
  (iOS ~44pt, Android ~48dp) where a product targets those platforms
  specifically, which are stricter and take precedence there.
- **Consistent help.** Where a help mechanism (chat, contact link, FAQ) is
  available across multiple screens, it appears in the same relative
  navigation position on each rather than moving — inconsistent placement
  itself becomes a discoverability defect.
- **Redundant entry.** Never require a user to re-enter information already
  supplied earlier in the same flow, unless it's a genuine security
  re-verification (e.g. re-entering a password to confirm a destructive
  action) — this sharpens `user-flow-engine.md` criterion 4's existing
  no-re-entry rule with its specific accessibility framing.
- **Accessible authentication.** No step in an authentication or
  re-verification flow may rely on a cognitive-function test alone (solving a
  puzzle, transcribing a distorted image) with no alternative — allow
  password-manager autofill and paste into credential fields rather than
  blocking them.

## High-contrast / forced-colors mode
Distinct from the light/dark theming `color-system.md` already covers: an
OS-level forced-colors or high-contrast mode overrides a product's own color
values with a small, user-chosen palette. Any visual distinction that relies
purely on a background-color or shadow difference (a card's subtle elevation,
a hover-state tint) disappears under forced-colors — verify that meaning
conveyed this way still has a non-color fallback (a visible border, an icon,
text) so the interface stays usable rather than just re-themed.

## Loop position
Applied continuously across the feature-level loop, not as a single pass —
re-checked by `agents/accessibility-expert.md` at every Prototype cycle and
again at Audit. A Test accessibility finding (dimension 6) traces here for
structural causes, or to `ui-engine/color-system.md` for perceptual causes, per
`methodology/design-thinking.md`'s routing table.

## Explicitly not here
- Color contrast ratios and color-blind-safe palette construction →
  `ui-engine/color-system.md`.
- The persona/role that enforces both halves of accessibility during review →
  `agents/accessibility-expert.md`.
- Domain-specific compliance mandates (e.g. healthcare) → the relevant
  `product-types/*.md`.
- The interactions being made accessible → `interaction-design.md`, `form-design.md`.
