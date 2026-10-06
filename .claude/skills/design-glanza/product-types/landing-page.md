# Product Type: Landing Page / Marketing Site

## Responsibility
Reusable domain knowledge for single-purpose, pre-product conversion surfaces
(a landing page, a marketing site, a launch/waitlist page) — applied on top
of the domain-agnostic core (`product-intelligence/*`, `ux-engine/*`,
`ui-engine/*`) per Rule 14 (`config/operating-rules.md`), never a replacement
for it. Distinct from every other pack in this directory: those describe
*application* products (a persistent tool a user returns to); this pack
describes a *persuasion* surface whose success metric is conversion/action on
a single visit, not task completion across repeated use. No individual
company's product, copy, or brand is described here (Rule 15, Product
Isolation) — anything specific to one actual page belongs in that product's
generated Product Builder under `products/`.

**Explicitly excluded from this pack, and why:** a fixed visual/token system
(a specific font whitelist, exact spacing/radius values, a mandated
scroll-triggered reveal animation) is deliberately not included here, even
though the external source material this pack draws from ships one. A fixed
token system belongs to `ui-engine/visual-trends.md`'s register-selection
rule — this pack's job is to say *when a landing page is the right product
shape and how its structure should work*, not to hardcode one studio's house
style as if it were universal law. Every landing page generated through this
pack still selects its visual register via `visual-trends.md` like any other
product.

## 1. Common product characteristics
Single scroll or a small number of scroll-length sections, not a multi-screen
application — the IA is shallow by design (see point 4). One offer, one
audience, one primary action per page; a page trying to serve two unrelated
audiences or offers is a sign it should be two pages, not one page with two
primary actions (which would itself violate `ui-engine/visual-hierarchy.md`'s
one-primary-action rule). Success is measured in conversion on a single visit
(sign-up, purchase, demo request, waitlist join), not repeat-usage task
completion — this changes which `methodology/test.md` dimensions matter most
(discoverability and feedback carry more weight than, say, edge-case
robustness across many sessions).

## 2. Common users
A first-time visitor with no prior product familiarity, arriving from a
specific, identifiable traffic source (an ad, a social post, a direct link, a
search result) — the page's message must match what that source promised, or
the visitor's trust drops immediately. There is rarely a "returning user"
role distinct from a first-time one in the way other packs define roles; the
one meaningful variant is traffic-source context, not permission level.

## 3. Common workflows
- Intake before structure: purpose (what action should the visitor take),
  audience/traffic-source context (what did they just see/click to arrive
  here), available proof/assets (testimonials, logos, data), and constraints
  (brand, timeline, compliance) — gathered the same way
  `methodology/empathize.md` and `define.md` gather this for any product,
  just scoped to a single page rather than a whole application.
- Visitor lands → reads/scans in the page's chosen scan pattern
  (`ui-engine/visual-hierarchy.md`'s Z-pattern, the register this pack
  defaults to per point 6) → resolves objections encountered along the way →
  takes the one primary action, or leaves.
