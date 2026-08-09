from pathlib import Path

import pandas as pd


def load_dataset(file_path: str) -> pd.DataFrame:

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    suffix = path.suffix.lower()

    if suffix == ".csv":

        df = pd.read_csv(
            path,
            encoding="utf-8-sig"
        )

    elif suffix == ".xls":

        df = pd.read_excel(
            path,
            engine="xlrd"
        )

    elif suffix == ".xlsx":

        df = pd.read_excel(
            path,
            engine="openpyxl"
        )

    elif suffix == ".parquet":

        df = pd.read_parquet(path)

    else:

        raise ValueError(
            f"Unsupported dataset format: {suffix}"
        )

    if df.empty:
        raise ValueError("Dataset is empty.")

    # Clean column names
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    return df