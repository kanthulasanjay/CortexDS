import logging

from utils.file_utils import load_dataset


logger = logging.getLogger(__name__)


def dataset_agent(state):

    logger.info("Loading Dataset...")

    df = load_dataset(
        state["dataset_path"]
    )

    state["dataframe"] = df

    state["dataset_summary"] = {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": df.columns.tolist(),
        "missing_values": int(
            df.isnull().sum().sum()
        ),
        "duplicates": int(
            df.duplicated().sum()
        )
    }

    target = state["target"]

    if target not in df.columns:

        raise ValueError(
            f"Target column '{target}' "
            f"not found.\n"
            f"Available columns: "
            f"{df.columns.tolist()}"
        )

    if df[target].dtype == "object":

        state["problem_type"] = "classification"

    elif df[target].nunique() <= 20:

        state["problem_type"] = "classification"

    else:

        state["problem_type"] = "regression"

    logger.info(
        "Columns: %s",
        df.columns.tolist()
    )

    logger.info(
        "Dataset Agent Completed"
    )

    return state