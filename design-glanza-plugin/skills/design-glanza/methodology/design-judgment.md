# Design Judgment Engine

## Responsibility
The applied reasoning procedure for **important UX/UI pattern decisions** —
distinct from `design-thinking.md`'s decision framework, which is a general,
cross-phase *index* ("here's where each step of a decision already gets
made"). This file is the other direction: a concrete procedure an agent
runs *when facing a specific pattern choice* (sort control vs. filter chip,
inline edit vs. a separate screen, tabs vs. accordion) that isn't already
fully resolved by a more specific technique file. It exists so that judgment
calls get reasoned through the same way every time, not improvised fresh —
and so the reasoning is checkable, not just plausible-sounding.

## When this engine applies — and when it doesn't
Run this procedure when a decision is **important**: it affects a primary
or frequently-used flow, has no existing precedent in this product's own
design system, has real trade-offs across **3 or more** of the 12 factors
below (i.e. it's not a clear-cut case), or was flagged by a Test/Audit
finding. Otherwise, skip it — this engine is not a ritual to perform on
every minor choice; that would itself be a failure of judgment.

**Do not use this engine when a more specific technique file already
resolves the decision** — cite that file directly instead of re-deriving
its reasoning here:
- Navigation pattern choice → `ux-engine/navigation-system.md`'s selection
  framework.
- Visual register/trend choice → `ui-engine/visual-trends.md`'s 3-point
  trend-adoption gate.
- Solution-approach selection at Ideate → `methodology/ideate.md`'s 8-point
  framework.
- Reversibility/confirmation choice → `ux-engine/interaction-design.md`'s
  risk matrix.

This engine is for everything *else* that's important enough to reason
through deliberately.

## The chain, applied to a pattern decision
Same 9 steps as `design-thinking.md`'s framework, defined here specifically
for a UX/UI pattern choice rather than a whole-product decision:

| Step | What it means for *this* decision |
|---|---|
| **Problem** | The actual interaction/information need at this exact screen/moment — not "what pattern is trendy," the real friction or ambiguity a user hits here. |
| **Context** | Which screen, which flow step, what surrounds it; the specific actor's environment/device (`methodology/empathize.md` dimensions 6–8) for *this* moment, not the product in general. |
| **User Need** | What the actor is trying to accomplish right here (ties to their JTBD, `empathize.md` dimension 4) — one sentence, specific to this moment. |
| **Constraints** | What's actually feasible: existing design-system components/tokens (`ui-engine/component-system.md`'s inventory), technical limits, remaining scope/timeline — real constraints, not hypothetical ones invented to justify a preference. |
| **Alternatives** | At least 2–3 *structurally different* patterns, not visual variations of one idea (the same divergence discipline as `ideate.md` item 1). |
| **Trade-offs** | Score every alternative against the 12 factors below, concretely — not "option A feels nicer." |
| **Selected Approach** | The pattern chosen, plus every rejected alternative and the *specific factor* that broke the tie against each. Label the deciding factor itself as **evidence-backed** (traceable to a stated fact — a frequency number, a requirement, a Test finding) or **craft judgment** (a defensible call with no single fact behind it, e.g. a spacing preference) — both are legitimate, but conflating them lets a taste call quietly borrow the authority of an evidence-backed one. |
| **Expected Outcome** | A falsifiable prediction: what should measurably hold if this was the right call (not "better UX"). |
| **Validation Method** | How you'd actually check the expected outcome — name the specific `methodology/test.md` dimension(s) or usability check, not just "test it." If the Trade-offs step drew on conflicting evidence (a stated requirement and an observed usage pattern point different ways, say), name what specifically conflicts and what a genuine resolution would look like — a validation method that can't be described because "we went with the stronger source" without saying what would have to be true for the other source to be right instead is building a case, not resolving one. |

## The 12 factors — each with a question and a stated effect
Vague "considerations" produce senior-*sounding* language. A real weighing
factor answers a specific question and changes the decision in a stated
direction:

| Factor | Question to ask | How the answer moves the decision |
|---|---|---|
| **User expertise** | Is this actor a novice or an expert with this kind of tool? | Novice → favor recognition over recall (labeled, visible options, guided). Expert → favor recall-based efficiency (shortcuts, denser UI, fewer confirmations). |
| **Task frequency** | Daily/hourly, or rare/occasional? (`empathize.md` dimension 7) | High frequency → optimize for speed even at some learnability cost. Low frequency → optimize for guidance even at some speed cost. |
| **Task complexity** | Single decision, or several interdependent sub-decisions? | Simple → flat, single-step pattern. Complex → progressive disclosure or multi-step (`ux-engine/form-design.md`'s single-page-vs-multi-step rule). |
| **Information density** | How much must be visible at once for the task to make sense? | Low → comfortable/spacious layout. High → compact/tabular layout (`ui-engine/visual-trends.md` register, `layout-system.md`). |
| **Decision speed** | Must the user act immediately, or can they compare at leisure? | Time-pressured → minimal options, one unmistakable primary action. Unhurried → richer comparison UI is affordable. |
| **Error risk** | What does it cost if the user picks wrong here? | Higher cost → add confirmation/undo per `interaction-design.md`'s reversibility×risk matrix (cited, not re-derived). |
| **Accessibility** | Does this pattern have a keyboard/non-visual equivalent *by construction*? | If not achievable — per `ideate.md`'s accessibility-by-construction check — the alternative is disqualified before scoring, not scored down. |
| **Responsiveness** | Does the pattern degrade sensibly at the smallest breakpoint? | If it requires real estate that doesn't exist on mobile with no fallback, it's disqualified or needs a stated breakpoint-specific alternative (`ui-engine/responsive-system.md`). |
| **Scalability** | Does it still work at 10× the data/user volume shown in the example? | If it visibly breaks at scale (e.g. an unpaginated list), that's disqualifying, not a later fix. |
| **Maintainability** | Does this reuse an existing component/pattern, or introduce a new one? | Reuse is preferred by default (`agents/design-system-expert.md`'s reuse-vs-new-variant rule); a new pattern needs a stated reason it can't reuse what exists. |
| **Business impact** | Does this choice materially affect a stated business/success metric (`product-definition.md`)? | Higher impact → warrants a stronger Validation Method before shipping, not just a plausibility check. |
| **Convention/familiarity** | Does an established convention already exist for this exact pattern — in this product's own design system, or broadly across the category the product competes in? | An established convention → favor it by default; departing from it is justified only by a stated failure or a tested finding the convention doesn't fit here, never by taste alone. No established convention, or the pattern is genuinely novel to this product's problem → this factor doesn't constrain the choice, defer to the others. |

Every alternative is checked once against real-world evidence before scoring:
never present an unverified or no-match result as if it were a confirmed
fact, and never let a plausible-sounding alternative stand in for one that
was actually checked. If a factor's supporting evidence is itself uncertain
(a frequency estimate, an assumption-tagged fact per Rule 10), say so in the
Trade-offs step rather than scoring it with unstated confidence. Where two
independently-sourced inputs to this decision could conflict without either
side noticing (e.g. a pattern chosen by `visual-trends.md`'s register and a
color chosen by `color-system.md` chosen without reference to each other),
resolve the conflict explicitly as part of Trade-offs before scoring —
don't let two correct-in-isolation decisions combine into a broken one.

Not every factor is decisive for every decision — but every factor gets
*considered*, and the ones that actually drove the choice are named
explicitly in Selected Approach. A factor that wasn't decisive doesn't need
a paragraph; it needs an honest "not decisive here, because X."

## The anti-fashion gate
A pattern is never selected because it is currently popular or visually
attractive on its own. Before finalizing Selected Approach, run this check
(the same discipline as `visual-trends.md`'s trend-adoption gate, applied
here to any pattern, not just visual style):

1. Did the Trade-offs step actually favor this alternative against the 11
   factors — or only against taste?
2. **The strip-away test**: if this pattern weren't currently fashionable,
   would the same Trade-offs scoring still select it? If the honest answer
   is "no, we'd have picked something else without the trend," the
   selection is disqualified — go back to Alternatives.

## Senior-level reasoning vs. senior-*sounding* language
This is the difference this whole engine exists to enforce, made concrete
with one worked contrast:

> **Sounds senior, isn't reasoning:** "Considering the user's needs and the
> various constraints, we selected a modal for this interaction because it
> provides a focused, clean experience for the user."
>
> **Is actually reasoning:** "Rejected a full-page redirect: this action
> happens ~20 times/day per Project Manager (task frequency — high), and a
> page redirect's load/return cost compounds at that frequency. Rejected an
> inline-expand-in-place: the form has 6 interdependent fields (task
> complexity), too dense to expand inline without shrinking the surrounding
> list below usable density (information density). Selected a modal: it
> interrupts fully (appropriate — error risk is real here, a partial
> half-visible form invites mistakes), and reuses the existing Modal
> component (maintainability) rather than introducing a new drawer variant
> for one screen."

If a written Selected Approach doesn't name which *specific* factor(s) from
the 11 broke each tie, it has been described, not reasoned — send it back
through Trade-offs before accepting it.

## Loop position
Invoked within Prototype (`ux-architect.md`, `ui-designer.md`,
`interaction-designer.md`) whenever an important pattern decision has no
more specific owning file. A Test finding that traces to a specific pattern
choice (`methodology/design-thinking.md`'s routing table) is exactly the
kind of signal that makes a *future* instance of that decision "important"
under the threshold above, even if it wasn't obviously so the first time.

## Explicitly not here
- The general, cross-phase decision index → `methodology/design-thinking.md`.
- Any already-owned specific pattern decision → the file named in "When
  this engine applies," above.
- The accessibility/responsive/scalability techniques themselves (cited,
  not redefined) → `ux-engine/accessibility.md`, `ui-engine/
  responsive-system.md`, `methodology/ideate.md`.
