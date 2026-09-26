# Design-Glanza Domain Standards

This folder is the domain knowledge library for the Design-Glanza master
skill — a finer-grained, externally-sourced UI/UX standards library
alongside (not instead of) the 12 `product-types/*.md` domain packs one
level up. The full matching/loading procedure, and how this library
relates to those packs, is `product-intelligence/domain-standards.md` —
this file only orients the folder itself.

## Folder model
`category / NNN-domain / standard.pdf`, indexed by `domain-registry.json`.

## Runtime summary
Detected and loaded by `agents/product-architect.md` at Architect, at the
same step it applies a `product-types/*.md` overlay. Treated as mandatory
domain-specific guidance, never as grounds to override an explicit product
requirement or the general source-of-truth order (Rule 2,
`config/operating-rules.md`) — see `domain-standards.md` for the exact
reconciliation rule rather than restating it here.

## Current status
The first 11 standards (`01-core-business`) are populated. Remaining domain
folders are reserved and contain a `README.md` placeholder until their
standard is generated — a `"pending"` entry in `domain-registry.json` has
nothing to load, which is expected, not an error.

## Attribution
This library's registry structure and initial 11 standards were prepared
externally and imported as-is; the runtime procedure above was reconciled
against Design-Glanza's actual architecture (see
`config/master-config.md`'s changelog for the exact integration).
