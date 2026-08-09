import os
import json
import streamlit as st
import pandas as pd
import plotly.express as px


def show_explainability(state):
    """
    Explainability Dashboard
    """

    st.title("📈 Explainability")

    if state is None:
        st.info("Run the AI Pipeline first.")
        return

    report_path = "reports/explainability/xai_report.json"

    report = {}

    if os.path.exists(report_path):
        with open(report_path, "r") as f:
            report = json.load(f)

    # ====================================================
    # Model Information
    # ====================================================

    st.subheader("Model Information")

    c1, c2 = st.columns(2)

    c1.metric(
        "Best Model",
        state.get("model_name", "-")
    )

    c2.metric(
        "Selected Features",
        len(state.get("selected_features", []))
    )

    st.divider()

    # ====================================================
    # SHAP Summary Plot
    # ====================================================

    st.subheader("SHAP Summary")

    shap_summary = "reports/explainability/shap_summary.png"

    if os.path.exists(shap_summary):

        st.image(
            shap_summary,
            use_container_width=True
        )

    else:

        st.warning("SHAP Summary not found.")

    st.divider()

    # ====================================================
    # SHAP Feature Importance
    # ====================================================

    st.subheader("SHAP Feature Importance")

    shap_bar = "reports/explainability/shap_feature_importance.png"

    if os.path.exists(shap_bar):

        st.image(
            shap_bar,
            use_container_width=True
        )

    else:

        st.warning("Feature importance image not found.")

    st.divider()

    # ====================================================
    # LIME Explanation
    # ====================================================

    st.subheader("LIME Explanation")

    lime_file = "reports/explainability/lime_explanation.html"

    if os.path.exists(lime_file):

        with open(
            lime_file,
            "r",
            encoding="utf-8"
        ) as f:

            html = f.read()

        st.components.v1.html(
            html,
            height=700,
            scrolling=True
        )

    else:

        st.info("LIME explanation not available.")

    st.divider()

    # ====================================================
    # Feature Importance Table
    # ====================================================

    st.subheader("Top Features")

    importance = "reports/feature_importance.csv"

    if os.path.exists(importance):

        df = pd.read_csv(importance)

        st.dataframe(
            df,
            use_container_width=True
        )

        if {
            "feature",
            "importance"
        }.issubset(df.columns):

            fig = px.bar(

                df.sort_values(
                    "importance",
                    ascending=False
                ),

                x="importance",

                y="feature",

                orientation="h",

                title="Feature Importance"

            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    st.divider()

    # ====================================================
    # XAI Report
    # ====================================================

    st.subheader("Explainability Report")

    if report:

        st.json(report)

    else:

        st.info("Explainability report not found.")

    st.divider()

    # ====================================================
    # AI Explanation
    # ====================================================

    st.subheader("AI Explanation")

    explanation = report.get("summary")

    if explanation:

        st.success(explanation)

    else:

        st.info(
            "No AI explanation available."
        )

    st.divider()

    # ====================================================
    # Download Report
    # ====================================================

    st.subheader("Download Explainability Report")

    if os.path.exists(report_path):

        with open(report_path, "rb") as f:

            st.download_button(

                "Download JSON",

                data=f.read(),

                file_name="xai_report.json",

                mime="application/json"

            )

    st.success("Explainability Completed ✅")