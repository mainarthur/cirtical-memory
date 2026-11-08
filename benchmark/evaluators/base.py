"""Base evaluator models and interfaces for Critical Memory Benchmark."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


@dataclass
class CheckResult:
    name: str
    passed: bool
    score: float  # 0.0 to 1.0
    weight: float
    message: str
    details: Optional[Dict[str, Any]] = None


@dataclass
class DimensionScore:
    name: str
    score: float  # 0.0 to 100.0
    passed_checks: int
    total_checks: int
    checks: List[CheckResult] = field(default_factory=list)


@dataclass
class ConditionResult:
    condition_name: str  # "With Critical Memory" or "Baseline (No Skills)"
    scenario_id: str
    dimensions: Dict[str, DimensionScore] = field(default_factory=dict)
    overall_score: float = 0.0
    token_profile: Optional[Any] = None


@dataclass
class ScenarioComparison:
    scenario_id: str
    scenario_title: str
    with_skills: ConditionResult
    baseline: ConditionResult
    score_delta: float = 0.0  # with_skills - baseline
    dimension_deltas: Dict[str, float] = field(default_factory=dict)


@dataclass
class BenchmarkReport:
    timestamp: str
    scenarios: List[ScenarioComparison] = field(default_factory=list)
    average_with_skills: float = 0.0
    average_baseline: float = 0.0
    overall_delta: float = 0.0
    dimension_summaries: Dict[str, Dict[str, float]] = field(default_factory=dict)

