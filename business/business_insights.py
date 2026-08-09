from core.logger import logger


class BusinessInsightGenerator:

    def generate(
        self,
        metrics,
        problem_type,
        model_name
    ):

        logger.info(
            "Generating Business Insights..."
        )

        # ==================================================
        # SAFE INPUTS
        # ==================================================

        if not isinstance(metrics, dict):
            metrics = {}

        problem_type = str(
            problem_type or ""
        ).strip().lower()

        model_name = str(
            model_name or "Selected Model"
        )

        insights = []

        # ==================================================
        # CLASSIFICATION
        # ==================================================

        if problem_type == "classification":

            accuracy = metrics.get(
                "accuracy",
                metrics.get(
                    "Accuracy",
                    None
                )
            )

            precision = metrics.get(
                "precision",
                metrics.get(
                    "Precision",
                    None
                )
            )

            recall = metrics.get(
                "recall",
                metrics.get(
                    "Recall",
                    None
                )
            )

            f1 = metrics.get(
                "f1_score",
                metrics.get(
                    "F1 Score",
                    metrics.get(
                        "f1",
                        None
                    )
                )
            )

            # ----------------------------------------------
            # Accuracy
            # ----------------------------------------------

            if accuracy is not None:

                try:

                    accuracy = float(
                        accuracy
                    )

                    if accuracy >= 0.90:

                        insights.append(
                            f"{model_name} achieved excellent "
                            f"classification accuracy of "
                            f"{accuracy:.4f}."
                        )

                    elif accuracy >= 0.80:

                        insights.append(
                            f"{model_name} achieved good "
                            f"classification accuracy of "
                            f"{accuracy:.4f}."
                        )

                    elif accuracy >= 0.70:

                        insights.append(
                            f"{model_name} achieved moderate "
                            f"classification accuracy of "
                            f"{accuracy:.4f}. Further model "
                            f"improvement may be beneficial."
                        )

                    else:

                        insights.append(
                            f"{model_name} achieved an accuracy "
                            f"of {accuracy:.4f}. Model improvement "
                            f"should be considered."
                        )

                except (
                    TypeError,
                    ValueError
                ):

                    pass

            # ----------------------------------------------
            # Precision
            # ----------------------------------------------

            if precision is not None:

                try:

                    insights.append(
                        f"Precision: "
                        f"{float(precision):.4f}"
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    pass

            # ----------------------------------------------
            # Recall
            # ----------------------------------------------

            if recall is not None:

                try:

                    insights.append(
                        f"Recall: "
                        f"{float(recall):.4f}"
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    pass

            # ----------------------------------------------
            # F1 Score
            # ----------------------------------------------

            if f1 is not None:

                try:

                    insights.append(
                        f"F1 Score: "
                        f"{float(f1):.4f}"
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    pass

            # ----------------------------------------------
            # Classification Recommendation
            # ----------------------------------------------

            insights.append(
                "The selected classification model can be "
                "used to predict the target class for new "
                "observations."
            )

        # ==================================================
        # REGRESSION
        # ==================================================

        elif problem_type == "regression":

            r2 = metrics.get(
                "r2_score",
                metrics.get(
                    "R²",
                    metrics.get(
                        "r2",
                        None
                    )
                )
            )

            mae = metrics.get(
                "mae",
                metrics.get(
                    "MAE",
                    None
                )
            )

            mse = metrics.get(
                "mse",
                metrics.get(
                    "MSE",
                    None
                )
            )

            rmse = metrics.get(
                "rmse",
                metrics.get(
                    "RMSE",
                    None
                )
            )

            # ----------------------------------------------
            # R² Score
            # ----------------------------------------------

            if r2 is not None:

                try:

                    r2 = float(
                        r2
                    )

                    if r2 >= 0.90:

                        insights.append(
                            f"{model_name} achieved excellent "
                            f"regression performance with an "
                            f"R² score of {r2:.4f}."
                        )

                    elif r2 >= 0.80:

                        insights.append(
                            f"{model_name} achieved strong "
                            f"regression performance with an "
                            f"R² score of {r2:.4f}."
                        )

                    elif r2 >= 0.60:

                        insights.append(
                            f"{model_name} achieved moderate "
                            f"regression performance with an "
                            f"R² score of {r2:.4f}."
                        )

                    else:

                        insights.append(
                            f"{model_name} achieved an R² score "
                            f"of {r2:.4f}. Further feature "
                            f"engineering or model improvement "
                            f"may be beneficial."
                        )

                except (
                    TypeError,
                    ValueError
                ):

                    pass

            # ----------------------------------------------
            # MAE
            # ----------------------------------------------

            if mae is not None:

                try:

                    insights.append(
                        f"Mean Absolute Error (MAE): "
                        f"{float(mae):.4f}"
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    pass

            # ----------------------------------------------
            # MSE
            # ----------------------------------------------

            if mse is not None:

                try:

                    insights.append(
                        f"Mean Squared Error (MSE): "
                        f"{float(mse):.4f}"
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    pass

            # ----------------------------------------------
            # RMSE
            # ----------------------------------------------

            if rmse is not None:

                try:

                    insights.append(
                        f"Root Mean Squared Error (RMSE): "
                        f"{float(rmse):.4f}"
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    pass

            # ----------------------------------------------
            # Regression Recommendation
            # ----------------------------------------------

            insights.append(
                "The selected regression model can be "
                "used to estimate continuous target values "
                "for new observations."
            )

        # ==================================================
        # UNKNOWN PROBLEM TYPE
        # ==================================================

        else:

            insights.append(
                "The problem type could not be determined "
                "from the available pipeline state."
            )

        # ==================================================
        # FALLBACK MESSAGE
        # ==================================================

        if not insights:

            insights.append(
                "Business insights could not be generated "
                "because the required model metrics were "
                "not available."
            )

        # ==================================================
        # FINAL RESULT
        # ==================================================

        result = {

            "model": model_name,

            "problem_type": problem_type,

            "insights": insights
        }

        logger.info(
            "Business Insights Generated"
        )

        return result