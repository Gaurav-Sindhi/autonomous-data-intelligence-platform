import pandas as pd
from ml_engine.pipeline.cleaning import clean_data
from ml_engine.insights.insight_generator import generate_basic_insights
from ml_engine.pipeline.problem_detector import detect_problem
from ml_engine.pipeline.model_trainer import train_models
from ml_engine.reports.new_pdf_generator import generate_professional_pdf
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
    import os

    os.makedirs(
        "uploads/cleaned",
        exist_ok=True
    )

    cleaned_file = (
        "uploads/cleaned/cleaned_dataset.csv"
    )

    df.to_csv(
        cleaned_file,
        index=False
)

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
    print("4. Training Started")
    training_results = train_models(
        df,
        target_column,
        problem_type
    )
    print("5. Training Completed")

    # ==========================
    # Charts
    # ==========================
    print("6. Charts Started")
    charts = generate_charts(
    df,
    target_column
    )
    print("6. Charts Completed")
    # ==========================
    # AI Dataset Insight Agent
    # ==========================
    print("8. AI Insights Started")
    ai_insights = generate_ai_insights(
    raw_insights,
    cleaned_insights,
    problem_info,
    training_results
)   
    print("9. AI Insights Completed")

    # ==========================
    # Model Reasoning Agent
    # ==========================
    print("12. Model Reasoning Started")

    model_reasoning = explain_model_choice(
    problem_info,
    training_results
)
    print("13. Model Reasoning Completed")
    # ==========================
    # Analytics Summary Agent
    # ==========================
    print("10. Analytics Started")
    analytics_summary = f"""
    BEFORE CLEANING

    Dataset Rows: {raw_insights['rows']}
    Dataset Columns: {raw_insights['columns']}
    Missing Values: {raw_insights['missing_values']}
    Duplicate Rows: {raw_insights['duplicate_rows']}

    AFTER CLEANING

    Dataset Rows: {cleaned_insights['rows']}
    Dataset Columns: {cleaned_insights['columns']}
    Missing Values: {cleaned_insights['missing_values']}
    Duplicate Rows: {cleaned_insights['duplicate_rows']}

    Problem Type: {problem_info['problem_type']}
    Target Column: {problem_info['target_column']}
    Best Model:
    {training_results['best_model']}
    """

    analytics_insight = (
    generate_analytics_insight(
        raw_insights,
        cleaned_insights
    )
) 
    print("11. Analytics Completed")


    print("14. PDF Started")
    pdf_report = generate_professional_pdf({

    "raw_insights": raw_insights,

    "cleaned_insights": cleaned_insights,

    "problem_info": problem_info,

    "training_results": training_results,

    "analytics_insight": analytics_insight,

    "ai_insights": ai_insights,

    "model_reasoning": model_reasoning
})
    print("15. PDF Completed")

    # ==========================
    # Final Response
    # ==========================
    return {

        "raw_insights": raw_insights,

        "cleaned_insights": cleaned_insights,

        "cleaned_dataset": cleaned_file,

        "problem_info": problem_info,

        "training_results": training_results,

        "model_file": training_results["model_path"],

        "charts": charts,

        "ai_insights": ai_insights,

        "model_reasoning": model_reasoning,

        "analytics_insight": analytics_insight,

        "pdf_report": pdf_report
    }