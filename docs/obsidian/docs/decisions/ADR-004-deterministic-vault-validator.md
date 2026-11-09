---
tags: [docs, adr, decisions]
status: Accepted
date: 2026-11-09
supersedes: null
superseded_by: null
---
# ADR-004: Deterministic Vault Validator (`validate-vault.py`) & Pre-Commit Hook

- **Date:** 2026-11-09
- **Status:** Accepted
- **Deciders:** Engineering Team

## Context & Problem Statement
Prompt-only conventions (`SKILL.md`, `AGENTS.md`) can still fail under heavy context pressure if an agent forgets to update `Index.md`, writes a broken `[[Wikilink]]`, or omits required task YAML frontmatter.

## Decision & Rationale
Ship a zero-dependency Python 3 validator CLI (`scripts/validate-vault.py`) with `--fix` (auto-indexing orphans and rotating `prompts-log.md`), `--strict`, and `--json` flags, paired with an optional Git `pre-commit` hook installer (`scripts/install-hooks.sh`).

## Debated Contradictions & Trade-offs
| Dimension | Prompt-Only Reliance | Prompt Instructions + `validate-vault.py` CLI | Trade-off Analysis |
| :--- | :--- | :--- | :--- |
| **Determinism** | Probabilistic compliance | 100% deterministic verification | Eliminates silent orphan/link bugs |
| **Dependencies** | Zero | Python 3 standard library only | Zero external package overhead |

## Consequences
- **Positive:** Catch broken wikilinks, unindexed orphans, and frontmatter schema errors deterministically in CI, pre-commit hooks, or agent self-checks.
- **Negative / Risks:** Requires Python 3.8+ (already standard across the repository).

## Migration & Rollback Strategy
Integrated into `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `copilot-instructions.md`, and `skills/memdoc/SKILL.md`.
