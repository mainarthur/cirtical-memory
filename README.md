# Memdoc Skill for Antigravity

[![Antigravity Skill](https://img.shields.io/badge/Antigravity-Customization-blue)](https://antigravity.google)
[![Format](https://img.shields.io/badge/Obsidian-Compatible-purple)](https://obsidian.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An agentic skill and plugin for **Google Antigravity (AGY)** that maintains a human-readable, bi-directionally linked Markdown documentation and project memory vault (**memdoc** = memory + documentation) alongside your software projects. Structured for seamless browsing in [Obsidian](https://obsidian.md) and task tracking via Obsidian Kanban boards.

---

## Features

- **Map of Content (`Index.md`):** Keeps an updated central hub linking all architectural notes, setup guides, and task logs.
- **Visual Kanban Board (`tasks/Kanban-Board.base`):** Configured as an [Obsidian Base](https://help.obsidian.md) with a native Kanban view, grouping cards by `status` (Epic, Backlog, Up next, Doing, Done, Archive) and sorting by priority.
- **Chronological Prompt & Execution Log (`tasks/prompts-log.md`):** Preserves an audit trail of agent interactions, decisions, and diff summaries.
- **ADR Merge Review & Contradiction Debate (`/adr-review`):** 3-phase pre-merge review that challenges contradictory decisions with devil's advocate debate, generates a trade-off matrix, and enforces superseding/migration rules.
- **Wikilinks & Atomic Notes:** Uses `[[Wikilink]]` internal navigation and YAML frontmatter properties for Obsidian Dataview / Bases compatibility.
- **Automatic Antigravity Discovery:** Works either globally across all Antigravity workspaces or scoped to individual projects.

---

## Vault Directory Layout

By default, the vault is maintained in `docs/obsidian/` or `.memdoc/`:

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

This repository is configured as a global Antigravity plugin under `~/.gemini/config/plugins/memdoc/`.

To verify or install on any machine:
```bash
# Symlink or clone into your global Antigravity plugins directory:
ln -s /path/to/obsidian-skill ~/.gemini/config/plugins/memdoc
```

Antigravity automatically discovers the plugin and loads the `memdoc` skill across every project you open.

### 2. Workspace Installation (Project-Specific)

To vendor or check the skill into a specific project repository:

```bash
# In your target project root:
mkdir -p .agents/skills/memdoc
cp /path/to/obsidian-skill/SKILL.md .agents/skills/memdoc/
```

Or add as a Git submodule:
```bash
git submodule add https://github.com/mainarthur/obsidian-skill.git .agents/skills/memdoc
```

---

## Triggering Skills in Antigravity

This plugin provides two complementary skills:

### 1. `/memdoc` — Vault & Task Management
- **Chat Slash Command:** Type `/memdoc` directly in the chat.
- **Natural Language:** Activates when you ask to initialize a vault, update the Kanban board, or log prompts and progress.
- **Architectural Conflict Check:** Automatically checks for contradictions with existing ADRs whenever architectural notes or task decisions are updated, auto-triggering `/adr-review` if a conflict is detected.

### 2. `/adr-review` — ADR Merge Review & Debate
- **Chat Slash Command:** Type `/adr-review` directly in the chat.
- **Auto-Triggered:** Automatically launches during `/memdoc` updates when an incoming change contradicts previously accepted ADRs.
- **Natural Language:** Activates when you propose a new architectural decision, evaluate conflicting trade-offs, or ask to review an ADR against historical choices.
- **Review Workflow:**
  1. **Devil's Advocate:** Socratic questioning on why past constraints are no longer binding.
  2. **Trade-off Matrix:** Side-by-side comparison table of old vs. new decisions across scale, complexity, and risk.
  3. **Gatekeeping:** Enforces explicit justification, `Superseded by [[ADR-xxx]]` status transition, and a migration/rollback strategy before drafting the merge diff for confirmation.

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
