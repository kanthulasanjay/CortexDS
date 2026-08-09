import os

def save_debate(debates):

    os.makedirs("reports", exist_ok=True)

    with open(
        "reports/debate_report.md",
        "w",
        encoding="utf-8"
    ) as f:

        for debate in debates:

            f.write(
                f"# {debate['model']}\n\n"
            )

            f.write(
                debate["argument"]
            )

            f.write("\n\n---\n\n")