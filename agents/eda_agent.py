from core.logger import logger

from ml.eda import EDAAnalyzer


def eda_agent(state):

    logger.info("EDA Agent Started")

    analyzer = EDAAnalyzer(
        state["dataframe"]
    )

    analyzer.save_histograms()

    analyzer.save_correlation_plot()

    report = analyzer.save_report()

    state["eda_report"] = report

    state["messages"].append(
        "EDA Completed"
    )

    logger.info("EDA Finished")

    return state