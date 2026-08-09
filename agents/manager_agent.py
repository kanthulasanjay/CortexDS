from core.llm import llm

def manager_agent(state):

    debate = state["debate"]

    leaderboard = state["leaderboard"]

    prompt = f"""
You are the Chief AI Officer.

Here are candidate models:

{leaderboard}

Here are their debates:

{debate}

Choose the best model.

Explain WHY.

Return JSON.

{{
    "selected_model":"",
    "reason":"",
    "confidence":0
}}
"""

    response = llm.invoke(prompt)

    state["manager_decision"] = response.content

    state["messages"].append(
        "Manager Selected Production Model"
    )

    return state