from sklearn.feature_selection import mutual_info_classif

import pandas as pd


class FeatureRanker:

    def rank(self,X,y):

        scores=mutual_info_classif(

            X,

            y

        )

        ranking=pd.DataFrame({

            "feature":X.columns,

            "score":scores

        })

        ranking=ranking.sort_values(

            "score",

            ascending=False

        )

        return ranking