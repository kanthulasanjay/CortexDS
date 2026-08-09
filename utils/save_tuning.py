import json
import os

def save_tuning(state):

    os.makedirs(
        "reports",
        exist_ok=True
    )

    report = {

        "model": state["model_name"],

        "best_parameters": state["best_params"],

        "optimized_score": state["optimized_score"]

    }

    with open(

        "reports/tuning_results.json",

        "w"

    ) as f:

        json.dump(

            report,

            f,

            indent=4

        )