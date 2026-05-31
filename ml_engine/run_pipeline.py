import pandas as pd

from ml_engine.pipeline.cleaning import clean_data
from ml_engine.insights.insight_generator import generate_basic_insights
from ml_engine.pipeline.problem_detector import detect_problem_type
from ml_engine.pipeline.model_trainer import train_models
from ml_engine.visualization.chart_generator import generate_charts

def run_pipeline(file_path):

    df = pd.read_csv(file_path)

    df = clean_data(df)

    chart_paths = generate_charts(df)

    insights = generate_basic_insights(df)

    problem_info = detect_problem_type(df)

    training_results = train_models(
        df,
        problem_info["target_column"],
        problem_info["problem_type"]
    )

    return {
    "insights": insights,
    "problem_info": problem_info,
    "training_results": training_results,
    "charts": chart_paths
}