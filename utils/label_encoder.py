from sklearn.preprocessing import LabelEncoder


def encode_target(df, target):

    encoder = LabelEncoder()

    df[target] = encoder.fit_transform(df[target])

    return df, encoder