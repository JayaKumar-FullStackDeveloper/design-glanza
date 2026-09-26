"""
create-product-builder.py

Responsibility
--------------
The Design-Glanza Product Builder Factory. Given a product definition, scaffold
`products/<product-slug>/` - directory structure, `product.json`, and a
product-specific `product-builder/SKILL.md` - without ever copying the master
Design-Glanza skill into the product. Every generated section *references* the
reusable master methodology (`config/`, `methodology/`, `product-intelligence/`,
`ux-engine/`, `ui-engine/`, `product-types/`) by relative path and carries only
product-specific content supplied in the definition (or a "pending" marker if
that phase hasn't run yet).

This script performs no reasoning (Rule 14/15, `config/operating-rules.md`): it
does not invent business objectives, requirements, flows, or rules. It only
templates whatever the caller's product definition already contains, and marks
everything else as pending for a later phase to fill in via `--update`.

Explicitly not here
--------------------
- The reasoning that produces requirements/flows/rules/etc. - that's the
  Design-Glanza phases themselves (`workflows/create-product.md` and friends),
  which call this script with their output as the product definition.
- Content-quality validation of an existing product-builder's requirements,
  screens, or states - see `validate-product.py`, `validate-requirements.py`,
  `validate-screens.py`, `validate-states.py`. This script's own `validate`
  subcommand checks *scaffold integrity* only (structure, presence, JSON
  validity) - a distinct, non-overlapping concern.

Usage
-----
    create-product-builder.py generate --definition path/to/definition.json
    create-product-builder.py generate --name "Acme Billing" --type saas --domain "Subscription billing"
    create-product-builder.py generate --definition definition.json --update
    create-product-builder.py validate <product-slug>

Status: implemented.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

import _common
from _common import (  # noqa: F401 - re-exported for backward compatibility
    SKILL_ROOT, PROJECT_ROOT, PRODUCTS_DIR, PRODUCT_TYPES_DIR,
    MASTER_CONFIG_PATH, TOP_LEVEL_DIRS, BUILDER_SUBDIRS, PRODUCT_JSON_FIELDS,
    discover_product_types,
)

# ---------------------------------------------------------------------------
# Path resolution - shared with every other script in this folder via
# _common.py, so a single source of truth backs the directory contract,
# product.json schema, and product-types discovery everywhere they're used.
# ---------------------------------------------------------------------------

MASTER_SKILL_MD = SKILL_ROOT / "SKILL.md"

METHODOLOGY_LABEL = (
    "Design-Glanza design-thinking engine - Empathize -> Define -> Ideate -> "
    "Prototype -> Test (continuous loop, see methodology/design-thinking.md)"
)

SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# Section order matches the 20 items required of a generated Product Builder
# SKILL.md. (title, definition_key, master_file_relpath, builder_artifact_relpath)
# definition_key is None for sections rendered purely from identity fields.
SECTION_SPECS = [
    ("Product Identity", None, None, None),
    ("Product Purpose", "purpose", None, "product/product-definition.md"),
    ("Product Type", None, None, None),
    ("Domain", None, None, None),
    ("Users", "users", "product-intelligence/user-roles.md", "requirements/user-roles.md"),
    ("Business Objectives", "business_objectives", "methodology/define.md", "product/product-definition.md"),
    ("Requirements", "requirements", "product-intelligence/requirement-engine.md", "requirements/requirement-matrix.md"),
    ("Business Rules", "business_rules", "product-intelligence/business-logic.md", "requirements/business-logic.md"),
    ("Dependencies", "dependencies", "product-intelligence/dependency-analysis.md", "requirements/dependency-analysis.md"),
    ("User Flows", "user_flows", "ux-engine/user-flow-engine.md", "ux/user-flows.md"),
    ("Information Architecture", "information_architecture", "ux-engine/information-architecture.md", "ux/sitemap.md"),
    ("Navigation", "navigation", "ux-engine/navigation-system.md", "ux/navigation.md"),
    ("UX Rules", "ux_rules", "ux-engine/interaction-design.md", "ux/ux-rules.md"),
    ("UI Rules", "ui_rules", "ui-engine/visual-hierarchy.md", "ui/ui-rules.md"),
    ("Design System", "design_system", "ui-engine/design-system.md", "ui/design-system.md"),
    ("State Rules", "state_rules", "ux-engine/state-design.md", "ux/state-matrix.md"),
    ("Edge Cases", "edge_cases", "product-intelligence/edge-case-engine.md", "requirements/edge-cases.md"),
    ("QA Rules", "qa_rules", "workflows/audit-product.md", "qa/qa-report.md"),
    ("Implementation Rules", "implementation_rules", "config/operating-rules.md", "workflows/implementation-notes.md"),
    ("Traceability Requirements", "traceability_requirements", "product-intelligence/traceability.md", "qa/traceability.md"),
]

BUILDER_SUBDIR_PURPOSE = {
    "product": ("Define-phase output for this product", "methodology/define.md"),
    "requirements": ("Requirement model, roles, business rules, dependencies, edge cases", "product-intelligence/requirement-engine.md"),
    "ux": ("Flows, information architecture, navigation, states", "ux-engine/user-flow-engine.md"),
    "ui": ("Design system, components, screen visuals", "ui-engine/design-system.md"),
    "domain": ("Which product-types/*.md pack applies and how it was adapted for this product", "product-types/custom-domain.md"),
    "workflows": ("Per-workflow entry->action->decision->system-response->next-action->completion specs and recovery paths", "ux-engine/user-flow-engine.md"),
    "qa": ("QA findings and the REQ->USER->FLOW->SCREEN->COMPONENT->TEST trace record", "product-intelligence/traceability.md"),
}

PENDING_MARKER = "_Pending - not yet run._"


# ---------------------------------------------------------------------------
# Validation: product name, slug, required fields, product_type.
# ---------------------------------------------------------------------------

def slugify(name: str) -> str:
    normalized = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", normalized).strip("-").lower()
    slug = re.sub(r"-{2,}", "-", slug)
    return slug


def read_master_skill_version() -> str:
    if not MASTER_CONFIG_PATH.is_file():
        return "unknown"
    text = MASTER_CONFIG_PATH.read_text(encoding="utf-8")
    match = re.search(r"\*\*Version:\*\*\s*([0-9]+\.[0-9]+\.[0-9]+)", text)
    return match.group(1) if match else "unknown"


def validate_product_name(name: str | None) -> list[str]:
    errors = []
    if not name or not name.strip():
        errors.append("product_name is required and cannot be empty")
    elif len(name) > 120:
        errors.append("product_name exceeds 120 characters")
    elif not any(ch.isalnum() for ch in name):
        errors.append("product_name must contain at least one alphanumeric character")
    return errors


def validate_slug(slug: str | None) -> list[str]:
    errors = []
    if not slug:
        errors.append("product_slug is required and cannot be empty")
    elif not SLUG_RE.match(slug):
        errors.append(
            f"product_slug '{slug}' is invalid - must be lowercase alphanumeric "
            "words separated by single hyphens (e.g. 'acme-billing')"
        )
    elif len(slug) > 64:
        errors.append("product_slug exceeds 64 characters")
    return errors


def validate_required_fields(definition: dict) -> list[str]:
    errors = []
    for field in ("product_name", "product_type", "domain"):
        if not definition.get(field):
            errors.append(f"missing required field: {field}")
    return errors


def validate_product_type(product_type: str | None, valid_types: list[str]) -> list[str]:
    if not product_type:
        return []  # already reported by validate_required_fields
    if product_type not in valid_types:
        return [
            f"product_type '{product_type}' is not a recognized domain pack "
            f"(known: {', '.join(valid_types)}). Author a new "
            "product-types/<domain>.md pack first (Rule 16, extensibility), "
            "or use 'custom-domain'."
        ]
    return []


def validate_definition(definition: dict) -> list[str]:
    """Full pre-generation validation. Returns a list of error strings; empty
    means the definition is valid enough to generate from."""
    errors: list[str] = []
    errors += validate_required_fields(definition)
    errors += validate_product_name(definition.get("product_name"))
    slug = definition.get("product_slug") or (
        slugify(definition["product_name"]) if definition.get("product_name") else None
    )
    errors += validate_slug(slug)
    errors += validate_product_type(definition.get("product_type"), discover_product_types())
    return errors


# ---------------------------------------------------------------------------
# Rendering helpers.
# ---------------------------------------------------------------------------

def render_item(item) -> str:
    if isinstance(item, str):
        return item
    if isinstance(item, dict):
        return ", ".join(f"**{k}**: {v}" for k, v in item.items())
    return str(item)


def relpath_from_builder(target: Path, builder_dir: Path) -> str:
    return Path(
        __import__("os").path.relpath(target, start=builder_dir)
    ).as_posix()


def render_section_body(
    key: str | None,
    definition: dict,
    master_relpath: str | None,
    artifact_relpath: str | None,
    builder_dir: Path,
    existing_sections: dict,
    title: str,
) -> str:
    value = definition.get(key) if key else None
    lines = []

    if master_relpath:
        master_link = relpath_from_builder(SKILL_ROOT / master_relpath, builder_dir)
        lines.append(f"_Master technique: [{master_relpath}]({master_link})_")
    if artifact_relpath:
        lines.append(f"_Product artifact: `product-builder/{artifact_relpath}`_")
    if lines:
        lines.append("")

    if value:
        if isinstance(value, (list, tuple)):
            lines.extend(f"- {render_item(v)}" for v in value)
        else:
            lines.append(render_item(value))
        return "\n".join(lines)

    # No new content supplied this run - preserve prior content if this
    # section was already filled in on an earlier `--update`, otherwise mark
    # pending.
    prior = existing_sections.get(title)
    if prior and PENDING_MARKER not in prior:
        return prior
    lines.append(PENDING_MARKER)
    return "\n".join(lines)


def parse_existing_skill_sections(skill_md_path: Path) -> dict:
    """Recover previously-rendered section bodies from an existing generated
    SKILL.md, keyed by section title, so `--update` never silently erases
    content from an earlier run that isn't resupplied this time."""
    if not skill_md_path.is_file():
        return {}
    text = skill_md_path.read_text(encoding="utf-8")
    sections: dict[str, str] = {}
    pattern = re.compile(r"^## (.+?)\n(.*?)(?=^## |\Z)", re.DOTALL | re.MULTILINE)
    for match in pattern.finditer(text):
        title, body = match.group(1).strip(), match.group(2).strip()
        sections[title] = body
    return sections


