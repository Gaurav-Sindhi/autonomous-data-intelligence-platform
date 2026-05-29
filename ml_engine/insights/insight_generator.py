def generate_basic_insights(df):

    insights = []

    insights.append(f"Dataset contains {df.shape[0]} rows")

    insights.append(f"Dataset contains {df.shape[1]} columns")

    missing = df.isnull().sum().sum()

    insights.append(f"Missing values detected: {missing}")

    return insights