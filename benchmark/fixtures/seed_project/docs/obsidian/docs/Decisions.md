---
tags: [docs, adr, decisions]
updated: 2026-11-03
---
# Architectural & Technical Decisions (ADR Log)

A chronological record of significant architectural, technical, and tool choices made during project development. Use `/adr-review` to debate proposed decisions against this log.

---

## ADR-001: Initial Architecture and Foundation
- **Date:** 2026-11-01
- **Status:** Accepted
- **Context:** Initial bootstrapping of the project.
- **Decision:** Modular monolith architecture with Python backend.
- **Consequences:** Simple deployment, single codebase.

---

## ADR-002: PostgreSQL as Primary Database
- **Date:** 2026-11-02
- **Status:** Superseded by [[ADR-003]]
- **Context:** Financial and cart data requires strict ACID compliance and relational integrity. NoSQL solutions were rejected due to eventual consistency concerns.
- **Decision:** Mandate PostgreSQL for all persistence needs.
- **Consequences:** Relational schema rigor, foreign keys enforced, vertical scalability.

---

## ADR-003: Adopt SQLite for Zero-Overhead Embedded Storage
- **Date:** 2026-11-03
- **Status:** Accepted (supersedes [[ADR-002]])
- **Context:** PostgreSQL added unnecessary server daemon, port, and credential overhead for test sandboxes and local development.
- **Decision:** Migrate primary storage to SQLite using Python standard library `sqlite3`.
- **Consequences:** Zero-overhead embedded persistence; simplified local runs; write concurrency limited to single-file locks.
