---
tags: [docs, adr, decisions]
status: Accepted
date: 2026-11-09
supersedes: "[[docs/decisions/ADR-001-initial-architecture|ADR-001]]"
superseded_by: null
---
# ADR-003: Compact ADR Registry + Atomic Sharding & 15-Entry Rolling Prompt Log

- **Date:** 2026-11-09
- **Status:** Accepted
- **Deciders:** Engineering Team

## Context & Problem Statement
In the initial vault design, `docs/Decisions.md` and `tasks/prompts-log.md` were append-only monolithic files. Over 50+ sprints, reading those files grows $O(N)$ in token count—contradicting the $O(1)$ Map of Content architecture.

## Decision & Rationale
1. **Compact ADR Registry + Atomic Shards:** Make `docs/Decisions.md` a lightweight 1-line-per-ADR summary table linking to full atomic ADR files in `docs/decisions/ADR-xxx-<slug>.md`.
2. **15-Entry Rolling Window on `prompts-log.md`:** Cap `tasks/prompts-log.md` at 15 recent `## [YYYY-MM-DD]` entries and automatically rotate older entries into `tasks/archive/YYYY-MM-prompts.md` via `./scripts/validate-vault.py --fix`.

## Debated Contradictions & Trade-offs
| Dimension | Monolithic `Decisions.md` / `prompts-log.md` | Compact Registry + Atomic Shards & Log Rotation | Trade-off Analysis |
| :--- | :--- | :--- | :--- |
| **Token Scaling** | $O(N)$ unbounded growth | $O(1)$ bounded lookup (~400–600 tokens) | Essential for longitudinal scale |
| **File Count** | Fewer files | More files in `docs/decisions/` and `tasks/archive/` | Mitigated by `Index.md` and `Decisions.md` registry |

## Consequences
- **Positive:** Guarantees true $O(1)$ context token scaling across 50+ development sprints.
- **Negative / Risks:** Requires keeping `Index.md` synchronized with `docs/decisions/` shards.

## Migration & Rollback Strategy
`scripts/init-vault.sh` and `scripts/validate-vault.py` support both inline ADR sections and `docs/decisions/` atomic shards for full backward compatibility.
