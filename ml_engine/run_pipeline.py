import pandas as pd

from pipeline.cleaning import clean_data
from insights.insight_generator import generate_basic_insights


def run_pipeline(file_path):
    """
    Complete ML Pipeline:
    1. Load Dataset
    2. Clean Dataset
    3. Generate Insights
    """

    print("\n==============================")
    print("LOADING DATASET...")
    print("==============================")

    df = pd.read_csv(file_path)

    print(f"Dataset Loaded Successfully")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\n==============================")
    print("CLEANING DATASET...")
    print("==============================")

    df = clean_data(df)

    print("Dataset Cleaned Successfully")

    print("\n==============================")
    print("GENERATING INSIGHTS...")
    print("==============================")

    insights = generate_basic_insights(df)

    print("\n===== DATASET INSIGHTS =====")

    for key, value in insights.items():
        print(f"{key}: {value}")

    return insights


# Entry Point
if __name__ == "__main__":

    file_path = "datasets/sample.csv"

    insights = run_pipeline(file_path)

    print("\nPipeline Executed Successfully!")