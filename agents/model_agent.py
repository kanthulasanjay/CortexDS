import numpy as np
import pandas as pd

from core.logger import logger

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.linear_model import (
    LogisticRegression,
    LinearRegression
)

from sklearn.ensemble import (
    RandomForestClassifier,
    RandomForestRegressor,
    GradientBoostingClassifier,
    GradientBoostingRegressor
)

from xgboost import (
    XGBClassifier,
    XGBRegressor
)

from sklearn.metrics import (
    accuracy_score,
    r2_score,
    mean_squared_error
)


# ==========================================================
# MODELS USED BY AI-DS OS
# ==========================================================

CLASSIFICATION_MODELS = [
    "Logistic Regression",
    "Random Forest Classifier",
    "Gradient Boosting Classifier",
    "XGBoost Classifier"
]


REGRESSION_MODELS = [
    "Linear Regression",
    "Random Forest Regressor",
    "Gradient Boosting Regressor",
    "XGBoost Regressor"
]


# ==========================================================
# MODEL REASONS
# ==========================================================

MODEL_REASONS = {

    "Logistic Regression":
        "Fast and interpretable baseline for classification.",

    "Random Forest Classifier":
        "Handles nonlinear relationships and is robust for structured tabular data.",

    "Gradient Boosting Classifier":
        "Builds strong predictive models by sequentially correcting previous errors.",

    "XGBoost Classifier":
        "Powerful gradient-boosting algorithm that performs well on structured tabular data.",

    "Linear Regression":
        "Simple and interpretable baseline for continuous numerical targets.",

    "Random Forest Regressor":
        "Captures nonlinear relationships and is robust against noisy features.",

    "Gradient Boosting Regressor":
        "Provides strong predictive performance for nonlinear regression problems.",

    "XGBoost Regressor":
        "Powerful gradient-boosting model for structured regression datasets."
}


# ==========================================================
# MODEL AGENT
# ==========================================================

