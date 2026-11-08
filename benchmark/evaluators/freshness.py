"""Evaluator for Dimension 4: Documentation Freshness & Code Synchronization."""

from pathlib import Path
import re
from typing import List
from .base import CheckResult, DimensionScore


def evaluate_doc_freshness(workspace: Path, scenario_id: str) -> DimensionScore:
    """Evaluates whether system documentation was updated alongside code modifications."""
    checks: List[CheckResult] = []
    vault_root = workspace / "docs" / "obsidian"

    arch_file = vault_root / "docs" / "Architecture.md"
    setup_file = vault_root / "docs" / "Setup-and-Usage.md"

    # Check 1: Architecture Documentation Exists and has substance
    has_arch = arch_file.exists()
    arch_len = len(arch_file.read_text(encoding="utf-8")) if has_arch else 0
    checks.append(CheckResult(
        name="architecture_documentation_substance",
        passed=(has_arch and arch_len > 200),
        score=1.0 if (has_arch and arch_len > 200) else (0.5 if has_arch else 0.0),
        weight=1.5,
        message="Architecture documentation is present and detailed."
                if (has_arch and arch_len > 200) else "Architecture documentation is missing or empty."
    ))

    # Check 2: Setup and Usage Guide Exists
    has_setup = setup_file.exists()
    setup_len = len(setup_file.read_text(encoding="utf-8")) if has_setup else 0
    checks.append(CheckResult(
        name="setup_and_usage_guidance",
        passed=(has_setup and setup_len > 200),
        score=1.0 if (has_setup and setup_len > 200) else (0.5 if has_setup else 0.0),
        weight=1.0,
        message="Developer setup and usage guide is maintained."
                if (has_setup and setup_len > 200) else "Setup and usage guide is missing or empty."
    ))

    # Check 3: Code Synchronization (Did docs update when features completed?)
    arch_text = arch_file.read_text(encoding="utf-8") if has_arch else ""
    if scenario_id == "task_lifecycle":
        has_synced_feature = bool(re.search(r"OAuth2 Callback", arch_text, re.IGNORECASE))
        checks.append(CheckResult(
            name="feature_synchronization_in_architecture",
            passed=has_synced_feature,
            score=1.0 if has_synced_feature else 0.0,
            weight=2.0,
            message="Architecture docs updated to reflect newly implemented features."
                    if has_synced_feature else "Architecture docs left stale without newly added feature details."
        ))

    # Check 4: Date Freshness in Frontmatter
    has_updated_date = bool(re.search(r"updated:\s*2026-11-08", arch_text))
    checks.append(CheckResult(
        name="documentation_date_freshness",
        passed=has_updated_date,
        score=1.0 if has_updated_date else 0.0,
        weight=1.0,
        message="Documentation frontmatter updated date is maintained."
                if has_updated_date else "Missing or unformatted updated date."
    ))

    total_weight = sum(c.weight for c in checks)
    weighted_score = sum(c.score * c.weight for c in checks)
    final_score = (weighted_score / total_weight) * 100.0 if total_weight > 0 else 0.0
    passed_count = sum(1 for c in checks if c.passed)

    return DimensionScore(
        name="Documentation Freshness",
        score=round(final_score, 1),
        passed_checks=passed_count,
        total_checks=len(checks),
        checks=checks
    )