- A/B or message-variant testing is common at this product type's own
  Ideate/ Iterate stage — different *messaging* directions, not different
  interaction models, are frequently the axis of divergence here (contrast
  with `methodology/ideate.md`'s general interaction-model divergence rule).

## 4. Common information structures
Shallow, linear, single-path IA — a sequence of sections building toward one
action, not a hierarchy of independent areas. `ux-engine/information-
architecture.md`'s depth/breadth framework still applies, but for this
product type the answer is almost always "depth 1, ordered list of sections,"
not a multi-level tree.

## 5. Common navigation patterns
In-page anchor navigation to the page's own sections (if any nav exists at
all) rather than a persistent sidebar or multi-item top nav —
`ux-engine/navigation-system.md`'s sidebar/top-nav selection framework
resolves to "neither" for a shallow, single-path IA at this scale. Breadcrumbs
are never appropriate here (`navigation-system.md` item 7's depth-3-plus
condition is essentially never met by this product type's shallow IA).

## 6. Common UI patterns
- **Layout selection is a condition-gated choice, not a default**, the same
  discipline `navigation-system.md` already applies to nav patterns, applied
  here to whole-page shape: a hero-plus-sections structure fits a single
  clear offer with strong existing brand recognition; a long-form/story
  structure fits a complex or unfamiliar offer needing more explanation
  before the ask; a minimal single-action structure fits a narrow, high-
  intent audience (e.g. arriving from an ad matching one specific promise); a
  comparison structure fits an audience actively evaluating alternatives.
  Pick the layout the audience/offer combination calls for, not whichever is
  currently common.
- Content-realism is a concrete, checkable quality bar distinct from anything
  in the core engine: no placeholder ("Lorem Ipsum," "Acme Corp") content in
  anything presented as final; no fabricated proof (invented statistics,
  invented customer logos/counts); copy grounded in a specific, falsifiable
  claim rather than generic marketing phrasing that could belong to any
  competitor with the name swapped — this is the same specificity discipline
  `methodology/design-judgment.md`'s senior-reasoning-vs-sounding contrast
  applies to design rationale, applied here to visitor-facing copy.
- One primary call-to-action per page, restated at natural decision points
  (end of each major section) rather than only once at the top —
  reinforcing, not duplicating, `ui-engine/visual-hierarchy.md`'s one-
  primary-action rule across a longer scroll.
- Section spacing is weight-tiered, not uniform: this product type's pivotal
  section (the hero, or whichever section carries the primary CTA) can
  legitimately exceed `ui-engine/layout-system.md`'s ordinary spacing-scale
  ceiling — a flat, equal-spacing treatment across every section under-weights
  the one section actually carrying the page's job, even when every value used
  is technically "on-scale."

### Section library
A concrete starting vocabulary for point 6's layout selection — named
sections to compose from, not a fixed template every page must use in
full:
- **Nav** — sticky, logo/name plus anchor links to this page's own
  sections, a CTA button right-aligned; collapses to a mobile menu per
  `navigation-system.md`'s pattern, never a persistent sidebar (point 5).
- **Hero** — the headline states the value proposition, not the business
  name; a supporting one-to-two-sentence subheadline; the primary CTA;
  text-left/image-right on desktop, centered on mobile, per the
  weight-tiered spacing rule below.
- **Features/services** — 3-6 items in a responsive grid (1 col mobile →
  2-3 cols desktop), each an icon/illustration plus heading plus short
  description; headings follow the section's own heading-hierarchy rule
  (h2 for the section, h3 per item — never skipping a level).
- **Social proof** — testimonial cards (quote, name, role/company) or a
  client/partner logo bar; every testimonial is real content (point 6's
  content-realism bar), never a fabricated quote.
- **Pricing** (only where the product actually has priced tiers) — 2-3
  tier cards, one visually distinguished as recommended, a feature list
  and CTA per tier.
- **FAQ** — an accordion pattern (native `<details>`/`<summary>` needs no
  script); carries `FAQPage` structured data (Technical requirements,
  below) since it is both content and SEO signal.
- **Footer** — business identity, contact info, social links, legal
  links, a copyright line.

Not every page uses every section (point 6 already states layout is
condition-gated, not a default) — a narrow, high-intent single-action
page may be Nav + Hero + one CTA, nothing else.

## 7. Common operational concerns
### Technical requirements (meta, structured data, sitemap)
Generalizes any SEO-focused external technique into this pack's own
requirements, regardless of business vertical (a local service business,
a SaaS product, a marketplace):
- **`<head>` tags**: a title (50-60 chars, `Primary offer | Brand`
  pattern), a meta description (150-160 chars stating the offer,
  benefit, and CTA), a canonical URL, Open Graph and Twitter Card tags
  (using `ui-engine/asset-pipeline.md`'s generated OG card as the
  image), and the favicon package (`asset-pipeline.md`).
- **Structured data (JSON-LD)**: an `Organization`/`LocalBusiness`-family
  schema (a more specific subtype — `Plumber`, `Restaurant`,
  `ProfessionalService`, etc. — when the domain-standard pack identifies
  one) with `name`/`description`/`url`/`telephone`/`address` at minimum;
  a `Service` schema per service/offer section when distinct services
  are listed; an `FAQPage` schema whenever a FAQ section exists — every
  block includes `@context` and, for cross-referencing entities, a
  stable `@id`.
- **`robots.txt`** (allow all, cite the sitemap) and **`sitemap.xml`**
  (one `<url>` per page/anchor-section that's independently linkable,
  priority weighted homepage-highest).
- **Validation**: structured data is checked against schema.org's
  validation rules before this is considered complete — a missing
  `@context`, an incorrectly-formatted phone number, or an empty
  required array (e.g. `areaServed` present but empty) is a defect, not
  a cosmetic gap.
- This is additive to, never a replacement for, the accessibility and
  performance requirements point 11 already states in full.

Page load performance directly affects conversion (a slow first paint loses
visitors before the message is even read) — treat this as a stated
non-functional requirement for this product type by default, not an
afterthought. Analytics/conversion-event instrumentation on the primary
action is a first-class requirement, not optional polish.

## 8. Common edge cases
Visitor arrives with JavaScript/images partially blocked or slow (the page's
core message must still be legible in a degraded state); visitor arrives on a
narrow mobile viewport as the majority case, not the edge case, for
ad-driven traffic specifically; the primary action's destination is
temporarily unavailable (form endpoint down, checkout unavailable) — this
needs a real `system error` state (`ux-engine/state-design.md`), not a silent
failure, since a broken CTA at the moment of conversion is the single most
expensive failure this product type can have.

## 9. Domain-specific terminology
Hero, above-the-fold, CTA (call-to-action), conversion, traffic source,
objection-handling, social proof, above/below-the-fold.

## 10. Domain-specific UX risks
Message-mismatch: the page's headline/offer not matching what the traffic
source promised, which reads as a bait-and-switch and spikes bounce rate
regardless of how well the rest of the page is designed. Cramming multiple
audiences/offers onto one page instead of splitting into multiple pages
(point 1). Over-animating the message itself (a word-by-word reveal
animation on the headline) at the cost of the frequency-based animate/don't-
animate gate in `ux-engine/interaction-design.md` — a first-time,
one-shot read is exactly the "rare/first-time moment" case that gate says
*can* justify expressive motion, but only if the motion doesn't delay the
visitor from reading the actual message it's dressing up.

## 11. Domain-specific accessibility considerations
Applies `ux-engine/accessibility.md`'s baseline in full — this product type
has no relaxation. One risk specific to this type: scroll-triggered reveal
effects (content that fades/slides in as the visitor scrolls) must not be the
only way the content becomes available — a screen-reader user or a user with
JavaScript disabled must still reach every section's content in document
order, not lose sections that never "trigger."

## 12. Domain-specific scalability considerations
Scalability here means traffic-spike readiness (a launch driving a large,
concentrated burst of first-time visitors) rather than data-volume growth —
this is a hosting/performance concern to flag to `product-intelligence/
dependency-analysis.md`, not a UI-pattern concern like most other packs'
point 12.

## Explicitly not here
- The general reasoning technique any point above specializes →
  `ux-engine/information-architecture.md` / `navigation-system.md`
  (structures/navigation), `ui-engine/visual-trends.md` (UI register),
  `ui-engine/visual-hierarchy.md` (primary-action/scan-pattern rules),
  `ux-engine/accessibility.md` (accessibility), `ux-engine/interaction-
  design.md` (the animate/don't-animate gate).
- A fixed visual/token system for this product type → deliberately absent,
  see Responsibility above; use `ui-engine/visual-trends.md`'s register
  selection instead.
- Product-specific knowledge for one actual landing page → that product's
  generated Product Builder under `products/`.