def model_agent(state):

    logger.info("=" * 60)
    logger.info("MODEL AGENT STARTED")
    logger.info("=" * 60)

    # ======================================================
    # GET PROBLEM TYPE
    # ======================================================

    problem_type = str(
        state.get("problem_type", "")
    ).lower()

    if problem_type not in [
        "classification",
        "regression"
    ]:

        raise ValueError(
            f"Unsupported problem type: {problem_type}"
        )

    # ======================================================
    # GET FEATURES
    # ======================================================

    X = state.get("clean_dataframe")

    if X is None:

        raise ValueError(
            "clean_dataframe is empty. "
            "Feature Agent did not provide features."
        )

    # ======================================================
    # GET TARGET
    # ======================================================

    y = state.get("target_series")

    if y is None:

        raise ValueError(
            "target_series is empty. "
            "Cleaning/Feature Agent did not provide target values."
        )

    # ======================================================
    # CONVERT TARGET TO ARRAY / SERIES
    # ======================================================

    if isinstance(y, pd.DataFrame):

        if y.shape[1] != 1:

            raise ValueError(
                "target_series contains multiple columns."
            )

        y = y.iloc[:, 0]

    elif isinstance(y, np.ndarray):

        y = y.ravel()

    else:

        y = pd.Series(y)

    # ======================================================
    # CONVERT FEATURES
    # ======================================================

    if isinstance(X, pd.DataFrame):

        logger.info(
            "Feature data type: DataFrame"
        )

        X_model = X.copy()

        # ----------------------------------------------
        # Remove ID columns if still present
        # ----------------------------------------------

        id_columns = [
            column
            for column in X_model.columns
            if str(column).lower() in [
                "id",
                "customer_id",
                "customerid"
            ]
        ]

        if id_columns:

            X_model = X_model.drop(
                columns=id_columns
            )

            logger.info(
                "Removed ID columns: %s",
                id_columns
            )

        # ----------------------------------------------
        # Encode categorical columns
        # ----------------------------------------------

        categorical_columns = X_model.select_dtypes(
            include=[
                "object",
                "category",
                "bool"
            ]
        ).columns

        for column in categorical_columns:

            X_model[column] = (
                X_model[column]
                .astype("category")
                .cat.codes
            )

        # ----------------------------------------------
        # Handle infinity
        # ----------------------------------------------

        X_model = X_model.replace(
            [np.inf, -np.inf],
            np.nan
        )

        # ----------------------------------------------
        # Handle missing values
        # ----------------------------------------------

        X_model = X_model.fillna(0)

        X = X_model

    else:

        # ==================================================
        # FEATURE AGENT ALREADY PREPROCESSED DATA
        # ==================================================

        logger.info(
            "Feature data type: %s",
            type(X).__name__
        )

        X = np.asarray(X)

        # ----------------------------------------------
        # Handle infinity
        # ----------------------------------------------

        X = np.nan_to_num(
            X,
            nan=0.0,
            posinf=0.0,
            neginf=0.0
        )

    # ======================================================
    # CHECK DATA SHAPE
    # ======================================================

    logger.info(
        "Feature shape: %s",
        X.shape
    )

    logger.info(
        "Target shape: %s",
        y.shape
    )

    if len(X) != len(y):

        raise ValueError(
            f"Feature/target length mismatch. "
            f"X={len(X)}, y={len(y)}"
        )

    # ======================================================
    # TRAIN TEST SPLIT
    # ======================================================

    X_train, X_test, y_train, y_test = train_test_split(

        X,
        y,

        test_size=0.20,

        random_state=42,

        stratify=y
        if problem_type == "classification"
        else None
    )

    logger.info(
        "Training rows: %d",
        len(X_train)
    )

    logger.info(
        "Testing rows: %d",
        len(X_test)
    )

    # ======================================================
    # CLASSIFICATION MODELS
    # ======================================================

    if problem_type == "classification":

        candidate_models = {

            "Logistic Regression":

                Pipeline([
                    (
                        "scaler",
                        StandardScaler()
                    ),

                    (
                        "model",
                        LogisticRegression(
                            max_iter=2000,
                            random_state=42
                        )
                    )
                ]),

            "Random Forest Classifier":

                RandomForestClassifier(
                    n_estimators=150,
                    random_state=42,
                    n_jobs=-1
                ),

            "Gradient Boosting Classifier":

                GradientBoostingClassifier(
                    n_estimators=150,
                    learning_rate=0.05,
                    max_depth=5,
                    random_state=42
                ),

            "XGBoost Classifier":

                XGBClassifier(
                    n_estimators=150,
                    max_depth=6,
                    learning_rate=0.05,
                    subsample=0.9,
                    colsample_bytree=0.9,
                    eval_metric="logloss",
                    random_state=42,
                    n_jobs=-1
                )
        }

    # ======================================================
    # REGRESSION MODELS
    # ======================================================

    else:

        candidate_models = {

            "Linear Regression":

                Pipeline([
                    (
                        "scaler",
                        StandardScaler()
                    ),

                    (
                        "model",
                        LinearRegression()
                    )
                ]),

            "Random Forest Regressor":

                RandomForestRegressor(
                    n_estimators=150,
                    random_state=42,
                    n_jobs=-1
                ),

            "Gradient Boosting Regressor":

                GradientBoostingRegressor(
                    n_estimators=150,
                    learning_rate=0.05,
                    max_depth=5,
                    random_state=42
                ),

            "XGBoost Regressor":

                XGBRegressor(
                    n_estimators=150,
                    max_depth=6,
                    learning_rate=0.05,
                    subsample=0.9,
                    colsample_bytree=0.9,
                    objective="reg:squarederror",
                    random_state=42,
                    n_jobs=-1
                )
        }

    # ======================================================
    # CANDIDATE MODEL INFORMATION
    # ======================================================

    state["candidate_models"] = []

    for name in candidate_models:

        state["candidate_models"].append({

            "name": name,

            "model": name,

            "reason": MODEL_REASONS[name]
        })

    logger.info(
        "Selected %d models for %s",
        len(candidate_models),
        problem_type
    )

    # ======================================================
    # MODEL EVALUATION
    # ======================================================

    leaderboard = []

    best_model_name = None

    best_model = None

    best_score = float("-inf")

    for name, model in candidate_models.items():

        logger.info(
            "Training: %s",
            name
        )

        try:

            # ----------------------------------------------
            # TRAIN
            # ----------------------------------------------

            model.fit(
                X_train,
                y_train
            )

            # ----------------------------------------------
            # PREDICT
            # ----------------------------------------------

            predictions = model.predict(
                X_test
            )

            # ==================================================
            # CLASSIFICATION
            # ==================================================

            if problem_type == "classification":

                accuracy = accuracy_score(
                    y_test,
                    predictions
                )

                score = float(accuracy)

                entry = {

                    "name": name,

                    "model": name,

                    "accuracy": score,

                    "score": score,

                    "reason":
                        MODEL_REASONS[name]
                }

            # ==================================================
            # REGRESSION
            # ==================================================

            else:

                r2 = r2_score(
                    y_test,
                    predictions
                )

                rmse = float(
                    np.sqrt(
                        mean_squared_error(
                            y_test,
                            predictions
                        )
                    )
                )

                score = float(r2)

                entry = {

                    "name": name,

                    "model": name,

                    "r2_score": score,

                    "score": score,

                    "rmse": rmse,

                    "reason":
                        MODEL_REASONS[name]
                }

            leaderboard.append(
                entry
            )

            # ==================================================
            # BEST MODEL
            # ==================================================

            if score > best_score:

                best_score = score

                best_model_name = name

                best_model = model

        except Exception as e:

            logger.exception(
                "Model failed: %s",
                name
            )

            leaderboard.append({

                "name": name,

                "model": name,

                "error": str(e),

                "reason":
                    MODEL_REASONS[name]
            })

    # ======================================================
    # CHECK MODELS
    # ======================================================

    if best_model is None:

        raise RuntimeError(
            "All candidate models failed."
        )

    # ======================================================
    # SAVE RESULTS
    # ======================================================

    state["leaderboard"] = leaderboard

    state["model_name"] = best_model_name

    state["best_model"] = best_model

    # ======================================================
    # METRICS
    # ======================================================

    if problem_type == "classification":

        state["metrics"] = {

            "accuracy":
                float(best_score)
        }

        state["model_selection_reason"] = (

            f"{best_model_name} was selected because "
            f"it achieved the highest accuracy of "
            f"{best_score:.4f} among the four selected "
            f"classification models."
        )

    else:

        best_entry = next(

            (
                item
                for item in leaderboard
                if item.get("name")
                == best_model_name
            ),

            {}
        )

        state["metrics"] = {

            "r2_score":
                float(best_score),

            "rmse":
                float(
                    best_entry.get(
                        "rmse",
                        0.0
                    )
                )
        }

        state["model_selection_reason"] = (

            f"{best_model_name} was selected because "
            f"it achieved the highest R² score of "
            f"{best_score:.4f} among the four selected "
            f"regression models."
        )

    # ======================================================
    # AGENT MESSAGES
    # ======================================================

    state["messages"].append(

        f"Model Agent evaluated "
        f"{len(candidate_models)} selected models."
    )

    state["messages"].append(

        f"Best Model: {best_model_name}"
    )

    if problem_type == "classification":

        state["messages"].append(

            f"Best Accuracy: {best_score:.4f}"
        )

    else:

        state["messages"].append(

            f"Best R² Score: {best_score:.4f}"
        )

    # ======================================================
    # LOG
    # ======================================================

    logger.info(
        "Best Model: %s",
        best_model_name
    )

    logger.info(
        "Score: %.4f",
        best_score
    )

    logger.info("=" * 60)
    logger.info("MODEL AGENT FINISHED")
    logger.info("=" * 60)

    return state