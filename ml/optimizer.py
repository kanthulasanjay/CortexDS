import numpy as np

import optuna

from sklearn.model_selection import train_test_split

from sklearn.metrics import (
    accuracy_score,
    r2_score
)

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


class HyperparameterOptimizer:

    # ======================================================
    # MAIN OPTIMIZER
    # ======================================================

    def optimize(
        self,
        model_name,
        X,
        y,
        n_trials=10
    ):

        # ==================================================
        # CONVERT X
        # ==================================================

        if hasattr(X, "values"):

            X = X.values

        else:

            X = np.asarray(X)

        # ==================================================
        # CONVERT Y
        # ==================================================

        if hasattr(y, "values"):

            y = y.values

        else:

            y = np.asarray(y)

        y = y.ravel()

        # ==================================================
        # CLEAN NUMERIC VALUES
        # ==================================================

        X = np.asarray(
            X,
            dtype=np.float64
        )

        X = np.nan_to_num(
            X,
            nan=0.0,
            posinf=0.0,
            neginf=0.0
        )

        # ==================================================
        # DETERMINE PROBLEM TYPE
        # ==================================================

        classification_models = {

            "Logistic Regression",
            "Random Forest Classifier",
            "Gradient Boosting Classifier",
            "XGBoost Classifier"
        }

        regression_models = {

            "Linear Regression",
            "Random Forest Regressor",
            "Gradient Boosting Regressor",
            "XGBoost Regressor"
        }

        if model_name in classification_models:

            problem_type = "classification"

        elif model_name in regression_models:

            problem_type = "regression"

        else:

            raise ValueError(
                f"Unsupported model: {model_name}"
            )

        # ==================================================
        # TRAIN TEST SPLIT
        # ==================================================

        X_train, X_test, y_train, y_test = train_test_split(

            X,

            y,

            test_size=0.20,

            random_state=42,

            stratify=y
            if problem_type == "classification"
            else None
        )

        # ==================================================
        # OPTUNA OBJECTIVE
        # ==================================================

        def objective(trial):

            # ==============================================
            # CLASSIFICATION
            # ==============================================

            if model_name == "Logistic Regression":

                C = trial.suggest_float(
                    "C",
                    0.01,
                    10.0,
                    log=True
                )

                model = LogisticRegression(

                    C=C,

                    max_iter=2000,

                    random_state=42
                )

            elif model_name == "Random Forest Classifier":

                n_estimators = trial.suggest_int(
                    "n_estimators",
                    100,
                    250
                )

                max_depth = trial.suggest_int(
                    "max_depth",
                    4,
                    15
                )

                min_samples_split = trial.suggest_int(
                    "min_samples_split",
                    2,
                    10
                )

                model = RandomForestClassifier(

                    n_estimators=n_estimators,

                    max_depth=max_depth,

                    min_samples_split=min_samples_split,

                    random_state=42,

                    n_jobs=-1
                )

            elif model_name == "Gradient Boosting Classifier":

                n_estimators = trial.suggest_int(
                    "n_estimators",
                    50,
                    200
                )

                learning_rate = trial.suggest_float(
                    "learning_rate",
                    0.01,
                    0.2
                )

                max_depth = trial.suggest_int(
                    "max_depth",
                    2,
                    8
                )

                model = GradientBoostingClassifier(

                    n_estimators=n_estimators,

                    learning_rate=learning_rate,

                    max_depth=max_depth,

                    random_state=42
                )

            elif model_name == "XGBoost Classifier":

                n_estimators = trial.suggest_int(
                    "n_estimators",
                    100,
                    300
                )

                max_depth = trial.suggest_int(
                    "max_depth",
                    3,
                    10
                )

                learning_rate = trial.suggest_float(
                    "learning_rate",
                    0.01,
                    0.2
                )

                subsample = trial.suggest_float(
                    "subsample",
                    0.7,
                    1.0
                )

                colsample_bytree = trial.suggest_float(
                    "colsample_bytree",
                    0.7,
                    1.0
                )

                model = XGBClassifier(

                    n_estimators=n_estimators,

                    max_depth=max_depth,

                    learning_rate=learning_rate,

                    subsample=subsample,

                    colsample_bytree=colsample_bytree,

                    eval_metric="logloss",

                    random_state=42,

                    n_jobs=-1
                )

            # ==============================================
            # REGRESSION
            # ==============================================

            elif model_name == "Linear Regression":

                model = LinearRegression()

            elif model_name == "Random Forest Regressor":

                n_estimators = trial.suggest_int(
                    "n_estimators",
                    100,
                    250
                )

                max_depth = trial.suggest_int(
                    "max_depth",
                    4,
                    15
                )

                min_samples_split = trial.suggest_int(
                    "min_samples_split",
                    2,
                    10
                )

                model = RandomForestRegressor(

                    n_estimators=n_estimators,

                    max_depth=max_depth,

                    min_samples_split=min_samples_split,

                    random_state=42,

                    n_jobs=-1
                )

            elif model_name == "Gradient Boosting Regressor":

                n_estimators = trial.suggest_int(
                    "n_estimators",
                    50,
                    200
                )

                learning_rate = trial.suggest_float(
                    "learning_rate",
                    0.01,
                    0.2
                )

                max_depth = trial.suggest_int(
                    "max_depth",
                    2,
                    8
                )

                model = GradientBoostingRegressor(

                    n_estimators=n_estimators,

                    learning_rate=learning_rate,

                    max_depth=max_depth,

                    random_state=42
                )

            elif model_name == "XGBoost Regressor":

                n_estimators = trial.suggest_int(
                    "n_estimators",
                    100,
                    300
                )

                max_depth = trial.suggest_int(
                    "max_depth",
                    3,
                    10
                )

                learning_rate = trial.suggest_float(
                    "learning_rate",
                    0.01,
                    0.2
                )

                subsample = trial.suggest_float(
                    "subsample",
                    0.7,
                    1.0
                )

                colsample_bytree = trial.suggest_float(
                    "colsample_bytree",
                    0.7,
                    1.0
                )

                model = XGBRegressor(

                    n_estimators=n_estimators,

                    max_depth=max_depth,

                    learning_rate=learning_rate,

                    subsample=subsample,

                    colsample_bytree=colsample_bytree,

                    objective="reg:squarederror",

                    random_state=42,

                    n_jobs=-1
                )

            else:

                raise ValueError(
                    f"Unsupported model: {model_name}"
                )

            # ==============================================
            # TRAIN
            # ==============================================

            model.fit(
                X_train,
                y_train
            )

            # ==============================================
            # PREDICT
            # ==============================================

            predictions = model.predict(
                X_test
            )

            # ==============================================
            # SCORE
            # ==============================================

            if problem_type == "classification":

                score = accuracy_score(
                    y_test,
                    predictions
                )

            else:

                score = r2_score(
                    y_test,
                    predictions
                )

            return float(score)

        # ==================================================
        # CREATE OPTUNA STUDY
        # ==================================================

        study = optuna.create_study(

            direction="maximize"
        )

        # ==================================================
        # RUN ONLY SELECTED NUMBER OF TRIALS
        # ==================================================

        study.optimize(

            objective,

            n_trials=n_trials,

            show_progress_bar=False
        )

        # ==================================================
        # BEST PARAMETERS
        # ==================================================

        best_params = study.best_params

        best_score = study.best_value

        # ==================================================
        # BUILD BEST MODEL
        # ==================================================

        if model_name == "Logistic Regression":

            best_model = LogisticRegression(

                **best_params,

                max_iter=2000,

                random_state=42
            )

        elif model_name == "Random Forest Classifier":

            best_model = RandomForestClassifier(

                **best_params,

                random_state=42,

                n_jobs=-1
            )

        elif model_name == "Gradient Boosting Classifier":

            best_model = GradientBoostingClassifier(

                **best_params,

                random_state=42
            )

        elif model_name == "XGBoost Classifier":

            best_model = XGBClassifier(

                **best_params,

                eval_metric="logloss",

                random_state=42,

                n_jobs=-1
            )

        elif model_name == "Linear Regression":

            best_model = LinearRegression()

        elif model_name == "Random Forest Regressor":

            best_model = RandomForestRegressor(

                **best_params,

                random_state=42,

                n_jobs=-1
            )

        elif model_name == "Gradient Boosting Regressor":

            best_model = GradientBoostingRegressor(

                **best_params,

                random_state=42
            )

        elif model_name == "XGBoost Regressor":

            best_model = XGBRegressor(

                **best_params,

                objective="reg:squarederror",

                random_state=42,

                n_jobs=-1
            )

        else:

            raise ValueError(
                f"Unsupported model: {model_name}"
            )

        # ==================================================
        # TRAIN BEST MODEL ON FULL DATA
        # ==================================================

        best_model.fit(
            X,
            y
        )

        # ==================================================
        # RETURN
        # ==================================================

        return (
            best_params,
            float(best_score),
            best_model
        )