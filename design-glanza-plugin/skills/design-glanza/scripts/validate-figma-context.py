"""
validate-figma-context.py

Responsibility
--------------
Deterministic, structural check of a product's Figma Design Context
(`BRD/figma/figma-context.json`, per
`design-reference-engine/figma-context.schema.json`):

- If `BRD/figma/figma-context.json` does not exist at all, this is
  **not applicable** — not every product uses a Figma reference, and
  this script never fails a product just for omitting one. A single
  disclosed Note is emitted and the result is a pass, mirroring
  `validate-product.py`'s own posture for an unavailable optional
  capability (an absent, optional thing is disclosed, never silently
  treated as a failure, and never silently treated as a pass that hides
  the absence either).
- Where the file exists:
  - Valid JSON, and `source.fileKey`, `source.fetchedAt`,
    `source.inspectionMode` present; `inspectionMode` is one of
    `structured`/`image-fallback`.
  - **The one non-negotiable check**: `inspectionMode: "image-fallback"`
    always carries a non-empty `source.fallbackReason` —
    `figma-reference.md`'s "never silently substitute one mode for the
    other" rule, enforced deterministically rather than left to an
    agent's memory.
  - Every `screens[]` entry has `frameName`, `frameId`, and a
    `confidence` value in `explicit`/`inferred`/`assumed`.
  - Every `{value, confidence}`-shaped leaf found anywhere under
    `tokens`/`interactions` carries a `confidence` in the same three-value
    set — a leaf with a `value` key but no `confidence` key is flagged,
    since `figma-context.schema.json` requires the pairing structurally
    (`figma-reference.md`'s "the tag records how the value was actually
    obtained" rule).
  - Every `components.components[]` entry has `name` and `nodeId`.

What this deliberately does NOT check
--------------------------------------
Whether an extracted value is actually *correct* (that the Figma file
really does define that color/spacing value) — this script has no network
access and never re-contacts Figma; it only checks that whatever was
written down is structurally well-formed and honestly confidence-tagged.
Whether a `matchedRegistryEntry` citation is the *right* registry entry —
that is `agents/design-system-expert.md`'s judgment call
(`component-registry/registry-integration.md`), not a structural fact this
script can verify. Full JSON Schema validation against
`figma-context.schema.json` — that file is the canonical shape reference;
this script implements the equivalent structural checks directly,
dependency-free, matching every other script in this folder's
stdlib-only posture (same relationship `validate-tokens.py` has to
`design-tokens.schema.json`).

This script is deliberately optional in the pipeline (per the finalized
Figma-integration TODO's Phase 7, explicitly flagged as deferrable) — no
other reference form (screenshots, website references) has a deterministic
validator either; this one exists because a Figma Design Context is
machine-structured to begin with, which a screenshot never is.

Status: implemented.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import _common
from _common import Finding

CONFIDENCE_VALUES = ("explicit", "inferred", "assumed")
INSPECTION_MODES = ("structured", "image-fallback")


def _load_json(path: Path):
    if not path.is_file():
        return None, "missing-file"
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, f"invalid JSON ({e})"


def _check_source(context: dict, rel: str) -> list[Finding]:
    findings: list[Finding] = []
    source = context.get("source")
    if not isinstance(source, dict):
        findings.append(Finding("Blocker", "Missing or malformed 'source' object", rel, "source"))
        return findings

    for field in ("fileKey", "fetchedAt", "inspectionMode"):
        if not source.get(field):
            findings.append(Finding("Major", f"source.{field} is missing or empty", rel, "source"))

    mode = source.get("inspectionMode")
    if mode is not None and mode not in INSPECTION_MODES:
        findings.append(Finding(
            "Major",
            f"source.inspectionMode '{mode}' is not one of {INSPECTION_MODES}",
            rel, "source",
        ))
    if mode == "image-fallback" and not source.get("fallbackReason"):
        findings.append(Finding(
            "Blocker",
            "source.inspectionMode is 'image-fallback' but source.fallbackReason is "
            "missing or empty — a fallback must always be explicitly recorded, never "
            "silent (figma-reference.md's mandatory tool-invocation procedure, step 4)",
            rel, "source",
        ))
    return findings


def _check_screens(context: dict, rel: str) -> list[Finding]:
    findings: list[Finding] = []
    screens = context.get("screens", [])
    if not isinstance(screens, list):
        findings.append(Finding("Major", "'screens' is present but not a list", rel, "screens"))
        return findings
    for i, screen in enumerate(screens):
        if not isinstance(screen, dict):
            findings.append(Finding("Major", f"screens[{i}] is not an object", rel, "screens"))
            continue
        for field in ("frameName", "frameId"):
            if not screen.get(field):
                findings.append(Finding("Major", f"screens[{i}].{field} is missing or empty", rel, "screens"))
        confidence = screen.get("confidence")
        if confidence not in CONFIDENCE_VALUES:
            findings.append(Finding(
                "Major",
                f"screens[{i}].confidence '{confidence}' is not one of {CONFIDENCE_VALUES}",
                rel, "screens",
            ))
    return findings


def _check_components(context: dict, rel: str) -> list[Finding]:
    findings: list[Finding] = []
    components = context.get("components", {})
    if not isinstance(components, dict):
        return findings
    entries = components.get("components", [])
    if not isinstance(entries, list):
        return findings
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            findings.append(Finding("Minor", f"components.components[{i}] is not an object", rel, "components"))
            continue
        for field in ("name", "nodeId"):
            if not entry.get(field):
                findings.append(Finding(
                    "Minor", f"components.components[{i}].{field} is missing or empty", rel, "components",
                ))
    return findings


def _walk_confidence_tags(node, path: str, rel: str, findings: list[Finding]) -> None:
    """Best-effort, forgiving walk (matches _common.split_table_rows's own
    posture) — not a strict schema walk. Any dict carrying a 'value' key
    is treated as a valueWithConfidence leaf and must also carry a
    'confidence' key with a recognized value."""
    if isinstance(node, dict):
        if "value" in node:
            confidence = node.get("confidence")
            if confidence not in CONFIDENCE_VALUES:
                findings.append(Finding(
                    "Minor",
                    f"{path}: has a 'value' with no recognized 'confidence' "
                    f"({confidence!r}) — every extracted value must carry an "
                    "explicit/inferred/assumed tag",
                    rel, "confidence-tag",
                ))
            return
        for key, child in node.items():
            _walk_confidence_tags(child, f"{path}.{key}", rel, findings)
    elif isinstance(node, list):
        for i, child in enumerate(node):
            _walk_confidence_tags(child, f"{path}[{i}]", rel, findings)


def _check_confidence_tags(context: dict, rel: str) -> list[Finding]:
    findings: list[Finding] = []
    tokens = context.get("tokens")
    if tokens is not None:
        _walk_confidence_tags(tokens, "tokens", rel, findings)
    interactions = context.get("interactions")
    if interactions is not None:
        _walk_confidence_tags(interactions, "interactions", rel, findings)
    return findings


def validate(product_dir: Path) -> list[Finding]:
    figma_context_path = product_dir / "BRD" / "figma" / "figma-context.json"
    rel = "BRD/figma/figma-context.json"

    if not figma_context_path.is_file():
        return [Finding("Note", "No Figma Design Context present — not applicable for this product", rel, "not-applicable")]

    context, err = _load_json(figma_context_path)
    if err:
        return [Finding("Blocker", f"figma-context.json {err}", rel, "load-error")]

    findings: list[Finding] = []
    findings += _check_source(context, rel)
    findings += _check_screens(context, rel)
    findings += _check_components(context, rel)
    findings += _check_confidence_tags(context, rel)
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("product_dir", help="Path to a products/<slug>/ directory.")
    args = parser.parse_args(argv)

    findings = validate(Path(args.product_dir))
    if not findings:
        print("validate-figma-context: no findings.")
        return 0
    for f in findings:
        print(f)
    return 1 if any(f.severity in ("Blocker", "Major") for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
