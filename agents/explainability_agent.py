import os
import json
import logging

import numpy as np
import pandas as pd

from sklearn.inspection import permutation_importance


logger = logging.getLogger(__name__)


def explainability_agent(state):

    logger.info("=" * 60)
    logger.info("Explainability Agent Started")
    logger.info("=" * 60)

    try:

        # ==================================================
        # GET MODEL
        # ==================================================

        model = state.get("best_model")

        if model is None:
            model = state.get("model")

        if model is None:
            logger.warning(
                "No trained model available for explainability."
            )

            state["explainability_report"] = {
                "status": "skipped",
                "message": "No trained model available."
            }

            state["messages"].append(
                "Explainability skipped: no model available."
            )

            return state


        # ==================================================
        # GET DATA
        # ==================================================

        X = state.get("clean_dataframe")

        if X is None:
            X = state.get("dataframe")


        if X is None:

            logger.warning(
                "No dataframe available for explainability."
            )

            state["explainability_report"] = {
                "status": "skipped",
                "message": "No dataframe available."
            }

            state["messages"].append(
                "Explainability skipped: no dataframe."
            )

            return state


        # ==================================================
        # TARGET
        # ==================================================

        target = state.get("target")


        # ==================================================
        # CONVERT DATAFRAME SAFELY
        # ==================================================

        if isinstance(X, pd.DataFrame):

            X_df = X.copy()

        elif isinstance(X, np.ndarray):

            logger.info(
                "X is NumPy array. Reconstructing feature names."
            )

            feature_names = state.get(
                "selected_features",
                []
            )

            if not feature_names:

                feature_names = [
                    f"feature_{i}"
                    for i in range(X.shape[1])
                ]

            # Make sure feature count matches

            if len(feature_names) != X.shape[1]:

                feature_names = [
                    f"feature_{i}"
                    for i in range(X.shape[1])
                ]

            X_df = pd.DataFrame(
                X,
                columns=feature_names
            )

        else:

            X_df = pd.DataFrame(X)


        # ==================================================
        # REMOVE TARGET IF PRESENT
        # ==================================================

        if target and target in X_df.columns:

            X_df = X_df.drop(
                columns=[target]
            )


        # ==================================================
        # TARGET SERIES
        # ==================================================

        y = state.get("target_series")


        if y is None:

            if (
                isinstance(
                    state.get("clean_dataframe"),
                    pd.DataFrame
                )
                and target in state["clean_dataframe"].columns
            ):

                y = state["clean_dataframe"][target]

            elif (
                isinstance(
                    state.get("dataframe"),
                    pd.DataFrame
                )
                and target in state["dataframe"].columns
            ):

                y = state["dataframe"][target]


        # ==================================================
        # BASIC FEATURE INFORMATION
        # ==================================================

        feature_names = list(
            X_df.columns
        )


        logger.info(
            "Number of features: %d",
            len(feature_names)
        )


        # ==================================================
        # FEATURE IMPORTANCE
        # ==================================================

        feature_importance = {}


        # --------------------------------------------------
        # Tree-based models
        # --------------------------------------------------

        if hasattr(
            model,
            "feature_importances_"
        ):

            importances = (
                model.feature_importances_
            )

            # Safety check

            if len(importances) == len(
                feature_names
            ):

                feature_importance = {
                    str(feature_names[i]):
                    float(importances[i])

                    for i in range(
                        len(feature_names)
                    )
                }


        # --------------------------------------------------
        # Linear models
        # --------------------------------------------------

        elif hasattr(
            model,
            "coef_"
        ):

            coefficients = model.coef_

            if coefficients.ndim > 1:

                coefficients = np.mean(
                    np.abs(coefficients),
                    axis=0
                )

            else:

                coefficients = np.abs(
                    coefficients
                )

            if len(coefficients) == len(
                feature_names
            ):

                feature_importance = {
                    str(feature_names[i]):
                    float(coefficients[i])

                    for i in range(
                        len(feature_names)
                    )
                }


        # ==================================================
        # SORT FEATURE IMPORTANCE
        # ==================================================

        sorted_importance = sorted(
            feature_importance.items(),
            key=lambda x: x[1],
            reverse=True
        )


        # ==================================================
        # TOP FEATURES
        # ==================================================

        top_features = [
            {
                "feature": feature,
                "importance": importance
            }

            for feature, importance
            in sorted_importance[:20]
        ]


        # ==================================================
        # EXPLAINABILITY REPORT
        # ==================================================

        report = {

            "status": "completed",

            "model": type(model).__name__,

            "feature_count": len(
                feature_names
            ),

            "features": feature_names,

            "feature_importance":
                dict(sorted_importance),

            "top_features":
                top_features
        }


        # ==================================================
        # SAVE REPORT
        # ==================================================

        os.makedirs(
            "reports",
            exist_ok=True
        )


        with open(
            "reports/explainability.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                report,
                f,
                indent=4
            )


        # ==================================================
        # UPDATE STATE
        # ==================================================

        state[
            "explainability_report"
        ] = report


        state[
            "messages"
        ].append(
            "Explainability Analysis Completed"
        )


        logger.info(
            "Explainability completed successfully."
        )

        logger.info(
            "Top features: %s",
            top_features[:5]
        )

        logger.info("=" * 60)


        return state


    except Exception as e:

        logger.exception(
            "Explainability Agent Failed"
        )


        # IMPORTANT:
        # Don't crash the entire Streamlit pipeline
        # because explainability is an optional stage.

        state[
            "explainability_report"
        ] = {

            "status": "failed",

            "error": str(e),

            "type": type(e).__name__
        }


        state[
            "messages"
        ].append(
            f"Explainability failed: {str(e)}"
        )


        return state