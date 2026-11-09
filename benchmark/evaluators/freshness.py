"""Evaluator for Dimension 4: Documentation Freshness & Code Synchronization."""

from pathlib import Path
import re
from typing import List
from .base import CheckResult, DimensionScore


SEED_BASELINE_DATE = "2026-11-03"


def _has_fresh_frontmatter_date(file_path: Path, baseline_date: str = SEED_BASELINE_DATE) -> bool:
    """Returns True if file_path has an updated/date frontmatter field newer than baseline_date."""
    if not file_path.exists():
        return False
    text = file_path.read_text(encoding="utf-8")
    for m in re.finditer(r"^(?:updated|date):\s*['\"]?(\d{4}-\d{2}-\d{2})['\"]?", text, flags=re.MULTILINE):
        if m.group(1) > baseline_date:
            return True
    return False


def evaluate_doc_freshness(workspace: Path, scenario_id: str) -> DimensionScore:
    """Evaluates whether system documentation was updated alongside code modifications."""
    checks: List[CheckResult] = []
    vault_root = workspace / "docs" / "obsidian"

    arch_file = vault_root / "docs" / "Architecture.md"
    setup_file = vault_root / "docs" / "Setup-and-Usage.md"
    decisions_file = vault_root / "docs" / "Decisions.md"
    auth_file = vault_root / "docs" / "Auth-System.md"

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
        has_synced_feature = bool(re.search(r"OAuth2 Callback.*(?:Complete|handle_oauth_callback|verified|Done)", arch_text, re.IGNORECASE | re.DOTALL))
        checks.append(CheckResult(
            name="feature_synchronization_in_architecture",
            passed=has_synced_feature,
            score=1.0 if has_synced_feature else 0.0,
            weight=2.0,
            message="Architecture docs updated to reflect newly implemented features."
                    if has_synced_feature else "Architecture docs left stale without newly added feature details."
        ))

    # Check 4: Date Freshness in Frontmatter (must be bumped past SEED_BASELINE_DATE 2026-11-03)
    target_files = [arch_file, decisions_file, auth_file]
    decisions_dir = vault_root / "docs" / "decisions"
    if decisions_dir.exists():
        target_files.extend(decisions_dir.glob("*.md"))

    has_updated_date = any(_has_fresh_frontmatter_date(f) for f in target_files)
    checks.append(CheckResult(
        name="documentation_date_freshness",
        passed=has_updated_date,
        score=1.0 if has_updated_date else 0.0,
        weight=1.5,
        message="Documentation frontmatter 'updated' date was bumped on modification."
                if has_updated_date else f"Documentation frontmatter dates left stale at seed baseline ({SEED_BASELINE_DATE})."
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
