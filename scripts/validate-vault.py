#!/usr/bin/env python3
"""Deterministic Vault Validator & Auto-Fixer for Critical Memory (memdoc).

Checks:
  1. Core vault file presence (Index.md, Architecture.md, Decisions.md, Kanban-Board.base, prompts-log.md)
  2. Map of Content (MOC) completeness: all docs/, docs/decisions/, and tasks/items/ notes indexed in Index.md
  3. Wikilink resolution: all [[Wikilinks]] resolve to existing files or ADR sections
  4. YAML frontmatter schema: valid status, priority, and YYYY-MM-DD dates on notes and tasks
  5. Scalability guardrails: tasks/prompts-log.md stays within the 15-entry rolling window

Usage:
  python3 ./scripts/validate-vault.py [VAULT_DIR] [--fix] [--strict] [--json] [--max-log-entries 15]
"""

import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Optional, Set, Tuple


TEMPLATE_FILENAMES = {
    "ADR-template.md",
    "task-template.md",
    "AGENTS.md",
}

PLACEHOLDER_LINKS = {
    "ADR-xxx",
    "ADR-yyy",
    "Note-Name",
    "subfolder/Note-Name",
    "Wikilink",
    "Wikilinks",
}

VALID_TASK_STATUSES = (
    "epic",
    "backlog",
    "up next",
    "doing",
    "done",
    "archive",
)

VALID_ADR_STATUSES = (
    "proposed",
    "accepted",
    "superseded",
    "rejected",
    "deprecated",
)


def strip_fenced_code_blocks(text: str) -> str:
    """Removes fenced code blocks (```...```) and inline code (`...`) so syntax examples are ignored."""
    no_fenced = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    return re.sub(r"`[^`\n]+`", "", no_fenced)


