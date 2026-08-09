from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

import xgboost as xgb
import lightgbm as lgb
from catboost import CatBoostClassifier


class AutoTrainer:

    def train(self, X, y):

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

        models = {

            "Random Forest":
                RandomForestClassifier(),

            "Logistic Regression":
                LogisticRegression(max_iter=1000),

            "XGBoost":
                xgb.XGBClassifier(),

            "LightGBM":
                lgb.LGBMClassifier(),

            "CatBoost":
                CatBoostClassifier(verbose=False)

        }

        leaderboard = []

        for name, model in models.items():

            model.fit(X_train, y_train)

            pred = model.predict(X_test)

            score = accuracy_score(
                y_test,
                pred
            )

            leaderboard.append({

                "model": name,

                "accuracy": round(score,4),

                "model_object": model

            })

        leaderboard.sort(
            key=lambda x: x["accuracy"],
            reverse=True
        )

        return leaderboard