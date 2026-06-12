import os

import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd


def generate_charts(
    df,
    target_column
):

    os.makedirs(
        "uploads/reports",
        exist_ok=True
    )

    charts = []

    numeric_cols = list(
        df.select_dtypes(
            include=["number"]
        ).columns
    )

    categorical_cols = list(
        df.select_dtypes(
            exclude=["number"]
        ).columns
    )

    # ==========================
    # TARGET DISTRIBUTION
    # ==========================

    if target_column in numeric_cols:

        plt.figure(figsize=(8, 5))

        sns.histplot(
            df[target_column],
            kde=True
        )

        plt.title(
            f"{target_column} Distribution"
        )

        path = (
            "uploads/reports/"
            "target_distribution.png"
        )

        plt.tight_layout()

        plt.savefig(path)

        plt.close()

        charts.append(
            {
                "title":
                "Target Distribution",

                "path":
                path
            }
        )

    # ==========================
    # CORRELATION HEATMAP
    # ==========================

    if len(numeric_cols) >= 2:

        plt.figure(figsize=(8, 6))

        sns.heatmap(
            df[numeric_cols].corr(),
            annot=True,
            cmap="coolwarm"
        )

        plt.title(
            "Correlation Heatmap"
        )

        path = (
            "uploads/reports/"
            "heatmap.png"
        )

        plt.tight_layout()

        plt.savefig(path)

        plt.close()

        charts.append(
            {
                "title":
                "Correlation Heatmap",

                "path":
                path
            }
        )

    # ==========================
    # FEATURE IMPORTANCE
    # ==========================

    if (
        target_column in numeric_cols
        and
        len(numeric_cols) >= 2
    ):

        corr = (
            df[numeric_cols]
            .corr()[target_column]
            .drop(target_column)
            .abs()
            .sort_values(
                ascending=False
            )
        )

        if len(corr) > 0:

            plt.figure(
                figsize=(8, 5)
            )

            corr.plot(
                kind="bar"
            )

            plt.title(
                "Feature Influence"
            )

            path = (
                "uploads/reports/"
                "feature_importance.png"
            )

            plt.tight_layout()

            plt.savefig(path)

            plt.close()

            charts.append(
                {
                    "title":
                    "Feature Importance",

                    "path":
                    path
                }
            )

    # ==========================
    # CATEGORICAL DISTRIBUTION
    # ==========================

    if len(categorical_cols) > 0:

        best_col = max(
            categorical_cols,
            key=lambda x:
            df[x].nunique()
        )

        if (
            df[best_col]
            .nunique()
            <= 20
        ):

            plt.figure(
                figsize=(8, 5)
            )

            df[
                best_col
            ].value_counts().plot(
                kind="bar"
            )

            plt.title(
                f"{best_col} Distribution"
            )

            path = (
                "uploads/reports/"
                "category_distribution.png"
            )

            plt.tight_layout()

            plt.savefig(path)

            plt.close()

            charts.append(
                {
                    "title":
                    "Category Distribution",

                    "path":
                    path
                }
            )

    return charts