import streamlit as st
import pandas as pd
import json

from utils.api import (
    upload_dataset,
    predict
)

st.title("📊 Dashboard")

uploaded_file = st.file_uploader(
    "Upload CSV Dataset",
    type=["csv"]
)

if uploaded_file:

    preview_df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")

    st.dataframe(
        preview_df.head(),
        use_container_width=True
    )

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            "text/csv"
        )
    }

    with st.spinner(
        "Analyzing Dataset..."
    ):

        response = upload_dataset(files)

    if response.status_code == 200:

        result = response.json()

        insights = result["insights"]

        basic = insights["insights"]

        st.markdown("---")

        st.header("📈 Dataset Overview")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Rows",
            basic["rows"]
        )

        c2.metric(
            "Columns",
            basic["columns"]
        )

        c3.metric(
            "Missing",
            basic["missing_values"]
        )

        c4.metric(
            "Duplicates",
            basic["duplicate_rows"]
        )

        st.markdown("---")

        st.header("🧠 Problem Detection")

        problem = insights["problem_info"]

        c1, c2 = st.columns(2)

        c1.info(
            f"Target Column: {problem['target_column']}"
        )

        c2.info(
            f"Problem Type: {problem['problem_type']}"
        )

        st.markdown("---")

        st.header("🤖 Model Leaderboard")

        training = insights["training_results"]

        leaderboard = pd.DataFrame(
            list(
                training["scores"].items()
            ),
            columns=[
                "Model",
                "Score"
            ]
        )

        leaderboard = leaderboard.sort_values(
            "Score",
            ascending=False
        )

        st.dataframe(
            leaderboard,
            use_container_width=True
        )

        st.success(
            f"🏆 Best Model: {training['best_model']}"
        )

        st.markdown("---")

        st.header("✨ AI Dataset Insights")

        st.info(
            insights.get(
                "ai_insights",
                "No AI insights available."
            )
        )

        st.markdown("---")

        st.header("🎯 Model Selection Reasoning")

        st.info(
            insights.get(
                "model_reasoning",
                "No reasoning available."
            )
        )

        st.markdown("---")

        st.header("📈 Visual Analytics")

        charts = insights.get(
            "charts",
            []
        )

        cols = st.columns(2)

        for idx, chart in enumerate(charts):

            chart_url = (
                "http://127.0.0.1:8000/"
                + chart.replace(
                    "uploads/",
                    ""
                )
            )

            cols[idx % 2].image(
                chart_url,
                use_container_width=True
            )

        st.markdown("---")

        st.download_button(
            "📥 Download Report",
            data=json.dumps(
                result,
                indent=4
            ),
            file_name="report.json",
            mime="application/json"
        )

st.markdown("---")

st.header("🔮 Prediction Center")

with st.form("prediction_form"):

    col1, col2 = st.columns(2)

    age = col1.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=30
    )

    experience = col2.number_input(
        "Experience",
        min_value=0,
        max_value=50,
        value=5
    )

    submit = st.form_submit_button(
        "Predict"
    )

if submit:

    payload = {
        "age": age,
        "experience": experience
    }

    response = predict(payload)

    if response.status_code == 200:

        result = response.json()

        st.success(
            f"💰 Predicted Value: ₹ {result['prediction']:,.2f}"
        )

        st.markdown(
            "### 🤖 AI Explanation"
        )

        st.info(
            result["explanation"]
        )