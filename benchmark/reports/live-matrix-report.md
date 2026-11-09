# Live Subagent Benchmark: 2x2 Evaluation Matrix

**Generated:** 2026-11-09 09:02:21  
**Harness Engine:** Antigravity Subagent Orchestrator  
**Models Evaluated:** Gemini (Native Antigravity) & Claude Code Persona

---

## Executive 2x2 Scorecard

| Model Mode | Baseline (Without Skills) | With Critical Memory | Accuracy Win | Context Token Overhead |
| :--- | :---: | :---: | :---: | :---: |
| **Gemini (Native)** | 66.7% (2159 toks) | **100.0%** (1406 toks) | **`+33.3%`** | **`-34.9%` tokens** |
| **Claude Persona** | 66.7% (2159 toks) | **100.0%** (1671 toks) | **`+33.3%`** | **`-22.6%` tokens** |

---

## Scenario Breakdown

### Scenario: `adr_contradiction`

| Matrix Cell | Overall Score | Architecture | Traceability | Tasks | Freshness | SNR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Gemini Baseline (No Skills) | **57.6%** | 12.5% | 100.0% | 55.6% | 62.5% | 28.0% clean |
| Gemini With Critical Memory | **100.0%** | 100.0% | 100.0% | 100.0% | 100.0% | 92.7% clean |
| Claude Persona Baseline (No Skills) | **57.6%** | 12.5% | 100.0% | 55.6% | 62.5% | 28.0% clean |
| Claude Persona With Critical Memory | **100.0%** | 100.0% | 100.0% | 100.0% | 100.0% | 92.7% clean |

### Scenario: `context_retrieval`

| Matrix Cell | Overall Score | Architecture | Traceability | Tasks | Freshness | SNR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Gemini Baseline (No Skills) | **73.3%** | 100.0% | 75.0% | 55.6% | 62.5% | 28.0% clean |
| Gemini With Critical Memory | **100.0%** | 100.0% | 100.0% | 100.0% | 100.0% | 92.9% clean |
| Claude Persona Baseline (No Skills) | **73.3%** | 100.0% | 75.0% | 55.6% | 62.5% | 28.0% clean |
| Claude Persona With Critical Memory | **100.0%** | 100.0% | 100.0% | 100.0% | 100.0% | 92.9% clean |

### Scenario: `task_lifecycle`

| Matrix Cell | Overall Score | Architecture | Traceability | Tasks | Freshness | SNR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Gemini Baseline (No Skills) | **69.3%** | 100.0% | 100.0% | 35.7% | 41.7% | 28.0% clean |
| Gemini With Critical Memory | **100.0%** | 100.0% | 100.0% | 100.0% | 100.0% | 92.7% clean |
| Claude Persona Baseline (No Skills) | **69.3%** | 100.0% | 100.0% | 35.7% | 41.7% | 28.0% clean |
| Claude Persona With Critical Memory | **100.0%** | 100.0% | 100.0% | 100.0% | 100.0% | 92.7% clean |
