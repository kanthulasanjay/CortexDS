import streamlit as st


def sidebar():
    """Render the application sidebar."""

    with st.sidebar:

        st.image(
            "https://img.icons8.com/fluency/96/artificial-intelligence.png",
            width=80,
        )

        st.title("🤖 AI-DS OS")

        st.caption("AI Data Science Operating System")

        st.divider()

        page = st.radio(
            "Navigation",
            [
                "Dashboard",
                "Dataset",
                "Workflow",
                "EDA",
                "Feature Engineering",
                "Models",
                "Explainability",
                "Business",
                "Memory",
                "Monitoring",
                "AI Chat",
            ],
        )

        st.divider()

        uploaded_file = st.file_uploader(
            "Upload Dataset",
            type=["csv", "xlsx", "xls", "parquet"],
        )

        target = st.text_input(
            "Target Column",
            placeholder="Example: target"
        )

        run = st.button(
            "🚀 Run AI Pipeline",
            use_container_width=True,
        )

    return {
        "page": page,
        "uploaded_file": uploaded_file,
        "target": target,
        "run": run,
    }