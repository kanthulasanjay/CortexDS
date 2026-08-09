import numpy as np

def detect_target_leakage(df, target):

    leakage = []

    if target not in df.columns:
        return leakage

    numeric = df.select_dtypes(include=np.number)

    if target not in numeric.columns:
        return leakage

    corr = numeric.corr()[target].abs()

    for col, value in corr.items():

        if col == target:
            continue

        if value > 0.95:
            leakage.append(col)

    return leakage