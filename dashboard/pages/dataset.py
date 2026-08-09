import pandas as pd
import streamlit as st


def show_dataset(state):
    """
    Display uploaded dataset information.
    """

    st.title("📂 Dataset Explorer")

    if state is None:
        st.info("Run the pipeline first.")
        return

    df = state.get("dataframe")

    if df is None:
        st.warning("Dataset not found.")
        return

    # -----------------------------
    # Dataset Overview
    # -----------------------------
    st.subheader("Dataset Overview")

    c1, c2, c3 = st.columns(3)

    c1.metric("Rows", df.shape[0])
    c2.metric("Columns", df.shape[1])
    c3.metric("Missing Values", int(df.isna().sum().sum()))

    st.divider()

    # -----------------------------
    # Preview
    # -----------------------------
    st.subheader("Preview")

    rows = st.slider(
        "Rows to Display",
        5,
        min(100, len(df)),
        10,
    )

    st.dataframe(
        df.head(rows),
        use_container_width=True,
    )

    st.divider()

    # -----------------------------
    # Column Information
    # -----------------------------
    st.subheader("Columns")

    info = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str),
        "Missing": df.isnull().sum().values,
        "Unique": df.nunique().values
    })

    st.dataframe(
        info,
        use_container_width=True,
    )

    st.divider()

    # -----------------------------
    # Statistics
    # -----------------------------
    st.subheader("Statistics")

    st.dataframe(
        df.describe(include="all").T,
        use_container_width=True,
    )

    st.divider()

    # -----------------------------
    # Missing Values
    # -----------------------------
    st.subheader("Missing Values")

    missing = pd.DataFrame({
        "Column": df.columns,
        "Missing Count": df.isna().sum().values,
        "Missing %": (
            df.isna().sum().values
            / len(df)
            * 100
        ).round(2)
    })

    st.dataframe(
        missing.sort_values(
            "Missing %",
            ascending=False
        ),
        use_container_width=True,
    )

    st.divider()

    # -----------------------------
    # Single Column Explorer
    # -----------------------------
    st.subheader("Column Explorer")

    column = st.selectbox(
        "Select Column",
        df.columns
    )

    st.write(f"### {column}")

    st.write(df[column])

    st.write("Value Counts")

    st.dataframe(
        df[column]
        .value_counts(dropna=False)
        .reset_index()
        .rename(
            columns={
                "index": column,
                column: "Count"
            }
        ),
        use_container_width=True,
    )