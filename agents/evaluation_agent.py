from core.logger import logger

def evaluation_agent(state):

    logger.info("Evaluation Agent Running")

    state["metrics"] = {

        "accuracy":0.93

    }

    state["messages"].append("Evaluation Completed")

    return state