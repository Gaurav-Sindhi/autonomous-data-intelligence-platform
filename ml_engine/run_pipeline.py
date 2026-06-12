import pandas as pd

from ml_engine import insights
from ml_engine.pipeline.cleaning import clean_data
from ml_engine.insights.insight_generator import generate_basic_insights
from ml_engine.pipeline.problem_detector import detect_problem
from ml_engine.pipeline.model_trainer import train_models
from ml_engine.reports.pdf_generator import generate_pdf_report
from ml_engine.visualization.chart_generator import generate_charts

from ml_engine.agents.insight_agent import generate_ai_insights
from ml_engine.agents.analytics_agent import generate_analytics_insight
from ml_engine.agents.model_selection_agent import explain_model_choice



def run_pipeline(file_path):

    # ==========================
    # Load Dataset
    # ==========================

    raw_df = pd.read_csv(file_path)

    raw_insights = generate_basic_insights(raw_df)

    df = clean_data(raw_df.copy())

    cleaned_insights = generate_basic_insights(df)

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
    raw_insights,
    cleaned_insights,
    problem_info,
    training_results
)

    # ==========================
    # Model Reasoning Agent
    # ==========================

    model_reasoning = explain_model_choice(
    problem_info,
    training_results
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

    analytics_insight = (
    generate_analytics_insight(
        raw_insights,
        cleaned_insights
    )
)

    pdf_report = generate_pdf_report(
        {
            "insights": insights,
            "problem_info": problem_info,
            "training_results": training_results,
            "analytics_insight": analytics_insight,
            "ai_insights": ai_insights,
            "model_reasoning": model_reasoning
         }
    )
    # ==========================
    # Final Response
    # ==========================

    return {

    "raw_insights": raw_insights,

    "cleaned_insights": cleaned_insights,

    "problem_info": problem_info,

    "training_results": training_results,

    "charts": charts,

    "ai_insights": ai_insights,

    "model_reasoning": model_reasoning,

    "analytics_insight": analytics_insight
}