def build_skill_md(definition: dict, builder_dir: Path, existing_sections: dict) -> str:
    slug = definition["product_slug"]
    name = definition["product_name"]
    product_type = definition["product_type"]
    domain = definition["domain"]
    sub_domain = definition.get("sub_domain")
    platform = definition.get("platform", "web")
    builder_version = definition["builder_version"]
    master_version = definition["master_skill_version"]
    generated_at = definition.get("updated_at", definition.get("created_at"))

    master_skill_link = relpath_from_builder(MASTER_SKILL_MD, builder_dir)
    domain_pack_relpath = f"product-types/{product_type}.md"
    domain_pack_link = relpath_from_builder(SKILL_ROOT / domain_pack_relpath, builder_dir)
    lifecycle_relpath = "workflows/execute-product-builder.md"
    lifecycle_link = relpath_from_builder(SKILL_ROOT / lifecycle_relpath, builder_dir)

    frontmatter = (
        "---\n"
        f"name: {slug}-product-builder\n"
        f"description: Product Builder for {name} ({product_type} domain - {domain}). "
        "Generated by Design-Glanza. Contains product-specific knowledge only; "
        f"references the master skill at {master_skill_link} for all reusable "
        "methodology.\n"
        "---\n"
    )

    header = (
        f"# {name} - Product Builder\n\n"
        f"> **Status:** {definition['status']} - generated/updated {generated_at}. "
        f"Builder version `{builder_version}`, generated against Design-Glanza "
        f"master skill `v{master_version}`.\n\n"
        "## What this is\n"
        "This is a **generated Product Builder**, not the Design-Glanza master "
        "skill. It contains only knowledge specific to this one product. Every "
        "reusable technique it relies on is referenced from the master skill "
        f"below, never copied - see [{master_skill_link}]({master_skill_link}) "
        "for the reasoning engine itself, and "
        f"[{domain_pack_relpath}]({domain_pack_link}) for the domain pack "
        "applied to this product. Do not edit the master skill from within "
        "this product builder (Rule 15, Product Isolation) - edits to shared "
        "methodology belong upstream, in Design-Glanza itself.\n\n"
        "## How to use this Product Builder\n"
        "This Product Builder's lifecycle is INTAKE -> EMPATHIZE -> DEFINE -> "
        "IDEATE -> ARCHITECT -> PROTOTYPE -> IMPLEMENT -> TEST -> AUDIT -> "
        "ITERATE. The full 24-action sequence - which phase does what, which "
        "master technique each action uses, and the exact "
        "`product-builder/` file each action must write - is defined once, "
        f"reusably, at [{lifecycle_relpath}]({lifecycle_link}). Follow it "
        "directly; it is not duplicated here. In short: work through "
        "`requirements/` and `product/` (Intake/Empathize/Define/Ideate), "
        "then `ux/` and `ui/` (Architect/Prototype), then implement into "
        "`output/` where applicable, then validate and audit into `qa/` - "
        "and do not consider anything complete until the relevant quality "
        f"gates pass, per [{lifecycle_relpath}]({lifecycle_link})'s "
        "completion criteria, not merely because the happy path works.\n\n"
        "Any section below marked pending has not been run yet - do not "
        "invent its content; run the corresponding Design-Glanza phase and "
        "regenerate this builder with `--update` instead (Rule 10, No "
        "Invented Business Rules).\n"
    )

    body_sections = []
    for title, key, master_relpath, artifact_relpath in SECTION_SPECS:
        if title == "Product Identity":
            content = (
                f"- **Name:** {name}\n"
                f"- **Slug:** `{slug}`\n"
                f"- **Platform:** {platform}\n"
                f"- **Builder version:** `{builder_version}`\n"
                f"- **Master skill version:** `{master_version}`\n"
                f"- **Methodology:** {definition['methodology']}\n"
                f"- **Status:** {definition['status']}"
            )
        elif title == "Product Type":
            content = (
                f"`{product_type}` - see the reusable domain pack at "
                f"[{domain_pack_relpath}]({domain_pack_link})."
            )
        elif title == "Domain":
            sub_line = f"\n- **Sub-domain:** {sub_domain}" if sub_domain else ""
            content = f"- **Domain:** {domain}{sub_line}"
        else:
            content = render_section_body(
                key, definition, master_relpath, artifact_relpath,
                builder_dir, existing_sections, title,
            )
        body_sections.append(f"## {title}\n\n{content}\n")

    footer_rows = "\n".join(
        f"| `{sub}/` | {purpose} | [{master}]({relpath_from_builder(SKILL_ROOT / master, builder_dir)}) |"
        for sub, (purpose, master) in BUILDER_SUBDIR_PURPOSE.items()
    )
    footer = (
        "## Directory map\n\n"
        "| Folder | Holds | Master technique referenced |\n"
        "|---|---|---|\n"
        f"{footer_rows}\n"
    )

    return frontmatter + "\n" + header + "\n" + "\n".join(body_sections) + "\n" + footer


