import os
import shap
import matplotlib.pyplot as plt


class SHAPEngine:

    def explain(self, model, X):

        os.makedirs("reports/explainability", exist_ok=True)

        explainer = shap.Explainer(model)

        shap_values = explainer(X)

        plt.figure()

        shap.plots.bar(
            shap_values,
            show=False
        )

        plt.savefig(
            "reports/explainability/shap_feature_importance.png",
            bbox_inches="tight"
        )

        plt.close()

        plt.figure()

        shap.summary_plot(
            shap_values,
            X,
            show=False
        )

        plt.savefig(
            "reports/explainability/shap_summary.png",
            bbox_inches="tight"
        )

        plt.close()

        return shap_values