from rag.rag_chain import RAGChain

from core.logger import logger


def rag_agent(state):

    logger.info(

        "Knowledge Retrieval Agent"

    )

    chain = RAGChain()

    answer = chain.ask(

        f"""

Best ML model for

{state["problem_type"]}

dataset.

"""

    )

    state["knowledge"] = answer

    state["messages"].append(

        "Knowledge Retrieved"

    )

    return state