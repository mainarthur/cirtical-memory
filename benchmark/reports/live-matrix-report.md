# Live Subagent Benchmark: 2x2 Evaluation Matrix

**Generated:** 2026-11-08 23:58:23  
**Harness Engine:** Antigravity Subagent Orchestrator  
**Models Evaluated:** Gemini (Native Antigravity) & Claude Code Persona

---

## Executive 2x2 Scorecard

| Model Mode | Baseline (Without Skills) | With Critical Memory | Accuracy Win | Context Token Overhead |
| :--- | :---: | :---: | :---: | :---: |
| **Gemini (Native)** | 73.9% (1800 toks) | **100.0%** (293 toks) | **`+26.1%`** | **`-83.7%` tokens** |
| **Claude Persona** | 73.9% (1800 toks) | **92.4%** (293 toks) | **`+18.5%`** | **`-83.7%` tokens** |

---

## Scenario Breakdown

### Scenario: `adr_contradiction`

| Matrix Cell | Overall Score | Architecture | Traceability | Tasks | Freshness | SNR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Gemini Baseline (No Skills) | **63.4%** | 31.2% | 66.7% | 55.6% | 100.0% | 22.0% clean |
| Gemini With Critical Memory | **100.0%** | 100.0% | 100.0% | 100.0% | 100.0% | 89.3% clean |
| Claude Persona Baseline (No Skills) | **63.4%** | 31.2% | 66.7% | 55.6% | 100.0% | 22.0% clean |
| Claude Persona With Critical Memory | **91.7%** | 100.0% | 66.7% | 100.0% | 100.0% | 89.3% clean |

### Scenario: `context_retrieval`

| Matrix Cell | Overall Score | Architecture | Traceability | Tasks | Freshness | SNR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Gemini Baseline (No Skills) | **82.7%** | 100.0% | 75.0% | 55.6% | 100.0% | 22.0% clean |
| Gemini With Critical Memory | **100.0%** | 100.0% | 100.0% | 100.0% | 100.0% | 89.7% clean |
| Claude Persona Baseline (No Skills) | **82.7%** | 100.0% | 75.0% | 55.6% | 100.0% | 22.0% clean |
| Claude Persona With Critical Memory | **93.8%** | 100.0% | 75.0% | 100.0% | 100.0% | 89.7% clean |

### Scenario: `task_lifecycle`

| Matrix Cell | Overall Score | Architecture | Traceability | Tasks | Freshness | SNR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Gemini Baseline (No Skills) | **75.6%** | 100.0% | 66.7% | 35.7% | 100.0% | 22.0% clean |
| Gemini With Critical Memory | **100.0%** | 100.0% | 100.0% | 100.0% | 100.0% | 89.7% clean |
| Claude Persona Baseline (No Skills) | **75.6%** | 100.0% | 66.7% | 35.7% | 100.0% | 22.0% clean |
| Claude Persona With Critical Memory | **91.7%** | 100.0% | 66.7% | 100.0% | 100.0% | 89.7% clean |
