---
name: adr-review
description: Review, debate, and reconcile proposed Architecture Decision Records (ADRs) against existing project decisions. Actively challenges contradictory decisions, produces a trade-off matrix, enforces superseding and migration rules, and merges accepted ADRs into the vault. Automatically triggered when conflicts are detected during memdoc updates. Also triggered by the /adr-review slash command.
---
# ADR Merge Review

Debate and stress-test proposed Architecture Decision Records (ADRs) before merging them into the project documentation vault. Protect the codebase from silent architectural drift and unvetted contradictions with past choices.

## When to Use

- Triggered via the `/adr-review` chat slash command.
- **Auto-triggered by `/memdoc`** whenever an update introduces technical changes, architecture modifications, or task decisions that conflict with previously accepted ADRs.
- Proposing or drafting a new architectural, technical, or tooling decision.
- Evaluating whether a proposed change conflicts with existing ADRs in `docs/Decisions.md` or `docs/decisions/`.
- Superseding, deprecating, or amending previous technical decisions.

---

## 3-Phase Review & Debate Process

```
[Proposed Decision]
        │
        ▼
Phase 1: Socratic Devil's Advocate (Challenge contradictions & past constraints)
        │
        ▼
Phase 2: Structured Trade-off Matrix (Side-by-side comparison of old vs. new)
        │
        ▼
Phase 3: Gatekeeper & Resolution (Verify supersedes tag, justification, migration plan)
        │
        ▼
[Draft for Confirmation] ──(Approved)──▶ [Merge into Vault & Update Index]
```

---

### Step 1: Discover & Index Existing ADRs

Before evaluating a proposal, read all existing ADR records in the vault:
- **Central Log:** Read `docs/Decisions.md` (or `.memdoc/docs/Decisions.md`).
- **Atomic Files:** Check `docs/decisions/` or `docs/adr/` if present.
- Identify decisions that share domain overlap, technology stack, data flow, or operational boundaries with the proposal.

---

### Step 2: Phase 1 — Socratic Devil's Advocate & Contradiction Debate

Actively adopt a **devil's advocate** posture representing the historical context and constraints of past decisions:

1. **Spot Contradictions:** Explicitly cite conflicting ADRs:
   - *"ADR-004 selected PostgreSQL because relational integrity was deemed non-negotiable. Your proposal introduces DynamoDB for the same service. Why has that constraint changed?"*
2. **Stress-Test Assumptions:**
   - Challenge why the past decision is considered inadequate now.
   - Question hidden costs (developer cognitive load, dual-stack maintenance, data migration).
   - Demand concrete triggers (scale, latency benchmarks, business requirements) rather than personal preference or trend-chasing.
3. **Engage the Author:** Ask direct, pointed questions one by one to uncover the true trade-off rationale.

---

### Step 3: Phase 2 — Structured Trade-off Matrix

Synthesize the debate into a side-by-side comparison matrix comparing the existing decision against the proposed direction:

```markdown
### Architectural Trade-off Matrix

| Dimension | Existing Decision ([[ADR-xxx]]) | Proposed Decision ([[ADR-yyy]]) | Trade-off Analysis & Risk |
| :--- | :--- | :--- | :--- |
| **Core Technology** | [e.g., PostgreSQL] | [e.g., DynamoDB] | Relational guarantees vs. horizontal scale |
| **Complexity & Stack** | Single database to operate | Adds NoSQL operational overhead | Increased operational surface area |
| **Performance / Scale** | Read replicas sufficient to 5k QPS | Sub-10ms latency at >50k QPS | Justified if sustained QPS > 20k |
| **Migration Cost** | \$0 (status quo) | High (dual-write & schema conversion) | Requires migration phase |
| **Reversibility** | N/A | Hard | High lock-in risk |
```

---

### Step 4: Phase 3 — Gatekeeper & Resolution Criteria

Enforce strict gatekeeping rules when an architectural proposal contradicts an accepted ADR:

1. **Explicit Justification:** Clearly document why past assumptions are no longer valid.
2. **Migration & Rollback Plan:** Every conflicting ADR (whether `Proposed` or `Accepted`) MUST include a concrete rollout and fallback plan detailing:
   - Data or code migration steps.
   - Compatibility bridge (e.g., dual-write or fallback adapter) during transition.
   - Criteria for aborting or rolling back.
3. **Default Safe Gatekeeping (`Proposed`) vs. Authorized Superseding (`Accepted`):**
   - **Without Explicit Human Override Authorization:** Record the new ADR with `Status: Proposed` (referencing the conflicting ADR via `supersedes: "[[ADR-xxx]]"`), include the full Trade-off Matrix and Migration/Rollback Plan, and **keep production code compliant with the active ADR** (or behind an opt-in adapter) until a human approves the transition.
   - **With Explicit Override Authorization:** Transition the new ADR to `Status: Accepted`, mark the replaced ADR's status as `Superseded by [[ADR-yyy]]`, and execute the migration plan.

---

### Step 5: Write Atomic ADR & Update Registry

1. **Write Atomic Shard (`docs/decisions/ADR-xxx-<slug>.md`):** Write the full ADR (including context, trade-off matrix, consequences, and migration/rollback strategy) to an atomic file in `docs/decisions/`.
2. **Update Compact Registry (`docs/Decisions.md`):** Add or update the 1-line summary row in the `docs/Decisions.md` registry table (and update any superseded ADR status).
3. **Update Central Index (`Index.md`):** Link `[[docs/decisions/ADR-xxx-<slug>|ADR-xxx: <Title>]]` under `## Architecture Decision Records (ADRs)` in `Index.md`.
4. **Audit & Validate:** Log the review outcome in `tasks/prompts-log.md` and run `python3 ./scripts/validate-vault.py` (if present) to verify link integrity.

---

## ADR Format Standard

Every ADR must follow this frontmatter and section layout:

```markdown
---
tags: [docs, adr, decisions]
status: Accepted # Proposed | Accepted | Superseded | Rejected
date: YYYY-MM-DD
supersedes: "[[ADR-001]]" # Optional
superseded_by: null # Optional
---
# ADR-002: <Decision Title>

- **Date:** YYYY-MM-DD
- **Status:** Accepted (supersedes [[ADR-001]])
- **Deciders:** <Author / Team>

## Context & Problem Statement
What context prompted this decision? What constraints or past decisions were evaluated?

## Decision & Rationale
What was decided and why? How does it resolve the problem statement?

## Debated Contradictions & Trade-offs
Summary of key tensions with previous decisions (e.g., trade-off matrix highlights).

## Consequences
- **Positive:** Benefits gained.
- **Negative / Risks:** Trade-offs accepted and potential risks.

## Migration & Rollback Strategy
Step-by-step transition plan, compatibility measures, and rollback triggers.
```

