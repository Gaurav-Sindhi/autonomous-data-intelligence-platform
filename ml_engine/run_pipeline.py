import pandas as pd

from ml_engine.pipeline.cleaning import clean_data
from ml_engine.insights.insight_generator import generate_basic_insights


def run_pipeline(file_path):

    df = pd.read_csv(file_path)

    df = clean_data(df)

    insights = generate_basic_insights(df)

    return insights
