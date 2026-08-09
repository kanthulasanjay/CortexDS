from dataclasses import dataclass

@dataclass
class CandidateModel:
    name: str
    reason: str


class ModelDiscovery:

    def recommend(self, state):

        df = state["dataframe"]

        target = state["target"]

        problem = state["problem_type"]

        rows = len(df)

        cols = len(df.columns)

        candidates = []

        if problem == "classification":

            candidates.extend([

                CandidateModel(
                    "Logistic Regression",
                    "Strong baseline for classification."
                ),

                CandidateModel(
                    "Random Forest",
                    "Handles nonlinear relationships."
                ),

                CandidateModel(
                    "XGBoost",
                    "Usually performs well on tabular data."
                ),

                CandidateModel(
                    "LightGBM",
                    "Fast gradient boosting."
                ),

                CandidateModel(
                    "CatBoost",
                    "Excellent for categorical features."
                )

            ])

            if rows > 50000:

                candidates.append(

                    CandidateModel(
                        "HistGradientBoosting",
                        "Efficient on large datasets."
                    )

                )

        else:

            candidates.extend([

                CandidateModel(
                    "Linear Regression",
                    "Baseline regression."
                ),

                CandidateModel(
                    "Random Forest Regressor",
                    "Captures nonlinear patterns."
                ),

                CandidateModel(
                    "XGBoost Regressor",
                    "High accuracy."
                )

            ])

        return candidates