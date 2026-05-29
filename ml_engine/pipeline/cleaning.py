import pandas as pd

def clean_data(df):
    """
    Basic cleaning:
    - Remove duplicates
    - Fill missing values
    """

    df = df.drop_duplicates()

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna(df[col].mode()[0])
        else:
            df[col] = df[col].fillna(df[col].median())

    return df