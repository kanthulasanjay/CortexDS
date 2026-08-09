import os
import json
import pandas as pd
import plotly.express as px
import streamlit as st


def show_memory(state):
    """
    Memory Dashboard
    """

    st.title("🧠 AI Memory")

    memory_file = "memory_db/experiences.json"

    if not os.path.exists(memory_file):

        st.warning("No memory database found.")

        return

    with open(memory_file, "r") as f:

        memory = json.load(f)

    if len(memory) == 0:

        st.info("Memory is empty.")

        return

    df = pd.DataFrame(memory)

    # =====================================================
    # Metrics
    # =====================================================

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Stored Experiments",
        len(df)
    )

    c2.metric(
        "Unique Models",
        df["best_model"].nunique()
        if "best_model" in df.columns
        else 0
    )

    c3.metric(
        "Average Score",
        round(
            df["best_score"].mean(),
            4
        )
        if "best_score" in df.columns
        else 0
    )

    st.divider()

    # =====================================================
    # Search
    # =====================================================

    search = st.text_input(
        "Search Dataset"
    )

    if search:

        df = df[
            df["dataset_name"]
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    # =====================================================
    # Memory Table
    # =====================================================

    st.subheader("Stored Experiences")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.divider()

    # =====================================================
    # Best Models
    # =====================================================

    if "best_model" in df.columns:

        st.subheader("Best Model Distribution")

        model_count = (

            df["best_model"]

            .value_counts()

            .reset_index()

        )

        model_count.columns = [

            "Model",

            "Count"

        ]

        fig = px.bar(

            model_count,

            x="Model",

            y="Count",

            color="Count"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    st.divider()

    # =====================================================
    # Score History
    # =====================================================

    if {

        "dataset_name",

        "best_score"

    }.issubset(df.columns):

        st.subheader("Performance History")

        fig = px.line(

            df,

            x="dataset_name",

            y="best_score",

            markers=True

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    st.divider()

    # =====================================================
    # Similar Dataset Finder
    # =====================================================

    st.subheader("Similar Dataset Search")

    if state:

        current_problem = state.get(
            "problem_type"
        )

        similar = df[
            df["problem_type"]
            == current_problem
        ]

        st.write(
            f"Found **{len(similar)}** similar datasets."
        )

        st.dataframe(

            similar,

            use_container_width=True

        )

    st.divider()

    # =====================================================
    # Experiment Details
    # =====================================================

    st.subheader("Experiment Details")

    dataset = st.selectbox(

        "Choose Dataset",

        df["dataset_name"]

    )

    details = df[
        df["dataset_name"] == dataset
    ].iloc[0]

    st.json(
        details.to_dict()
    )

    st.divider()

    # =====================================================
    # Delete Memory
    # =====================================================

    st.subheader("Memory Management")

    if st.button("🗑 Clear Memory Database"):

        with open(memory_file, "w") as f:

            json.dump([], f)

        st.success(
            "Memory Cleared!"
        )

        st.rerun()

    st.success(
        "Memory Dashboard Loaded Successfully ✅"
    )