import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def show_dashboard(state):

    st.title("📊 Dashboard")

    if state is None:
        st.info("Upload a dataset and run the pipeline.")
        return

    summary = state.get("dataset_summary", {})
    quality = state.get("quality_report", {})
    metrics = state.get("metrics", {})

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows", summary.get("rows", 0))
    c2.metric("Columns", summary.get("columns", 0))
    c3.metric("Quality", quality.get("quality_score", 0))
    c4.metric("Problem", state.get("problem_type", "-"))

    st.divider()

    left, right = st.columns([1, 2])

    with left:

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=quality.get("quality_score", 0),
                title={"text": "Dataset Health"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "green"},
                },
            )
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:

        st.subheader("Agent Status")

        for message in state.get("messages", []):

            st.success(message)

    st.divider()

    if state.get("leaderboard"):

        st.subheader("🏆 Model Leaderboard")

        leaderboard = pd.DataFrame(state["leaderboard"])

        if "model_object" in leaderboard.columns:
            leaderboard = leaderboard.drop(columns=["model_object"])

        st.dataframe(
            leaderboard,
            use_container_width=True,
        )

    st.divider()

    if metrics:

        st.subheader("Performance")

        cols = st.columns(len(metrics))

        for i, (k, v) in enumerate(metrics.items()):

            cols[i].metric(k.upper(), round(v, 4))