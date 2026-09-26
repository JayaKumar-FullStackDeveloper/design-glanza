# Domain Standards

## Responsibility
Match an incoming product against `product-types/domain-standards/domain-
registry.json` — a much finer-grained, externally-sourced library of named
UI/UX standard documents (122 named domains across 12 categories, as of this
writing) — and load whichever standard(s) genuinely apply as **mandatory,
domain-specific design guidance layered on top of** the domain-agnostic core
engine and any matched `product-types/*.md` pack. This file never replaces
either: it supplies *content* those already-established techniques get
applied to, exactly the same relationship a `product-types/*.md` pack
already has to the core engine (per `product-types/custom-domain.md`'s
Domain Pack Contract framing — specialize, don't replace).

## Relationship to `product-types/*.md` — two distinct registries, one job
Design-Glanza has two domain-matching systems that answer different
questions, run at the same moment, and compose rather than compete:

| | `product-intelligence/domain-classifier.md` | This file |
|---|---|---|
| Matches against | The 12 `product-types/*.md` packs | The 122-entry `domain-registry.json` |
| Granularity | Broad (SaaS, Healthcare, ERP...) | Narrow (Telemedicine, Dental PMS, Payroll...) |
| Content | Design-Glanza's own authored guidance | An externally-sourced standard document (PDF) |
| Runs | Confirmed/refined at Architect (`agents/product-architect.md` step 1) | Matched and loaded at Architect (`agents/product-architect.md` step 2, same moment the pack overlay is applied) |

A registry entry's `slug` sometimes names the same domain a `product-types/
*.md` pack already covers (`admin-panel`, `erp`, `crm`, `hrms`, `healthcare`,
`fintech`, `logistics`, `marketplace`, and `e-commerce` against `ecommerce.md`)
— in that case, a loaded standard **enriches** the matched pack, it doesn't
supersede it. For the majority of registry entries with no corresponding
pack (e.g. "Telemedicine," "Dental PMS," "Payroll," "LegalTech" — most of the
122), `product-types/custom-domain.md`'s no-match/partial-match procedure
still runs exactly as it does for any unmatched domain, now additionally
informed by whichever standard matched, if one is complete (below). Neither
system is optional because of the other; they answer independent questions
("which broad pack, if any" vs. "which specific external standard, if any").

## Registry schema
Each entry in `domain-registry.json`:

| Field | Meaning |
|---|---|
| `id` | Stable `DG-NNN` identifier, cited in `product-builder/domain/domain-application-notes.md` when this entry is selected. |
| `domain` | The human-readable domain name — the primary matching vocabulary. |
| `category` | Which of the 12 top-level folders it lives under. |
| `slug` | Filesystem-safe name; compared against `product-types/*.md` filenames per the table above. |
| `path` | Relative path under `product-types/domain-standards/` to this entry's folder. |
| `standard` | `"complete"` (a real standard exists, load it) or `"pending"` (none yet — see below). |
| `standard_file` | The filename to load when `standard` is `"complete"` (currently always `standard.pdf`), or `null`. |

## Matching procedure
Run at Architect, by `agents/product-architect.md`, the same step that
applies the `product-types/*.md` overlay (its analysis-procedure step 2) —
this is the "Domain Detection → Domain Standard(s)" moment. Score the
registry's `domain` names and near-synonyms against `brd-analysis.md`'s
extracted facts (entity/role vocabulary, stated module names, explicit
product-category language) using the same signal-strength discipline
`domain-classifier.md` already uses for the pack match — a single weak
mention doesn't select an entry; a clear, repeated, specific match does.

- **Single confident match** — load that entry.
- **Multiple genuinely applicable entries** (a product spanning more than one
  named domain, e.g. a clinic-management product with its own pharmacy
  module) — load all of them, tagged one **primary** (the dominant domain)
  and the rest **supporting**, recorded together in `product-builder/domain/
  domain-application-notes.md` alongside the confidence/signals that drove
  each — the same confidence-reporting discipline `domain-classifier.md`
  already requires for its own match, applied here.
- **No entry matches with real confidence** — load nothing from this
  library; this is not an error and needs no fallback procedure of its own,
  since `product-types/custom-domain.md`'s existing no-match procedure
  already covers "no domain-specific content beyond the core engine."

**Never load an entry that doesn't genuinely match** merely for breadth or
because it's adjacent to one that did — an unrelated standard's guidance
(e.g. loading Banking's standard for a general Fintech product with no
banking-specific module) actively misleads downstream agents the same way a
wrong `product-types/*.md` classification would.

## Load procedure
For each selected entry:
- If `standard` is `"complete"` — read `product-types/domain-standards/
  <path>/<standard_file>` in full. Its guidance becomes mandatory input to
  every agent named in "Application," below, for this product, cited by this
  entry's `id`.
- If `standard` is `"pending"` — there is nothing to load. Proceed exactly as
  if this entry didn't exist; **never improvise substitute guidance** for a
  pending domain (that would be inventing domain-specific content the same
  way Rule 10 prohibits inventing a business rule — a `"pending"` entry is an
  honest, stated gap, not license to guess). A recurring gap here is exactly
  what would eventually justify preparing that standard, not fabricating one
  in the meantime.

## Application
A loaded standard is mandatory domain-specific guidance for the same eleven
concerns a `product-types/*.md` pack's Domain Pack Contract already
specializes — information architecture, user flows, UX patterns, UI
components, the design system, states, data visualization, accessibility,
responsive behavior, domain terminology, and the UX quality gates it
constrains. Concretely, this means the relevant agent treats the loaded
standard as a citable input alongside its existing technique file, exactly
as it already treats a `product-types/*.md` pack:

| Agent | Where the loaded standard applies |
|---|---|
| `agents/ux-architect.md` | Flow structure, IA, navigation choices |
| `agents/interaction-designer.md` | State/behavior specifics, domain terminology in copy |
| `agents/ui-designer.md` | Visual register fit, domain-specific UI/component conventions |
| `agents/design-system-expert.md` | Domain-specific component/token needs the standard calls for |
| `agents/accessibility-expert.md` | Any domain-mandated accessibility bar stricter than the default |
| `agents/qa-expert.md` | Domain-specific quality-gate criteria the standard adds |

None of these agents' own technique files (`ux-engine/*`, `ui-engine/*`)
are edited to accommodate a domain standard — Rule 14 (Domain-Agnostic Core)
applies to this library exactly as it applies to `product-types/*.md`; the
standard is consumed at the agent layer, which is where domain-specific and
domain-agnostic content are already meant to combine.

## Reconciliation
Not a separate priority system — a loaded domain standard sits at **Rule
2's tier 6** (`config/operating-rules.md`: "established domain conventions"),
the same tier `product-types/*.md` conventions already occupy: subordinate to
explicit requirements, acceptance criteria, existing product behavior,
existing design system, and existing code (tiers 1–5, all of which already
carry any regulatory/safety requirement that's been explicitly documented as
such), and senior to tier 7's generic `ux-engine/*`/`ui-engine/*` defaults
where the standard says something more specific. A genuine conflict between
a loaded standard and a tier 1–5 fact is resolved by the tier order exactly
as any other Rule 2 conflict is — this file does not introduce a competing
hierarchy.

## Explicitly not here
- The 12 `product-types/*.md` packs' own broad-domain matching → `domain-
  classifier.md`.
- The no-match/partial-match/graduation procedure for a product with no
  matching pack → `product-types/custom-domain.md`.
- The registry file and the standards themselves → `product-types/domain-
  standards/`.
- The general source-of-truth tier order this file cites → Rule 2,
  `config/operating-rules.md`.
