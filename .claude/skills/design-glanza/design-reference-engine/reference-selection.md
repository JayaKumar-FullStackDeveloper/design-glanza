# Reference Selection

## Responsibility
The decision technique that classifies, once `reference-analysis.md` and
`design-questionnaire.md` have run, which of four design-reference modes
this product is actually in — and, only for one of the four, selects a
default sample. This is a classification with the same rigor
`product-intelligence/domain-classifier.md` already requires for a domain
match: stated explicitly, with the evidence behind it, never asserted
silently.

## The four modes, in priority order

### 1. Reference-Driven
**When:** the user provided real visual references (screenshots, Figma,
website references, existing product/application UI).
**Rule:** use the references as the primary visual direction. Do not
blindly copy individual screens. Extract the underlying design language
(`reference-analysis.md`'s technique) and adapt it to this product's own
requirements — a reference informs the *language*, this product's actual
IA/flows/content still come from `ux-engine/*`, not from the reference's
own structure.

### 2. Guideline-Driven
**When:** the user provided brand/design guidelines (written rules, brand
colors, typography guidelines, existing design tokens) but no visual
references to extract a language from.
**Rule:** build the design system from those guidelines directly — they
already state the rules; this mode is closer to direct application than
extraction.

### 3. Custom Design
**When:** the user provided explicit design expectations through the
questionnaire (Step 2) — stated preferences, not references or formal
guidelines.
**Rule:** create a design direction from those stated requirements,
resolved against `ui-engine/*`'s general technique wherever the
questionnaire didn't specify something.

### 4. Default Design-Glanza
**When:** none of the above apply — no references, no guidelines, no
meaningful questionnaire answers beyond generic ones.
**Rule:** select the best-fitting entry from `design-samples/`, matched by
Product Architect's confirmed domain classification (the same
`product-types/*.md` slug, or its nearest named sample if the domain has no
exact sample of its own). **Never** reach for this mode when any of modes
1–3 already apply — Default is the fallback of last resort, not a
convenience default.

## Classification is not always exclusive
A product can combine modes for different surfaces exactly as
`ui-engine/visual-trends.md` already allows two registers for two surfaces
of one product (e.g. Guideline-Driven for the account-facing app because
brand guidelines exist, Reference-Driven for a marketing site because a
specific competitor reference was supplied for that surface only) — state
the split explicitly rather than forcing one mode over the whole product.

## Selecting a default sample (mode 4 only)
`design-samples/` holds one folder per named product type (mirroring, not
duplicating, `product-types/*.md`'s domain list): SaaS, Admin Panel, ERP,
CRM, E-commerce, Healthcare, HRMS, Fintech, Logistics, Marketplace, Mobile
applications, Responsive web applications — plus one shared, domain-agnostic
folder, `common/`. Select by:
1. **Always include `common/`** — its domain-agnostic component/layout/
   interaction patterns apply regardless of which domain or platform folder
   also applies; it is never selected *instead of* a domain match, only
   *alongside* it.
2. An exact match to the confirmed `product-types/<domain>.md` slug.
3. Where no exact folder exists for a matched domain (most of
   `product-types/domain-standards/`'s 122 finer entries have no
   correspondingly-named sample), the nearest broader category — e.g. a
   "Telemedicine" product with no dedicated sample uses the Healthcare
   sample, not an arbitrary or unrelated one.
4. Where the platform is mobile-first or the product is explicitly a
   responsive web app rather than a desktop-first admin/SaaS surface, the
   Mobile applications or Responsive web applications sample may apply
   *instead of or alongside* the domain-matched one — platform and domain
   are independent axes here, same as `ui-engine/visual-trends.md`'s
   register-vs-domain independence.

A product where nothing more specific applies at all (a genuinely novel
domain with no matched pack, no platform signal) still has `common/` alone
to start from — Default mode is never left with literally nothing to
select.

A sample folder currently containing only a placeholder (see
`design-samples/README.md` for current population status) is used as a
*named starting register* (cite `ui-engine/visual-trends.md`'s matching
register — Modern SaaS, Dense Enterprise, or Consumer Playful — for the
actual token values) rather than left unresolved; population with real
curated references is tracked separately and does not block a product from
proceeding.

## Output
The stated mode (or modes, per-surface), its rationale, and — for mode 4 —
the selected sample folder, all recorded in `product-builder/ui/
design-direction.md`'s Design objective / Design inspiration fields.

## Explicitly not here
- The extraction technique that produces the material this file classifies
  → `reference-analysis.md`, `design-questionnaire.md`.
- The default sample library's own content/structure → `design-samples/`.
- The register a Default-mode product actually renders in → `ui-engine/
  visual-trends.md` (this file selects the *starting point*, that file's
  gate still governs any trend/style choice made from there).
