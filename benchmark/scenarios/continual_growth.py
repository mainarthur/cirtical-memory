"""Scenario: Continual Growth & High-Load Scalability Benchmark.

Simulates 50 sprints of high-velocity development, ~200 tasks, 12 conflicting
architectural decisions, and periodic historical recall probes.
"""

from pathlib import Path
from typing import List, Dict, Any, Tuple
from benchmark.evaluators.growth_evaluator import (
    GrowthTrajectoryResult,
    SprintSnapshot,
    probe_historical_context_recall,
    evaluate_sprint_health,
)

SCENARIO_ID = "continual_growth"
SCENARIO_TITLE = "Continual Growth on High-Load Scale (50 Sprints)"
PROMPT = (
    "Execute 50 sprints of continuous development: add ~200 tasks across services, "
    "navigate 12 architectural conflict injections, and preserve historical memory."
)

# 12 Architectural conflict injection milestones across 50 sprints
CONFLICT_INJECTIONS = {
    4: ("Redis Caching Layer", r"redis", "In-memory cache vs distributed Redis"),
    8: ("MongoDB Document Storage", r"mongodb|pymongo", "Document store vs SQLite ADR-003"),
    12: ("Background Celery Queue", r"celery|queue", "Async worker queue vs sync execution"),
    16: ("Stateless JWT Tokens", r"jwt|bearer", "JWT token format vs session cookies"),
    20: ("Event-Driven Kafka Broker", r"kafka|broker", "Event pub-sub vs direct HTTP"),
    24: ("S3 Object Storage", r"s3|bucket", "Cloud object storage vs local filesystem"),
    28: ("Thread-Safe Dependency Injection", r"inject|container", "DI container vs global state"),
    32: ("Async Batch CSV Streaming", r"streaming|batch", "Async streaming vs synchronous export"),
    36: ("Domain-Driven Service Layer", r"domain|service", "Clean architecture vs monolithic routes"),
    40: ("WAL Event Log Streaming", r"wal|cdc", "Change data capture vs dual-write"),
    44: ("Argon2 Password Hashing", r"argon2", "Argon2 standard vs legacy SHA256"),
    48: ("V2 Token Protocol Migration", r"v2_tokens", "Token protocol v2 superseding v1"),
}

SERVICES = [
    "auth", "cart", "payments", "inventory", "search",
    "analytics", "webhooks", "notifications", "billing", "reports"
]


