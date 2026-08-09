from core.graph import graph

import json
import numpy as np
import pandas as pd


class PipelineService:

    @staticmethod
    def execute(dataset_path, target):

        # ==================================================
        # INITIAL PIPELINE STATE
        # ==================================================

        state = {

            # -------------------------------
            # DATASET
            # -------------------------------

            "dataset_path": dataset_path,
            "target": target,

            "dataframe": None,
            "clean_dataframe": None,
            "target_series": None,
            "preprocessing_pipeline": None,

            # -------------------------------
            # PROBLEM UNDERSTANDING
            # -------------------------------

            "problem_type": "",
            "plan": [],

            # -------------------------------
            # DATASET ANALYSIS
            # -------------------------------

            "dataset_summary": {},
            "quality_report": {},
            "eda_report": {},

            # -------------------------------
            # FEATURE ENGINEERING
            # -------------------------------

            "selected_features": [],

            # -------------------------------
            # MODEL SELECTION
            # -------------------------------

            "candidate_models": [],
            "leaderboard": [],

            "debate": [],
            "manager_decision": {},

            "model_name": "",
            "best_model": None,

            # -------------------------------
            # HYPERPARAMETER OPTIMIZATION
            # -------------------------------

            "best_params": {},
            "optimized_score": 0.0,

            # -------------------------------
            # MODEL METRICS
            # -------------------------------

            "metrics": {},

            "model_selection_reason": "",

            # -------------------------------
            # EXPLAINABILITY
            # -------------------------------

            "explainability_report": {},

            # -------------------------------
            # BUSINESS INTELLIGENCE
            # -------------------------------

            "business_report": {},

            # -------------------------------
            # MEMORY
            # -------------------------------

            "knowledge": "",
            "previous_experiments": [],

            # -------------------------------
            # AGENT COMMUNICATION
            # -------------------------------

            "messages": [],

            # -------------------------------
            # DEPLOYMENT
            # -------------------------------

            "deployment_ready": False
        }

        # ==================================================
        # RUN LANGGRAPH
        # ==================================================

        try:

            result = graph.invoke(state)

        except Exception as e:

            print("\n" + "=" * 70)
            print("CORTEXDS PIPELINE ERROR")
            print("=" * 70)
            print(f"Error Type : {type(e).__name__}")
            print(f"Error      : {str(e)}")
            print("=" * 70)

            raise

        # ==================================================
        # CONVERT RESULT TO JSON-SAFE FORMAT
        # ==================================================

        return PipelineService.make_json_safe(result)

    # ======================================================
    # JSON SAFE CONVERTER
    # ======================================================

    @staticmethod
    def make_json_safe(obj):

        # --------------------------------------------------
        # None
        # --------------------------------------------------

        if obj is None:
            return None

        # --------------------------------------------------
        # Pandas DataFrame
        # --------------------------------------------------

        if isinstance(obj, pd.DataFrame):

            return obj.head(100).to_dict(
                orient="records"
            )

        # --------------------------------------------------
        # Pandas Series
        # --------------------------------------------------

        if isinstance(obj, pd.Series):

            return obj.head(100).tolist()

        # --------------------------------------------------
        # NumPy Integer
        # --------------------------------------------------

        if isinstance(obj, np.integer):

            return int(obj)

        # --------------------------------------------------
        # NumPy Float
        # --------------------------------------------------

        if isinstance(obj, np.floating):

            return float(obj)

        # --------------------------------------------------
        # NumPy Boolean
        # --------------------------------------------------

        if isinstance(obj, np.bool_):

            return bool(obj)

        # --------------------------------------------------
        # Dictionary
        # --------------------------------------------------

        if isinstance(obj, dict):

            return {
                str(key):
                PipelineService.make_json_safe(value)
                for key, value in obj.items()
            }

        # --------------------------------------------------
        # List / Tuple / Set
        # --------------------------------------------------

        if isinstance(
            obj,
            (list, tuple, set)
        ):

            return [
                PipelineService.make_json_safe(value)
                for value in obj
            ]

        # --------------------------------------------------
        # Primitive Values
        # --------------------------------------------------

        if isinstance(
            obj,
            (str, int, float, bool)
        ):

            return obj

        # --------------------------------------------------
        # Everything Else
        # --------------------------------------------------

        try:

            json.dumps(obj)

            return obj

        except Exception:

            return str(obj)