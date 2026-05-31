import pandas as pd


def detect_problem_type(df):

    target_column = df.columns[-1]

    # If target is text -> Classification
    if not pd.api.types.is_numeric_dtype(df[target_column]):
        problem_type = "classification"

    else:
        unique_values = df[target_column].nunique()

        # Numeric target with many unique values = Regression
        if unique_values > 10:
            problem_type = "regression"
        else:
            problem_type = "regression"

    return {
        "target_column": target_column,
        "problem_type": problem_type
    }