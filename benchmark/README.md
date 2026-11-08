# Critical Memory Benchmark Suite

An automated evaluation harness to measure and contrast AI coding agent performance **With Critical Memory (`memdoc` + `adr-review`)** versus **Baseline (Without Skills / Vanilla)**.

---

## 4 Evaluation Dimensions

Every scenario is graded across 4 quantitative dimensions (0–100%):

1. **Architectural Consistency & ADR Gatekeeping:** Resistance to silent architectural drift, detection and debate of contradictory choices, and adherence to formal `Superseded by` status transitions and migration plans.
2. **Traceability & MOC Hygiene:** Centralization of all project notes in `Index.md`, valid `[[Wikilink]]` syntax, and complete absence of unindexed or orphaned notes.
3. **Task & Kanban Hygiene:** Proper audit trail in `tasks/prompts-log.md`, valid YAML frontmatter (`status`, `priority`), and correct Kanban card state transitions.
4. **Documentation Freshness:** Synchronization of living system documentation (`docs/Architecture.md`, `Setup-and-Usage.md`) with code modifications.

---

## Benchmark Scenarios

| Scenario ID | Title | Description |
| :--- | :--- | :--- |
| `adr_contradiction` | **ADR Contradiction Attack** | Agent is tasked to introduce MongoDB into an application whose `ADR-003` mandated SQLite. Measures whether contradiction is detected and formally superseded vs silently drifted. |
| `context_retrieval` | **Context Retrieval & Onboarding** | Agent is tasked to query and expand system authentication architecture. Measures whether knowledge is centralized in `Index.md` vs left as an unindexed orphan note. |
| `task_lifecycle` | **Task State Progression** | Agent completes an in-progress feature. Measures whether task card frontmatter is progressed (`status: Done`), audit logged, and synced with architecture docs. |
| `continual_growth` | **Continual Growth (High-Load)** | Longitudinal multi-sprint simulation (50 cycles, ~200 tasks, 12 conflict injections) evaluating compounding architectural drift, context decay curves, and task hygiene over time. |

---

## Running the Benchmark

### 1. Run All Standard Scenarios (Default)
```bash
./benchmark/run.sh
```

### 2. Run Continual Growth High-Load Stress Test (50 Sprints)
```bash
./benchmark/run.sh --scenario continual_growth --sprints 50
```

### 3. Run Live Subagent 2x2 Matrix (Gemini & Claude Persona)
```bash
# Run full 2x2 evaluation across all standard scenarios:
./benchmark/run.sh --live-agent

# Run specific model persona (e.g., Gemini or Claude):
./benchmark/run.sh --live-agent --models gemini
./benchmark/run.sh --live-agent --models claude

# Scaffold isolated sandboxes and manifest without executing (dry run):
./benchmark/run.sh --live-agent --dry-run
```

### 4. Run a Specific Scenario
```bash
./benchmark/run.sh --scenario adr_contradiction
./benchmark/run.sh --scenario context_retrieval
./benchmark/run.sh --scenario task_lifecycle
```

### 5. Custom Output Directory and Formats
```bash
./benchmark/run.sh --output-dir custom_reports/ --format both
```

Outputs generated:
- `benchmark/reports/benchmark-report.md`: GitHub-flavored Markdown report with executive summary, comparative scorecard, and check highlights.
- `benchmark/reports/live-matrix-report.md`: 2x2 comparative evaluation scorecard across Gemini and Claude persona modes.
- `benchmark/reports/continual-growth-report.md`: 50-sprint longitudinal scalability analysis and degradation curves.
- `benchmark/reports/context-pollution-analysis.md`: Detailed Context Pollution (Usage vs. Win), Signal-to-Noise Ratio (SNR), and token economics report.
- `benchmark/reports/results.json`, `growth_results.json` & `live_matrix_results.json`: Machine-readable structured benchmark results.

---

## Directory Structure

```text
benchmark/
├── README.md               # Benchmark documentation
├── run.sh                  # One-command executable wrapper
├── runner.py               # Main CLI benchmark driver
├── evaluators/             # 4-dimension metric evaluators
│   ├── architectural.py    # Dimension 1: ADR gatekeeping & drift check
│   ├── traceability.py     # Dimension 2: Index.md & orphaned notes
│   ├── task_hygiene.py     # Dimension 3: Kanban & prompts-log
│   └── freshness.py        # Dimension 4: Doc synchronization
├── fixtures/               # Test fixtures & seed projects
│   └── seed_project/       # Seed repo with SQLite db, auth, and vault
├── scenarios/              # Evaluation scenarios
│   ├── adr_contradiction.py
│   ├── context_retrieval.py
│   └── task_lifecycle.py
└── reports/                # Generated reports
    ├── benchmark-report.md
    └── results.json
```

