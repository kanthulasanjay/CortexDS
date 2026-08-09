import joblib
import os

import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder


def build_preprocessor(df, target):

    X = df.drop(columns=[target])

    numeric = X.select_dtypes(include="number").columns.tolist()

    categorical = X.select_dtypes(exclude="number").columns.tolist()

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore"))
        ]
    )

    preprocessor = ColumnTransformer(

        transformers=[

            ("num", numeric_pipeline, numeric),

            ("cat", categorical_pipeline, categorical)

        ]

    )

    return preprocessor


def fit_pipeline(df, target):

    X = df.drop(columns=[target])

    y = df[target]

    preprocessor = build_preprocessor(df, target)

    X_processed = preprocessor.fit_transform(X)

    os.makedirs("models", exist_ok=True)

    joblib.dump(
        preprocessor,
        "models/pipeline.pkl"
    )

    return X_processed, y, preprocessor