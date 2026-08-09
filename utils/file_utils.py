import os
import pandas as pd


def clean_columns(df):
    """Clean column names."""

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    return df


def load_dataset(path):
    """Load CSV, XLS, XLSX, or CSV disguised as XLS."""

    if not os.path.isfile(path):
        raise FileNotFoundError(
            f"Dataset not found: {path}"
        )

    extension = os.path.splitext(path)[1].lower()

    # --------------------------------------------------
    # CSV
    # --------------------------------------------------

    if extension == ".csv":

        df = pd.read_csv(
            path,
            encoding="utf-8-sig"
        )

        return clean_columns(df)

    # --------------------------------------------------
    # XLS
    # --------------------------------------------------

    if extension == ".xls":

        try:

            # Try real XLS first
            df = pd.read_excel(
                path,
                engine="xlrd"
            )

            return clean_columns(df)

        except Exception:

            # Some files have .xls extension
            # but are actually CSV files.

            df = pd.read_csv(
                path,
                encoding="utf-8-sig"
            )

            return clean_columns(df)

    # --------------------------------------------------
    # XLSX
    # --------------------------------------------------

    if extension == ".xlsx":

        df = pd.read_excel(
            path,
            engine="openpyxl"
        )

        return clean_columns(df)

    # --------------------------------------------------
    # UNKNOWN FORMAT
    # --------------------------------------------------

    raise ValueError(
        f"Unsupported dataset format: {extension}"
    )