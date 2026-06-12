import pandas as pd

from ml_engine.pipeline.cleaning import clean_data
from ml_engine.insights.insight_generator import generate_basic_insights
from ml_engine.pipeline.problem_detector import detect_problem
from ml_engine.pipeline.model_trainer import train_models

from ml_engine.visualization.chart_generator import generate_charts

from ml_engine.agents.insight_agent import generate_ai_insights
from ml_engine.agents.analytics_agent import generate_analytics_insight
from ml_engine.agents.model_selection_agent import generate_model_reasoning


def run_pipeline(file_path):

    # ==========================
    # Load Dataset
    # ==========================

    df = pd.read_csv(file_path)

    # ==========================
    # Data Cleaning
    # ==========================

    df = clean_data(df)

    # ==========================
    # Dataset Insights
    # ==========================

    insights = generate_insights(df)

    # ==========================
    # Problem Detection
    # ==========================

    problem_info = detect_problem(df)

    target_column = problem_info["target_column"]

    problem_type = problem_info["problem_type"]

    # ==========================
    # AutoML Training
    # ==========================

    training_results = train_models(
        df,
        target_column,
        problem_type
    )

    # ==========================
    # Charts
    # ==========================

    charts = generate_charts(
    df,
    target_column
    )

    # ==========================
    # AI Dataset Insight Agent
    # ==========================

    ai_insights = generate_ai_insights(
        insights,
        problem_info,
        training_results
    )

    # ==========================
    # Model Reasoning Agent
    # ==========================

    model_reasoning = generate_model_reasoning(
        training_results,
        problem_type
    )

    # ==========================
    # Analytics Summary Agent
    # ==========================

    analytics_summary = f"""
    Dataset Rows: {insights['rows']}
    Dataset Columns: {insights['columns']}
    Missing Values: {insights['missing_values']}
    Duplicate Rows: {insights['duplicate_rows']}

    Problem Type:
    {problem_type}

    Target Column:
    {target_column}

    Best Model:
    {training_results['best_model']}
    """

    analytics_insight = generate_analytics_insight(
        analytics_summary
    )

    # ==========================
    # Final Response
    # ==========================

    return {

        "insights": insights,

        "problem_info": problem_info,

        "training_results": training_results,

        "charts": charts,

        "ai_insights": ai_insights,

        "model_reasoning": model_reasoning,

        "analytics_insight": analytics_insight
    }