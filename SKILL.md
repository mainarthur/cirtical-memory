---
name: obsidian-memory
description: Maintain an Obsidian-compatible Markdown documentation vault alongside a software development project. Use when the user mentions Obsidian memory, project documentation vault, tracking prompts and tasks in Obsidian, updating the project index note, or organizing project notes and Kanban boards.
---
# Obsidian Memory

Maintain a human-readable reference documentation vault in a dedicated folder alongside a development project, structured for Obsidian navigation and Kanban task tracking.

## When to Use

- Initializing a documentation vault for a new or existing software project.
- Logging prompts, implementation decisions, and completed work during development.
- Updating project architecture, setup guides, or general usage documentation.
- Managing development tasks using an Obsidian Kanban board workflow.
- Updating the central index note (Map of Content) to keep all notes linked by category.

## Vault Directory Structure

Keep all documentation inside a dedicated root folder (default to `docs/obsidian/` or `.obsidian-memory/` unless specified by the user):

```text
obsidian-memory/
├── Index.md
├── docs/
│   ├── Architecture.md
│   ├── Setup-and-Usage.md
│   └── Decisions.md
└── tasks/
    ├── Kanban-Board.base
    ├── prompts-log.md
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
# Project Memory Index

## General & Usage Documentation
- [[docs/Setup-and-Usage|Setup and Usage]]
- [[docs/Architecture|Architecture Overview]]
- [[docs/Decisions|Technical Decisions]]

## Task Management & Prompts
- [[tasks/Kanban-Board|Kanban Task Board]]
- [[tasks/prompts-log|Prompts & Execution Log]]

## Active & Completed Task Notes
- [[tasks/items/2026-11-03-example-task|Example Task]]
```

### 4. Track Tasks and Prompts in Kanban Flow

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

For each significant prompt or task, log the entry in `tasks/prompts-log.md` or create a dedicated task note in `tasks/items/` containing:

- **Prompt Summary:** The core user request or goal.
- **Changes Made:** Files modified, added, or removed.
- **Outcome / Verification:** What was accomplished and any follow-up work needed.

## Gotchas

- **Orphaned Notes:** Never create a new Markdown file in `docs/` or `tasks/items/` without adding a corresponding `[[Wikilink]]` in `Index.md` (and setting its frontmatter `status` for the Kanban base).
- **Mixing Docs and Tasks:** Keep timeless usage guides in `docs/` and chronological prompt/task history in `tasks/`. When a task introduces a permanent feature, update the relevant note in `docs/` as well as updating the task item `status: Done`.
- **Broken Wikilinks:** Match filenames and Wikilinks exactly, using kebab-case for task items and consistent casing for main documentation notes.
