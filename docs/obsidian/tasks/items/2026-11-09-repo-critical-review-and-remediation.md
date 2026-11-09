---
type: task
category: task
tags: [task, review, architecture, benchmark]
status: Done
priority: "🚨 Critical / Blocker"
epic: "[[docs/Architecture|Architecture Overview]]"
created: 2026-11-09
updated: 2026-11-09
---
# Repository Critical Review & Full Remediation of Cons

- **Status:** Done
- **Priority:** 🚨 Critical / Blocker
- **Epic:** [[docs/Architecture|Architecture Overview]]

## Summary & Scope
Conducted a comprehensive critical audit of the `critical-memory` repository (`REVIEW.md`) and resolved all identified cons across vault scalability, deterministic validation, token accounting, evaluator logic, and self-dogfooding.

## Resolution Notes
1. **Scalability ($O(1)$ Sharding & Log Rotation):** Upgraded `Decisions.md` into a compact registry table with atomic shards in `docs/decisions/` ([[docs/decisions/ADR-003-atomic-sharding-and-rolling-logs|ADR-003]]) and added a 15-entry rolling window on `tasks/prompts-log.md`.
2. **Deterministic Validator (`scripts/validate-vault.py`):** Built zero-dependency Python 3 linter (`--fix`, `--strict`, `--json`) and Git pre-commit hook (`scripts/install-hooks.sh`) per [[docs/decisions/ADR-004-deterministic-vault-validator|ADR-004]].
3. **Evaluator & Token Profiler Integrity:** Removed the artificial `1,800`-token baseline floor, added upfront `AGENTS.md` instruction overhead + break-even curve + live `transcript.jsonl` parser, fixed pre-satisfied seed checks, and implemented dual-tier ADR gatekeeping per [[docs/decisions/ADR-002-socratic-adr-gatekeeping|ADR-002]].
4. **Self-Dogfooding:** Initialized `docs/obsidian/` and root `AGENTS.md` on this repository and verified 100% validation pass.
