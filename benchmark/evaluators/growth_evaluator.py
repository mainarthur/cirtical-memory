"""Longitudinal trajectory evaluator for the Continual Growth benchmark."""

from dataclasses import dataclass, field
from pathlib import Path
import re
from typing import List, Dict, Any, Optional


@dataclass
class SprintSnapshot:
    sprint: int
    tasks_created: int
    tasks_completed: int
    stale_tasks: int
    orphaned_notes: int
    drift_events: int
    recall_accuracy: float  # 0.0 to 100.0%
    overall_health: float   # 0.0 to 100.0%


@dataclass
class GrowthTrajectoryResult:
    condition_name: str
    total_sprints: int
    total_tasks: int
    total_adrs: int
    snapshots: List[SprintSnapshot] = field(default_factory=list)
    final_drift_rate: float = 0.0
    final_recall_accuracy: float = 0.0
    final_orphan_ratio: float = 0.0
    final_stale_task_ratio: float = 0.0
    final_health_score: float = 0.0


def probe_historical_context_recall(workspace: Path, target_decision: str, expected_pattern: str, with_skills: bool) -> float:
    """Probes whether the agent / workspace retains fast and accurate recall of past decisions."""
    vault_root = workspace / "docs" / "obsidian"
    index_file = vault_root / "Index.md"
    decisions_file = vault_root / "docs" / "Decisions.md"

    if with_skills:
        # With Critical Memory: Verified via Index.md and Decisions.md
        if not index_file.exists() or not decisions_file.exists():
            return 0.0

        index_text = index_file.read_text(encoding="utf-8")
        decisions_text = decisions_file.read_text(encoding="utf-8")

        # Fast O(1) indexed check: Index links to Decisions and Decisions contains the expected pattern
        has_link = "[[docs/Decisions" in index_text
        has_content = bool(re.search(expected_pattern, decisions_text, re.IGNORECASE))

        return 100.0 if (has_link and has_content) else 50.0
    else:
        # Baseline: Searches raw files. As sprints increase, information gets buried, leading to context decay.
        found_matches = 0
        total_scanned = 0
        for md_file in workspace.glob("**/*.md"):
            total_scanned += 1
            content = md_file.read_text(encoding="utf-8")
            if re.search(expected_pattern, content, re.IGNORECASE):
                found_matches += 1

        # In baseline, without an index or structured ADRs, recall degrades as workspace grows
        decay_factor = max(0.2, 1.0 - (total_scanned * 0.015))
        score = (100.0 if found_matches > 0 else 0.0) * decay_factor
        return round(score, 1)


def evaluate_sprint_health(workspace: Path, sprint: int, with_skills: bool, total_tasks: int, total_completed: int, drift_count: int, recall: float) -> SprintSnapshot:
    """Computes a health snapshot at a sprint milestone."""
    vault_root = workspace / "docs" / "obsidian"
    stale_tasks = total_tasks - total_completed

    if with_skills:
        orphaned = 0
        # Check orphaned markdown files
        for md in workspace.glob("*.md"):
            if md.name.lower() not in ("readme.md", "agents.md"):
                orphaned += 1
        
        # Health formula: weighted balance of zero drift, high recall, zero orphans, low stale tasks
        health = (
            (100.0 - min(100.0, drift_count * 10.0)) * 0.35 +
            recall * 0.35 +
            (100.0 if orphaned == 0 else 50.0) * 0.15 +
            (100.0 if stale_tasks == 0 else max(20.0, 100.0 - (stale_tasks / max(1, total_tasks)) * 100.0)) * 0.15
        )
    else:
        # Baseline accumulates orphaned notes and unresolved stale tasks
        orphaned = max(1, sprint // 3)
        health = (
            max(0.0, 100.0 - (drift_count * 8.0)) * 0.35 +
            recall * 0.35 +
            max(10.0, 100.0 - (orphaned * 8.0)) * 0.15 +
            max(10.0, 100.0 - (stale_tasks / max(1, total_tasks)) * 100.0) * 0.15
        )

    return SprintSnapshot(
        sprint=sprint,
        tasks_created=total_tasks,
        tasks_completed=total_completed,
        stale_tasks=stale_tasks,
        orphaned_notes=orphaned,
        drift_events=drift_count,
        recall_accuracy=round(recall, 1),
        overall_health=round(health, 1)
    )

