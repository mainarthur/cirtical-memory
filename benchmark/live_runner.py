"""Critical Memory Live Agent Benchmark Runner.

Orchestrates a 2x2 evaluation matrix:
  [Gemini vs Claude Persona] x [Baseline vs With Critical Memory]

Supports manifest generation, workspace sandbox initialization, subagent prompt preparation,
and 4-dimension metric evaluation with Context Token ROI profiling.
"""

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
from typing import Dict, List, Any, Optional

from benchmark.evaluators import evaluate_workspace
from benchmark.evaluators.token_profiler import profile_task_tokens
from benchmark.scenarios import list_scenarios, get_scenario
from benchmark.subagents.prompts import AGENT_CONFIGS


REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES_DIR = REPO_ROOT / "benchmark" / "fixtures" / "seed_project"
TEMPLATES_DIR = REPO_ROOT / "templates"
REPORTS_DIR = REPO_ROOT / "benchmark" / "reports"


def setup_sandbox(
    dest_dir: Path,
    config_key: str,
    with_skills: bool,
    persona: str
) -> Path:
    """Prepares an isolated workspace sandbox with proper integration templates."""
    dest_dir.mkdir(parents=True, exist_ok=True)

    # Copy fixture contents
    if FIXTURES_DIR.exists():
        for item in FIXTURES_DIR.iterdir():
            dest = dest_dir / item.name
            if item.is_dir():
                shutil.copytree(item, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dest)

    # Setup integration files according to skill condition and persona
    agents_md = dest_dir / "AGENTS.md"
    claude_md = dest_dir / "CLAUDE.md"

    if with_skills:
        # Install root AGENTS.md
        tmpl_agents = TEMPLATES_DIR / "AGENTS.md"
        if tmpl_agents.exists() and not agents_md.exists():
            shutil.copy2(tmpl_agents, agents_md)

        # If Claude persona, also install CLAUDE.md
        if persona == "claude":
            tmpl_claude = TEMPLATES_DIR / "integrations" / "CLAUDE.md"
            if tmpl_claude.exists() and not claude_md.exists():
                shutil.copy2(tmpl_claude, claude_md)
    else:
        # Baseline: Ensure no guiding instruction files exist at root
        if agents_md.exists():
            agents_md.unlink()
        if claude_md.exists():
            claude_md.unlink()

    return dest_dir


def generate_matrix_manifest(
    base_dir: Path,
    scenarios: List[str],
    selected_configs: List[str]
) -> Dict[str, Any]:
    """Generates the live benchmark manifest and scaffolds isolated sandboxes."""
    base_dir.mkdir(parents=True, exist_ok=True)
    manifest_cells = {}

    for cfg_key in selected_configs:
        cfg = AGENT_CONFIGS[cfg_key]
        sandbox_path = base_dir / f"sandbox_{cfg_key}"
        setup_sandbox(
            sandbox_path,
            config_key=cfg_key,
            with_skills=cfg["with_skills"],
            persona=cfg["persona"]
        )

        task_list = []
        for s_id in scenarios:
            mod = get_scenario(s_id)
            if mod:
                task_list.append({
                    "scenario_id": s_id,
                    "title": getattr(mod, "SCENARIO_TITLE", s_id),
                    "prompt": getattr(mod, "PROMPT", ""),
                })

        manifest_cells[cfg_key] = {
            "name": cfg["name"],
            "model": cfg["model"],
            "persona": cfg["persona"],
            "with_skills": cfg["with_skills"],
            "system_prompt": cfg["system_prompt"],
            "workspace_path": str(sandbox_path),
            "tasks": task_list,
        }

    manifest = {
        "benchmark_mode": "live_subagent_2x2_matrix",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "scenarios": scenarios,
        "cells": manifest_cells,
    }

    manifest_file = base_dir / "live_manifest.json"
    manifest_file.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


def execute_matrix_cells(manifest: Dict[str, Any]) -> None:
    """Executes the scenarios across all matrix cells using the defined scenario protocol."""
    cells = manifest.get("cells", {})
    for cell_key, cell_info in cells.items():
        ws = Path(cell_info["workspace_path"])
        with_skills = cell_info["with_skills"]
        for task in cell_info.get("tasks", []):
            s_id = task["scenario_id"]
            mod = get_scenario(s_id)
            if mod and hasattr(mod, "run_scenario"):
                mod.run_scenario(ws, with_skills=with_skills)


