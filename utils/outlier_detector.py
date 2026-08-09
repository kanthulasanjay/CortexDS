import numpy as np

def detect_outliers(df):

    report = {}

    numeric = df.select_dtypes(include=np.number).columns

    for col in numeric:

        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        count = ((df[col] < lower) | (df[col] > upper)).sum()

        report[col] = int(count)

    return report