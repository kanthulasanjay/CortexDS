from core.logger import logger
from memory.long_memory import LongTermMemory


def memory_agent(state):

    logger.info(
        "Memory Agent Started"
    )

    try:

        memory = LongTermMemory()

        experience = {
            "dataset_path": state.get(
                "dataset_path",
                ""
            ),

            "target": state.get(
                "target",
                ""
            ),

            "model": state.get(
                "model_name",
                ""
            ),

            "metrics": state.get(
                "metrics",
                {}
            ),

            "optimized_score": state.get(
                "optimized_score",
                0.0
            )
        }

        memory.add(
            experience
        )

        state["messages"].append(
            "Memory Agent Completed"
        )

        logger.info(
            "Memory Agent Completed"
        )

        return state

    except Exception as e:

        logger.exception(
            "Memory Agent Failed"
        )

        state["messages"].append(
            f"Memory Agent Failed: {str(e)}"
        )

        return state