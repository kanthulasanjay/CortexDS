import json
import os


def save_cleaning_report(df, removed_duplicates, removed_constant_columns):

    os.makedirs("reports", exist_ok=True)

    report = {
        "rows_after_cleaning": len(df),
        "columns_after_cleaning": len(df.columns),
        "duplicates_removed": removed_duplicates,
        "constant_columns_removed": removed_constant_columns,
        "missing_values": df.isnull().sum().to_dict()
    }

    with open("reports/cleaning_report.json", "w") as f:
        json.dump(report, f, indent=4)