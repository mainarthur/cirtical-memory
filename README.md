# Obsidian Memory Skill for Antigravity

[![Antigravity Skill](https://img.shields.io/badge/Antigravity-Customization-blue)](https://antigravity.google)
[![Format](https://img.shields.io/badge/Obsidian-Compatible-purple)](https://obsidian.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An agentic skill and plugin for **Google Antigravity (AGY)** that maintains a human-readable, bi-directionally linked Markdown documentation vault alongside your software projects. Structured for seamless browsing in [Obsidian](https://obsidian.md) and task tracking via Obsidian Kanban boards.

---

## Features

- **Map of Content (`Index.md`):** Keeps an updated central hub linking all architectural notes, setup guides, and task logs.
- **Visual Kanban Board (`tasks/Kanban-Board.base`):** Configured as an [Obsidian Base](https://help.obsidian.md) with a native Kanban view, grouping cards by `status` (Epic, Backlog, Up next, Doing, Done, Archive) and sorting by priority.
- **Chronological Prompt & Execution Log (`tasks/prompts-log.md`):** Preserves an audit trail of agent interactions, decisions, and diff summaries.
- **Wikilinks & Atomic Notes:** Uses `[[Wikilink]]` internal navigation and YAML frontmatter properties for Obsidian Dataview / Bases compatibility.
- **Automatic Antigravity Discovery:** Works either globally across all Antigravity workspaces or scoped to individual projects.

---

## Vault Directory Layout

By default, the vault is maintained in `docs/obsidian/` or `.obsidian-memory/`:

```text
docs/obsidian/
├── Index.md                 # Central Map of Content (MOC)
├── docs/                    # Living system documentation
│   ├── Architecture.md      # System design, data flow, component layout
│   ├── Setup-and-Usage.md   # Developer onboarding and run instructions
│   └── Decisions.md         # Architecture Decision Records (ADRs)
└── tasks/                   # Tasks and chronological prompt execution
    ├── Kanban-Board.base    # Obsidian Base Kanban view
    ├── prompts-log.md       # Audit trail of AI agent prompts and changes
    └── items/               # Individual atomic task notes
        └── YYYY-MM-DD-slug.md
```

---

## How to Use in Antigravity

### 1. Global Installation (All Projects)

This repository is already configured as a global Antigravity plugin under `~/.gemini/config/plugins/obsidian-memory/`.

To verify or install on any machine:
```bash
# Symlink or clone into your global Antigravity plugins directory:
ln -s /path/to/obsidian-skill ~/.gemini/config/plugins/obsidian-memory
```

Antigravity automatically discovers the plugin and loads the `obsidian-memory` skill across every project you open.

### 2. Workspace Installation (Project-Specific)

To vendor or check the skill into a specific project repository:

```bash
# In your target project root:
mkdir -p .agents/skills/obsidian-memory
cp /path/to/obsidian-skill/SKILL.md .agents/skills/obsidian-memory/
```

Or add as a Git submodule:
```bash
git submodule add https://github.com/mainarthur/obsidian-skill.git .agents/skills/obsidian-memory
```

---

## Triggering the Skill in Antigravity

The agent automatically activates this skill whenever you mention:
- *"Initialize an Obsidian memory vault for this project"*
- *"Log this prompt and changes to Obsidian"*
- *"Update the project index and Kanban board"*
- *"Document this architectural decision in my Obsidian vault"*

You can also run the bundled bootstrap script to initialize a new vault in seconds:
```bash
./scripts/init-vault.sh [TARGET_DIR] [PROJECT_NAME]
```

---

## Recommended Obsidian Configuration

When opening the documentation directory as an Obsidian vault:
1. **Obsidian Bases:** Native support for `.base` files renders `tasks/Kanban-Board.base` directly into an interactive Kanban board grouped by status with priority sorting.
2. **[Dataview](https://github.com/blacksmithgu/obsidian-dataview):** Allows querying notes by YAML properties (`status`, `priority`, `epic`, `tags`, `updated`).
3. **Internal Link Format:** In Obsidian settings, set *Default location for new attachments* to a subfolder (e.g. `assets/`) and *Use [[Wikilinks]]* to **ON**.

---

## License

MIT

