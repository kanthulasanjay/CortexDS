import os
import json
import streamlit as st
import plotly.graph_objects as go


def show_business(state):
    """
    Business Intelligence Dashboard
    """

    st.title("💼 Business Intelligence")

    if state is None:
        st.info("Run the AI Pipeline first.")
        return

    report = state.get("business_report", {})

    if not report:

        report_file = "reports/business/executive_report.json"

        if os.path.exists(report_file):

            with open(report_file, "r") as f:
                report = json.load(f)

    if not report:

        st.warning("Business report not found.")
        return

    # =========================================================
    # Executive Summary
    # =========================================================

    st.subheader("📄 Executive Summary")

    summary = report.get(
        "executive_summary",
        "Not available."
    )

    st.info(summary)

    st.divider()

    # =========================================================
    # Business Insights
    # =========================================================

    st.subheader("💡 Business Insights")

    insights = report.get("insights", [])

    if insights:

        for item in insights:
            st.success(item)

    else:
        st.info("No business insights available.")

    st.divider()

    # =========================================================
    # ROI
    # =========================================================

    roi = report.get("roi", {})

    st.subheader("💰 ROI Estimation")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Customers",
        roi.get("customers", 0)
    )

    c2.metric(
        "Prevented Defaults",
        roi.get(
            "estimated_prevented_defaults",
            0
        )
    )

    c3.metric(
        "Estimated Savings",
        f"₹ {roi.get('estimated_savings',0):,.0f}"
    )

    st.divider()

    # =========================================================
    # ROI Gauge
    # =========================================================

    savings = roi.get(
        "estimated_savings",
        0
    )

    gauge = min(
        savings / 1_000_000,
        100
    )

    fig = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=gauge,

            title={
                "text":"ROI Score"
            },

            gauge={

                "axis":{

                    "range":[0,100]

                }

            }

        )

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # =========================================================
    # Decision Simulation
    # =========================================================

    simulation = report.get(
        "simulation",
        {}
    )

    st.subheader("🎯 Decision Simulation")

    left, right = st.columns(2)

    left.metric(
        "Risk",
        simulation.get("risk", "-")
    )

    right.metric(
        "Approvals",
        simulation.get("approvals", "-")
    )

    st.divider()

    # =========================================================
    # Recommendations
    # =========================================================

    st.subheader("✅ Recommendations")

    recommendations = report.get(
        "recommendations",
        [
            "Deploy model after validation.",
            "Monitor drift weekly.",
            "Retrain when performance drops."
        ]
    )

    for rec in recommendations:
        st.success(rec)

    st.divider()

    # =========================================================
    # Download Report
    # =========================================================

    report_path = "reports/business/executive_report.json"

    if os.path.exists(report_path):

        with open(report_path, "rb") as f:

            st.download_button(

                "📥 Download Business Report",

                data=f.read(),

                file_name="executive_report.json",

                mime="application/json"

            )

    st.success("Business Dashboard Loaded Successfully ✅")