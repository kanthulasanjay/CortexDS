import os
import json
import joblib
import pandas as pd
import plotly.express as px
import streamlit as st


def show_models(state):
    """
    Model Dashboard
    """

    st.title("🏆 Model Intelligence")

    if state is None:
        st.info("Run the AI Pipeline first.")
        return

    leaderboard = state.get("leaderboard", [])

    model_name = state.get("model_name", "Not Selected")

    metrics = state.get("metrics", {})

    debate = state.get("debate", [])

    manager = state.get("manager_decision", {})

    # =====================================================
    # BEST MODEL
    # =====================================================

    st.subheader("🥇 Best Model")

    col1, col2 = st.columns(2)

    col1.metric(
        "Selected Model",
        model_name
    )

    if metrics:

        accuracy = metrics.get("accuracy", 0)

        col2.metric(
            "Accuracy",
            round(accuracy, 4)
        )

    st.divider()

    # =====================================================
    # LEADERBOARD
    # =====================================================

    st.subheader("🏆 Leaderboard")

    if leaderboard:

        df = pd.DataFrame(leaderboard)

        if "model_object" in df.columns:
            df = df.drop(columns=["model_object"])

        st.dataframe(
            df,
            use_container_width=True
        )

        metric_column = None

        for col in [
            "accuracy",
            "f1",
            "roc_auc",
            "score"
        ]:

            if col in df.columns:
                metric_column = col
                break

        if metric_column:

            fig = px.bar(

                df.sort_values(
                    metric_column,
                    ascending=False
                ),

                x="model",

                y=metric_column,

                color=metric_column,

                title="Model Comparison"

            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    else:

        st.warning("Leaderboard not available.")

    st.divider()

    # =====================================================
    # METRICS
    # =====================================================

    st.subheader("Performance Metrics")

    if metrics:

        cols = st.columns(len(metrics))

        for i, (k, v) in enumerate(metrics.items()):

            cols[i].metric(
                k.upper(),
                round(v, 4)
            )

    st.divider()

    # =====================================================
    # MODEL DEBATE
    # =====================================================

    st.subheader("💬 Model Debate")

    if debate:

        for model in debate:

            with st.expander(model["model"]):

                st.write(model["argument"])

    else:

        st.info("Debate not available.")

    st.divider()

    # =====================================================
    # MANAGER DECISION
    # =====================================================

    st.subheader("🤖 Manager Agent")

    if manager:

        if isinstance(manager, dict):

            st.success(
                manager.get(
                    "reason",
                    "Decision Completed"
                )
            )

            st.json(manager)

        else:

            st.write(manager)

    else:

        st.warning("Manager decision not available.")

    st.divider()

    # =====================================================
    # DOWNLOAD MODEL
    # =====================================================

    st.subheader("📥 Download Model")

    model_path = "models/best_model.pkl"

    if os.path.exists(model_path):

        with open(model_path, "rb") as f:

            st.download_button(

                label="Download Best Model",

                data=f.read(),

                file_name="best_model.pkl",

                mime="application/octet-stream"

            )

    else:

        st.info("Best model has not been saved yet.")

    st.divider()

    # =====================================================
    # TUNING RESULTS
    # =====================================================

    tuning = "reports/tuning_results.json"

    if os.path.exists(tuning):

        st.subheader("Hyperparameter Optimization")

        with open(tuning) as f:

            report = json.load(f)

        st.json(report)

    st.success("Model Analysis Completed ✅")