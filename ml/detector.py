import pandas as pd

class FeatureDetector:

    def __init__(self, df):

        self.df = df

    def detect(self):

        return {

            "numeric":
                self.df.select_dtypes(
                    include="number"
                ).columns.tolist(),

            "categorical":
                self.df.select_dtypes(
                    exclude="number"
                ).columns.tolist(),

            "datetime":[

                c

                for c in self.df.columns

                if "date" in c.lower()
                or "time" in c.lower()

            ]
        }