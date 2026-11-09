---
tags: [docs, architecture]
updated: 2026-11-09
---
# Critical Memory — Architecture Overview

**Critical Memory** is a GenAI-agnostic project memory, living documentation, and architectural gatekeeping system built on native Markdown and Obsidian conventions.

## System Components

1. **Skills Layer (`skills/`)**
   - **`memdoc` (`skills/memdoc/SKILL.md`):** Maintains the central Map of Content (`Index.md`), atomic documentation shards, Obsidian Base Kanban boards (`tasks/Kanban-Board.base`), and rolling 15-entry prompt logs (`tasks/prompts-log.md`).
   - **`adr-review` (`skills/adr-review/SKILL.md`):** 3-phase Socratic gatekeeper (Devil's Advocate debate, Trade-off Matrix, and `Proposed` vs. `Accepted` superseding verification) triggered whenever a change contradicts an accepted ADR.

2. **Universal Agent Templates (`templates/`)**
   - Provides `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, and `copilot-instructions.md` alongside vault seed files (`Index.md`, `docs/Decisions.md`, `docs/decisions/ADR-001-initial-architecture.md`, `tasks/Kanban-Board.base`).

3. **Deterministic Tooling (`scripts/`)**
   - **`init-vault.sh`:** Bootstraps a fresh `docs/obsidian/` vault and root `AGENTS.md` in any project.
   - **`validate-vault.py`:** Zero-dependency Python 3 linter (`--fix`, `--strict`, `--json`) enforcing MOC completeness, wikilink resolution, YAML frontmatter schemas, and 15-entry log rotation into `tasks/archive/`.
   - **`install-hooks.sh`:** Installs a Git `pre-commit` hook that executes `validate-vault.py`.

4. **Evaluation & Benchmark Suite (`benchmark/`)**
   - 4-dimension grading engine (`architectural`, `traceability`, `task_hygiene`, `freshness`) + dual-mode honest token profiler (`token_profiler.py`) supporting both file-discovery break-even modeling and live Antigravity `transcript.jsonl` parsing.

## Core Reference Links
- [[docs/Setup-and-Usage|Setup and Usage Guide]]
- [[docs/Decisions|Technical Decisions Registry (ADRs)]]
- [[tasks/Kanban-Board|Kanban Task Board]]
