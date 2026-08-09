from core.logger import logger

from ml.feature_engineering.detector import FeatureDetector

from ml.feature_engineering.generator import (
    FeatureGenerator,
    generate_datetime
)

from ml.feature_engineering.selector import FeatureSelector

from ml.feature_engineering.ranker import FeatureRanker

from ml.feature_engineering.report import save_feature_report


def feature_agent(state):

    logger.info("Feature Agent Started")

    df = state["dataframe"].copy()

    target = state["target"]

    detector = FeatureDetector(df)

    feature_types = detector.detect()

    generator = FeatureGenerator(df)

    df, created = generator.generate()

    df, datetime_created = generate_datetime(df)

    selector = FeatureSelector(df)

    df, removed = selector.remove_correlated()

    X = df.drop(columns=[target])

    y = df[target]

    # Only numeric features for MI
    X_numeric = X.select_dtypes(include="number").fillna(0)

    ranker = FeatureRanker()

    ranking = ranker.rank(X_numeric, y)

    state["dataframe"] = df

    state["selected_features"] = ranking["feature"].head(20).tolist()

    report = {

        "feature_types": feature_types,

        "generated_features": created + datetime_created,

        "removed_features": removed,

        "top_features": state["selected_features"]

    }

    save_feature_report(report)

    state["messages"].append(
        "Feature Engineering Completed"
    )

    logger.info("Feature Engineering Finished")

    return state