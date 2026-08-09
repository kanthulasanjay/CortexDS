from core.logger import logger

from business.business_insights import (
    BusinessInsightGenerator
)


def business_agent(state):

    logger.info(
        "Business Intelligence Agent Started"
    )

    try:

        # ==================================================
        # GET PIPELINE DATA
        # ==================================================

        metrics = state.get(
            "metrics",
            {}
        )

        problem_type = state.get(
            "problem_type",
            ""
        )

        model_name = state.get(
            "model_name",
            "Selected Model"
        )

        # ==================================================
        # GENERATE BUSINESS INSIGHTS
        # ==================================================

        generator = BusinessInsightGenerator()

        insights = generator.generate(
            metrics=metrics,
            problem_type=problem_type,
            model_name=model_name
        )

        # ==================================================
        # SAVE RESULT
        # ==================================================

        state["business_report"] = insights

        # ==================================================
        # AGENT MESSAGE
        # ==================================================

        if "messages" not in state:

            state["messages"] = []

        state["messages"].append(
            "Business Intelligence Agent Completed"
        )

        logger.info(
            "Business Intelligence Agent Completed"
        )

        return state

    except Exception as e:

        # ==================================================
        # ERROR HANDLING
        # ==================================================

        logger.error(
            f"Business Agent Error: {str(e)}"
        )

        state["business_report"] = {
            "model": state.get(
                "model_name",
                "Unknown"
            ),

            "problem_type": state.get(
                "problem_type",
                "Unknown"
            ),

            "insights": [
                "Business insight generation "
                f"failed: {str(e)}"
            ]
        }

        if "messages" not in state:

            state["messages"] = []

        state["messages"].append(
            "Business Intelligence Agent completed with warning"
        )

        return state