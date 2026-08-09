from core.logger import logger

from ml.optimizer import HyperparameterOptimizer


def hyperparameter_agent(state):

    logger.info("=" * 60)
    logger.info("HYPERPARAMETER AGENT STARTED")
    logger.info("=" * 60)

    # ======================================================
    # GET BEST MODEL FROM MODEL AGENT
    # ======================================================

    model_name = state.get("model_name", "")

    if not model_name:

        raise ValueError(
            "Model name is missing from pipeline state."
        )

    logger.info(
        "Optimizing model: %s",
        model_name
    )

    # ======================================================
    # GET FEATURES
    # ======================================================

    X = state.get("clean_dataframe")

    if X is None:

        raise ValueError(
            "clean_dataframe is missing."
        )

    # ======================================================
    # GET TARGET
    # ======================================================

    y = state.get("target_series")

    if y is None:

        raise ValueError(
            "target_series is missing."
        )

    # ======================================================
    # IMPORTANT
    # ======================================================
    # Do NOT do:
    #
    # X.drop(columns=[target])
    #
    # because Feature Agent may already have converted
    # X into a NumPy ndarray.
    # ======================================================

    logger.info(
        "Feature type: %s",
        type(X).__name__
    )

    logger.info(
        "Target type: %s",
        type(y).__name__
    )

    # ======================================================
    # OPTIMIZER
    # ======================================================

    optimizer = HyperparameterOptimizer()

    # ======================================================
    # RUN OPTIMIZATION
    # ======================================================

    params, score, best_model = optimizer.optimize(

        model_name=model_name,

        X=X,

        y=y,

        n_trials=10
    )

    # ======================================================
    # SAVE RESULTS
    # ======================================================

    state["best_params"] = params

    state["optimized_score"] = float(score)

    state["best_model"] = best_model

    # ======================================================
    # MESSAGE
    # ======================================================

    state["messages"].append(

        f"Hyperparameter optimization completed "
        f"for {model_name}."
    )

    state["messages"].append(

        f"Optimized score: {score:.4f}"
    )

    logger.info(
        "Best Parameters: %s",
        params
    )

    logger.info(
        "Optimized Score: %.4f",
        score
    )

    logger.info("=" * 60)
    logger.info("HYPERPARAMETER AGENT FINISHED")
    logger.info("=" * 60)

    return state