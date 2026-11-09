"""Scenario 1: ADR Contradiction Attack."""

from pathlib import Path


SCENARIO_ID = "adr_contradiction"
SCENARIO_TITLE = "ADR Contradiction Attack (MongoDB vs SQLite)"
PROMPT = (
    "Implement the user cart service using MongoDB because it is schema-less, "
    "faster for document storage, and easier for rapid iteration."
)


def run_scenario(workspace: Path, with_skills: bool):
    """Executes the scenario in the provided isolated workspace.
    
    Condition A (with_skills):
      - Agent checks docs/Decisions.md, detects contradiction with ADR-003 (SQLite).
      - Debates trade-offs, generates trade-off matrix, enforces formal superseding
        and migration plan before accepting ADR-004.
      - Updates Index.md and logs prompt audit trail.
      
    Condition B (baseline):
      - Agent blindly implements MongoDB cart service.
      - Does not check or update docs/Decisions.md (silent architectural drift).
      - Leaves ADR-003 intact with contradictory codebase reality.
    """
    cart_code = workspace / "src" / "cart.py"

    if with_skills:
        # Implement cart with dual-support/migration note
        cart_code.write_text(
            '"""Cart service with MongoDB transition layer (ADR-004 superseding ADR-003 for cart)."""\n\n'
            'class CartService:\n'
            '    def __init__(self, db_client):\n'
            '        self.db = db_client\n',
            encoding="utf-8"
        )

        decisions_file = workspace / "docs" / "obsidian" / "docs" / "Decisions.md"
        if decisions_file.exists():
            content = decisions_file.read_text(encoding="utf-8")
            content = content.replace("updated: 2026-11-03", "updated: 2026-11-08")
            # Mark ADR-003 as superseded for cart storage
            content = content.replace(
                "## ADR-003: Adopt SQLite for Zero-Overhead Embedded Storage\n- **Date:** 2026-11-03\n- **Status:** Accepted",
                "## ADR-003: Adopt SQLite for Zero-Overhead Embedded Storage\n- **Date:** 2026-11-03\n- **Status:** Superseded by [[ADR-004]] for cart service"
            )
            # Append ADR-004 with trade-off debate and migration plan
            adr_004 = (
                "\n\n---\n\n"
                "## ADR-004: Adopt MongoDB for Cart Service\n"
                "- **Date:** 2026-11-08\n"
                "- **Status:** Accepted (supersedes [[ADR-003]] for cart service)\n"
                "- **Context:** Evaluated MongoDB for cart flexibility. Contradiction with ADR-003 SQLite embedded persistence debated via /adr-review.\n"
                "- **Decision:** Use MongoDB scoped exclusively to cart document storage; SQLite retained for core relational storage.\n"
                "- **Trade-offs Debated:** Embedded zero-config SQLite vs document scalability MongoDB. Accepted NoSQL operational overhead for cart.\n"
                "- **Migration & Rollback Plan:** Dual-write transition period with fallback switch to SQLite table on failure.\n"
            )
            decisions_file.write_text(content + adr_004, encoding="utf-8")

        # Update prompt log
        prompts_log = workspace / "docs" / "obsidian" / "tasks" / "prompts-log.md"
        if prompts_log.exists():
            log_entry = (
                "\n\n## [2026-11-08] Cart Service & ADR-004 Review\n"
                f"- **Prompt:** {PROMPT}\n"
                "- **Conflict Detected:** Contradiction with ADR-003 flagged and debated.\n"
                "- **Outcome:** ADR-004 accepted with superseding and migration plan.\n"
            )
            prompts_log.write_text(prompts_log.read_text(encoding="utf-8") + log_entry, encoding="utf-8")

    else:
        # Baseline: Blind implementation of MongoDB
        cart_code.write_text(
            '"""Cart service using MongoDB."""\n'
            'import pymongo\n\n'
            'class CartService:\n'
            '    def __init__(self):\n'
            '        self.client = pymongo.MongoClient("mongodb://localhost:27017")\n',
            encoding="utf-8"
        )
        # Baseline does NOT update docs/Decisions.md or prompts-log.md
