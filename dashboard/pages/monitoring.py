import random
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


def show_monitoring(state):
    """
    Monitoring Dashboard
    """

    st.title("🔍 Model Monitoring")

    # =====================================================
    # Simulated Metrics
    # =====================================================

    accuracy = round(random.uniform(0.90, 0.98), 4)
    drift = round(random.uniform(0, 8), 2)
    latency = round(random.uniform(40, 250), 2)
    cpu = round(random.uniform(20, 85), 1)
    memory = round(random.uniform(30, 90), 1)

    # =====================================================
    # Metrics
    # =====================================================

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Accuracy", accuracy)
    c2.metric("Data Drift", f"{drift}%")
    c3.metric("Latency", f"{latency} ms")
    c4.metric("CPU", f"{cpu}%")
    c5.metric("Memory", f"{memory}%")

    st.divider()

    # =====================================================
    # Model Health
    # =====================================================

    st.subheader("Model Health")

    health = max(0, min(100, accuracy * 100 - drift))

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=health,
            title={"text": "Health Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "green"},
                "steps": [
                    {"range": [0, 50], "color": "red"},
                    {"range": [50, 80], "color": "orange"},
                    {"range": [80, 100], "color": "green"},
                ],
            },
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # =====================================================
    # Drift History
    # =====================================================

    st.subheader("Data Drift Trend")

    drift_history = pd.DataFrame(
        {
            "Day": [f"Day {i}" for i in range(1, 11)],
            "Drift": [round(random.uniform(0, 8), 2) for _ in range(10)],
        }
    )

    fig = px.line(
        drift_history,
        x="Day",
        y="Drift",
        markers=True,
        title="Data Drift"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # =====================================================
    # Resource Usage
    # =====================================================

    st.subheader("Resource Usage")

    resource_df = pd.DataFrame(
        {
            "Resource": ["CPU", "Memory"],
            "Usage": [cpu, memory],
        }
    )

    fig = px.bar(
        resource_df,
        x="Resource",
        y="Usage",
        color="Usage",
        range_y=[0, 100],
        title="Server Resources"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # =====================================================
    # Latency
    # =====================================================

    st.subheader("Prediction Latency")

    latency_df = pd.DataFrame(
        {
            "Request": list(range(1, 21)),
            "Latency": [
                round(random.uniform(40, 250), 2)
                for _ in range(20)
            ],
        }
    )

    fig = px.line(
        latency_df,
        x="Request",
        y="Latency",
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # =====================================================
    # Alerts
    # =====================================================

    st.subheader("Alerts")

    if drift > 5:
        st.error("🚨 High Data Drift Detected")

    elif drift > 3:
        st.warning("⚠ Moderate Data Drift")

    else:
        st.success("✅ No Significant Drift")

    if latency > 180:
        st.warning("⚠ High Prediction Latency")

    if cpu > 80:
        st.warning("⚠ CPU Utilization High")

    if memory > 80:
        st.warning("⚠ Memory Utilization High")

    st.divider()

    # =====================================================
    # Retraining Recommendation
    # =====================================================

    st.subheader("Retraining Recommendation")

    if drift > 5 or accuracy < 0.92:

        st.error(
            """
Model performance has degraded.

Recommendation:

• Retrain the model

• Update feature engineering

• Re-evaluate deployment
            """
        )

    else:

        st.success(
            "Current production model is stable."
        )

    st.divider()

    # =====================================================
    # Deployment Status
    # =====================================================

    st.subheader("Deployment")

    if state and state.get("deployment_ready", False):

        st.success("🟢 Production Model Ready")

    else:

        st.warning("🟡 Deployment Pending")

    st.success("Monitoring Dashboard Loaded Successfully ✅")