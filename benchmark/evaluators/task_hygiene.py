"""Evaluator for Dimension 3: Task State & Kanban Hygiene."""

from pathlib import Path
import re
from typing import List
from .base import CheckResult, DimensionScore


def evaluate_task_hygiene(workspace: Path, scenario_id: str) -> DimensionScore:
    """Evaluates task tracking, prompt audit logging, and Kanban board compatibility."""
    checks: List[CheckResult] = []
    vault_root = workspace / "docs" / "obsidian"

    # Check 1: Kanban-Board.base Presence & Schema
    kanban_base = vault_root / "tasks" / "Kanban-Board.base"
    has_kanban = kanban_base.exists()
    checks.append(CheckResult(
        name="kanban_base_presence",
        passed=has_kanban,
        score=1.0 if has_kanban else 0.0,
        weight=1.0,
        message="Native Obsidian Base Kanban board exists." if has_kanban else "Kanban-Board.base missing."
    ))

    # Check 2: Prompts & Execution Audit Log
    prompts_log = vault_root / "tasks" / "prompts-log.md"
    has_prompts_log = prompts_log.exists()
    prompts_text = prompts_log.read_text(encoding="utf-8") if has_prompts_log else ""

    # Check if a new entry was appended for the current execution (2026-11-08)
    has_recent_run_entry = bool(re.search(r"##\s+\[2026-11-08\]", prompts_text))

    checks.append(CheckResult(
        name="prompt_audit_log_traceability",
        passed=has_recent_run_entry,
        score=1.0 if has_recent_run_entry else 0.0,
        weight=2.0,
        message="Prompt execution log was updated with an audit entry for this task."
                if has_recent_run_entry else "No audit log entry recorded in prompts-log.md for completed task."
    ))

    # Check 3: Task Card State Progression
    task_file = vault_root / "tasks" / "items" / "2026-11-03-oauth2-callback.md"
    if scenario_id == "task_lifecycle":
        task_text = task_file.read_text(encoding="utf-8") if task_file.exists() else ""
        is_done = bool(re.search(r"status:\s*['\"]?Done['\"]?", task_text, re.IGNORECASE))

        checks.append(CheckResult(
            name="task_card_state_progression",
            passed=is_done,
            score=1.0 if is_done else 0.0,
            weight=2.5,
            message="Task card successfully transitioned to 'Done' upon feature completion."
                    if is_done else "Task card was left in stale 'Doing' state despite code completion."
        ))

    # Check 4: Task Card Frontmatter Properties
    task_items_dir = vault_root / "tasks" / "items"
    valid_tasks = 0
    total_tasks = 0
    task_issues: List[str] = []

    if task_items_dir.exists():
        for tf in task_items_dir.glob("*.md"):
            if tf.name == "task-template.md":
                continue
            total_tasks += 1
            content = tf.read_text(encoding="utf-8")

            has_status = bool(re.search(r"^status:\s*['\"]?(Epic|Backlog|Up next|Doing|Done|Archive)", content, re.MULTILINE | re.IGNORECASE))
            has_priority = bool(re.search(r"^priority:", content, re.MULTILINE))

            if has_status and has_priority:
                valid_tasks += 1
            else:
                task_issues.append(f"{tf.name} (missing status or priority)")

    task_frontmatter_score = 1.0 if total_tasks > 0 and valid_tasks == total_tasks else (valid_tasks / total_tasks if total_tasks > 0 else 0.0)
    checks.append(CheckResult(
        name="kanban_card_frontmatter_properties",
        passed=(valid_tasks > 0 and len(task_issues) == 0),
        score=round(task_frontmatter_score, 2),
        weight=1.5,
        message=f"All task cards ({valid_tasks}/{total_tasks}) carry valid status and priority frontmatter."
                if len(task_issues) == 0 and total_tasks > 0 else f"Task card property issues: {task_issues}"
    ))

    total_weight = sum(c.weight for c in checks)
    weighted_score = sum(c.score * c.weight for c in checks)
    final_score = (weighted_score / total_weight) * 100.0 if total_weight > 0 else 0.0
    passed_count = sum(1 for c in checks if c.passed)

    return DimensionScore(
        name="Task & Kanban Hygiene",
        score=round(final_score, 1),
        passed_checks=passed_count,
        total_checks=len(checks),
        checks=checks
    )