def parse_frontmatter(text: str) -> Optional[Dict[str, str]]:
    """Extracts flat key-value pairs from YAML frontmatter at the start of a Markdown file."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, flags=re.DOTALL)
    if not match:
        return None
    fm_block = match.group(1)
    props: Dict[str, str] = {}
    for line in fm_block.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        val = v.split("#", 1)[0].strip().strip("'\"")
        props[k.strip()] = val
    return props


def extract_wikilinks(text: str) -> List[str]:
    """Extracts raw link targets from [[target|alias]] or [[target#heading]] outside code blocks."""
    clean = strip_fenced_code_blocks(text)
    raw_matches = re.findall(r"\[\[([^\]|#\n]+)(?:[|#][^\]]*)?\]\]", clean)
    return [m.strip().rstrip("\\").strip() for m in raw_matches if m.strip()]


def rotate_prompts_log(prompts_log: Path, archive_dir: Path, max_entries: int) -> int:
    """Rotates oldest entries from prompts-log.md into tasks/archive/YYYY-MM-prompts.md."""
    text = prompts_log.read_text(encoding="utf-8")
    # Split header from chronological ## [YYYY-MM-DD] sections
    pattern = re.compile(r"(?=^##\s+\[\d{4}-\d{2}-\d{2}\])", flags=re.MULTILINE)
    parts = pattern.split(text)
    if len(parts) <= 1:
        return 0

    header = parts[0]
    entries = parts[1:]
    if len(entries) <= max_entries:
        return 0

    # Keep the most recent `max_entries` entries; assuming chronological append order,
    # detect whether newest are at top or bottom by comparing first and last dates.
    first_date_m = re.search(r"##\s+\[(\d{4}-\d{2}-\d{2})\]", entries[0])
    last_date_m = re.search(r"##\s+\[(\d{4}-\d{2}-\d{2})\]", entries[-1])
    first_date = first_date_m.group(1) if first_date_m else "0000-00-00"
    last_date = last_date_m.group(1) if last_date_m else "0000-00-00"

    if last_date >= first_date:
        # Newest at bottom -> archive earliest entries at the top
        to_archive = entries[:-max_entries]
        to_keep = entries[-max_entries:]
    else:
        # Newest at top -> archive oldest entries at the bottom
        to_keep = entries[:max_entries]
        to_archive = entries[max_entries:]

    archive_dir.mkdir(parents=True, exist_ok=True)
    for entry in to_archive:
        m = re.search(r"##\s+\[(\d{4}-\d{2})-\d{2}\]", entry)
        ym = m.group(1) if m else datetime.now().strftime("%Y-%m")
        archive_file = archive_dir / f"{ym}-prompts.md"
        if not archive_file.exists():
            archive_file.write_text(
                f"---\ntags: [tasks, prompts, archive]\nupdated: {datetime.now().strftime('%Y-%m-%d')}\n---\n"
                f"# Archived Prompts Log ({ym})\n\n",
                encoding="utf-8",
            )
        with archive_file.open("a", encoding="utf-8") as f:
            f.write("\n" + entry.strip() + "\n")

    prompts_log.write_text(header.rstrip() + "\n\n" + "\n\n".join(e.strip() for e in to_keep) + "\n", encoding="utf-8")
    return len(to_archive)


def auto_index_orphans(index_file: Path, vault_root: Path, orphans: List[Path]) -> int:
    """Appends missing [[Wikilinks]] for orphaned notes into Index.md."""
    if not index_file.exists() or not orphans:
        return 0
    content = index_file.read_text(encoding="utf-8").rstrip() + "\n"
    added = 0
    for orphan in orphans:
        rel = orphan.relative_to(vault_root).with_suffix("").as_posix()
        title = orphan.stem.replace("-", " ")
        link_line = f"- [[{rel}|{title}]]"
        if rel.startswith("docs/decisions/"):
            section_header = "## Architecture Decision Records (ADRs)"
        elif rel.startswith("tasks/items/"):
            section_header = "## Active & Recent Tasks"
        else:
            section_header = "## General & Usage Documentation"

        if section_header in content:
            idx = content.index(section_header) + len(section_header)
            content = content[:idx] + f"\n{link_line}" + content[idx:]
        else:
            content += f"\n{section_header}\n{link_line}\n"
        added += 1

    index_file.write_text(content, encoding="utf-8")
    return added


def validate_vault(
    vault_root: Path,
    fix: bool = False,
    strict: bool = False,
    max_log_entries: int = 15,
) -> Dict[str, Any]:
    """Runs all 5 deterministic validation checks on a Critical Memory vault."""
    errors: List[str] = []
    warnings: List[str] = []
    fixes_applied: List[str] = []

    if not vault_root.exists():
        return {
            "valid": False,
            "vault_root": str(vault_root),
            "errors": [f"Vault directory does not exist: {vault_root}"],
            "warnings": [],
            "fixes_applied": [],
        }

    # 1. Core structure check
    required_files = [
        vault_root / "Index.md",
        vault_root / "docs" / "Architecture.md",
        vault_root / "docs" / "Setup-and-Usage.md",
        vault_root / "docs" / "Decisions.md",
        vault_root / "tasks" / "Kanban-Board.base",
        vault_root / "tasks" / "prompts-log.md",
    ]
    for req in required_files:
        if not req.exists():
            errors.append(f"Missing core vault file: {req.relative_to(vault_root)}")

    index_file = vault_root / "Index.md"
    index_links: Set[str] = set()
    if index_file.exists():
        index_links = set(extract_wikilinks(index_file.read_text(encoding="utf-8")))

    # Collect all indexable notes in docs/, docs/decisions/, and tasks/items/
    candidate_notes: List[Path] = []
    for sub in ("docs", "docs/decisions", "tasks/items"):
        subdir = vault_root / sub
        if subdir.exists():
            for md in sorted(subdir.glob("*.md")):
                if md.name in TEMPLATE_FILENAMES:
                    continue
                candidate_notes.append(md)

    # 2. MOC Completeness (Orphan Detection)
    orphans: List[Path] = []
    for note in candidate_notes:
        rel_no_ext = note.relative_to(vault_root).with_suffix("").as_posix()
        stem = note.stem
        is_linked = any(
            link == rel_no_ext or link == stem or link.endswith(f"/{stem}")
            for link in index_links
        )
        if not is_linked:
            orphans.append(note)

    if orphans and fix and index_file.exists():
        fixed_count = auto_index_orphans(index_file, vault_root, orphans)
        if fixed_count:
            fixes_applied.append(f"Auto-indexed {fixed_count} orphaned note(s) in Index.md")
            index_links = set(extract_wikilinks(index_file.read_text(encoding="utf-8")))
            orphans = []

    for orphan in orphans:
        errors.append(f"Orphaned note not linked in Index.md: {orphan.relative_to(vault_root)}")

    # 3. Wikilink Resolution across all Markdown files
    all_vault_files: Set[str] = set()
    all_stems: Set[str] = set()
    for ext in ("*.md", "*.base"):
        for f in vault_root.rglob(ext):
            rel = f.relative_to(vault_root).with_suffix("").as_posix()
            all_vault_files.add(rel)
            all_stems.add(f.stem)

    # Also collect inline ADR headings (e.g. ADR-001, ADR-002) in Decisions.md
    decisions_file = vault_root / "docs" / "Decisions.md"
    inline_adr_ids: Set[str] = set()
    if decisions_file.exists():
        dec_text = decisions_file.read_text(encoding="utf-8")
        for m in re.findall(r"\b(ADR-\d{3,4})\b", dec_text):
            inline_adr_ids.add(m)

    for md_file in sorted(vault_root.rglob("*.md")):
        if md_file.name in TEMPLATE_FILENAMES:
            continue
        links = extract_wikilinks(md_file.read_text(encoding="utf-8"))
        for target in links:
            if target in PLACEHOLDER_LINKS or "{{" in target:
                continue
            # Check if target matches relative path, stem, or prefix match (e.g. ADR-001 matching ADR-001-slug)
            resolved = (
                target in all_vault_files
                or target in all_stems
                or target in inline_adr_ids
                or any(s.startswith(f"{target}-") for s in all_stems)
            )
            if not resolved:
                errors.append(
                    f"Broken [[{target}]] wikilink in {md_file.relative_to(vault_root)}"
                )

    # 4. YAML Frontmatter Schema Validation
    date_re = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    for note in candidate_notes:
        rel_path = note.relative_to(vault_root).as_posix()
        text = note.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if fm is None:
            errors.append(f"Missing YAML frontmatter in {rel_path}")
            continue

        if rel_path.startswith("tasks/items/"):
            status_val = fm.get("status", "").lower()
            if not any( status_val.startswith(valid_s) for valid_s in VALID_TASK_STATUSES ):
                errors.append(f"Invalid or missing task 'status' in {rel_path}: '{fm.get('status', '')}'")
            if not fm.get("priority"):
                errors.append(f"Missing task 'priority' frontmatter in {rel_path}")
            for d_key in ("created", "updated"):
                if d_key in fm and not date_re.match(fm[d_key]):
                    errors.append(f"Invalid {d_key} date format in {rel_path}: '{fm[d_key]}' (expected YYYY-MM-DD)")

        elif rel_path.startswith("docs/decisions/"):
            status_val = fm.get("status", "").lower()
            if not any(status_val.startswith(valid_s) for valid_s in VALID_ADR_STATUSES):
                errors.append(f"Invalid or missing ADR 'status' in {rel_path}: '{fm.get('status', '')}'")
            date_val = fm.get("date") or fm.get("updated") or ""
            if not date_re.match(date_val):
                errors.append(f"Invalid or missing 'date' frontmatter in {rel_path}: '{date_val}'")

        elif rel_path.startswith("docs/"):
            upd = fm.get("updated") or fm.get("date") or ""
            if not date_re.match(upd):
                errors.append(f"Missing or invalid 'updated: YYYY-MM-DD' frontmatter in {rel_path}")

    # 5. Rolling Window Cap on tasks/prompts-log.md
    prompts_log = vault_root / "tasks" / "prompts-log.md"
    if prompts_log.exists():
        log_text = prompts_log.read_text(encoding="utf-8")
        entries = re.findall(r"^##\s+\[\d{4}-\d{2}-\d{2}\]", log_text, flags=re.MULTILINE)
        if len(entries) > max_log_entries:
            if fix:
                archived = rotate_prompts_log(prompts_log, vault_root / "tasks" / "archive", max_log_entries)
                if archived:
                    fixes_applied.append(
                        f"Rotated {archived} older prompt log entry/entries to tasks/archive/"
                    )
            else:
                msg = (
                    f"tasks/prompts-log.md has {len(entries)} entries (exceeds rolling cap of {max_log_entries}). "
                    f"Run with --fix to rotate older entries into tasks/archive/."
                )
                if strict:
                    errors.append(msg)
                else:
                    warnings.append(msg)

    is_valid = len(errors) == 0 and (not strict or len(warnings) == 0)
    return {
        "valid": is_valid,
        "vault_root": str(vault_root),
        "checked_notes": len(candidate_notes),
        "errors": errors,
        "warnings": warnings,
        "fixes_applied": fixes_applied,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Critical Memory (memdoc) vault.")
    parser.add_argument(
        "vault_dir",
        nargs="?",
        default="docs/obsidian",
        help="Path to the vault directory (default: docs/obsidian)",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Auto-fix unindexed orphans in Index.md and rotate prompts-log.md entries exceeding window cap",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings (such as prompts-log window cap) as errors",
    )
    parser.add_argument(
        "--max-log-entries",
        type=int,
        default=15,
        help="Maximum recent entries to keep in tasks/prompts-log.md before archiving (default: 15)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output machine-readable JSON result",
    )

    args = parser.parse_args()
    vault_path = Path(args.vault_dir).resolve()
    result = validate_vault(
        vault_path,
        fix=args.fix,
        strict=args.strict,
        max_log_entries=args.max_log_entries,
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        status_icon = "✅ PASS" if result["valid"] else "❌ FAIL"
        print(f"{status_icon} | Critical Memory Vault Validation: {result['vault_root']}")
        print(f"  Checked Notes : {result.get('checked_notes', 0)}")
        for fix_msg in result["fixes_applied"]:
            print(f"  🔧 FIXED      : {fix_msg}")
        for warn_msg in result["warnings"]:
            print(f"  ⚠️  WARNING    : {warn_msg}")
        for err_msg in result["errors"]:
            print(f"  ❌ ERROR      : {err_msg}")

    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
