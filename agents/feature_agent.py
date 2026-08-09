from core.logger import logger

def feature_agent(state):

    logger.info("Feature Agent Running")

    state["messages"].append("Features Generated")

    return state