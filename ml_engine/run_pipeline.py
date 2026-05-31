import pandas as pd

from ml_engine.pipeline.cleaning import clean_data
from ml_engine.insights.insight_generator import generate_basic_insights
from ml_engine.pipeline.problem_detector import detect_problem_type
from ml_engine.pipeline.model_trainer import train_models


def run_pipeline(file_path):

    # Load Dataset
    df = pd.read_csv(file_path)

    # Clean Dataset
    df = clean_data(df)

    # Generate Insights
    insights = generate_basic_insights(df)

    # Detect Problem Type
    problem_info = detect_problem_type(df)

    # Train Models
    model_results = train_models(
        df,
        problem_info["target_column"],
        problem_info["problem_type"]
    )

    # Select Best Model
    best_model = max(
        model_results,
        key=model_results.get
    )

    return {
        "insights": insights,
        "problem_info": problem_info,
        "model_results": model_results,
        "best_model": best_model
    }