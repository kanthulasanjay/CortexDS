import streamlit as st


def show_chat(state):
    """
    AI Copilot Chat Page
    """

    st.title("🤖 AI Data Science Copilot")

    st.markdown(
        """
Ask questions about:

- 📊 Dataset
- 🧠 Feature Engineering
- 🏆 Models
- 📈 Explainability
- 💼 Business Insights
- 📚 Previous Experiments
- 🔍 Monitoring
"""
    )

    if state is None:
        st.info("Run the pipeline first.")
        return

    # ------------------------------------
    # Chat History
    # ------------------------------------

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ------------------------------------
    # User Question
    # ------------------------------------

    question = st.chat_input(
        "Ask anything about your AI project..."
    )

    if question:

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        # ------------------------------------
        # Build Context
        # ------------------------------------

        context = f"""
Dataset Summary

{state.get("dataset_summary", {})}

Problem Type

{state.get("problem_type", "")}

Selected Features

{state.get("selected_features", [])}

Metrics

{state.get("metrics", {})}

Leaderboard

{state.get("leaderboard", [])}

Business Report

{state.get("business_report", {})}

Manager Decision

{state.get("manager_decision", {})}
"""

        # ------------------------------------
        # RAG Response
        # ------------------------------------

        try:

            from rag.rag_chain import RAGChain

            rag = RAGChain()

            answer = rag.ask(

                f"""
Context

{context}

Question

{question}
"""

            )

        except Exception as e:

            answer = f"""
AI Copilot could not access the RAG system.

Reason:

{e}
"""

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        with st.chat_message("assistant"):

            st.markdown(answer)

    st.divider()

    # ------------------------------------
    # Suggested Questions
    # ------------------------------------

    st.subheader("💡 Suggested Questions")

    suggestions = [

        "Which model performed best?",

        "Why did the Manager Agent choose this model?",

        "Explain the SHAP results.",

        "Summarize the business report.",

        "How can I improve the model?",

        "Which features are most important?",

        "Was there any data quality issue?",

        "Explain the feature engineering pipeline.",

        "Should I retrain this model?",

        "Generate an executive summary."

    ]

    cols = st.columns(2)

    for i, item in enumerate(suggestions):

        with cols[i % 2]:

            if st.button(item):

                st.info(
                    "Copy this question into the chat above."
                )