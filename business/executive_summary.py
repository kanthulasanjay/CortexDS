from core.llm import llm


class ExecutiveSummary:

    def summarize(

        self,

        state,

        roi,

        simulation

    ):

        prompt = f"""

You are a Chief Data Officer.

Dataset Summary

{state["dataset_summary"]}

Model Performance

{state["metrics"]}

ROI

{roi}

Decision Simulation

{simulation}

Write an executive summary.

Include

• Main findings

• Business impact

• Risks

• Recommendations

Keep it professional.

"""

        return llm.invoke(prompt).content