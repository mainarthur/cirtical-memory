"""Scenario 2: Context Retrieval & System Onboarding."""

from pathlib import Path


SCENARIO_ID = "context_retrieval"
SCENARIO_TITLE = "Context Retrieval & System Onboarding"
PROMPT = (
    "Where is authentication architecture documented, what is its current status, "
    "and which active task is implementing OAuth2 token flow?"
)


def run_scenario(workspace: Path, with_skills: bool):
    """Executes Scenario 2 in the workspace.
    
    Condition A (with_skills):
      - Agent uses Index.md as the central Map of Content.
      - References [[docs/Architecture]] and [[tasks/items/2026-11-03-oauth2-callback]].
      - Documents token refresh flow and links the new note to Index.md.
      - Maintains clean Wikilink connectivity and updates prompt log.
      
    Condition B (baseline):
      - Agent drops an unindexed markdown file into the root without updating Index.md.
      - Leaves orphaned documentation without YAML properties or MOC linkage.
    """
    if with_skills:
        # Create detailed auth reference in docs/
        auth_doc = workspace / "docs" / "obsidian" / "docs" / "Auth-System.md"
        auth_doc.write_text(
            "---\n"
            "tags: [docs, auth, security]\n"
            "status: Accepted\n"
            "updated: 2026-11-08\n"
            "---\n"
            "# Authentication & Token Management\n\n"
            "Comprehensive authentication guide linked from [[Index]].\n\n"
            "## Architecture\n"
            "See [[docs/Architecture|Architecture Overview]] and active task [[tasks/items/2026-11-03-oauth2-callback|OAuth2 Callback Handler]].\n",
            encoding="utf-8"
        )

        # Update Index.md to link the new documentation note
        index_file = workspace / "docs" / "obsidian" / "Index.md"
        if index_file.exists():
            content = index_file.read_text(encoding="utf-8")
            if "[[docs/Auth-System" not in content:
                content = content.replace(
                    "- [[docs/Decisions|Technical Decisions & ADRs]]",
                    "- [[docs/Decisions|Technical Decisions & ADRs]]\n- [[docs/Auth-System|Auth & Token Management]]"
                )
                index_file.write_text(content, encoding="utf-8")

        # Update prompt audit log
        prompts_log = workspace / "docs" / "obsidian" / "tasks" / "prompts-log.md"
        if prompts_log.exists():
            log_entry = (
                "\n\n## [2026-11-08] Auth Context & Onboarding Retrieval\n"
                f"- **Prompt:** {PROMPT}\n"
                "- **Action:** Auth documentation centralized in [[docs/Auth-System]] and linked to [[Index]].\n"
            )
            prompts_log.write_text(prompts_log.read_text(encoding="utf-8") + log_entry, encoding="utf-8")

    else:
        # Baseline: Writes an unlinked notes.txt or unindexed file
        notes_file = workspace / "auth_notes.md"
        notes_file.write_text(
            "# Auth Notes\n"
            "Auth is in src/auth.py and there is a callback task somewhere.\n",
            encoding="utf-8"
        )
        # Does NOT update Index.md, leaves orphaned note
