def generate_basic_insights(df):

    insights = {

        "rows": int(df.shape[0]),

        "columns": int(df.shape[1]),

        "missing_values":
            int(df.isnull().sum().sum()),

        "duplicate_rows":
            int(df.duplicated().sum()),

        "column_names":
            list(df.columns)

    }

    return insights