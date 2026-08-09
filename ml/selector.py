import numpy as np

class FeatureSelector:

    def __init__(self,df):

        self.df=df

    def remove_correlated(self):

        numeric=self.df.select_dtypes(include=np.number)

        corr=numeric.corr().abs()

        upper=corr.where(

            np.triu(

                np.ones(corr.shape),

                k=1

            ).astype(bool)

        )

        remove=[

            column

            for column in upper.columns

            if any(

                upper[column]>0.95

            )

        ]

        self.df=self.df.drop(columns=remove)

        return self.df,remove