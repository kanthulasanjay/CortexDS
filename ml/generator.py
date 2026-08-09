import pandas as pd


class FeatureGenerator:

    def __init__(self, df):
        self.df = df

    def generate(self):
        numeric = self.df.select_dtypes(include="number")

        cols = numeric.columns.tolist()
        created = []

        for i in range(len(cols)):
            for j in range(i + 1, len(cols)):

                # Limit interaction features
                if len(created) >= 20:
                    break

                name = f"{cols[i]}_x_{cols[j]}"

                self.df[name] = (
                    numeric[cols[i]] * numeric[cols[j]]
                )

                created.append(name)

        return self.df, created


def generate_datetime(df):
    created = []

    for col in df.columns:

        if "date" in col.lower():

            try:
                df[col] = pd.to_datetime(df[col], errors="coerce")

                df[f"{col}_year"] = df[col].dt.year
                df[f"{col}_month"] = df[col].dt.month
                df[f"{col}_day"] = df[col].dt.day
                df[f"{col}_dayofweek"] = df[col].dt.dayofweek
                df[f"{col}_quarter"] = df[col].dt.quarter

                created.extend([
                    f"{col}_year",
                    f"{col}_month",
                    f"{col}_day",
                    f"{col}_dayofweek",
                    f"{col}_quarter",
                ])

            except Exception:
                continue

    return df, created