import os
import streamlit as st

from core.graph import graph

from dashboard.components.sidebar import sidebar

from dashboard.pages.dashboard import show_dashboard
from dashboard.pages.dataset import show_dataset
from dashboard.pages.workflow import show_workflow
from dashboard.pages.eda import show_eda
from dashboard.pages.feature import show_feature_engineering
from dashboard.pages.models import show_models
from dashboard.pages.explainability import show_explainability
from dashboard.pages.business import show_business
from dashboard.pages.memory import show_memory
from dashboard.pages.monitoring import show_monitoring
from dashboard.pages.chat import show_chat

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI Data Science Operating System",
    page_icon="🤖",
    layout="wide"
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "result" not in st.session_state:
    st.session_state.result = None

if "pipeline_finished" not in st.session_state:
    st.session_state.pipeline_finished = False

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

ui = sidebar()

page = ui["page"]
uploaded_file = ui["uploaded_file"]
target = ui["target"]
run = ui["run"]

# --------------------------------------------------
# RUN PIPELINE
# --------------------------------------------------

if run:

    if uploaded_file is None:

        st.error("Please upload a dataset.")

    elif target.strip() == "":

        st.error("Please enter the target column.")

    else:

        os.makedirs("data", exist_ok=True)

        dataset_path = os.path.join(
            "data",
            uploaded_file.name
        )

        with open(dataset_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        initial_state = {

            "dataset_path": dataset_path,

            "target": target,

            "dataframe": None,

            "clean_dataframe": None,

            "target_series": None,

            "problem_type": "",

            "dataset_summary": {},

            "quality_report": {},

            "eda_report": {},

            "selected_features": [],

            "candidate_models": [],

            "leaderboard": [],

            "debate": [],

            "manager_decision": {},

            "metrics": {},

            "business_report": {},

            "messages": [],

            "best_model": None,

            "best_params": {},

            "optimized_score": 0,

            "knowledge": "",

            "previous_experiments": [],

            "deployment_ready": False

        }

        with st.spinner("Running AI Data Science Operating System..."):

            try:

                result = graph.invoke(initial_state)

                st.session_state.result = result

                st.session_state.pipeline_finished = True

                st.success("Pipeline Completed Successfully ✅")

            except Exception as e:

                st.exception(e)

# --------------------------------------------------
# DISPLAY PAGE
# --------------------------------------------------

state = st.session_state.result

if page == "Dashboard":

    show_dashboard(state)

elif page == "Dataset":

    show_dataset(state)

elif page == "Workflow":

    show_workflow(state)

elif page == "EDA":

    show_eda(state)

elif page == "Feature Engineering":

    show_feature_engineering(state)

elif page == "Models":

    show_models(state)

elif page == "Explainability":

    show_explainability(state)

elif page == "Business":

    show_business(state)

elif page == "Memory":

    show_memory(state)

elif page == "Monitoring":

    show_monitoring(state)

elif page == "AI Chat":

    show_chat(state)