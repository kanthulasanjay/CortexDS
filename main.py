from core.graph import graph


def main():

    initial_state = {

        "dataset_path": r"C:\Users\Kanth\Downloads\Credit Card Defaulter Prediction.csv",

        "target": "default",

        "dataframe": None,
        "clean_dataframe": None,
        "target_series": None,
        "preprocessing_pipeline": None,

        "problem_type": "",

        "plan": [],

        "dataset_summary": {},
        "quality_report": {},
        "eda_report": {},

        "selected_features": [],

        "candidate_models": [],
        "leaderboard": [],
        "debate": [],

        "model_name": "",
        "metrics": {},

        "best_params": {},
        "optimized_score": 0.0,

        "business_summary": "",

        # IMPORTANT
        "messages": [],

        "deployment_ready": False

    }

    result = graph.invoke(initial_state)

    # -------------------------------------------------
    # DATASET SUMMARY
    # -------------------------------------------------

    print("\n" + "=" * 60)
    print("DATASET SUMMARY")
    print("=" * 60)

    for key, value in result["dataset_summary"].items():
        print(f"{key}: {value}")

    # -------------------------------------------------
    # QUALITY REPORT
    # -------------------------------------------------

    print("\n" + "=" * 60)
    print("QUALITY REPORT")
    print("=" * 60)

    for key, value in result["quality_report"].items():
        print(f"{key}: {value}")

    # -------------------------------------------------
    # EDA
    # -------------------------------------------------

    print("\n" + "=" * 60)
    print("EDA SUMMARY")
    print("=" * 60)

    print(result["eda_report"]["summary"])

    print("\n" + "=" * 60)
    print("EDA INSIGHTS")
    print("=" * 60)

    for insight in result["eda_report"]["insights"]:
        print(f"• {insight}")

    # -------------------------------------------------
    # MODEL DISCOVERY
    # -------------------------------------------------

    print("\n" + "=" * 60)
    print("CANDIDATE MODELS")
    print("=" * 60)

    for model in result["candidate_models"]:
        print(f"{model['name']}")
        print(f"Reason : {model['reason']}")
        print()

    # -------------------------------------------------
    # LEADERBOARD
    # -------------------------------------------------

    print("\n" + "=" * 60)
    print("MODEL LEADERBOARD")
    print("=" * 60)

    for i, row in enumerate(result["leaderboard"], start=1):

        print(
            f"{i}. {row['model']}  ->  Accuracy : {row['accuracy']:.4f}"
        )

    # -------------------------------------------------
    # BEST MODEL
    # -------------------------------------------------

    print("\n" + "=" * 60)
    print("BEST MODEL")
    print("=" * 60)

    print(result["model_name"])

    # -------------------------------------------------
    # METRICS
    # -------------------------------------------------

    print("\n" + "=" * 60)
    print("METRICS")
    print("=" * 60)

    for key, value in result["metrics"].items():
        print(f"{key}: {value}")

    # -------------------------------------------------
    # BUSINESS SUMMARY
    # -------------------------------------------------

    print("\n" + "=" * 60)
    print("BUSINESS SUMMARY")
    print("=" * 60)

    print(result["business_summary"])

    # -------------------------------------------------
    # WORKFLOW LOG
    # -------------------------------------------------

    print("\n" + "=" * 60)
    print("WORKFLOW LOG")
    print("=" * 60)

    for message in result["messages"]:
        print(f"• {message}")


if __name__ == "__main__":
    main()