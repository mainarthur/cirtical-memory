"""Evaluator for Dimension 2: Traceability & MOC (Map of Content) Hygiene."""

from pathlib import Path
import re
from typing import List, Set
from .base import CheckResult, DimensionScore


def evaluate_traceability(workspace: Path, scenario_id: str) -> DimensionScore:
    """Evaluates link integrity, Index.md Map of Content completeness, and orphaned files."""
    checks: List[CheckResult] = []
    vault_root = workspace / "docs" / "obsidian"
    index_file = vault_root / "Index.md"

    # Check 1: Central Map of Content (Index.md) exists
    has_index = index_file.exists()
    checks.append(CheckResult(
        name="moc_index_presence",
        passed=has_index,
        score=1.0 if has_index else 0.0,
        weight=1.5,
        message="Central Index.md MOC exists." if has_index else "Index.md Map of Content is missing."
    ))

    index_text = index_file.read_text(encoding="utf-8") if has_index else ""

    # Extract all wikilinks in Index.md
    index_wikilinks = set(re.findall(r"\[\[([^\]|#]+)(?:\||#|\]\])", index_text))

    # Check 2: All docs/ and docs/decisions/ notes are indexed in Index.md
    docs_dir = vault_root / "docs"
    unindexed_docs: List[str] = []
    total_docs = 0
    if docs_dir.exists():
        doc_candidates = list(docs_dir.glob("*.md"))
        decisions_subdir = docs_dir / "decisions"
        if decisions_subdir.exists():
            doc_candidates.extend(decisions_subdir.glob("*.md"))
        for doc in doc_candidates:
            if doc.name in ("ADR-template.md", "task-template.md"):
                continue
            total_docs += 1
            doc_rel = doc.relative_to(vault_root).with_suffix("").as_posix()
            if not any(doc.stem in link or doc_rel in link for link in index_wikilinks):
                unindexed_docs.append(doc.name)

    docs_indexed_ratio = 1.0 if total_docs == 0 else (total_docs - len(unindexed_docs)) / total_docs
    checks.append(CheckResult(
        name="documentation_notes_indexed",
        passed=(len(unindexed_docs) == 0 and total_docs > 0),
        score=round(docs_indexed_ratio, 2),
        weight=1.5,
        message="All documentation notes are linked from Index.md."
                if len(unindexed_docs) == 0 else f"Orphaned docs unlinked in Index.md: {unindexed_docs}"
    ))

    # Check 3: Orphaned Markdown Files in Repository
    # Check if files like auth_notes.md or unindexed markdown notes exist outside vault
    orphaned_repo_md = [
        f.name for f in workspace.glob("*.md")
        if f.name.lower() != "readme.md" and f.name not in ("AGENTS.md", "CLAUDE.md", "REVIEW.md")
    ]
    has_no_orphans = len(orphaned_repo_md) == 0
    checks.append(CheckResult(
        name="no_orphaned_workspace_notes",
        passed=has_no_orphans,
        score=1.0 if has_no_orphans else 0.0,
        weight=2.0,
        message="No unindexed orphaned markdown notes in workspace root."
                if has_no_orphans else f"Orphaned notes found in workspace root: {orphaned_repo_md}"
    ))

    # Check 4: Scenario-specific Context Retrieval Integration
    if scenario_id == "context_retrieval":
        has_auth_in_index = any("Auth-System" in link or "auth" in link.lower() for link in index_wikilinks)
        checks.append(CheckResult(
            name="new_knowledge_linked_to_moc",
            passed=has_auth_in_index,
            score=1.0 if has_auth_in_index else 0.0,
            weight=2.0,
            message="New system knowledge was linked directly to central Map of Content."
                    if has_auth_in_index else "New knowledge was created in isolation without MOC linkage."
        ))

    # Check 5: Valid Wikilink Syntax
    wikilink_count = len(re.findall(r"\[\[.+?\]\]", index_text))
    has_wikilinks = wikilink_count >= 2
    checks.append(CheckResult(
        name="wikilink_navigation_format",
        passed=has_wikilinks,
        score=1.0 if has_wikilinks else (0.5 if wikilink_count > 0 else 0.0),
        weight=1.0,
        message=f"Obsidian [[Wikilinks]] used properly ({wikilink_count} links found)."
                if has_wikilinks else "Insufficient or missing [[Wikilink]] navigation."
    ))

    total_weight = sum(c.weight for c in checks)
    weighted_score = sum(c.score * c.weight for c in checks)
    final_score = (weighted_score / total_weight) * 100.0 if total_weight > 0 else 0.0
    passed_count = sum(1 for c in checks if c.passed)

    return DimensionScore(
        name="Traceability & MOC Hygiene",
        score=round(final_score, 1),
        passed_checks=passed_count,
        total_checks=len(checks),
        checks=checks
    )
