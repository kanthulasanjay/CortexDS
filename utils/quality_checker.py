import numpy as np

from utils.outlier_detector import detect_outliers
from utils.leakage_detector import detect_target_leakage


def quality_report(df, target):

    report = {}

    report["missing"] = (
        df.isnull()
          .sum()
          .to_dict()
    )

    report["duplicates"] = int(
        df.duplicated().sum()
    )

    report["constant_columns"] = [

        c for c in df.columns

        if df[c].nunique() == 1

    ]

    numeric = df.select_dtypes(include=np.number)

    report["low_variance"] = [

        c

        for c in numeric.columns

        if numeric[c].var() < 1e-5

    ]

    report["high_cardinality"] = [

        c

        for c in df.select_dtypes(exclude=np.number)

        if df[c].nunique() > 100

    ]

    report["outliers"] = detect_outliers(df)

    report["target_leakage"] = detect_target_leakage(
        df,
        target
    )

    report["datetime_columns"] = [

        c

        for c in df.columns

        if "date" in c.lower()
        or "time" in c.lower()

    ]

    score = 100

    score -= len(report["constant_columns"]) * 5

    score -= report["duplicates"] * 0.01

    score -= sum(report["missing"].values()) * 0.01

    score -= len(report["target_leakage"]) * 10

    score = max(0, min(100, round(score,2)))

    report["quality_score"] = score

    recommendations = []

    if sum(report["missing"].values()) > 0:
        recommendations.append(
            "Handle missing values."
        )

    if report["duplicates"] > 0:
        recommendations.append(
            "Remove duplicate rows."
        )

    if len(report["constant_columns"]) > 0:
        recommendations.append(
            "Drop constant columns."
        )

    if len(report["target_leakage"]) > 0:
        recommendations.append(
            "Potential target leakage detected."
        )

    report["recommendations"] = recommendations

    return report