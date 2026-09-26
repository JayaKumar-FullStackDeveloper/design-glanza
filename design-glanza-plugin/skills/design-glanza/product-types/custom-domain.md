# Product Type: Custom Domain

## Responsibility
Two jobs in one file: (1) define the **Domain Pack Contract** — the schema
every `product-types/*.md` file, including a newly-authored one, must
satisfy — and (2) serve as the fallback procedure for a product
`product-intelligence/domain-classifier.md` cannot confidently match to any
named domain. This file deliberately holds no fixed domain content of its
own — its 12 points below are answered *procedurally*, not with concrete
domain knowledge.

## The Domain Pack Contract
This is what makes the architecture extensible: **adding a new domain means
authoring one new `product-types/<domain>.md` file that answers these same 12
points with real, specific content — nothing else changes.** No core
engine file (`config/`, `methodology/`, `product-intelligence/`, `ux-engine/`,
`ui-engine/`) is ever edited to accommodate a new domain (Rule 14, Domain-
Agnostic Core), and no company-specific product detail belongs in a pack —
that's a generated Product Builder's job under `products/` (Rule 15, Product
Isolation).

Every pack answers, for its domain:
1. Common product characteristics
2. Common users
3. Common workflows
4. Common information structures
5. Common navigation patterns
6. Common UI patterns
7. Common operational concerns
8. Common edge cases
9. Domain-specific terminology
10. Domain-specific UX risks
11. Domain-specific accessibility considerations
12. Domain-specific scalability considerations

Each point *specializes* a core-engine file's general technique — it doesn't
replace it. A pack that tries to redefine, say, how contrast compliance works
instead of citing `ui-engine/color-system.md`'s existing rule has broken the
contract; a pack only ever adds domain-specific *content* on top of the
core's *technique*.

## Applying the 12 points when no domain matches
When `product-intelligence/domain-classifier.md` reports no confident match,
this file's procedure runs instead of a concrete pack — independently of
that, still check `product-intelligence/domain-standards.md`'s separate,
finer-grained registry: a product with no matching `product-types/*.md` pack
frequently still has a specific, complete entry there (e.g. "Telemedicine"
or "Dental PMS" have no pack of their own but may have a loaded standard),
which enriches the procedure below with real domain-specific content rather
than leaving every point to the generic fallback:

1. **Common product characteristics** — do not infer characteristics from a
   guessed domain; work only from what `product-intelligence/brd-analysis.md`
   actually extracted, tagging every inferred characteristic as an assumption.
2. **Common users** — use `product-intelligence/user-roles.md`'s general
   actor-identification technique with no domain-typical role list to check
   against; every role comes from the source material alone.
3. **Common workflows** — use `product-intelligence/business-logic.md` and
   `ux-engine/user-flow-engine.md`'s general technique with no domain-typical
   workflow shape assumed.
4. **Common information structures** — use `ux-engine/information-architecture.md`'s
   general grouping technique; do not borrow a structure from a
   superficially-similar named domain without confirming the fit.
5. **Common navigation patterns** — use `ux-engine/navigation-system.md`'s
   selection framework exactly as written; it already requires deriving the
   pattern from the actual IA shape, not from domain convention, so no
   fallback adjustment is needed here.
6. **Common UI patterns** — use `ui-engine/visual-trends.md`'s register
   selection based on `methodology/empathize.md` audience findings alone.
7. **Common operational concerns** — derive only from
   `product-intelligence/business-logic.md`'s extracted rules; do not assume
   an operational concern (audit trail, approval chains, etc.) common to some
   other domain applies here.
8. **Common edge cases** — rely entirely on
   `product-intelligence/edge-case-engine.md`'s general enumeration
   categories; there is no domain-typical edge-case list to check against.
9. **Domain-specific terminology** — use the source material's own vocabulary
   verbatim (per `ux-engine/information-architecture.md`'s labeling
   convention); do not invent domain jargon.
10. **Domain-specific UX risks** — flag only risks with direct evidence in
    the source or in `methodology/test.md` findings; do not import a risk
    list from an unrelated domain.
11. **Domain-specific accessibility considerations** — apply
    `ux-engine/accessibility.md` and `ui-engine/color-system.md`'s general
    rules at their strictest reasonable reading, since no domain-specific
    relaxation or tightening is known to apply.
12. **Domain-specific scalability considerations** — derive only from
    `product-intelligence/dependency-analysis.md`'s actual findings about
    expected data/user volume; do not assume enterprise- or consumer-scale by
    default.

## Partial-match procedure
When a domain's signals are present but incomplete
(`product-intelligence/domain-classifier.md`'s partial-match case): apply only
the specific numbered points from that domain's pack that clearly match the
extracted facts, mark the rest **not-applicable-here** with a one-line reason,
and fall back to this file's procedure for the remaining points rather than
importing the whole pack uncritically.

## Graduation rule
When the same "custom" domain recurs across multiple products built with this
skill, that recurrence is the signal to author a proper new
`product-types/<domain>.md` file — following the Domain Pack Contract above —
rather than keep routing it through this fallback indefinitely. Extending
Design-Glanza to a new domain always happens by adding a file here, never by
editing the domain-agnostic core.

## Explicitly not here
- Any named domain's actual characteristics → its own `product-types/*.md`
  file, once one exists.
- The classification logic that decides a match failed or is partial →
  `product-intelligence/domain-classifier.md`.
