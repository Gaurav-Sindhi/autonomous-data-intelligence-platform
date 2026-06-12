import pandas as pd


def detect_problem(df):

    # Common target names
    possible_targets = [
        "target",
        "label",
        "class",
        "outcome",
        "result",
        "prediction",
        "survived",
        "attrition",
        "saleprice",
        "price",
        "salary",
        "marks",
        "score"
    ]

    target_column = None

    # Try finding a known target column
    for col in df.columns:

        if col.lower() in possible_targets:

            target_column = col
            break

    # Fallback
    if target_column is None:

        target_column = df.columns[-1]

    target = df[target_column]

    # Classification
    if not pd.api.types.is_numeric_dtype(target):

        problem_type = "classification"

    else:

        unique_values = target.nunique()

        # Binary classification
        if unique_values <= 10:

            ratio = unique_values / len(target)

            if ratio < 0.05:

                problem_type = "classification"

            else:

                problem_type = "regression"

        else:

            problem_type = "regression"

    return {

        "target_column": target_column,

        "problem_type": problem_type
    }