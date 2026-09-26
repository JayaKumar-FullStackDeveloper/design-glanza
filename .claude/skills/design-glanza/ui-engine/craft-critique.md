# Craft Critique

## Responsibility
A concrete, checkable self-critique pass for "does this actually look
professionally designed, or just competently assembled" — sharper and more
numeric than `visual-hierarchy.md`'s qualitative rules, and narrower in scope
than `methodology/design-judgment.md`'s general pattern-decision engine. This
file operationalizes Rule 11 and `visual-trends.md`'s trend-adoption gate at
the finished-composition level: it's run *after* a screen/page's visual
design exists, as part of Rule 12 (Self-Critique) and Audit, not during
initial composition.

**Provenance note:** checks 1–8 converged independently across three
unrelated external design-engineering sources reviewed in an earlier
integration pass — treated as a stable, real pattern rather than one
project's house taste, which is why they were adopted as a citable checklist
rather than left as prose advice. Check 9 and the anti-cliché catalog's
gradient entry were corroborated by additional, separately-authored sources
in a later pass — noted at each addition rather than folded silently into
the "three sources" count above.

## When to run this
At Prototype's UI pass (`agents/ui-designer.md`) once a screen's visual
composition is done, and again at Audit (`agents/qa-expert.md`) across the
finished set — the same two checkpoints `design-system-expert.md` already
uses for drift review. Not a blocking quality gate in its own right (it does
not add a new `config/quality-gates.md` B-dimension); a failure here is
routed the same way any Rule 12 self-critique finding is, through the normal
Iterate loop.

## The checks

### 1. Hierarchy squint test (numeric)
The primary heading should read at roughly **2.5× or more** the body text's
visual size/weight combined. Below that ratio, a viewer blurring/squinting at
the screen can no longer reliably name what's primary vs. secondary — this is
the numeric, testable version of `visual-hierarchy.md`'s existing primary-
action and information-priority rules, not a new rule alongside them.

