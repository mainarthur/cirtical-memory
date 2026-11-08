"""Evaluators package for Critical Memory Benchmark."""

from pathlib import Path
from typing import Dict
from .base import DimensionScore, ConditionResult
from .architectural import evaluate_architectural_consistency
from .traceability import evaluate_traceability
from .task_hygiene import evaluate_task_hygiene
from .freshness import evaluate_doc_freshness


def evaluate_workspace(workspace: Path, scenario_id: str, condition_name: str) -> ConditionResult:
    """Evaluates all 4 dimensions for a workspace under a specific condition."""
    dim1 = evaluate_architectural_consistency(workspace, scenario_id)
    dim2 = evaluate_traceability(workspace, scenario_id)
    dim3 = evaluate_task_hygiene(workspace, scenario_id)
    dim4 = evaluate_doc_freshness(workspace, scenario_id)

    dims: Dict[str, DimensionScore] = {
        "architectural": dim1,
        "traceability": dim2,
        "task_hygiene": dim3,
        "freshness": dim4,
    }

    overall = round((dim1.score + dim2.score + dim3.score + dim4.score) / 4.0, 1)

    return ConditionResult(
        condition_name=condition_name,
        scenario_id=scenario_id,
        dimensions=dims,
        overall_score=overall
    )

