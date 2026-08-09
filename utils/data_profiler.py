import pandas as pd


def profile_dataset(df: pd.DataFrame):

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    categorical_cols = df.select_dtypes(exclude="number").columns.tolist()

    profile = {

        "rows": df.shape[0],

        "columns": df.shape[1],

        "missing_values": df.isnull().sum().sum(),

        "duplicate_rows": df.duplicated().sum(),

        "memory_mb": round(
            df.memory_usage(deep=True).sum()/1024**2,
            2
        ),

        "numeric_columns": numeric_cols,

        "categorical_columns": categorical_cols,

        "dtypes": {
            c: str(df[c].dtype)
            for c in df.columns
        }

    }

    return profile