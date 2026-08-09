from lime.lime_tabular import LimeTabularExplainer


class LimeEngine:

    def explain(
        self,
        model,
        X_train,
        feature_names,
        class_names
    ):

        explainer = LimeTabularExplainer(

            training_data=X_train.values,

            feature_names=feature_names,

            class_names=class_names,

            mode="classification"

        )

        explanation = explainer.explain_instance(

            X_train.iloc[0].values,

            model.predict_proba

        )

        explanation.save_to_file(

            "reports/explainability/lime_explanation.html"

        )