from langgraph.graph import StateGraph

from core.state import DSState

from agents.dataset_agent import dataset_agent
from agents.quality_agent import quality_agent
from agents.cleaning_agent import cleaning_agent
from agents.eda_agent import eda_agent
from agents.feature_agent import feature_agent
from agents.model_agent import model_agent
from agents.debate_agent import debate_agent
from agents.manager_agent import manager_agent
from agents.hyperparameter_agent import hyperparameter_agent
from agents.explainability_agent import explainability_agent
from agents.business_agent import business_agent
from agents.memory_agent import memory_agent


# ==========================================================
# CREATE GRAPH
# ==========================================================

builder = StateGraph(DSState)


# ==========================================================
# ADD AGENTS
# ==========================================================

builder.add_node(
    "dataset",
    dataset_agent
)

builder.add_node(
    "quality",
    quality_agent
)

builder.add_node(
    "cleaning",
    cleaning_agent
)

builder.add_node(
    "eda",
    eda_agent
)

builder.add_node(
    "feature",
    feature_agent
)

builder.add_node(
    "model",
    model_agent
)

builder.add_node(
    "debate",
    debate_agent
)

builder.add_node(
    "manager",
    manager_agent
)

builder.add_node(
    "hyperparameter",
    hyperparameter_agent
)

builder.add_node(
    "explainability",
    explainability_agent
)

builder.add_node(
    "business",
    business_agent
)

builder.add_node(
    "memory",
    memory_agent
)


# ==========================================================
# ENTRY POINT
# ==========================================================

builder.set_entry_point(
    "dataset"
)


# ==========================================================
# PIPELINE FLOW
# ==========================================================

builder.add_edge(
    "dataset",
    "quality"
)

builder.add_edge(
    "quality",
    "cleaning"
)

builder.add_edge(
    "cleaning",
    "eda"
)

builder.add_edge(
    "eda",
    "feature"
)

builder.add_edge(
    "feature",
    "model"
)

builder.add_edge(
    "model",
    "debate"
)

builder.add_edge(
    "debate",
    "manager"
)

builder.add_edge(
    "manager",
    "hyperparameter"
)

builder.add_edge(
    "hyperparameter",
    "explainability"
)

builder.add_edge(
    "explainability",
    "business"
)

builder.add_edge(
    "business",
    "memory"
)


# ==========================================================
# FINISH POINT
# ==========================================================

builder.set_finish_point(
    "memory"
)


# ==========================================================
# COMPILE GRAPH
# ==========================================================

graph = builder.compile()