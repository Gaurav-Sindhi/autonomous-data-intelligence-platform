from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet

import os


def generate_pdf_report(result):

    os.makedirs(
        "uploads/reports",
        exist_ok=True
    )

    pdf_path = (
        "uploads/reports/"
        "analysis_report.pdf"
    )

    doc = SimpleDocTemplate(
        pdf_path
    )

    styles = getSampleStyleSheet()

    elements = []

    # =====================
    # Title
    # =====================

    elements.append(
        Paragraph(
            "Autonomous Data Intelligence Report",
            styles["Title"]
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    # =====================
    # Dataset Summary
    # =====================

    raw_insights = result["raw_insights"]

    cleaned_insights = result["cleaned_insights"]

    elements.append(
        Paragraph(
            "Dataset Summary",
            styles["Heading1"]
        )
    )

    # =====================
    # BEFORE CLEANING
    # =====================

    elements.append(
        Paragraph(
            "Before Cleaning",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            f"Rows: {raw_insights['rows']}",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            f"Columns: {raw_insights['columns']}",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            f"Missing Values: {raw_insights['missing_values']}",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            f"Duplicate Rows: {raw_insights['duplicate_rows']}",
            styles["BodyText"]
        )
    )

    elements.append(
        Spacer(1, 10)
    )

    # =====================
    # AFTER CLEANING
    # =====================

    elements.append(
        Paragraph(
            "After Cleaning",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            f"Rows: {cleaned_insights['rows']}",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            f"Columns: {cleaned_insights['columns']}",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            f"Missing Values: {cleaned_insights['missing_values']}",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            f"Duplicate Rows: {cleaned_insights['duplicate_rows']}",
            styles["BodyText"]
        )
    )

    elements.append(
        Spacer(1, 15)
    )

    # =====================
    # Problem Detection
    # =====================

    elements.append(
        Paragraph(
            "Problem Detection",
            styles["Heading1"]
        )
    )

    elements.append(
        Paragraph(
            f"Target Column: {result['problem_info']['target_column']}",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            f"Problem Type: {result['problem_info']['problem_type']}",
            styles["BodyText"]
        )
    )

    elements.append(
        Spacer(1, 15)
    )

    # =====================
    # Model Results
    # =====================

    elements.append(
        Paragraph(
            "Model Performance",
            styles["Heading1"]
        )
    )

    scores = result[
        "training_results"
    ]["scores"]

    for model, score in scores.items():

        elements.append(
            Paragraph(
                f"{model}: {score}",
                styles["BodyText"]
            )
        )

    elements.append(
        Paragraph(
            f"Best Model: {result['training_results']['best_model']}",
            styles["BodyText"]
        )
    )

    elements.append(
        Spacer(1, 15)
    )

    # =====================
    # Analytics Agent
    # =====================

    elements.append(
        Paragraph(
            "Analytics Summary",
            styles["Heading1"]
        )
    )

    elements.append(
        Paragraph(
            result["analytics_insight"],
            styles["BodyText"]
        )
    )

    elements.append(
        Spacer(1, 15)
    )

    # =====================
    # AI Insights
    # =====================

    elements.append(
        Paragraph(
            "AI Dataset Insights",
            styles["Heading1"]
        )
    )

    elements.append(
        Paragraph(
            result["ai_insights"],
            styles["BodyText"]
        )
    )

    elements.append(
        Spacer(1, 15)
    )

    # =====================
    # Model Reasoning
    # =====================

    elements.append(
        Paragraph(
            "Model Selection Reasoning",
            styles["Heading1"]
        )
    )

    elements.append(
        Paragraph(
            result["model_reasoning"],
            styles["BodyText"]
        )
    )

    doc.build(elements)

    return pdf_path