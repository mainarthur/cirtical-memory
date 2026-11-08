"""Evaluator for Dimension 1: Architectural Consistency & ADR Conflict Detection."""

from pathlib import Path
import re
from typing import List
from .base import CheckResult, DimensionScore


def evaluate_architectural_consistency(workspace: Path, scenario_id: str) -> DimensionScore:
    """Evaluates architectural consistency and ADR gatekeeping in the workspace."""
    checks: List[CheckResult] = []

    decisions_file = workspace / "docs" / "obsidian" / "docs" / "Decisions.md"
    atomic_adr_dir = workspace / "docs" / "obsidian" / "docs" / "decisions"
    has_adr_file = decisions_file.exists() or (atomic_adr_dir.exists() and any(atomic_adr_dir.glob("*.md")))

    checks.append(CheckResult(
        name="adr_documentation_presence",
        passed=has_adr_file,
        score=1.0 if has_adr_file else 0.0,
        weight=1.0,
        message="ADR file or directory is maintained." if has_adr_file else "No ADR records found in workspace."
    ))

    # Read all ADR content
    adr_text = ""
    if decisions_file.exists():
        adr_text += decisions_file.read_text(encoding="utf-8")
    if atomic_adr_dir.exists():
        for adr_path in atomic_adr_dir.glob("*.md"):
            adr_text += "\n" + adr_path.read_text(encoding="utf-8")

    # Read source code to check for silent architectural drift
    src_text = ""
    src_dir = workspace / "src"
    if src_dir.exists():
        for sf in src_dir.glob("**/*.py"):
            src_text += "\n" + sf.read_text(encoding="utf-8")

    # Check: Silent Architectural Drift (Code vs ADR)
    has_mongodb_in_code = bool(re.search(r"pymongo|mongodb|MongoClient", src_text, re.IGNORECASE))
    adr_mentions_mongodb = bool(re.search(r"mongodb", adr_text, re.IGNORECASE))
    has_adr_superseding_for_mongo = bool(
        re.search(r"ADR-004.*mongodb|mongodb.*supersed", adr_text, re.IGNORECASE | re.DOTALL)
    )

    if scenario_id == "adr_contradiction":
        # Check 2: Contradiction Flagged & Debated
        caught_conflict = bool(
            adr_mentions_mongodb and
            re.search(r"ADR-003|sqlite|ADR-002|postgres", adr_text, re.IGNORECASE) and
            re.search(r"conflict|contradict|trade-off|versus|vs\.?|supersed", adr_text, re.IGNORECASE)
        )
        checks.append(CheckResult(
            name="contradiction_detection",
            passed=caught_conflict,
            score=1.0 if caught_conflict else 0.0,
            weight=2.5,
            message="Contradiction with prior decision (ADR-003) was detected and debated."
                    if caught_conflict else "Agent silently accepted contradictory architecture without flagging prior ADR."
        ))

        # Check 3: Silent Drift Penalty
        drift_free = (not has_mongodb_in_code) or (has_mongodb_in_code and has_adr_superseding_for_mongo)
        checks.append(CheckResult(
            name="resistance_to_silent_drift",
            passed=drift_free,
            score=1.0 if drift_free else 0.0,
            weight=2.0,
            message="Code changes adhere to vetted ADRs (no unvetted drift)."
                    if drift_free else "Silent drift detected: Code uses MongoDB without formal ADR approval."
        ))

        # Check 4: Formal Superseding
        has_superseding = bool(
            re.search(r"supersed(es|ed|ed by)|supersedes:\s*\[\[", adr_text, re.IGNORECASE)
        )
        checks.append(CheckResult(
            name="formal_superseding_declared",
            passed=has_superseding,
            score=1.0 if has_superseding else 0.0,
            weight=1.5,
            message="Prior ADR status updated or superseding explicitly declared."
                    if has_superseding else "No formal superseding relationship recorded."
        ))

        # Check 5: Migration / Rollback Strategy
        has_migration = bool(
            re.search(r"migration|rollback|transition plan|dual-write", adr_text, re.IGNORECASE)
        )
        checks.append(CheckResult(
            name="migration_rollback_documented",
            passed=has_migration,
            score=1.0 if has_migration else 0.0,
            weight=1.0,
            message="Migration and rollback strategy documented."
                    if has_migration else "No migration or rollback strategy specified."
        ))
    else:
        # General ADR hygiene checks for other scenarios
        has_status = bool(re.search(r"(?:\*{0,2}Status:\*{0,2}|status:)\s*(?:\[\[)?(Accepted|Proposed|Superseded)", adr_text, re.IGNORECASE))
        checks.append(CheckResult(
            name="adr_status_lifecycle",
            passed=has_status,
            score=1.0 if has_status else 0.0,
            weight=1.5,
            message="ADR follows standard lifecycle states." if has_status else "ADR missing formal status."
        ))

    total_weight = sum(c.weight for c in checks)
    weighted_score = sum(c.score * c.weight for c in checks)
    final_score = (weighted_score / total_weight) * 100.0 if total_weight > 0 else 0.0
    passed_count = sum(1 for c in checks if c.passed)

    return DimensionScore(
        name="Architectural Consistency",
        score=round(final_score, 1),
        passed_checks=passed_count,
        total_checks=len(checks),
        checks=checks
    )
