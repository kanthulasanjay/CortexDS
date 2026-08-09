from core.logger import logger


def debate_agent(state):

    logger.info("=" * 60)
    logger.info("MODEL DEBATE AGENT STARTED")
    logger.info("=" * 60)

    try:

        problem_type = state.get(
            "problem_type",
            ""
        ).lower()

        leaderboard = state.get(
            "leaderboard",
            []
        )

        # ==================================================
        # NO RESULTS
        # ==================================================

        if not leaderboard:

            state["debate"] = []

            state["messages"].append(
                "Model Debate Agent: No model results available."
            )

            return state

        # ==================================================
        # VALID RESULTS ONLY
        # ==================================================

        valid_models = []

        for item in leaderboard:

            if "error" in item:
                continue

            if problem_type == "classification":

                score = item.get(
                    "accuracy",
                    item.get("score", 0)
                )

            else:

                score = item.get(
                    "r2_score",
                    item.get("score", 0)
                )

            try:

                score = float(score)

            except:

                score = 0.0

            valid_models.append({

                "model": item.get(
                    "model",
                    item.get(
                        "name",
                        "Unknown"
                    )
                ),

                "score": score,

                "original": item
            })

        # ==================================================
        # FIND BEST MODEL
        # ==================================================

        if not valid_models:

            state["messages"].append(
                "Model Debate Agent: No valid model scores found."
            )

            return state

        best = max(
            valid_models,
            key=lambda x: x["score"]
        )

        best_model = best["model"]

        best_score = best["score"]

        # ==================================================
        # DEBATE RESULTS
        # ==================================================

        debate = []

        for item in valid_models:

            model_name = item["model"]

            score = item["score"]

            if model_name == best_model:

                opinion = (
                    f"{model_name} achieved the "
                    f"highest validation score "
                    f"of {score:.4f}."
                )

            else:

                difference = (
                    best_score - score
                )

                opinion = (
                    f"{model_name} achieved "
                    f"{score:.4f}, which is "
                    f"{difference:.4f} below "
                    f"the selected model."
                )

            debate.append({

                "model": model_name,

                "score": score,

                "opinion": opinion
            })

        # ==================================================
        # SAVE DEBATE
        # ==================================================

        state["debate"] = debate

        # ==================================================
        # KEEP BEST MODEL
        # ==================================================

        state["model_name"] = best_model

        # ==================================================
        # METRIC
        # ==================================================

        if problem_type == "classification":

            metric_name = "accuracy"

        else:

            metric_name = "R² score"

        # ==================================================
        # MANAGER DECISION
        # ==================================================

        state["manager_decision"] = {

            "decision": best_model,

            "score": best_score,

            "metric": metric_name,

            "reason": (

                f"{best_model} achieved the highest "
                f"{metric_name} among the selected "
                f"candidate models."
            )
        }

        # ==================================================
        # SELECTION REASON
        # ==================================================

        state["model_selection_reason"] = (

            f"{best_model} was selected because it "
            f"achieved the highest {metric_name} "
            f"({best_score:.4f}) among the selected "
            f"candidate models."
        )

        # ==================================================
        # MESSAGES
        # ==================================================

        state["messages"].append(
            "Model Debate Agent completed."
        )

        state["messages"].append(
            f"Debate confirmed {best_model} "
            f"as the best model."
        )

        logger.info(
            "Debate Best Model: %s",
            best_model
        )

        logger.info(
            "Debate Score: %.4f",
            best_score
        )

        return state

    except Exception as e:

        logger.error(
            "Debate Agent Error: %s",
            str(e)
        )

        state["debate"] = []

        state["messages"].append(
            f"Model Debate Agent encountered an error: {str(e)}"
        )

        return state