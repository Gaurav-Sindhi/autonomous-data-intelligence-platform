import pandas as pd


def generate_basic_insights(df):

    numeric_columns = list(
        df.select_dtypes(
            include=["number"]
        ).columns
    )

    categorical_columns = list(
        df.select_dtypes(
            include=["object"]
        ).columns
    )

    insights = {

        "rows":
            int(df.shape[0]),

        "columns":
            int(df.shape[1]),

        "missing_values":
            int(
                df.isnull()
                .sum()
                .sum()
            ),

        "duplicate_rows":
            int(
                df.duplicated()
                .sum()
            ),

        "column_names":
            list(df.columns),

        "numeric_columns":
            numeric_columns,

        "categorical_columns":
            categorical_columns,

        "memory_usage_mb":
            round(
                df.memory_usage(
                    deep=True
                ).sum()
                / (1024 * 1024),
                2
            ),

        "missing_percentage":
            round(
                (
                    df.isnull()
                    .sum()
                    .sum()
                    /
                    (df.shape[0] * df.shape[1])
                )
                * 100,
                2
            )
    }

    return insights