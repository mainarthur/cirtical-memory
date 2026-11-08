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
│   ├── Decisions.md         # Architecture Decision Records (ADRs)
│   └── ADR-template.md      # Template for individual atomic ADRs
└── tasks/                   # Tasks and execution history
    ├── Kanban-Board.base    # Obsidian Base Kanban view
    ├── prompts-log.md       # Audit trail of AI prompts and changes
    └── items/               # Individual task notes (YYYY-MM-DD-slug.md)
```

---

## 2. Core Operational Rules for AI Assistants

1. **Always Update `Index.md` (Map of Content):**
   Whenever a new note is added or renamed in `docs/` or `tasks/items/`, add a corresponding `[[Wikilink]]` under the appropriate heading in `Index.md`.

2. **Log Prompts & Completed Tasks:**
   - Log significant user requests, modifications, and outcomes chronologically in `tasks/prompts-log.md`.
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

3. **Use Obsidian Conventions:**
   - Use `[[Note-Name]]` or `[[subfolder/Note-Name|Display Title]]` for internal linking.
   - Use standard YAML frontmatter for properties.

---

## 3. ADR Merge Review & Architectural Conflict Gatekeeping

When proposing new architectural choices, introducing major libraries, or altering existing system designs:

1. **Cross-Check Existing Decisions:** Read `docs/Decisions.md` (and `docs/decisions/` if present) before making structural changes.
2. **Never Silently Overwrite Past Decisions:** If a proposed change contradicts an accepted ADR:
   - **Pause and flag the contradiction** to the user.
   - **Present a Trade-off Matrix:** Compare the existing decision with the proposed direction across performance, complexity, migration cost, and operational risks.
   - **Enforce Superseding:** If accepted, update the previous ADR's status to `Superseded by [[ADR-xxx]]`, and record the new ADR with `supersedes: [[ADR-xxx]]` and a concrete migration/rollback plan.
