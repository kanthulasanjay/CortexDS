from core.logger import logger

from ml.preprocessing import fit_pipeline
from utils.save_cleaning_report import save_cleaning_report
from utils.label_encoder import encode_target


def cleaning_agent(state):

    logger.info("Cleaning Agent Started")

    df = state["dataframe"]
    target = state["target"]

    duplicates_before = len(df)

    # Remove duplicates
    df = df.drop_duplicates()

    duplicates_removed = duplicates_before - len(df)

    # Encode target labels
    df, encoder = encode_target(df, target)

    state["target_encoder"] = encoder

    # Remove constant columns
    constant_columns = [
        c for c in df.columns
        if df[c].nunique() == 1
    ]

    df = df.drop(columns=constant_columns)

    # Save cleaning report
    save_cleaning_report(
        df,
        duplicates_removed,
        constant_columns
    )

    # Build preprocessing pipeline
    X, y, pipeline = fit_pipeline(df, target)

    state["clean_dataframe"] = X
    state["target_series"] = y
    state["preprocessing_pipeline"] = pipeline
    state["dataframe"] = df

    state["messages"].append("Cleaning Completed")

    logger.info("Cleaning Finished")

    return state