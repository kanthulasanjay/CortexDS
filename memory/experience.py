from dataclasses import dataclass

@dataclass
class Experience:

    dataset_name: str

    problem_type: str

    rows: int

    columns: int

    best_model: str

    best_score: float

    best_parameters: dict

    quality_score: float

    feature_count: int

    timestamp: str