"""Benchmark Scenarios package."""

from typing import List, Dict, Any
from . import adr_contradiction
from . import context_retrieval
from . import task_lifecycle
from . import continual_growth

SCENARIOS: Dict[str, Any] = {
    "adr_contradiction": adr_contradiction,
    "context_retrieval": context_retrieval,
    "task_lifecycle": task_lifecycle,
    "continual_growth": continual_growth,
}


def get_scenario(scenario_id: str):
    return SCENARIOS.get(scenario_id)


def list_scenarios() -> List[str]:
    return list(SCENARIOS.keys())
