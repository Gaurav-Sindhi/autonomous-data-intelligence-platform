import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def generate_charts(df, target_column):

    os.makedirs(
        "uploads/reports",
        exist_ok=True
    )

    charts = []

    # ==========================
    # Correlation Heatmap
    # ==========================

    numeric_df = df.select_dtypes(
        include=["number"]
    )

    if len(numeric_df.columns) > 1:

        plt.figure(figsize=(10, 8))

        sns.heatmap(
            numeric_df.corr(),
            annot=True,
            cmap="coolwarm"
        )

        plt.title(
            "Correlation Heatmap"
        )

        heatmap_path = (
            "uploads/reports/"
            "heatmap.png"
        )

        plt.tight_layout()

        plt.savefig(
            heatmap_path
        )

        plt.close()

        charts.append(
            heatmap_path
        )

    # ==========================
    # Missing Values Analysis
    # ==========================

    plt.figure(figsize=(8, 5))

    missing_values = (
        df.isnull().sum()
    )

    missing_values.plot(
        kind="bar"
    )

    plt.title(
        "Missing Values Analysis"
    )

    plt.ylabel(
        "Count"
    )

    missing_path = (
        "uploads/reports/"
        "missing_values.png"
    )

    plt.tight_layout()

    plt.savefig(
        missing_path
    )

    plt.close()

    charts.append(
        missing_path
    )

    # ==========================
    # Target Distribution
    # ==========================

    if target_column in df.columns:

        plt.figure(figsize=(8, 5))

        sns.histplot(
            df[target_column],
            kde=True
        )

        plt.title(
            f"{target_column} Distribution"
        )

        distribution_path = (
            "uploads/reports/"
            "target_distribution.png"
        )

        plt.tight_layout()

        plt.savefig(
            distribution_path
        )

        plt.close()

        charts.append(
            distribution_path
        )

    # ==========================
    # Feature Importance
    # ==========================

    if (
        target_column in numeric_df.columns
        and len(numeric_df.columns) > 1
    ):

        correlation = (
            numeric_df.corr()[
                target_column
            ]
            .drop(target_column)
            .sort_values(
                ascending=False
            )
        )

        plt.figure(figsize=(8, 5))

        correlation.plot(
            kind="bar"
        )

        plt.title(
            f"Feature Impact on {target_column}"
        )

        importance_path = (
            "uploads/reports/"
            "feature_importance.png"
        )

        plt.tight_layout()

        plt.savefig(
            importance_path
        )

        plt.close()

        charts.append(
            importance_path
        )

    return charts