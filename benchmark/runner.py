"""Critical Memory Benchmark Runner.

Runs tasks under two conditions:
  Condition A: With Critical Memory (memdoc + adr-review)
  Condition B: Baseline (Vanilla / Without Skills)
Computes 4-dimension metric scores and generates comparative reports.
"""

import argparse
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
from datetime import datetime
from typing import List, Dict, Any

from benchmark.evaluators.base import (
    ScenarioComparison,
    BenchmarkReport,
    ConditionResult,
)
from benchmark.evaluators import evaluate_workspace
from benchmark.scenarios import SCENARIOS, list_scenarios, get_scenario


REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES_DIR = REPO_ROOT / "benchmark" / "fixtures" / "seed_project"


def create_isolated_workspace(fixture_path: Path, prefix: str) -> Path:
    """Creates a temporary isolated directory copied from the seed fixture."""
    temp_dir = Path(tempfile.mkdtemp(prefix=f"cm_bench_{prefix}_"))
    if fixture_path.exists():
        for item in fixture_path.iterdir():
            dest = temp_dir / item.name
            if item.is_dir():
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)
    return temp_dir


def run_benchmark_for_scenario(scenario_id: str) -> ScenarioComparison:
    """Executes a single scenario across both conditions and evaluates them."""
    mod = get_scenario(scenario_id)
    if not mod:
        raise ValueError(f"Unknown scenario: {scenario_id}")

    # Condition A: With Skills
    ws_skills = create_isolated_workspace(FIXTURES_DIR, f"{scenario_id}_skills")
    # Condition B: Baseline
    ws_base = create_isolated_workspace(FIXTURES_DIR, f"{scenario_id}_base")

    try:
        mod.run_scenario(ws_skills, with_skills=True)
        mod.run_scenario(ws_base, with_skills=False)

        res_skills = evaluate_workspace(ws_skills, scenario_id, "With Critical Memory")
        res_base = evaluate_workspace(ws_base, scenario_id, "Baseline (No Skills)")

        delta = round(res_skills.overall_score - res_base.overall_score, 1)

        dim_deltas = {}
        for dim_key in res_skills.dimensions:
            s_score = res_skills.dimensions[dim_key].score
            b_score = res_base.dimensions[dim_key].score
            dim_deltas[dim_key] = round(s_score - b_score, 1)

        return ScenarioComparison(
            scenario_id=scenario_id,
            scenario_title=getattr(mod, "SCENARIO_TITLE", scenario_id),
            with_skills=res_skills,
            baseline=res_base,
            score_delta=delta,
            dimension_deltas=dim_deltas
        )
    finally:
        shutil.rmtree(ws_skills, ignore_errors=True)
        shutil.rmtree(ws_base, ignore_errors=True)


def generate_markdown_report(report: BenchmarkReport) -> str:
    """Renders a comprehensive GitHub-flavored Markdown report."""
    md = []
    md.append("# Critical Memory Benchmark Report\n")
    md.append(f"**Generated:** {report.timestamp}  ")
    md.append(f"**Overall Score (With Critical Memory):** `{report.average_with_skills:.1f}%`  ")
    md.append(f"**Overall Score (Baseline / Vanilla):** `{report.average_baseline:.1f}%`  ")
    md.append(f"**Overall Performance Delta:** `+{report.overall_delta:.1f}%`\n")

    md.append("---\n")
    md.append("## Executive Summary\n")
    md.append("| Metric / Dimension | Baseline (No Skills) | With Critical Memory | Delta |")
    md.append("| :--- | :---: | :---: | :---: |")

    for dim_key, vals in report.dimension_summaries.items():
        dim_name = dim_key.replace("_", " ").title()
        b_val = vals["baseline"]
        s_val = vals["with_skills"]
        d_val = vals["delta"]
        sign = "+" if d_val > 0 else ""
        md.append(f"| **{dim_name}** | {b_val:.1f}% | **{s_val:.1f}%** | `{sign}{d_val:.1f}%` |")

    sign_total = "+" if report.overall_delta > 0 else ""
    md.append(f"| **AVERAGE COMPOSITE** | {report.average_baseline:.1f}% | **{report.average_with_skills:.1f}%** | `{sign_total}{report.overall_delta:.1f}%` |\n")

    md.append("---\n")
    md.append("## Scenario Breakdown\n")

    for sc in report.scenarios:
        sign = "+" if sc.score_delta > 0 else ""
        md.append(f"### {sc.scenario_title} (`{sc.scenario_id}`)\n")
        md.append(f"- **Overall Score:** Baseline: `{sc.baseline.overall_score:.1f}%` ➔ With Skills: **`{sc.with_skills.overall_score:.1f}%`** (`{sign}{sc.score_delta:.1f}%`)")
        md.append("\n| Dimension | Baseline | With Skills | Delta |")
        md.append("| :--- | :---: | :---: | :---: |")

        for d_key, d_score in sc.with_skills.dimensions.items():
            b_score = sc.baseline.dimensions[d_key].score
            s_score = d_score.score
            d_delta = sc.dimension_deltas.get(d_key, 0.0)
            d_sign = "+" if d_delta > 0 else ""
            md.append(f"| {d_score.name} | {b_score:.1f}% | **{s_score:.1f}%** | `{d_sign}{d_delta:.1f}%` |")

        md.append("\n#### Detailed Check Highlights (With Critical Memory):")
        for d_key, d_score in sc.with_skills.dimensions.items():
            for chk in d_score.checks:
                status_icon = "✅" if chk.passed else "❌"
                md.append(f"- {status_icon} **{chk.name}**: {chk.message}")

        md.append("\n")

    return "\n".join(md)


