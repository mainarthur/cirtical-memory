"""Benchmark Scenarios package."""

from typing import List, Dict, Any
from . import adr_contradiction
from . import context_retrieval
from . import task_lifecycle

SCENARIOS: Dict[str, Any] = {
    "adr_contradiction": adr_contradiction,
    "context_retrieval": context_retrieval,
    "task_lifecycle": task_lifecycle,
}


def get_scenario(scenario_id: str):
    return SCENARIOS.get(scenario_id)


def list_scenarios() -> List[str]:
    return list(SCENARIOS.keys())