### 2. Hero subtraction test
List every element in a screen's hero/opening region. Keep only what answers
one of: what is this, why should I care, what do I do next, what does "good"
look like here. Move everything else below the fold or cut it. Applies most
directly to `product-types/landing-page.md` heroes, but the same test is
valid for any screen with a dominant above-the-fold region (a dashboard's top
summary band, an empty state's call-to-action area).

### 3. Section headline scale ceiling
A non-hero section heading renders at roughly **50–65%** of the hero's own
display size — never competing with it. This is `visual-hierarchy.md`'s
emphasis-level cap (3–4 levels) made concrete for the specific, common
failure of a secondary heading sized to match the hero.

### 4. Internal padding ≤ external gap
Within a grouped element (a card, a form section), the padding inside it
should be less than or equal to the gap separating it from its neighbors —
the direct, numeric form of Gestalt proximity that `visual-hierarchy.md`'s
Grouping rule already states qualitatively ("visual proximity mirrors IA
grouping"). A card with more internal padding than external gap visually
merges with its neighbor regardless of a dividing line between them.

### 5. Deletion test (restraint)
For each decorative or borderline element: if it were deleted, does the
design get *worse*? If the honest answer is no, delete it. This is the
concrete operational form of `methodology/design-judgment.md`'s anti-fashion
strip-away test, applied to finished visual elements rather than pattern
selections.

### 6. Specificity test
Could this screen/page be handed to a direct competitor with only the name
and colors swapped, and still make sense? If yes, the design has not
actually responded to this product's own content, audience, or constraints —
it has produced a generic template. This is the visual-composition sibling of
`product-types/landing-page.md`'s content-realism check ("could this copy
belong to any competitor") and of `design-judgment.md`'s senior-reasoning-vs-
sounding contrast.

### 7. Structural variety (across a set, not one screen)
When producing more than one screen/page of the same type in sequence
(several landing pages, several empty-state designs), avoid defaulting to the
exact same section order/component choice every time out of habit rather than
fit — a deliberate repeat because it's the right structure for both cases is
fine; an unexamined repeat because it's the last thing produced is drift, the
same category of problem `agents/design-system-expert.md` already watches
for at the token/component level, applied here to whole-composition shape.

Two color-swapped instances of the same page shape still read as
templated even with a perfect color story — this check needs a concrete
point of comparison to be checkable rather than a vague reminder to "vary
more": before finalizing, name the current build's whole-page shape and its
key section choices (hero treatment, nav pattern, footer shape) in one line,
and compare that line against the immediately preceding build of the same
screen type. A match on every named choice is the drift this check exists to
catch; a match on one or two with a stated reason is not.

### 8. Anti-cliché catalog
Concrete, checkable "have I defaulted to a generic AI-tool-ism" tells,
independently confirmed across multiple, unrelated source materials this
file draws from — treat any of these as a flag to justify or remove, not an
automatic rejection (a pattern here can be the *right, register-justified*
choice per `visual-trends.md`'s gate; the point is that it must be a stated
choice, not a reflex):
- A decorative purple-to-pink or blue-to-purple "AI gradient" with no
  semantic reason for that specific color pairing — named as a recurring,
  specifically-flagged anti-pattern independently across every source
  reviewed for craft/genericness, including one source's own dataset of
  professional-domain design rules (trust-sensitive categories like
  government/public-service explicitly list it as a disqualifying tell) —
  treat repeated independent convergence like this as stronger evidence than
  a single source's taste.
- A card with a colored left border used purely as decoration rather than to
  encode a real status/category (compare `ui-engine/color-system.md`'s
  color-only-meaning prohibition — the same failure at the container level).
- An emoji standing in for a real icon in a production UI.
- A fabricated metric, testimonial, logo, or "X users" style claim with no
  real source (direct instance of point 6's content-realism concern).
- The identical single entrance animation (fade/slide) reused for every
  section regardless of what that section actually is — the animation
  equivalent of point 7's structural-variety drift, and a direct case of
  `ux-engine/interaction-design.md`'s purpose-must-be-stated rule failing:
  "it's the default" is not a stated purpose.
- Constant ambient decorative motion (a permanently pulsing glow, a
  perpetual slow pan) on a screen with no actual state change to justify
  it — this is exactly what the frequency-based animate/don't-animate gate
  in `ux-engine/interaction-design.md` exists to catch.

### 9. Cognitive load and scanning fit
Distinct from check 1's hierarchy ratio: count how many independent
decisions or information sources the screen asks the viewer to hold at once
(the same estimate `methodology/ideate.md` and `design-judgment.md`'s
information-density factor use, applied here to a finished composition
rather than a pattern choice), and confirm the composition's visual density
actually matches the scan pattern `visual-hierarchy.md` selected for it (an
F-pattern screen crowding unrelated information into the left column defeats
its own scan path; a Z-pattern screen with too many competing elements never
resolves to the one intended end point). A screen that passes every other
check here can still fail this one by simply presenting too much
undifferentiated information density for the scan pattern it committed to.

## Reporting format
Route every finding from checks 1–9 through the same triad:
**Observation** (what's actually on screen, stated neutrally) →
**Problem** (which check it fails and why that matters) → **Fix** (the
specific, actionable change) — plus a `pass` / `minor issue` / `major issue`
rating per check. This is `agents/qa-expert.md`'s literal reporting shape for
a craft-critique pass, distinct from — and mapped onto —
`config/output-contract.md`'s Blocker/Major/Minor/Note severity vocabulary
used everywhere else (a `major issue` here is reported as `Major`, never as
a second, competing severity scale).

## Worked example (what "passing" looks like)
> **Fails silently:** a landing page hero with a 1.3× heading-to-body ratio,
> a purple-pink gradient background because "that's what looks modern," and
> a headline that reads "The smarter way to manage your workflow" — could be
> any product in the category.
>
> **Passes:** heading-to-body ratio checked and adjusted to ~2.8× (check 1);
> gradient either removed or kept with a stated reason tied to the product's
> actual register (e.g. "kept — matches the Consumer Playful register
> selected for this onboarding flow per `visual-trends.md`," check 8);
> headline rewritten to name a specific, falsifiable claim about this
> product rather than a swappable generic sentence (check 6).

## Explicitly not here
- The systematic hierarchy/spacing/color rules this file makes numeric →
  `visual-hierarchy.md`, `layout-system.md`, `color-system.md` (this file
  cites and sharpens them, it doesn't redefine them).
- General pattern-decision reasoning (which control, which nav pattern) →
  `methodology/design-judgment.md`, `navigation-system.md`,
  `visual-trends.md`.
- Motion-specific behavior rules → `ux-engine/interaction-design.md`'s
  Motion and animation section (cited above, not restated).
- Adding a new blocking quality gate → deliberately not done; see "When to
  run this," above.
