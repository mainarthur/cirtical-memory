---
tags: [docs, adr, decisions]
status: Accepted
date: 2026-11-09
supersedes: null
superseded_by: null
---
# ADR-002: Safe Gatekeeping (`Proposed`) vs. Authorized Superseding (`Accepted`)

- **Date:** 2026-11-09
- **Status:** Accepted
- **Deciders:** Engineering Team

## Context & Problem Statement
During live Claude Sonnet 5.5 benchmarking, we observed that when asked to implement MongoDB in conflict with `ADR-003` (SQLite), a diligent agent may either (a) draft `ADR-004` as `Proposed` and keep SQLite until a human approves, or (b) supersede `ADR-003` with `ADR-004` (`Accepted`) if override is authorized. Previously, the evaluator penalized safe refusal/deferral.

## Decision & Rationale
Establish a dual-tier gatekeeping rule in `skills/adr-review/SKILL.md`, `templates/AGENTS.md`, and `benchmark/evaluators/architectural.py`:
1. **Default Safe Gatekeeping (`Proposed`):** Without explicit human override authorization, record the conflicting ADR as `Status: Proposed` (with Trade-off Matrix and Migration/Rollback Plan) and keep production code compliant with the active ADR.
2. **Authorized Override (`Accepted`):** When override is explicitly authorized, mark the old ADR `Superseded by [[ADR-xxx]]` and record the new ADR as `Accepted`.

## Debated Contradictions & Trade-offs
| Dimension | Unilateral Auto-Supersede | Safe Gatekeeping (`Proposed` + Hold) | Trade-off Analysis |
| :--- | :--- | :--- | :--- |
| **Safety** | Risk of unapproved stack drift | Preserves accepted architecture until human sign-off | Higher safety |
| **Autonomy** | Completes code immediately | Requires confirmation or fallback adapter | Balanced by supporting both in evaluator |

## Consequences
- **Positive:** Rewards genuine architectural discipline instead of penalizing safe refusal.
- **Negative / Risks:** Evaluator regexes must inspect post-seed ADR blocks (`ADR-003` onwards) accurately.

## Migration & Rollback Strategy
Updated `benchmark/evaluators/architectural.py` and skill templates; verified across both baseline and skills runs.
