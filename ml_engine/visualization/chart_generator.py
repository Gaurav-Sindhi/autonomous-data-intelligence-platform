import os
import matplotlib.pyplot as plt


def generate_charts(df):

    os.makedirs("uploads/reports", exist_ok=True)

    charts = []

    numeric_columns = df.select_dtypes(include=["number"]).columns

    for col in numeric_columns:

        plt.figure(figsize=(6,4))

        df[col].hist()

        plt.title(col)

        chart_path = f"uploads/reports/{col}.png"

        plt.savefig(chart_path)

        plt.close()

        charts.append(chart_path)

    return charts