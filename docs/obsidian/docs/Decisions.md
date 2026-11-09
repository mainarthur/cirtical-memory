---
tags: [docs, adr, decisions]
updated: 2026-11-09
---
# Architectural & Technical Decisions (ADR Registry)

A compact $O(1)$ registry of significant architectural, technical, and tool choices made during Critical Memory development. Full debate histories, trade-off matrices, and migration plans live in atomic files under `docs/decisions/ADR-xxx-<slug>.md`.

## ADR Registry Table

| ADR | Title | Status | Date | Supersedes | Summary |
| :--- | :--- | :---: | :---: | :---: | :--- |
| [[docs/decisions/ADR-001-initial-architecture\|ADR-001]] | Initial Architecture and Foundation | `Accepted` | 2026-11-09 | — | GenAI-agnostic Markdown vault with Obsidian Base Kanban and MOC navigation. |
| [[docs/decisions/ADR-002-socratic-adr-gatekeeping\|ADR-002]] | Safe Gatekeeping (`Proposed`) vs. Authorized Superseding (`Accepted`) | `Accepted` | 2026-11-09 | — | Rewards both safe deferral (`Proposed` + keep active ADR) and authorized override (`Accepted`). |
| [[docs/decisions/ADR-003-atomic-sharding-and-rolling-logs\|ADR-003]] | Compact ADR Registry + Atomic Sharding & 15-Entry Rolling Prompt Log | `Accepted` | 2026-11-09 | [[docs/decisions/ADR-001-initial-architecture\|ADR-001]] | Shards full ADRs into `docs/decisions/` and caps `prompts-log.md` at 15 entries. |
| [[docs/decisions/ADR-004-deterministic-vault-validator\|ADR-004]] | Deterministic Vault Validator (`validate-vault.py`) & Pre-Commit Hook | `Accepted` | 2026-11-09 | — | Enforces MOC completeness, wikilink resolution, and frontmatter schemas deterministically. |