def evaluate_matrix_manifest(manifest: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluates all matrix cells and computes 2x2 comparison metrics."""
    results = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cells": {},
        "comparison_matrix": {},
    }

    cells = manifest.get("cells", {})
    for cell_key, cell_info in cells.items():
        ws = Path(cell_info["workspace_path"])
        with_skills = cell_info["with_skills"]

        scenario_evals = []
        cell_scores = []
        cell_tokens = []

        for task in cell_info.get("tasks", []):
            s_id = task["scenario_id"]
            res = evaluate_workspace(ws, s_id, cell_info["name"])
            profile = profile_task_tokens(ws, s_id, with_skills, res.overall_score)
            res.token_profile = profile

            scenario_evals.append({
                "scenario_id": s_id,
                "overall_score": res.overall_score,
                "dimensions": {k: v.score for k, v in res.dimensions.items()},
                "tokens": {
                    "signal_tokens": profile.signal_tokens,
                    "noise_tokens": profile.noise_tokens,
                    "total_tokens": profile.total_tokens,
                    "snr_percent": profile.snr_percent,
                    "pollution_percent": profile.pollution_percent,
                    "efficiency_roi": profile.efficiency_roi,
                }
            })
            cell_scores.append(res.overall_score)
            cell_tokens.append(profile.total_tokens)

        avg_score = round(sum(cell_scores) / max(1, len(cell_scores)), 1)
        avg_tokens = int(sum(cell_tokens) / max(1, len(cell_tokens)))

        results["cells"][cell_key] = {
            "name": cell_info["name"],
            "persona": cell_info["persona"],
            "with_skills": with_skills,
            "average_score": avg_score,
            "average_tokens": avg_tokens,
            "scenarios": scenario_evals,
        }

    # Compute 2x2 comparisons
    if "gemini_skills" in results["cells"] and "gemini_baseline" in results["cells"]:
        g_s = results["cells"]["gemini_skills"]["average_score"]
        g_b = results["cells"]["gemini_baseline"]["average_score"]
        results["comparison_matrix"]["gemini_delta"] = round(g_s - g_b, 1)

    if "claude_skills" in results["cells"] and "claude_baseline" in results["cells"]:
        c_s = results["cells"]["claude_skills"]["average_score"]
        c_b = results["cells"]["claude_baseline"]["average_score"]
        results["comparison_matrix"]["claude_delta"] = round(c_s - c_b, 1)

    return results


def generate_markdown_matrix_report(results: Dict[str, Any], output_path: Path) -> None:
    """Formats 2x2 benchmark results into a clean GitHub Flavored Markdown report."""
    cells = results.get("cells", {})
    matrix = results.get("comparison_matrix", {})

    g_base = cells.get("gemini_baseline", {})
    g_skills = cells.get("gemini_skills", {})
    c_base = cells.get("claude_baseline", {})
    c_skills = cells.get("claude_skills", {})

    md = []
    md.append("# Live Subagent Benchmark: 2x2 Evaluation Matrix\n")
    md.append(f"**Generated:** {results.get('timestamp')}  ")
    md.append(f"**Harness Engine:** Antigravity Subagent Orchestrator  ")
    md.append(f"**Models Evaluated:** Gemini (Native Antigravity) & Claude Code Persona\n")
    md.append("---\n")
    md.append("## Executive 2x2 Scorecard\n")
    md.append("| Model Mode | Baseline (Without Skills) | With Critical Memory | Accuracy Win | Context Token Overhead |")
    md.append("| :--- | :---: | :---: | :---: | :---: |")

    if g_base and g_skills:
        g_delta = matrix.get("gemini_delta", 0.0)
        tok_red_g = round((1.0 - (g_skills["average_tokens"] / max(1, g_base["average_tokens"]))) * 100, 1)
        md.append(
            f"| **Gemini (Native)** | {g_base['average_score']}% ({g_base['average_tokens']} toks) | "
            f"**{g_skills['average_score']}%** ({g_skills['average_tokens']} toks) | "
            f"**`+{g_delta}%`** | **`-{tok_red_g}%` tokens** |"
        )

    if c_base and c_skills:
        c_delta = matrix.get("claude_delta", 0.0)
        tok_red_c = round((1.0 - (c_skills["average_tokens"] / max(1, c_base["average_tokens"]))) * 100, 1)
        md.append(
            f"| **Claude Persona** | {c_base['average_score']}% ({c_base['average_tokens']} toks) | "
            f"**{c_skills['average_score']}%** ({c_skills['average_tokens']} toks) | "
            f"**`+{c_delta}%`** | **`-{tok_red_c}%` tokens** |"
        )

    md.append("\n---\n")
    md.append("## Scenario Breakdown\n")

    # Group by scenario across cells
    sample_cell = next(iter(cells.values())) if cells else {}
    for sc_idx, sc_item in enumerate(sample_cell.get("scenarios", [])):
        s_id = sc_item["scenario_id"]
        md.append(f"### Scenario: `{s_id}`\n")
        md.append("| Matrix Cell | Overall Score | Architecture | Traceability | Tasks | Freshness | SNR |")
        md.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: |")

        for c_key, c_val in cells.items():
            sc_data = c_val["scenarios"][sc_idx]
            dims = sc_data["dimensions"]
            snr = sc_data["tokens"]["snr_percent"]
            md.append(
                f"| {c_val['name']} | **{sc_data['overall_score']}%** | "
                f"{dims.get('architectural', 0.0)}% | {dims.get('traceability', 0.0)}% | "
                f"{dims.get('task_hygiene', 0.0)}% | {dims.get('freshness', 0.0)}% | "
                f"{snr}% clean |"
            )
        md.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(md), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Critical Memory Live Agent Benchmark Runner")
    parser.add_argument("action", choices=["generate", "evaluate", "run"], nargs="?", default="run",
                        help="Action to perform: generate (sandboxes only), evaluate (score existing), or run (end-to-end)")
    parser.add_argument("--models", choices=["gemini", "claude", "all"], default="all",
                        help="Target model personas to evaluate (default: all)")
    parser.add_argument("--scenario", choices=list_scenarios() + ["all"], default="all",
                        help="Scenario to run (default: all)")
    parser.add_argument("--output-dir", default=None,
                        help="Directory to place sandboxes and reports")
    parser.add_argument("--dry-run", action="store_true",
                        help="Generate manifests and sandboxes without running evaluation")
    parser.add_argument("--keep-sandboxes", action="store_true",
                        help="Do not delete temporary sandboxes after evaluation")

    args = parser.parse_args()

    # Determine scenarios
    if args.scenario == "all":
        scenarios = [s for s in list_scenarios() if s != "continual_growth"]
    else:
        scenarios = [args.scenario]

    # Determine agent configs
    if args.models == "gemini":
        selected_configs = ["gemini_baseline", "gemini_skills"]
    elif args.models == "claude":
        selected_configs = ["claude_baseline", "claude_skills"]
    else:
        selected_configs = ["gemini_baseline", "gemini_skills", "claude_baseline", "claude_skills"]

    # Determine working sandbox root
    cleanup_temp = False
    if args.output_dir:
        sandbox_root = Path(args.output_dir).resolve()
    else:
        sandbox_root = Path(tempfile.mkdtemp(prefix="cm_live_matrix_"))
        cleanup_temp = not args.keep_sandboxes

    try:
        print("\n" + "=" * 54)
        print("  CRITICAL MEMORY LIVE SUBAGENT BENCHMARK (2x2 MATRIX)")
        print("=" * 54)
        print(f"Models Target : {args.models.upper()}")
        print(f"Scenarios     : {', '.join(scenarios)}")
        print(f"Working Dir   : {sandbox_root}")
        print("-" * 54)

        # 1. Generate Manifest & Sandboxes
        print("▶ Generating live execution manifest and sandboxes...")
        manifest = generate_matrix_manifest(sandbox_root, scenarios, selected_configs)
        print(f"  ✓ Manifest created at: {sandbox_root / 'live_manifest.json'}")

        if args.dry_run or args.action == "generate":
            print("\n[Dry Run / Generate Only Complete]")
            print(f"Sandboxes ready in: {sandbox_root}")
            return

        # 2. Execute Matrix Cells
        print("\n▶ Executing scenarios across matrix cells...")
        execute_matrix_cells(manifest)
        print("  ✓ All matrix cells executed.")

        # 3. Evaluate & Grade
        print("\n▶ Scoring 4-dimension metrics and token economics...")
        eval_results = evaluate_matrix_manifest(manifest)

        # Write reports
        report_md = REPORTS_DIR / "live-matrix-report.md"
        report_json = REPORTS_DIR / "live_matrix_results.json"

        generate_markdown_matrix_report(eval_results, report_md)
        report_json.write_text(json.dumps(eval_results, indent=2), encoding="utf-8")

        print(f"📊 Markdown Report generated: {report_md}")
        print(f"📁 JSON Results generated:    {report_json}")

        print("\n" + "-" * 54)
        print("LIVE BENCHMARK COMPLETED")
        matrix = eval_results.get("comparison_matrix", {})
        if "gemini_delta" in matrix:
            print(f"  Gemini Advantage : +{matrix['gemini_delta']}%")
        if "claude_delta" in matrix:
            print(f"  Claude Advantage : +{matrix['claude_delta']}%")
        print("-" * 54 + "\n")

    finally:
        if cleanup_temp:
            shutil.rmtree(sandbox_root, ignore_errors=True)


if __name__ == "__main__":
    main()
