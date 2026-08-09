import json
import os

def save_feature_report(report):

    os.makedirs("reports",exist_ok=True)

    with open(

        "reports/feature_report.json",

        "w"

    ) as f:

        json.dump(

            report,

            f,

            indent=4,

            default=str

        )