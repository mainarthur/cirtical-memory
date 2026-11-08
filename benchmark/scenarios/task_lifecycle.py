"""Scenario 3: Task Traceability & Kanban State Progression."""

from pathlib import Path


SCENARIO_ID = "task_lifecycle"
SCENARIO_TITLE = "Task Traceability & Kanban State Progression"
PROMPT = (
    "Finish implementing the OAuth2 callback handler in the auth service, "
    "and update the task card and documentation to mark it completed."
)


def run_scenario(workspace: Path, with_skills: bool):
    """Executes Scenario 3 in the workspace.
    
    Condition A (with_skills):
      - Completes auth handler in src/auth.py.
      - Updates task item frontmatter: status -> Done, updated -> 2026-11-08.
      - Appends detailed entry in tasks/prompts-log.md.
      - Updates docs/Architecture.md reflecting completed callback implementation.
      
    Condition B (baseline):
      - Completes auth handler in src/auth.py.
      - Leaves tasks/items/2026-11-03-oauth2-callback.md in stale 'Doing' status.
      - Does not update prompt audit log or architecture documentation.
    """
    auth_code = workspace / "src" / "auth.py"
    auth_code.write_text(
        '"""Authentication module with OAuth2 callback handler."""\n\n'
        'def verify_token(token: str) -> bool:\n'
        '    return token.startswith("valid_")\n\n'
        'def handle_oauth_callback(code: str) -> dict:\n'
        '    return {"access_token": f"valid_{code}", "token_type": "bearer"}\n',
        encoding="utf-8"
    )

    if with_skills:
        # Update task item frontmatter to status: Done
        task_file = workspace / "docs" / "obsidian" / "tasks" / "items" / "2026-11-03-oauth2-callback.md"
        if task_file.exists():
            content = task_file.read_text(encoding="utf-8")
            content = content.replace("status: Doing", "status: Done")
            content = content.replace("- **Status:** Doing", "- **Status:** Done")
            content = content.replace("updated: 2026-11-03", "updated: 2026-11-08")
            task_file.write_text(content, encoding="utf-8")

        # Update prompt log
        prompts_log = workspace / "docs" / "obsidian" / "tasks" / "prompts-log.md"
        if prompts_log.exists():
            log_entry = (
                "\n\n## [2026-11-08] Completed OAuth2 Callback Handler\n"
                f"- **Prompt:** {PROMPT}\n"
                "- **Changes:** Implemented handle_oauth_callback in src/auth.py.\n"
                "- **Task Card Updated:** [[tasks/items/2026-11-03-oauth2-callback]] transitioned to status: Done.\n"
                "- **Outcome:** OAuth2 flow verified and Kanban board updated.\n"
            )
            prompts_log.write_text(prompts_log.read_text(encoding="utf-8") + log_entry, encoding="utf-8")

        # Update docs/Architecture.md freshness
        arch_file = workspace / "docs" / "obsidian" / "docs" / "Architecture.md"
        if arch_file.exists():
            arch_text = arch_file.read_text(encoding="utf-8")
            arch_text = arch_text.replace("updated: 2026-11-03", "updated: 2026-11-08")
            arch_text += "\n- **OAuth2 Callback:** Complete and verified via handle_oauth_callback.\n"
            arch_file.write_text(arch_text, encoding="utf-8")

    else:
        # Baseline leaves task card stale in Doing, no prompt log, no doc freshness
        pass
