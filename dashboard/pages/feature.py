import os
import json
import pandas as pd
import plotly.express as px
import streamlit as st


def show_feature_engineering(state):
    """
    Feature Engineering Dashboard
    """

    st.title("🧠 Feature Engineering")

    if state is None:
        st.info("Run the pipeline first.")
        return

    # =====================================================
    # Load Feature Report
    # =====================================================

    report_path = "reports/feature_report.json"

    report = {}

    if os.path.exists(report_path):

        with open(report_path, "r") as f:

            report = json.load(f)

    selected = state.get("selected_features", [])

    generated = report.get("generated_features", [])

    removed = report.get("removed_features", [])

    feature_types = report.get("feature_types", {})

    # =====================================================
    # Metrics
    # =====================================================

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Selected Features",
        len(selected)
    )

    c2.metric(
        "Generated Features",
        len(generated)
    )

    c3.metric(
        "Removed Features",
        len(removed)
    )

    st.divider()

    # =====================================================
    # Feature Types
    # =====================================================

    st.subheader("Feature Types")

    if feature_types:

        types_df = pd.DataFrame({

            "Type": feature_types.keys(),

            "Count": [

                len(v)

                for v in feature_types.values()

            ]

        })

        fig = px.pie(

            types_df,

            names="Type",

            values="Count",

            title="Feature Type Distribution"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    st.divider()

    # =====================================================
    # Selected Features
    # =====================================================

    st.subheader("Selected Features")

    if selected:

        df = pd.DataFrame({

            "Feature": selected

        })

        search = st.text_input(
            "Search Feature"
        )

        if search:

            df = df[
                df["Feature"].str.contains(
                    search,
                    case=False
                )
            ]

        st.dataframe(
            df,
            use_container_width=True
        )

    st.divider()

    # =====================================================
    # Generated Features
    # =====================================================

    st.subheader("Generated Features")

    if generated:

        st.dataframe(

            pd.DataFrame({

                "Generated": generated

            }),

            use_container_width=True

        )

    else:

        st.info("No generated features.")

    st.divider()

    # =====================================================
    # Removed Features
    # =====================================================

    st.subheader("Removed Features")

    if removed:

        st.dataframe(

            pd.DataFrame({

                "Removed": removed

            }),

            use_container_width=True

        )

    else:

        st.success(
            "No removed features."
        )

    st.divider()

    # =====================================================
    # Feature Importance
    # =====================================================

    st.subheader("Feature Importance")

    importance_path = "reports/feature_importance.csv"

    if os.path.exists(importance_path):

        importance = pd.read_csv(
            importance_path
        )

        st.dataframe(
            importance,
            use_container_width=True
        )

        if {

            "feature",
            "importance"

        }.issubset(importance.columns):

            fig = px.bar(

                importance.sort_values(
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

    else:

        st.warning(
            "Feature importance file not found."
        )

    st.divider()

    # =====================================================
    # SHAP Feature Importance
    # =====================================================

    st.subheader("SHAP Feature Importance")

    shap_plot = "reports/explainability/shap_summary.png"

    if os.path.exists(shap_plot):

        st.image(

            shap_plot,

            use_container_width=True

        )

    else:

        st.info(
            "SHAP plot not generated."
        )

    st.divider()

    # =====================================================
    # Feature Correlation
    # =====================================================

    st.subheader("Correlation with Target")

    df = state.get("dataframe")

    target = state.get("target")

    if (
        isinstance(df, pd.DataFrame)
        and target in df.columns
    ):

        numeric = df.select_dtypes(
            include="number"
        )

        if target in numeric.columns:

            corr = numeric.corr()[target]

            corr_df = (

                corr.reset_index()

                .rename(

                    columns={

                        "index": "Feature",

                        target: "Correlation"

                    }

                )

            )

            st.dataframe(

                corr_df,

                use_container_width=True

            )

            fig = px.bar(

                corr_df.sort_values(

                    "Correlation",

                    ascending=False

                ),

                x="Correlation",

                y="Feature",

                orientation="h"

            )

            st.plotly_chart(

                fig,

                use_container_width=True

            )

    st.success(
        "Feature Engineering Completed ✅"
    )