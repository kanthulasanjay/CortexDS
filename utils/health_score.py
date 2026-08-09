def calculate_health(df):

    score = 100

    missing = df.isnull().sum().sum()

    duplicates = df.duplicated().sum()

    if missing > 0:
        score -= 20

    if duplicates > 0:
        score -= 10

    if score < 0:
        score = 0

    return score