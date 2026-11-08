# Critical Memory

[![GenAI Agnostic](https://img.shields.io/badge/GenAI-Agnostic-orange)](https://github.com/mainarthur/cirtical-memory)
[![Obsidian Compatible](https://img.shields.io/badge/Obsidian-Compatible-purple)](https://obsidian.md)
[![Agents: Claude | Cursor | Antigravity | Copilot](https://img.shields.io/badge/Agents-Claude%20%7C%20Cursor%20%7C%20AGY%20%7C%20Copilot-blue)](https://github.com/mainarthur/cirtical-memory)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Critical Memory** is a **GenAI-agnostic** project memory and documentation system designed for AI coding assistants and developers. It establishes a human-readable, bi-directionally linked Markdown vault alongside software projects, structured for native browsing in [Obsidian](https://obsidian.md) and task tracking via Obsidian Kanban boards.

Whether you use **Claude Code**, **Cursor**, **Google Antigravity (AGY)**, **GitHub Copilot**, **Windsurf**, or **Aider**, Critical Memory ensures that AI assistants never lose context, silently break architectural decisions, or leave unlinked notes.

---

## Two Core Capabilities

Critical Memory bundles two specialized skills:

1. **`memdoc` (Memory + Documentation):**
   - **Central Map of Content (`Index.md`):** Keeps all architectural documentation, guides, and task histories discoverable from a single hub.
   - **Visual Kanban Board (`tasks/Kanban-Board.base`):** Configured as an [Obsidian Base](https://help.obsidian.md) with a native Kanban view, grouping cards by `status` (Epic, Backlog, Up next, Doing, Done, Archive) and sorting by priority.
   - **Audit Trail (`tasks/prompts-log.md`):** Chronological log of AI agent prompts, changes, and implementation milestones.
   - **Atomic Notes & Wikilinks:** Standard `[[Wikilink]]` navigation with YAML properties for Dataview and Bases queries.

2. **`adr-review` (ADR Merge Review & Contradiction Debate):**
   - **Phase 1 (Devil's Advocate):** Socratic challenge questioning why historical constraints and assumptions are no longer binding.
   - **Phase 2 (Trade-off Matrix):** Side-by-side comparison table contrasting past vs. proposed decisions across scale, complexity, operational cost, and reversibility.
   - **Phase 3 (Gatekeeping & Superseding):** Enforces explicit justification, `Superseded by [[ADR-xxx]]` status transitions, and a documented migration/rollback strategy.
   - **Automatic Trigger:** Automatically pauses updates during `memdoc` operations if a proposed change contradicts an accepted ADR.

---

## Vault Directory Layout

By default, the vault is maintained in `docs/obsidian/` or `.memdoc/`:

```text
docs/obsidian/
├── Index.md                 # Central Map of Content (MOC)
├── AGENTS.md                # Universal AI agent instructions
├── docs/                    # Living system documentation
│   ├── Architecture.md      # System design, data flow, component layout
│   ├── Setup-and-Usage.md   # Developer onboarding and run instructions
│   ├── Decisions.md         # Architecture Decision Records (ADRs log)
│   └── ADR-template.md      # Template for individual atomic ADR notes
└── tasks/                   # Tasks and chronological prompt execution
    ├── Kanban-Board.base    # Obsidian Base Kanban view
    ├── prompts-log.md       # Audit trail of AI agent prompts and changes
    └── items/               # Individual atomic task notes
        └── YYYY-MM-DD-slug.md
```

---

## Quickstart (Any Project)

Bootstrap a fresh Critical Memory vault in seconds:

```bash
# In your target project root:
/path/to/critical-memory/scripts/init-vault.sh [TARGET_DIR] [PROJECT_NAME]

# Example:
./scripts/init-vault.sh docs/obsidian MyApp
```

This creates the full directory structure, seed notes, Kanban board, and a root `AGENTS.md` file.

---

## Benchmark Results: Value Delivered vs. Token Cost (ROI)

Critical Memory includes an automated evaluation harness in [`benchmark/`](benchmark/) to measure agent performance across both isolated single tasks and longitudinal 50-sprint high-load scaling.

### 1. Single-Task Evaluation (Value vs. Token Overhead)

A common concern with agent memory systems is token cost. The benchmark shows that **Critical Memory reduces context token consumption by 71%–91%** while delivering superior task accuracy:

| Scenario | Baseline (Without Skills) | With Critical Memory | Accuracy Win | Token Reduction | Signal-to-Noise Ratio (SNR) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **ADR Contradiction Attack** | 71.7% (`1,800` toks, 78% noise) | **100.0%** (`524` toks, 11% noise) | **`+28.3%`** | **`-71%` tokens** | `89.3%` clean signal |
| **Context Retrieval & Onboarding** | 82.7% (`1,800` toks, 78% noise) | **100.0%** (`174` toks, 10% noise) | **`+17.3%`** | **`-90%` tokens** | `89.7%` clean signal |
| **Task State & Kanban Progression** | 83.9% (`1,800` toks, 78% noise) | **100.0%** (`165` toks, 10% noise) | **`+16.1%`** | **`-91%` tokens** | `89.7%` clean signal |
| **OVERALL COMPOSITE** | 79.4% (`1,800` toks) | **100.0%** (`288` avg toks) | **`+20.6%`** | **`-84.0%` tokens** | **`+67.5%` higher SNR** |

---

### 2. High-Load Scaling (50-Sprint Longitudinal Simulation)

Stress-tested across 50 development sprints processing ~200 tasks and 12 conflicting architectural injections:

| Scale Metric | Baseline (Without Skills) | With Critical Memory | Longitudinal Advantage |
| :--- | :---: | :---: | :---: |
| **Final System Health** | 33.3% (collapsing) | **100.0% (healthy)** | **`+66.7%` system health** |
| **Historical Context Recall** | 65.5% (decaying) | **100.0% (constant)** | **`+34.5%` context retention** |
| **Cumulative Architectural Drift** | 100.0% (12/12 unvetted) | **0.0% (all vetted & superseded)** | **`100%` drift prevention** |
| **Stale Task Leakage** | 50.0% (100 unclosed tasks) | **0.0% (all closed in Done)** | **`0` leaked tasks** |
| **Context Pollution (Sprint 50)** | `93.8%` noise (5,650 toks) | **`14.8%` noise (610 toks)** | **`89.2%` token savings** |

---

### 3. Economic ROI: Cost of Maintaining Memory vs. Cost of Noise

Without structured memory, agents must greedily scan raw files, logs, and commit histories, filling 78%–94% of the context window with useless noise. By using the `Index.md` Map of Content to retrieve targeted atomic notes ($O(1)$ discovery), Critical Memory achieves:

- **Per 1,000 Developer Prompts:**
  - **Baseline:** Consumes **~5,200,000 tokens** (mostly noise, resulting in 12 unvetted architectural drift events).
  - **With Critical Memory:** Consumes **~550,000 tokens** (**89.4% token cost reduction**, zero architectural drift).

To run the benchmark suite locally:
```bash
# Run all standard scenarios:
./benchmark/run.sh

# Run live subagent 2x2 matrix (Gemini & Claude personas):
./benchmark/run.sh --matrix

# Run 50-sprint longitudinal stress test:
./benchmark/run.sh --scenario continual_growth --sprints 50
```

Detailed reports:
- [Full Benchmark Report](benchmark/reports/benchmark-report.md)
- [Live Subagent 2x2 Matrix Report](benchmark/reports/live-matrix-report.md)
- [Continual Growth Scalability Report](benchmark/reports/continual-growth-report.md)
- [Context Pollution & Token ROI Analysis](benchmark/reports/context-pollution-analysis.md)

---

## Setup for Your AI Assistant

Critical Memory works out of the box with any modern coding agent:

### 1. Universal Standard (`AGENTS.md`)
The repository includes a universal [`templates/AGENTS.md`](templates/AGENTS.md). Placing `AGENTS.md` at your repository root instructs any compliant agent (Cursor, Claude, Copilot, Codex, Aider) on how to navigate the vault, maintain `Index.md`, and observe ADR conflict reviews.

### 2. Claude Code
Copy or reference the Claude instructions in your project's `CLAUDE.md`:
```bash
cp /path/to/critical-memory/templates/integrations/CLAUDE.md ./CLAUDE.md
```
Or vendor the skills into `.claude/skills/`.

### 3. Cursor
Add the preconfigured rules to your workspace:
```bash
cp /path/to/critical-memory/templates/integrations/.cursorrules ./.cursorrules
# Or for modern Cursor rules:
mkdir -p .cursor/rules && cp /path/to/critical-memory/templates/integrations/.cursorrules .cursor/rules/critical-memory.mdc
```

### 4. GitHub Copilot
Add instructions to `.github/copilot-instructions.md`:
```bash
mkdir -p .github && cp /path/to/critical-memory/templates/integrations/copilot-instructions.md .github/copilot-instructions.md
```

### 5. Google Antigravity (AGY)
Install globally as a plugin:
```bash
ln -s /path/to/critical-memory ~/.gemini/config/plugins/critical-memory
```
This enables native slash commands in the Antigravity chat:
- **`/memdoc`**: Initialize vault, update index, manage tasks.
- **`/adr-review`**: Debate and review proposed architectural decisions.

---

## Recommended Obsidian Configuration

When opening `docs/obsidian/` (or your vault folder) in Obsidian:

1. **Obsidian Bases:** Native support for `.base` files renders `tasks/Kanban-Board.base` directly into an interactive Kanban board grouped by status with priority sorting.
2. **[Dataview](https://github.com/blacksmithgu/obsidian-dataview):** Allows querying notes by YAML properties (`status`, `priority`, `epic`, `tags`, `updated`).
3. **Internal Link Format:** In Obsidian settings (*Files & Links*), set *Default location for new attachments* to a subfolder (e.g. `assets/`) and toggle *Use [[Wikilinks]]* to **ON**.

---

## License

MIT
