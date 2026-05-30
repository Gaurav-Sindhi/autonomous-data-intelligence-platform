import pandas as pd


def clean_data(df):

    # Remove duplicates
    df = df.drop_duplicates()

    # Fill missing values
    for col in df.columns:

        if pd.api.types.is_numeric_dtype(df[col]):

            df[col] = df[col].fillna(df[col].median())

        else:

            if not df[col].mode().empty:
                df[col] = df[col].fillna(df[col].mode()[0])

    return df