def main():
    parser = argparse.ArgumentParser(description="Critical Memory Benchmark Runner")
    parser.add_argument(
        "--scenario",
        default="all",
        choices=["all"] + list_scenarios(),
        help="Specific scenario to evaluate, or 'all'"
    )
    parser.add_argument(
        "--output-dir",
        default=str(REPO_ROOT / "benchmark" / "reports"),
        help="Output directory for reports"
    )
    parser.add_argument(
        "--format",
        default="both",
        choices=["markdown", "json", "both"],
        help="Report export format"
    )

    args = parser.parse_args()

    scenario_ids = list_scenarios() if args.scenario == "all" else [args.scenario]
    comparisons: List[ScenarioComparison] = []

    print("\n==================================================")
    print("      CRITICAL MEMORY BENCHMARK HARNESS           ")
    print("==================================================")
    print(f"Evaluating {len(scenario_ids)} scenario(s)...")

    for sid in scenario_ids:
        print(f"\n▶ Running Scenario: {sid}...")
        comp = run_benchmark_for_scenario(sid)
        comparisons.append(comp)
        sign = "+" if comp.score_delta > 0 else ""
        print(f"  ✓ Complete: Baseline {comp.baseline.overall_score:.1f}% vs With Skills {comp.with_skills.overall_score:.1f}% ({sign}{comp.score_delta:.1f}%)")

    # Aggregate metrics
    avg_skills = sum(c.with_skills.overall_score for c in comparisons) / len(comparisons)
    avg_base = sum(c.baseline.overall_score for c in comparisons) / len(comparisons)
    tot_delta = avg_skills - avg_base

    dim_summaries: Dict[str, Dict[str, float]] = {}
    sample_dims = comparisons[0].with_skills.dimensions.keys()
    for dk in sample_dims:
        s_avg = sum(c.with_skills.dimensions[dk].score for c in comparisons) / len(comparisons)
        b_avg = sum(c.baseline.dimensions[dk].score for c in comparisons) / len(comparisons)
        dim_summaries[dk] = {
            "with_skills": round(s_avg, 1),
            "baseline": round(b_avg, 1),
            "delta": round(s_avg - b_avg, 1)
        }

    report = BenchmarkReport(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        scenarios=comparisons,
        average_with_skills=round(avg_skills, 1),
        average_baseline=round(avg_base, 1),
        overall_delta=round(tot_delta, 1),
        dimension_summaries=dim_summaries
    )

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.format in ("markdown", "both"):
        md_content = generate_markdown_report(report)
        md_file = out_dir / "benchmark-report.md"
        md_file.write_text(md_content, encoding="utf-8")
        print(f"\n📊 Markdown Report generated: {md_file}")

    if args.format in ("json", "both"):
        # Custom serializer for dataclasses
        def default_serializer(obj):
            if hasattr(obj, "__dict__"):
                return obj.__dict__
            return str(obj)

        json_file = out_dir / "results.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(report, f, default=default_serializer, indent=2)
        print(f"📁 JSON Results generated: {json_file}")

    print("\n--------------------------------------------------")
    print(f"BENCHMARK COMPLETED: Overall Delta = +{report.overall_delta:.1f}%")
    print(f"With Critical Memory: {report.average_with_skills:.1f}%  |  Baseline: {report.average_baseline:.1f}%")
    print("--------------------------------------------------\n")


if __name__ == "__main__":
    main()
