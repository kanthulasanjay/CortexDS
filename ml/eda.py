import os
import json

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


class EDAAnalyzer:

    def __init__(self, df):

        self.df = df

        # Create report directories
        os.makedirs("reports", exist_ok=True)
        os.makedirs("reports/images", exist_ok=True)

    # ---------------------------------------------------------
    # DATASET SUMMARY
    # ---------------------------------------------------------

    def summary(self):

        return {
            "rows": len(self.df),

            "columns": len(self.df.columns),

            "missing_values": int(
                self.df.isnull().sum().sum()
            ),

            "duplicates": int(
                self.df.duplicated().sum()
            ),

            "memory_mb": round(
                self.df.memory_usage(
                    deep=True
                ).sum() / 1024**2,
                2
            )
        }

    # ---------------------------------------------------------
    # DESCRIPTIVE STATISTICS
    # ---------------------------------------------------------

    def statistics(self):

        return self.df.describe(
            include="all"
        ).to_dict()

    # ---------------------------------------------------------
    # CORRELATION
    # ---------------------------------------------------------

    def correlation(self):

        numeric = self.df.select_dtypes(
            include="number"
        )

        if numeric.empty:
            return {}

        return (
            numeric
            .corr()
            .round(3)
            .to_dict()
        )

    # ---------------------------------------------------------
    # HISTOGRAMS
    # ---------------------------------------------------------

    def save_histograms(self):

        numeric = self.df.select_dtypes(
            include="number"
        )

        for column in numeric.columns:

            plt.figure(
                figsize=(5, 3)
            )

            numeric[column].hist(
                bins=30
            )

            plt.title(
                f"Distribution of {column}"
            )

            plt.xlabel(column)
            plt.ylabel("Frequency")

            plt.tight_layout()

            # Make filename safe
            safe_column = (
                str(column)
                .replace("/", "_")
                .replace("\\", "_")
                .replace(" ", "_")
            )

            plt.savefig(
                f"reports/images/{safe_column}_hist.png",
                dpi=150,
                bbox_inches="tight"
            )

            # IMPORTANT:
            # Close figure so memory does not accumulate
            plt.close()

    # ---------------------------------------------------------
    # CORRELATION HEATMAP
    # ---------------------------------------------------------

    def save_correlation_plot(self):

        numeric = self.df.select_dtypes(
            include="number"
        )

        if numeric.empty:
            return

        corr = numeric.corr()

        plt.figure(
            figsize=(10, 8)
        )

        plt.imshow(
            corr,
            aspect="auto"
        )

        plt.colorbar(
            label="Correlation"
        )

        plt.xticks(
            range(len(corr.columns)),
            corr.columns,
            rotation=90
        )

        plt.yticks(
            range(len(corr.columns)),
            corr.columns
        )

        plt.title(
            "Correlation Matrix"
        )

        plt.tight_layout()

        plt.savefig(
            "reports/images/correlation_matrix.png",
            dpi=150,
            bbox_inches="tight"
        )

        plt.close()

    # ---------------------------------------------------------
    # AUTOMATED INSIGHTS
    # ---------------------------------------------------------

    def insights(self):

        insights = []

        numeric = self.df.select_dtypes(
            include="number"
        )

        # Detect skewness
        for col in numeric.columns:

            # Skip columns with insufficient data
            if numeric[col].dropna().empty:
                continue

            skew = numeric[col].skew()

            if pd.isna(skew):
                continue

            if skew > 1:

                insights.append(
                    f"{col} is strongly positively skewed."
                )

            elif skew < -1:

                insights.append(
                    f"{col} is strongly negatively skewed."
                )

        # Detect missing values
        missing = self.df.isnull().sum()

        for col, value in missing.items():

            if value > 0:

                percentage = (
                    value / len(self.df)
                ) * 100

                insights.append(
                    f"{col} contains {value} "
                    f"missing values "
                    f"({percentage:.2f}%)."
                )

        # Detect high-cardinality columns
        for col in self.df.columns:

            unique_ratio = (
                self.df[col].nunique(dropna=True)
                / len(self.df)
            )

            if unique_ratio > 0.95:

                insights.append(
                    f"{col} has very high "
                    f"cardinality "
                    f"({self.df[col].nunique()} unique values)."
                )

        # Detect constant columns
        for col in self.df.columns:

            if self.df[col].nunique(
                dropna=False
            ) <= 1:

                insights.append(
                    f"{col} is a constant column "
                    f"and may not provide predictive value."
                )

        return insights

    # ---------------------------------------------------------
    # SAVE COMPLETE EDA REPORT
    # ---------------------------------------------------------

    def save_report(self):

        # Generate visualizations
        self.save_histograms()

        self.save_correlation_plot()

        report = {

            "summary": self.summary(),

            "statistics": self.statistics(),

            "correlation": self.correlation(),

            "insights": self.insights()
        }

        with open(
            "reports/eda_summary.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                report,
                f,
                indent=4,
                default=str
            )

        return report