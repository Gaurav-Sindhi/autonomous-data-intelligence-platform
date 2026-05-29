import pandas as pd

from pipeline.cleaning import clean_data
from insights.insight_generator import generate_basic_insights


def run_pipeline(file_path):

    print("Loading dataset...")

    df = pd.read_csv(file_path)

    print("Cleaning data...")

    df = clean_data(df)

    print("Generating insights...")

    insights = generate_basic_insights(df)

    print("\n=== INSIGHTS ===")

    for insight in insights:
        print(insight)

    return insights