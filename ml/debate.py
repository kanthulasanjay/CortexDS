from pathlib import Path
from core.llm import llm

PROMPT = Path("prompts/debate_prompt.txt").read_text()

class DebateEngine:

    def debate(self, leaderboard):

        discussions = []

        for model in leaderboard:

            prompt = PROMPT.format(
                model=model["model"],
                accuracy=model["accuracy"],
                training_time=model.get("training_time", "Unknown")
            )

            response = llm.invoke(prompt)

            discussions.append({

                "model": model["model"],

                "accuracy": model["accuracy"],

                "argument": response.content

            })

        return discussions