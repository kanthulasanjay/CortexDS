from typing import Any, Dict, List
from typing_extensions import TypedDict


class DSState(TypedDict):

    dataset_path: str
    target: str

    dataframe: Any
    clean_dataframe: Any
    target_series: Any
    preprocessing_pipeline: Any

    problem_type: str

    plan: List

    dataset_summary: Dict
    quality_report: Dict
    eda_report: Dict

    selected_features: List[str]

    candidate_models: List
    leaderboard: List

    debate: List
    manager_decision: Dict

    model_name: str
    best_model: Any

    best_params: Dict
    optimized_score: float

    metrics: Dict

    model_selection_reason: str

    explainability_report: Dict
    business_report: Dict

    knowledge: str
    previous_experiments: List

    deployment_ready: bool

    messages: List[str]