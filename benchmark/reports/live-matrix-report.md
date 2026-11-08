# Live Subagent Benchmark: 2x2 Evaluation Matrix

**Generated:** 2026-11-09 00:15:00  
**Harness Engine:** Antigravity Subagent Orchestrator  
**Models Evaluated:** Gemini (Native Antigravity) & Claude Code Persona

---

## Executive 2x2 Scorecard

| Model Mode | Baseline (Without Skills) | With Critical Memory | Accuracy Win | Context Token Overhead |
| :--- | :---: | :---: | :---: | :---: |
| **Gemini (Native)** | 94.3% (1800 toks) | **100.0%** (714 toks) | **`+5.7%`** | **`-60.3%` tokens** |
| **Claude Persona** | 94.3% (1847 toks) | **100.0%** (676 toks) | **`+5.7%`** | **`-63.4%` tokens** |

---

## Scenario Breakdown

### Scenario: `adr_contradiction`

| Matrix Cell | Overall Score | Architecture | Traceability | Tasks | Freshness | SNR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Gemini Baseline (No Skills) | **82.8%** | 31.2% | 100.0% | 100.0% | 100.0% | 22.0% clean |
| Gemini With Critical Memory | **100.0%** | 100.0% | 100.0% | 100.0% | 100.0% | 89.3% clean |
| Claude Persona Baseline (No Skills) | **82.8%** | 31.2% | 100.0% | 100.0% | 100.0% | 22.0% clean |
| Claude Persona With Critical Memory | **100.0%** | 100.0% | 100.0% | 100.0% | 100.0% | 89.3% clean |

### Scenario: `context_retrieval`

| Matrix Cell | Overall Score | Architecture | Traceability | Tasks | Freshness | SNR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Gemini Baseline (No Skills) | **100.0%** | 100.0% | 100.0% | 100.0% | 100.0% | 22.0% clean |
| Gemini With Critical Memory | **100.0%** | 100.0% | 100.0% | 100.0% | 100.0% | 89.3% clean |
| Claude Persona Baseline (No Skills) | **100.0%** | 100.0% | 100.0% | 100.0% | 100.0% | 22.0% clean |
| Claude Persona With Critical Memory | **100.0%** | 100.0% | 100.0% | 100.0% | 100.0% | 89.4% clean |

### Scenario: `task_lifecycle`

| Matrix Cell | Overall Score | Architecture | Traceability | Tasks | Freshness | SNR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Gemini Baseline (No Skills) | **100.0%** | 100.0% | 100.0% | 100.0% | 100.0% | 22.0% clean |
| Gemini With Critical Memory | **100.0%** | 100.0% | 100.0% | 100.0% | 100.0% | 89.3% clean |
| Claude Persona Baseline (No Skills) | **100.0%** | 100.0% | 100.0% | 100.0% | 100.0% | 22.0% clean |
| Claude Persona With Critical Memory | **100.0%** | 100.0% | 100.0% | 100.0% | 100.0% | 89.3% clean |
