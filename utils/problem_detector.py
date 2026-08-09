def detect_problem(df, target):

    unique = df[target].nunique()

    dtype = str(df[target].dtype)

    if dtype in ["object", "category", "bool"]:
        return "classification"

    if unique <= 20:
        return "classification"

    return "regression"