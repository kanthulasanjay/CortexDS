from core.logger import logger

from utils.quality_checker import quality_report


def quality_agent(state):

    logger.info("Running Data Quality Agent...")

    report = quality_report(

        state["dataframe"],

        state["target"]

    )

    state["quality_report"] = report

    state["messages"].append(
        "Quality Report Generated"
    )

    logger.info(report)

    return state