# ---------------------------------------------------------------------------
# Scaffolding.
# ---------------------------------------------------------------------------

def write_if_absent(path: Path, content: str) -> None:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def scaffold_top_level(product_dir: Path) -> None:
    (product_dir / "BRD").mkdir(parents=True, exist_ok=True)
    write_if_absent(
        product_dir / "BRD" / "README.md",
        "# BRD\n\nRaw source input for this product - BRD/PRD/SOW, user stories, "
        "acceptance criteria, specifications, screenshots, or notes on an "
        "existing product/codebase. This is the *original* material; "
        "Design-Glanza's analysis of it lives in `product-builder/`, not here.\n",
    )
    (product_dir / "output").mkdir(parents=True, exist_ok=True)
    write_if_absent(
        product_dir / "output" / "README.md",
        "# Output\n\nBuilt artifacts land here once the Implement phase "
        "(`workflows/build-product.md`) runs. Empty until then.\n",
    )


def scaffold_builder_subdirs(builder_dir: Path) -> None:
    for sub, (purpose, master_relpath) in BUILDER_SUBDIR_PURPOSE.items():
        subdir = builder_dir / sub
        subdir.mkdir(parents=True, exist_ok=True)
        master_link = relpath_from_builder(SKILL_ROOT / master_relpath, subdir)
        write_if_absent(
            subdir / "README.md",
            f"# {sub}/\n\n{purpose}.\n\n"
            f"Master technique referenced: [{master_relpath}]({master_link})\n\n"
            f"{PENDING_MARKER}\n",
        )


