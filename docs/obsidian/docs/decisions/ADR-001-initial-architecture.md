---
tags: [docs, adr, decisions]
status: Accepted
date: 2026-11-09
supersedes: null
superseded_by: null
---
# ADR-001: Initial Architecture and Foundation

- **Date:** 2026-11-09
- **Status:** Accepted
- **Deciders:** Engineering Team

## Context & Problem Statement
Initial bootstrapping of `Critical-Memory`. We need a clean baseline architecture and living documentation vault (`docs/obsidian/`) that scales without context bloat.

## Decision & Rationale
Establish the core project layout alongside a **Critical Memory** vault using atomic ADR sharding (`docs/decisions/`) and a central Map of Content (`Index.md`).

## Debated Contradictions & Trade-offs
- **Monolithic ADR file vs. Compact Registry + Atomic Shards:** Single-file logs grow $O(N)$ over time. Using a compact registry table in `docs/Decisions.md` plus atomic files in `docs/decisions/` keeps discovery $O(1)$.

## Consequences
- **Positive:** Fast $O(1)$ context lookup, explicit decision history, zero silent architectural drift.
- **Negative / Risks:** Requires maintaining links in `Index.md` and `Decisions.md` (enforced via `./scripts/validate-vault.py`).

## Migration & Rollback Strategy
Baseline initialization; no prior system migration required.
