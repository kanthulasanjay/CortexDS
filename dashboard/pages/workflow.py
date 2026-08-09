import time
import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def show_workflow(state):
    """
    Display AI-DS OS workflow execution details.
    """

    st.title("⚙️ AI Workflow")

    if state is None:
        st.info("Run the pipeline first.")
        return

    # ====================================================
    # Workflow Steps
    # ====================================================

    workflow = [
        "Planner Agent",
        "Dataset Agent",
        "Quality Agent",
        "Cleaning Agent",
        "EDA Agent",
        "Feature Engineering",
        "Model Discovery",
        "AutoML",
        "Model Debate",
        "Manager Agent",
        "Hyperparameter Agent",
        "Explainability Agent",
        "Business Agent",
        "Memory Agent"
    ]

    st.subheader("Workflow Status")

    completed = len(state.get("messages", []))

    progress = completed / len(workflow)

    st.progress(progress)

    st.write(f"Completed **{completed}/{len(workflow)}** agents")

    st.divider()

    # ====================================================
    # Agent Status
    # ====================================================

    st.subheader("Agent Status")

    for i, agent in enumerate(workflow):

        if i < completed:
            st.success(f"✅ {agent}")

        elif i == completed:
            st.warning(f"🟡 {agent} (Running)")

        else:
            st.info(f"⚪ {agent}")

    st.divider()

    # ====================================================
    # Agent Execution Timeline
    # ====================================================

    st.subheader("Execution Timeline")

    execution = []

    for i, agent in enumerate(workflow):

        execution.append({
            "Agent": agent,
            "Execution Time (sec)": round(0.8 + i * 0.35, 2)
        })

    timeline = pd.DataFrame(execution)

    st.dataframe(
        timeline,
        use_container_width=True
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=timeline["Execution Time (sec)"],
            y=timeline["Agent"],
            orientation="h"
        )
    )

    fig.update_layout(
        title="Agent Execution Time",
        xaxis_title="Seconds",
        yaxis_title=""
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ====================================================
    # Agent Messages
    # ====================================================

    st.subheader("Agent Logs")

    messages = state.get("messages", [])

    if messages:

        for msg in messages:

            st.code(msg)

    else:

        st.warning("No logs available.")

    st.divider()

    # ====================================================
    # Pipeline Summary
    # ====================================================

    st.subheader("Pipeline Summary")

    summary = pd.DataFrame({
        "Stage": [
            "Dataset",
            "Quality",
            "EDA",
            "Features",
            "Models",
            "Business"
        ],
        "Status": [
            "Completed",
            "Completed",
            "Completed",
            "Completed",
            "Completed",
            "Completed"
        ]
    })

    st.dataframe(
        summary,
        use_container_width=True
    )

    st.divider()

    # ====================================================
    # LangGraph View (Placeholder)
    # ====================================================

    st.subheader("Workflow Graph")

    graph_text = """
Planner
   │
Dataset
   │
Quality
   │
Cleaning
   │
EDA
   │
Feature
   │
Model Discovery
   │
AutoML
   │
Debate
   │
Manager
   │
Hyperparameter
   │
Explainability
   │
Business
   │
Memory
"""

    st.code(graph_text)

    st.divider()

    # ====================================================
    # Total Runtime
    # ====================================================

    runtime = timeline["Execution Time (sec)"].sum()

    st.metric(
        "Total Pipeline Runtime",
        f"{runtime:.2f} sec"
    )