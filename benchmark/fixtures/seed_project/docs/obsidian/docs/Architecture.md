---
tags: [docs, architecture]
updated: 2026-11-03
---
# Architecture Overview

This document describes the high-level architecture of SampleApp.

## Components
- **API Server:** Fast, stateless API handling client requests.
- **Data Layer:** SQLite embedded storage according to [[docs/Decisions|ADR-003]] (superseding [[docs/Decisions|ADR-002]]).
- **Auth Service:** Bearer token authentication with OAuth2 callback flow.