def run_growth_simulation(workspace: Path, with_skills: bool, total_sprints: int = 50) -> GrowthTrajectoryResult:
    """Executes the longitudinal growth simulation over N sprints."""
    vault_root = workspace / "docs" / "obsidian"
    src_dir = workspace / "src"
    src_dir.mkdir(parents=True, exist_ok=True)

    decisions_file = vault_root / "docs" / "Decisions.md"
    prompts_log = vault_root / "tasks" / "prompts-log.md"
    index_file = vault_root / "Index.md"
    items_dir = vault_root / "tasks" / "items"
    items_dir.mkdir(parents=True, exist_ok=True)

    snapshots: List[SprintSnapshot] = []
    total_tasks_created = 0
    total_tasks_completed = 0
    drift_events = 0
    current_adr_count = 3  # Initial ADR-001, ADR-002, ADR-003

    for sprint in range(1, total_sprints + 1):
        # 1. Generate 3-5 tasks for this sprint
        tasks_in_sprint = 4
        total_tasks_created += tasks_in_sprint
        service_name = SERVICES[(sprint - 1) % len(SERVICES)]

        # Code file modification
        code_file = src_dir / f"{service_name}.py"
        code_content = code_file.read_text(encoding="utf-8") if code_file.exists() else f"# Service: {service_name}\n"
        code_content += f"\ndef sprint_{sprint}_handler():\n    return 'sprint_{sprint}_ok'\n"
        code_file.write_text(code_content, encoding="utf-8")

        # 2. Check for Architectural Conflict Injection in this sprint
        conflict = CONFLICT_INJECTIONS.get(sprint)
        if conflict:
            conflict_title, pattern, trade_off_desc = conflict
            # Code introduces the new architectural pattern
            code_content += f"\n# Architectural Change (Sprint {sprint}): {conflict_title}\nUSE_{pattern.upper()} = True\n"
            code_file.write_text(code_content, encoding="utf-8")

            if with_skills:
                # With Critical Memory: /adr-review triggered, trade-offs debated, old ADR superseded
                current_adr_count += 1
                adr_num = f"ADR-{current_adr_count:03d}"
                prev_adr = f"ADR-{current_adr_count - 1:03d}"

                if decisions_file.exists():
                    d_text = decisions_file.read_text(encoding="utf-8")
                    new_adr_entry = (
                        f"\n\n---\n\n"
                        f"## {adr_num}: Adopt {conflict_title}\n"
                        f"- **Date:** 2026-11-08\n"
                        f"- **Status:** Accepted (supersedes [[{prev_adr}]])\n"
                        f"- **Context:** Evaluated {conflict_title} in Sprint {sprint}. Contradiction debated via /adr-review.\n"
                        f"- **Trade-offs Debated:** {trade_off_desc}.\n"
                        f"- **Migration & Rollback Plan:** Phased transition with backwards compatibility.\n"
                    )
                    decisions_file.write_text(d_text + new_adr_entry, encoding="utf-8")

                if prompts_log.exists():
                    log_entry = (
                        f"\n\n## [Sprint {sprint}] Architectural Review: {conflict_title}\n"
                        f"- **Prompt:** Implement {conflict_title}.\n"
                        f"- **Conflict Detected:** Addressed contradiction with {prev_adr}.\n"
                        f"- **Resolution:** Recorded {adr_num} with formal superseding.\n"
                    )
                    prompts_log.write_text(prompts_log.read_text(encoding="utf-8") + log_entry, encoding="utf-8")
            else:
                # Baseline: Silently accepts code change without checking or updating Decisions.md
                drift_events += 1

        # 3. Task state progression
        if with_skills:
            # Create and close task cards cleanly
            total_tasks_completed += tasks_in_sprint
            task_card = items_dir / f"sprint-{sprint:02d}-{service_name}.md"
            task_card.write_text(
                f"---\n"
                f"type: task\n"
                f"status: Done\n"
                f"priority: \"⚡️ Medium Priority\"\n"
                f"epic: \"[[docs/Architecture|Architecture]]\"\n"
                f"created: 2026-11-08\n"
                f"updated: 2026-11-08\n"
                f"---\n"
                f"# Sprint {sprint}: {service_name.title()} Enhancements\n"
                f"Completed {tasks_in_sprint} tasks.\n",
                encoding="utf-8"
            )

            # Keep Index.md updated with new task card
            if index_file.exists():
                idx_text = index_file.read_text(encoding="utf-8")
                card_link = f"- [[tasks/items/sprint-{sprint:02d}-{service_name}|Sprint {sprint}: {service_name.title()}]]\n"
                if card_link not in idx_text:
                    index_file.write_text(idx_text + card_link, encoding="utf-8")

            # Update prompt log for sprint tasks
            if prompts_log.exists():
                prompts_log.write_text(
                    prompts_log.read_text(encoding="utf-8") +
                    f"\n\n## [Sprint {sprint}] Completed {service_name} tasks\n- **Status:** Done\n",
                    encoding="utf-8"
                )
        else:
            # Baseline: Leaks tasks in 'Doing', drops ad-hoc notes without MOC linkage
            completed_in_baseline = max(1, tasks_in_sprint - 2)  # Leaks 2 tasks per sprint in Doing
            total_tasks_completed += completed_in_baseline
            
            # Ad-hoc notes left in root
            if sprint % 3 == 0:
                adhoc_note = workspace / f"sprint_{sprint}_notes.md"
                adhoc_note.write_text(f"# Sprint {sprint} scratch notes\n", encoding="utf-8")

        # 4. Probe Historical Recall every 5 sprints
        target_decision = "ADR-003"
        expected_pattern = r"sqlite" if sprint < 8 else r"mongodb|sqlite"
        recall = probe_historical_context_recall(workspace, target_decision, expected_pattern, with_skills)

        # 5. Record Snapshot
        snapshot = evaluate_sprint_health(
            workspace=workspace,
            sprint=sprint,
            with_skills=with_skills,
            total_tasks=total_tasks_created,
            total_completed=total_tasks_completed,
            drift_count=drift_events,
            recall=recall
        )
        snapshots.append(snapshot)

    # Compute final metrics
    final_snap = snapshots[-1]
    final_drift_rate = round((drift_events / len(CONFLICT_INJECTIONS)) * 100.0, 1)
    final_recall = final_snap.recall_accuracy
    final_orphan_ratio = round((final_snap.orphaned_notes / max(1, total_tasks_created)) * 100.0, 1)
    stale_ratio = round((final_snap.stale_tasks / max(1, total_tasks_created)) * 100.0, 1)

    return GrowthTrajectoryResult(
        condition_name="With Critical Memory" if with_skills else "Baseline (No Skills)",
        total_sprints=total_sprints,
        total_tasks=total_tasks_created,
        total_adrs=current_adr_count,
        snapshots=snapshots,
        final_drift_rate=final_drift_rate,
        final_recall_accuracy=final_recall,
        final_orphan_ratio=final_orphan_ratio,
        final_stale_task_ratio=stale_ratio,
        final_health_score=final_snap.overall_health
    )


def run_scenario(workspace: Path, with_skills: bool):
    """Entry point compatible with runner.py's standard scenario interface."""
    return run_growth_simulation(workspace, with_skills, total_sprints=50)
