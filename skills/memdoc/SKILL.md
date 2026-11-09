---
name: memdoc
description: Maintain an Obsidian-compatible Markdown documentation and memory vault (memdoc: memory + documentation) alongside a software development project. Use when the user mentions memdoc, runs the /memdoc slash command, tracks prompts and tasks in Obsidian, updates the project index note, or organizes project notes and Kanban boards. Automatically checks for architectural conflicts during updates and triggers adr-review when contradictions are found. Also triggered by the /memdoc slash command.
---
# Memdoc

Maintain a human-readable reference documentation and project memory vault in a dedicated folder alongside a development project, structured for Obsidian navigation and Kanban task tracking.

## When to Use

- Triggered via the `/memdoc` chat slash command.
- Initializing a memdoc documentation vault for a new or existing software project.
- Logging prompts, implementation decisions, and completed work during development.
- Updating project architecture, setup guides, or general usage documentation.
- Managing development tasks using an Obsidian Kanban board workflow.
- Updating the central index note (Map of Content) to keep all notes linked by category.

## Vault Directory Structure

Keep all documentation inside a dedicated root folder (default to `docs/obsidian/` or `.memdoc/` unless specified by the user):

```text
docs/obsidian/
├── Index.md
├── docs/
│   ├── Architecture.md
│   ├── Setup-and-Usage.md
│   ├── Decisions.md              # Compact 1-line-per-ADR registry table (O(1) lookup)
│   ├── ADR-template.md
│   └── decisions/                # Atomic ADR shards (ADR-xxx-slug.md)
│       └── ADR-001-initial-architecture.md
└── tasks/
    ├── Kanban-Board.base
    ├── prompts-log.md            # Rolling window log (max 15 recent entries)
    ├── archive/                  # Rotated historical prompt logs (YYYY-MM-prompts.md)
    └── items/
        └── YYYY-MM-DD-task-slug.md
```

## Steps

### 1. Initialize or Verify the Vault Structure

Check whether the documentation folder exists. If starting fresh, provide or generate the base files (`Index.md`, `tasks/Kanban-Board.base`, `tasks/prompts-log.md`, and core `docs/` files). You can also run the bundled bootstrap script:
```bash
./scripts/init-vault.sh [TARGET_DIR] [PROJECT_NAME]
```
Base file templates are available in the `templates/` directory.

### 2. Format Notes with Obsidian Conventions

- **YAML Frontmatter:** Start every note with YAML properties (`created`, `updated`, `tags`, `status`, `category`) so Obsidian Bases / Dataview and properties views can query them.
- **Wikilinks:** Use `[[Note-Name]]` or `[[subfolder/Note-Name|Display Title]]` for internal links instead of standard Markdown relative paths.
- **Atomic Notes:** Keep general usage and architectural documentation in `docs/`, and task/prompt execution records in `tasks/`.

### 3. Maintain the Central Index Note (`Index.md`)

Always update `Index.md` whenever a new note is created or renamed. Group links by category so the project remains navigable from a single entry point:

```markdown
---
tags: [index, moc]
updated: YYYY-MM-DD
---
# Project Memdoc Index

## General & Usage Documentation
- [[docs/Setup-and-Usage|Setup and Usage]]
- [[docs/Architecture|Architecture Overview]]
- [[docs/Decisions|Technical Decisions Registry]]

## Architecture Decision Records (ADRs)
- [[docs/decisions/ADR-001-initial-architecture|ADR-001: Initial Architecture]]

## Task Management & Prompts
- [[tasks/Kanban-Board|Kanban Task Board]]
- [[tasks/prompts-log|Prompts & Execution Log]]

## Active & Completed Task Notes
- [[tasks/items/2026-11-03-example-task|Example Task]]
```

### 4. Track Tasks and Prompts in Kanban Flow (With Rolling Log Window)

Maintain `tasks/Kanban-Board.base` using the native Obsidian Base Kanban view, where cards are driven by task frontmatter (`status`, `priority`, `epic`).

```yaml
# In tasks/Kanban-Board.base
views:
  - type: kanban
    name: Main
    filters:
      and:
        - file.hasProperty("status")
    groupBy:
      property: status
      direction: ASC
```