def build_product_json(definition: dict, existing: dict | None) -> dict:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    merged = dict(existing) if existing else {}
    merged.update({k: v for k, v in definition.items() if k in PRODUCT_JSON_FIELDS and v is not None})

    if existing:
        # bump the patch component of builder_version on update
        version_parts = re.match(r"(\d+)\.(\d+)\.(\d+)", str(existing.get("builder_version", "0.1.0")))
        if version_parts:
            major, minor, patch = (int(g) for g in version_parts.groups())
            merged["builder_version"] = f"{major}.{minor}.{patch + 1}"
        merged["created_at"] = existing.get("created_at", now)
    else:
        merged.setdefault("builder_version", "0.1.0")
        merged["created_at"] = now

    merged["master_skill_version"] = read_master_skill_version()
    merged.setdefault("methodology", METHODOLOGY_LABEL)
    merged.setdefault("status", "scaffolded")
    merged.setdefault("sub_domain", None)
    merged.setdefault("platform", "web")
    merged["updated_at"] = now

    # stable field order
    ordered = {field: merged.get(field) for field in PRODUCT_JSON_FIELDS}
    ordered["created_at"] = merged["created_at"]
    ordered["updated_at"] = merged["updated_at"]
    return ordered


def generate(definition: dict, update: bool) -> int:
    errors = validate_definition(definition)
    if errors:
        print("Cannot generate - the product definition is invalid:")
        for err in errors:
            print(f"  - {err}")
        return 1

    definition = dict(definition)
    definition["product_slug"] = definition.get("product_slug") or slugify(definition["product_name"])
    slug = definition["product_slug"]
    product_dir = PRODUCTS_DIR / slug
    exists = product_dir.exists()

    if exists and not update:
        report_conflict(slug, product_dir)
        return 1

    existing_product_json = None
    if exists:
        pj_path = product_dir / "product.json"
        if pj_path.is_file():
            try:
                existing_product_json = json.loads(pj_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                print(
                    f"Refusing to update - existing product.json at {pj_path} "
                    f"is not valid JSON ({exc}). Fix or remove it manually before "
                    "retrying, or regenerate with a fresh slug."
                )
                return 1

    product_json = build_product_json(definition, existing_product_json)
    definition.update({
        "builder_version": product_json["builder_version"],
        "master_skill_version": product_json["master_skill_version"],
        "methodology": product_json["methodology"],
        "status": product_json["status"],
        "sub_domain": product_json["sub_domain"],
        "platform": product_json["platform"],
        "created_at": product_json["created_at"],
        "updated_at": product_json["updated_at"],
    })

    builder_dir = product_dir / "product-builder"
    scaffold_top_level(product_dir)
    scaffold_builder_subdirs(builder_dir)

    existing_sections = parse_existing_skill_sections(builder_dir / "SKILL.md") if exists else {}
    skill_md = build_skill_md(definition, builder_dir, existing_sections)
    (builder_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")
    (product_dir / "product.json").write_text(
        json.dumps(product_json, indent=2) + "\n", encoding="utf-8"
    )

    action = "Updated" if exists else "Created"
    print(f"{action} product builder for '{definition['product_name']}' at "
          f"products/{slug}/ (builder v{product_json['builder_version']}).")

    ok, report = validate_scaffold(slug)
    print(report)
    return 0 if ok else 1


def report_conflict(slug: str, product_dir: Path) -> None:
    print(
        f"Conflict: a product already exists at products/{slug}/.\n"
        "Refusing to overwrite it without explicit instruction.\n\n"
        "To update it in place (existing product-specific content in "
        "requirements/ux/ui/domain/workflows/qa is preserved; only structure, "
        "product.json, and unfilled SKILL.md sections are refreshed), re-run "
        "with --update.\n"
        "To create a new, separate product, choose a different --slug/--name."
    )


# ---------------------------------------------------------------------------
# Scaffold-integrity validation (structure, presence, JSON validity).
# Content-quality validation of requirements/screens/states is a separate
# concern - see validate-product.py.
# ---------------------------------------------------------------------------

def validate_scaffold(slug: str) -> tuple[bool, str]:
    product_dir = PRODUCTS_DIR / slug
    checks: list[tuple[str, bool, str]] = []

    if not product_dir.is_dir():
        return False, f"FAIL: no product found at products/{slug}/"

    for d in TOP_LEVEL_DIRS:
        ok = (product_dir / d).is_dir()
        checks.append((f"top-level directory '{d}/'", ok, "" if ok else "missing"))

    builder_dir = product_dir / "product-builder"
    for d in BUILDER_SUBDIRS:
        ok = (builder_dir / d).is_dir()
        checks.append((f"product-builder/{d}/", ok, "" if ok else "missing"))

    skill_md_ok = (builder_dir / "SKILL.md").is_file()
    checks.append(("product-builder/SKILL.md presence", skill_md_ok, "" if skill_md_ok else "missing"))

    pj_path = product_dir / "product.json"
    pj_ok = pj_path.is_file()
    pj_detail = ""
    if not pj_ok:
        pj_detail = "missing"
    else:
        try:
            data = json.loads(pj_path.read_text(encoding="utf-8"))
            missing_fields = [f for f in PRODUCT_JSON_FIELDS if f not in data]
            if missing_fields:
                pj_ok = False
                pj_detail = f"missing fields: {', '.join(missing_fields)}"
            elif data.get("product_slug") != slug:
                pj_ok = False
                pj_detail = (
                    f"product_slug '{data.get('product_slug')}' does not match "
                    f"directory name '{slug}'"
                )
            elif data.get("product_type") not in discover_product_types():
                pj_ok = False
                pj_detail = f"product_type '{data.get('product_type')}' is not a recognized domain pack"
        except json.JSONDecodeError as exc:
            pj_ok = False
            pj_detail = f"invalid JSON: {exc}"
    checks.append(("product.json validity", pj_ok, pj_detail))

    artifact_checks_ok = True
    for d in BUILDER_SUBDIRS:
        subdir = builder_dir / d
        has_artifact = subdir.is_dir() and any(subdir.iterdir())
        checks.append((f"product-builder/{d}/ has a required artifact (at least its index file)", has_artifact, "" if has_artifact else "empty directory"))
        artifact_checks_ok = artifact_checks_ok and has_artifact

    lines = ["Scaffold validation:"]
    all_ok = True
    for name, ok, detail in checks:
        status = "PASS" if ok else "FAIL"
        all_ok = all_ok and ok
        suffix = f" ({detail})" if detail else ""
        lines.append(f"  [{status}] {name}{suffix}")
    lines.append(f"Overall: {'PASS' if all_ok else 'FAIL'}")
    return all_ok, "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def load_definition(args: argparse.Namespace) -> dict:
    definition: dict = {}
    if args.definition:
        definition = json.loads(Path(args.definition).read_text(encoding="utf-8"))
    overrides = {
        "product_name": args.name,
        "product_slug": args.slug,
        "product_type": args.type,
        "domain": args.domain,
        "sub_domain": args.sub_domain,
        "platform": args.platform,
    }
    for key, value in overrides.items():
        if value is not None:
            definition[key] = value
    return definition


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest="command", required=True)

    gen = subparsers.add_parser("generate", help="Scaffold or update a product builder.")
    gen.add_argument("--definition", help="Path to a JSON product definition file.")
    gen.add_argument("--name", help="product_name (overrides --definition if both given)")
    gen.add_argument("--slug", help="product_slug (derived from --name if omitted)")
    gen.add_argument("--type", help="product_type (must match a product-types/*.md pack)")
    gen.add_argument("--domain", help="domain")
    gen.add_argument("--sub-domain", dest="sub_domain", help="sub_domain")
    gen.add_argument("--platform", default=None, help="platform (default: web)")
    gen.add_argument("--update", action="store_true", help="Update an existing product builder in place instead of refusing on conflict.")

    val = subparsers.add_parser("validate", help="Validate an existing product builder's scaffold integrity.")
    val.add_argument("slug", help="product_slug to validate under products/")

    args = parser.parse_args(argv)

    if args.command == "generate":
        definition = load_definition(args)
        return generate(definition, update=args.update)

    if args.command == "validate":
        ok, report = validate_scaffold(args.slug)
        print(report)
        return 0 if ok else 1

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
