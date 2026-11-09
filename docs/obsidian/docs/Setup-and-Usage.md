---
tags: [docs, setup, usage]
updated: 2026-11-09
---
# Setup and Usage Guide

## 1. Bootstrap a Vault in Any Project
```bash
./scripts/init-vault.sh [TARGET_DIR] [PROJECT_NAME]
```
This creates `docs/obsidian/` (with `Index.md`, `docs/Decisions.md`, `docs/decisions/`, `tasks/Kanban-Board.base`, `tasks/prompts-log.md`, and `tasks/archive/`) plus a root `AGENTS.md`.

## 2. Deterministic Validation & Auto-Fixing
```bash
# Check vault integrity (MOC completeness, wikilinks, frontmatter, log window):
python3 ./scripts/validate-vault.py docs/obsidian --strict

# Auto-index orphaned notes and rotate prompt logs exceeding 15 entries:
python3 ./scripts/validate-vault.py docs/obsidian --fix

# Install Git pre-commit hook:
./scripts/install-hooks.sh
```

## 3. Running the Benchmark Suite
```bash
# Standard 3-scenario evaluation + honest break-even report:
./benchmark/run.sh

# 50-sprint longitudinal scaling simulation:
./benchmark/run.sh --scenario continual_growth --sprints 50

# 2x2 per-scenario isolated matrix (Gemini & Claude personas):
./benchmark/run.sh --matrix
```

## Related Notes
- [[docs/Architecture|Architecture Overview]]
- [[docs/Decisions|Technical Decisions Registry (ADRs)]]
