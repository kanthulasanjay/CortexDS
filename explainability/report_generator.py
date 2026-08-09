import json
import os


def save_xai_report(report):

    os.makedirs(
        "reports/explainability",
        exist_ok=True
    )

    with open(

        "reports/explainability/xai_report.json",

        "w"

    ) as f:

        json.dump(

            report,

            f,

            indent=4,

            default=str

        )