Task notes in `tasks/items/` automatically appear in the board based on their YAML frontmatter properties:
- **`status`**: `Epic (Vision)` | `Backlog (Ideas)` | `Up next (Pull)` | `Doing (In progress)` | `Done` | `Archive`
- **`priority`**: `🚨 Critical / Blocker` (5) | `🔥 High Priority` (4) | `⚡️ Medium Priority` (3) | `🌱 Low Priority` (2) | `🧊 Icebox` (1)
- **`epic`**: Wikilink to the feature stream or milestone (e.g., `[[Architecture]]`, `[[Auth-System]]`)
- **`type` / `category` / `tags`**: Set to `task` (`type: task`, `category: task`, `tags: [task]`)
- **`created` / `updated`**: Standard `YYYY-MM-DD` dates (feeds the `days` age formula)

When generating a task note, always populate these fields so that cards are automatically grouped into their column, sorted with high-priority items at the top, and filterable across views (`Main`, `Active Sprint`, `All Tasks`).

For each significant prompt or task, log the entry in `tasks/prompts-log.md` (keeping at most **15 recent entries** and rotating older entries to `tasks/archive/YYYY-MM-prompts.md`) or create a dedicated task note in `tasks/items/` containing:

- **Prompt Summary:** The core user request or goal.
- **Changes Made:** Files modified, added, or removed.
- **Outcome / Verification:** What was accomplished and any follow-up work needed.

### 5. Conflict Detection & Auto-Triggering ADR Review

Whenever an update introduces new technical decisions, changes architecture in `docs/`, or logs tasks that alter established technical patterns:

1. **Conflict Check:** Cross-reference the proposed change against the registry in `docs/Decisions.md` and atomic notes in `docs/decisions/`.
2. **Auto-Trigger ADR Review:** If the update contradicts, breaks, or silently reverses a previously accepted decision (e.g., swapping databases, altering auth schemes, bypassing established API conventions):
   - **Immediately pause the memdoc update.**
   - **Invoke the `adr-review` workflow** to debate the contradiction:
     1. Present the Socratic challenge highlighting the specific conflicting ADR.
     2. Generate the Trade-off Matrix comparing old vs. new choices and a Migration/Rollback Plan.
     3. **Safe Gatekeeping (`Proposed` vs `Accepted`):** Unless the user explicitly authorizes overriding the prior ADR, record the new ADR as `Status: Proposed` (keeping production code compliant with the active ADR until human sign-off). When override is explicitly authorized, transition the old ADR to `Superseded by [[ADR-xxx]]` and record the new ADR as `Accepted`.
3. **Resume Memdoc Update:** Only apply breaking architectural changes after the contradiction has been explicitly reconciled.

### 6. Deterministic Validation (`validate-vault.py`)

Before completing a memdoc operation, run the deterministic vault linter if available:
```bash
python3 ./scripts/validate-vault.py [VAULT_DIR] --fix
```
This verifies that all `docs/`, `docs/decisions/`, and `tasks/items/` notes are linked in `Index.md`, all `[[Wikilinks]]` resolve, frontmatter schemas are valid, and `prompts-log.md` stays within its 15-entry rolling window.

## Gotchas

- **Orphaned Notes:** Never create a new Markdown file in `docs/`, `docs/decisions/`, or `tasks/items/` without adding a corresponding `[[Wikilink]]` in `Index.md` (and setting its frontmatter `status` for the Kanban base).
- **$O(N)$ Monolithic Log Bloat:** Never dump unbounded full ADR essays into `docs/Decisions.md` or let `tasks/prompts-log.md` grow past 15 entries—shard full ADRs into `docs/decisions/ADR-xxx-slug.md` and archive old prompt logs into `tasks/archive/`.
- **Silent Architectural Drift:** Never silently update `docs/` or code with architecture/tooling changes that contradict past ADRs. Always auto-trigger `/adr-review` when a conflict is detected.
- **Mixing Docs and Tasks:** Keep timeless usage guides in `docs/` and chronological prompt/task history in `tasks/`. When a task introduces a permanent feature, update the relevant note in `docs/` as well as updating the task item `status: Done`.
- **Broken Wikilinks:** Match filenames and Wikilinks exactly, using kebab-case for task items and consistent casing for main documentation notes.
