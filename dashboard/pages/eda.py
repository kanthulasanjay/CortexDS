import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


def show_eda(state):
    """
    Interactive Exploratory Data Analysis Page
    """

    st.title("📊 Exploratory Data Analysis")

    if state is None:
        st.info("Run the pipeline first.")
        return

    df = state.get("dataframe")

    if df is None:
        st.warning("No dataset available.")
        return

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=np.number).columns.tolist()

    # ====================================================
    # Dataset Summary
    # ====================================================

    st.subheader("Dataset Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows", len(df))
    c2.metric("Columns", len(df.columns))
    c3.metric("Numeric", len(numeric_cols))
    c4.metric("Categorical", len(categorical_cols))

    st.divider()

    # ====================================================
    # Histogram
    # ====================================================

    if numeric_cols:

        st.subheader("Histogram")

        col = st.selectbox(
            "Select Numeric Column",
            numeric_cols,
            key="histogram"
        )

        fig = px.histogram(
            df,
            x=col,
            nbins=30,
            title=f"Distribution of {col}"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # ====================================================
    # Box Plot
    # ====================================================

    if numeric_cols:

        st.subheader("Box Plot")

        col = st.selectbox(
            "Select Column",
            numeric_cols,
            key="box"
        )

        fig = px.box(
            df,
            y=col,
            title=f"Box Plot - {col}"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # ====================================================
    # Correlation Heatmap
    # ====================================================

    if len(numeric_cols) >= 2:

        st.subheader("Correlation Heatmap")

        corr = df[numeric_cols].corr()

        fig = px.imshow(
            corr,
            text_auto=".2f",
            aspect="auto",
            color_continuous_scale="RdBu_r",
            title="Correlation Matrix"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # ====================================================
    # Scatter Plot
    # ====================================================

    if len(numeric_cols) >= 2:

        st.subheader("Scatter Plot")

        x = st.selectbox(
            "X Axis",
            numeric_cols,
            key="scatter_x"
        )

        y = st.selectbox(
            "Y Axis",
            numeric_cols,
            index=min(1, len(numeric_cols)-1),
            key="scatter_y"
        )

        color = None

        if categorical_cols:
            color = st.selectbox(
                "Color By",
                ["None"] + categorical_cols
            )

        fig = px.scatter(
            df,
            x=x,
            y=y,
            color=None if color == "None" else color,
            title=f"{x} vs {y}"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # ====================================================
    # Missing Values
    # ====================================================

    st.subheader("Missing Values")

    missing = pd.DataFrame({

        "Column": df.columns,

        "Missing": df.isnull().sum(),

        "Percentage":
            (
                df.isnull().sum()
                / len(df)
                * 100
            ).round(2)

    })

    st.dataframe(
        missing,
        use_container_width=True
    )

    st.divider()

    # ====================================================
    # Pie Chart
    # ====================================================

    if categorical_cols:

        st.subheader("Category Distribution")

        cat = st.selectbox(
            "Select Category",
            categorical_cols
        )

        vc = df[cat].value_counts()

        fig = px.pie(

            names=vc.index,

            values=vc.values,

            title=cat

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # ====================================================
    # Target Distribution
    # ====================================================

    target = state.get("target")

    if target and target in df.columns:

        st.subheader("Target Distribution")

        fig = px.histogram(
            df,
            x=target,
            color=target
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # ====================================================
    # Numeric Summary
    # ====================================================

    st.subheader("Numeric Summary")

    if numeric_cols:

        st.dataframe(
            df[numeric_cols].describe().T,
            use_container_width=True
        )

    st.divider()

    # ====================================================
    # Correlation Table
    # ====================================================

    if len(numeric_cols) >= 2:

        st.subheader("Correlation Table")

        st.dataframe(
            corr.round(3),
            use_container_width=True
        )

    st.success("EDA Completed Successfully ✅")