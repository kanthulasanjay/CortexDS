from core.logger import logger

def planner_agent(state):
    logger.info("Planner Agent Started")

    print("=" * 50)
    print("STATE RECEIVED")
    print(state)
    print("=" * 50)
    print("KEYS:", list(state.keys()))

    state.setdefault("messages", [])

    state["plan"] = [
        "dataset",
        "quality",
        "cleaning",
        "eda",
        "feature",
        "model",
        "evaluation",
        "business"
    ]

    state["messages"].append("Workflow Created")

    return state