# Pattern Analysis

## Responsibility
The technique for recognizing a UI/UX pattern's **purpose**, not just its
name — and the Anti-Generic Design challenge every common pattern must
clear before it's adopted. This is the file `competitor-analysis.md` applies
to one named product; here the technique itself is defined, domain-neutral.

## The shallow-vs-deep test
A shallow pattern observation names the pattern:

> "Competitor uses cards."

A research-grade pattern observation names the pattern, the problem it
solves, and why the mechanism actually solves it:

> "Cards group independent summary metrics where users need rapid
> comparison — each card is a self-contained unit a user can scan in
> isolation without reading the others first, which matters when the
> metrics being compared don't share a common axis a table row would
> otherwise imply."

Every pattern recorded by this file or `competitor-analysis.md` must reach
the second form. A finding that stops at naming the pattern is incomplete —
route it back through the four questions below before recording it.

## Recognizing a pattern, in four parts
1. **What pattern is being used** — name it precisely (a card grid, a
   status badge, a stepper, a command palette — not just "a nice layout").
2. **What user problem it solves** — the specific task/friction this
   pattern addresses, stated as a user need, not a design description.
3. **Why it works** — the actual mechanism connecting the pattern's
   structure to the problem it solves (per the shallow-vs-deep test above).
4. **Whether it's relevant to this product** — does *this* product's user/
   task/domain/density combination share the problem the pattern solves?
   A pattern that solves a real problem *somewhere else* is not evidence it
   solves a problem *here*.

## The Anti-Generic Design challenge
Before accepting any common/default pattern — especially one that's the
first idea that comes to mind, or the one every AI-generated interface
reaches for — ask all five, and record the answers, not just the
conclusion:

1. **Why is this pattern appropriate?** — for this specific product, not
   "because it's common."
2. **What user problem does it solve?** — stated concretely (per part 2
   above), not assumed.
3. **What evidence supports it?** — cite the actual `RF-NNN` evidence,
   never asserted from taste alone.
4. **Is there a better pattern for this domain?** — genuinely consider at
   least one structurally different alternative before defaulting,
   mirroring `methodology/ideate.md`'s divergence requirement (at least 3
   structurally different approaches) applied here at the pattern-selection
   grain.
5. **Is the pattern consistent with the product's information
   architecture?** — a pattern that fits the domain in the abstract but
   fights the IA `agents/ux-architect.md` already built is not a free pass;
   name the conflict rather than forcing the pattern in anyway.

A pattern that clears all five is recorded as **researched-and-adopted**,
with its answers as the finding's Insight/Design Principle
(`research-to-design.md`). A pattern that fails one or more is recorded as
**researched-and-rejected**, with the reason — the same disclosed-rejection
posture `methodology/ideate.md`'s rejected-concepts register already uses,
applied here at the pattern-selection stage specifically.

## Relationship to existing anti-fashion machinery
This challenge does not replace `ui-engine/visual-trends.md`'s
trend-adoption gate or `methodology/design-judgment.md`'s anti-fashion
strip-away test — it runs earlier, at the research stage, before a pattern
is even proposed as a candidate; those two run later, at the point a
specific visual/UX decision is actually being made. A pattern that clears
this challenge still has to clear those gates when it's actually applied.

## Explicitly not here
- Applying this technique to one named competitor/reference product →
  `competitor-analysis.md`.
- The trend-adoption gate and register definitions → `ui-engine/visual-
  trends.md`.
- The anti-fashion strip-away test for an in-flight decision →
  `methodology/design-judgment.md`.
- How an adopted pattern's Design Principle maps to a UX Decision → 
  `research-to-design.md`.
