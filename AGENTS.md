# Critical Memory — AI Agent Instructions

This repository maintains a structured **Critical Memory** (`memdoc`) vault to preserve architectural decisions, task history, and living documentation alongside the code.

All AI coding assistants (Claude Code, Cursor, Antigravity, GitHub Copilot, Windsurf, Aider, etc.) operating in this codebase MUST follow these instructions.

---

## 1. Vault Location & Structure

The memory vault is located at `docs/obsidian/` (or `.memdoc/`):

```text
docs/obsidian/
├── Index.md                 # Central Map of Content (MOC)
├── docs/                    # System architecture & technical decisions
│   ├── Architecture.md      # Component design and data flow
│   ├── Setup-and-Usage.md   # Developer onboarding and run instructions
│   ├── Decisions.md         # Compact ADR Registry table (O(1) lookup)
│   ├── ADR-template.md      # Template for individual atomic ADRs
│   └── decisions/           # Atomic ADR shards (ADR-xxx-slug.md)
└── tasks/                   # Tasks and execution history
    ├── Kanban-Board.base    # Obsidian Base Kanban view
    ├── prompts-log.md       # Rolling window audit trail (max 15 recent entries)
    ├── archive/             # Historical prompt log archives (YYYY-MM-prompts.md)
    └── items/               # Individual task notes (YYYY-MM-DD-slug.md)
```

---

## 2. Core Operational Rules for AI Assistants

1. **Always Update `Index.md` (Map of Content):**
   Whenever a new note is added or renamed in `docs/`, `docs/decisions/`, or `tasks/items/`, add a corresponding `[[Wikilink]]` under the appropriate heading in `Index.md`.

2. **Log Prompts & Completed Tasks (With Rolling Window Cap):**
   - Log significant user requests, modifications, and outcomes chronologically in `tasks/prompts-log.md` (keep at most 15 entries; rotate older entries to `tasks/archive/YYYY-MM-prompts.md`).
   - For distinct feature tasks, create an atomic note in `tasks/items/YYYY-MM-DD-<slug>.md` with YAML frontmatter:
     ```yaml
     ---
     status: Done # Epic (Vision) | Backlog (Ideas) | Up next (Pull) | Doing (In progress) | Done | Archive
     priority: "🔥 High Priority" # Critical (5) | High (4) | Medium (3) | Low (2) | Icebox (1)
     epic: "[[Architecture]]"
     type: task
     created: YYYY-MM-DD
     updated: YYYY-MM-DD
     ---
     ```

3. **Use Obsidian Conventions & Deterministic Validation:**
   - Use `[[Note-Name]]` or `[[subfolder/Note-Name|Display Title]]` for internal linking.
   - Use standard YAML frontmatter for properties (`updated: YYYY-MM-DD`).
   - Before completing a task, run `./scripts/validate-vault.py` (if present) to verify zero broken links, zero unindexed orphans, and valid frontmatter.

---

## 3. ADR Merge Review & Architectural Conflict Gatekeeping

When proposing new architectural choices, introducing major libraries, or altering existing system designs:

1. **Cross-Check Existing Decisions:** Read `docs/Decisions.md` (and relevant shards in `docs/decisions/`) before making structural changes.
2. **Never Silently Overwrite Past Decisions:** If a proposed change contradicts an accepted ADR:
   - **Challenge & Debate:** Flag the specific conflicting ADR and present a structured **Trade-off Matrix** comparing existing vs. proposed choices across scale, complexity, migration cost, and reversibility, plus a **Migration & Rollback Plan**.
   - **Default Safe Gatekeeping (`Proposed`):** Unless the user explicitly authorizes overriding the prior ADR, record the new ADR as `Status: Proposed` (in `docs/decisions/ADR-xxx-<slug>.md` and `docs/Decisions.md`) and keep production code compliant with the active ADR (or behind an opt-in adapter) pending human sign-off.
   - **Authorized Superseding (`Accepted`):** When overriding is explicitly authorized, mark the prior ADR's status as `Superseded by [[ADR-xxx]]` and record the new ADR as `Accepted` with `supersedes: [[ADR-xxx]]` and the migration/rollback plan.

