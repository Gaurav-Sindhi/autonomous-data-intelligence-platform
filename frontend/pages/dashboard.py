import streamlit as st
import pandas as pd
import json

from utils.api import (
    upload_dataset,
    predict
)

BACKEND_URL = "http://127.0.0.1:8000"

st.title("🚀 Autonomous Data Intelligence Platform")

st.caption(
    "Upload datasets, generate AI insights, train models automatically, and make predictions."
)

st.markdown("---")

# =====================================================
# DATASET UPLOAD
# =====================================================

st.header("📂 Dataset Upload")

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
        "Analyzing dataset and training models..."
    ):

        response = upload_dataset(files)

    if response.status_code == 200:

        result = response.json()

        insights = result["insights"]

        basic = insights["insights"]

        problem = insights["problem_info"]

        training = insights["training_results"]

        # =====================================================
        # EXECUTIVE SUMMARY
        # =====================================================

        st.markdown("---")

        st.header("📋 Executive Summary")

        best_score = max(
            training["scores"].values()
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Problem Type",
            problem["problem_type"]
        )

        c2.metric(
            "Target Column",
            problem["target_column"]
        )

        c3.metric(
            "Best Model",
            training["best_model"]
        )

        c4.metric(
            "Best Score",
            round(best_score, 4)
        )

        # =====================================================
        # DATASET HEALTH
        # =====================================================

        st.markdown("---")

        st.header("📊 Dataset Health")

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
            "Missing Values",
            basic["missing_values"]
        )

        c4.metric(
            "Duplicate Rows",
            basic["duplicate_rows"]
        )

        # =====================================================
        # AI ANALYTICS SUMMARY
        # =====================================================

        st.markdown("---")

        st.header("🤖 AI Analytics Summary")

        st.info(
            insights.get(
                "analytics_insight",
                "No analytics summary available."
            )
        )

        # =====================================================
        # MODEL PERFORMANCE
        # =====================================================

        st.markdown("---")

        st.header("🏆 Model Performance")

        scores_df = pd.DataFrame(
            list(
                training["scores"].items()
            ),
            columns=[
                "Model",
                "Score"
            ]
        )

        scores_df = scores_df.sort_values(
            "Score",
            ascending=False
        )

        left, right = st.columns(2)

        with left:

            st.subheader(
                "Model Leaderboard"
            )

            st.dataframe(
                scores_df,
                use_container_width=True
            )

        with right:

            st.subheader(
                "Performance Comparison"
            )

            st.bar_chart(
                scores_df.set_index(
                    "Model"
                )
            )

        # =====================================================
        # ADVANCED ANALYTICS
        # =====================================================

        st.markdown("---")

        st.header("📈 Advanced Analytics")

        charts = insights.get(
            "charts",
            []
        )

        if len(charts) >= 4:

            row1_col1, row1_col2 = st.columns(2)

            with row1_col1:

                st.subheader(
                    "🔥 Correlation Heatmap"
                )

                st.image(
                    BACKEND_URL + "/" +
                    charts[0].replace(
                        "uploads/",
                        ""
                    ),
                    use_container_width=True
                )

            with row1_col2:

                st.subheader(
                    "🎯 Feature Importance"
                )

                st.image(
                    BACKEND_URL + "/" +
                    charts[3].replace(
                        "uploads/",
                        ""
                    ),
                    use_container_width=True
                )

            row2_col1, row2_col2 = st.columns(2)

            with row2_col1:

                st.subheader(
                    "📈 Target Distribution"
                )

                st.image(
                    BACKEND_URL + "/" +
                    charts[2].replace(
                        "uploads/",
                        ""
                    ),
                    use_container_width=True
                )

            with row2_col2:

                st.subheader(
                    "🧹 Data Quality Analysis"
                )

                st.image(
                    BACKEND_URL + "/" +
                    charts[1].replace(
                        "uploads/",
                        ""
                    ),
                    use_container_width=True
                )

        else:

            st.warning(
                "Charts not available."
            )

        # =====================================================
        # AI DATASET INSIGHTS
        # =====================================================

        st.markdown("---")

        st.header("🧠 AI Dataset Insights")

        st.success(
            insights.get(
                "ai_insights",
                "No AI insights generated."
            )
        )

        # =====================================================
        # MODEL REASONING
        # =====================================================

        st.markdown("---")

        st.header("🎯 Model Selection Reasoning")

        st.info(
            insights.get(
                "model_reasoning",
                "No model reasoning available."
            )
        )

        # =====================================================
        # DOWNLOAD REPORT
        # =====================================================

        st.markdown("---")

        st.header("📥 Download Report")

        st.download_button(
            label="Download Full Analysis Report",
            data=json.dumps(
                result,
                indent=4
            ),
            file_name="analysis_report.json",
            mime="application/json"
        )

# =====================================================
# PREDICTION CENTER
# =====================================================

st.markdown("---")

st.header("🔮 Prediction Center")

st.caption(
    "Predict values using the best trained model."
)

with st.form(
    "prediction_form"
):

    col1, col2 = st.columns(2)

    age = col1.number_input(
        "Age",
        min_value=0,
        value=30
    )

    experience = col2.number_input(
        "Experience",
        min_value=0,
        value=5
    )

    submit = st.form_submit_button(
        "Generate Prediction"
    )

if submit:

    payload = {
        "age": age,
        "experience": experience
    }

    response = predict(
        payload
    )

    if response.status_code == 200:

        prediction = response.json()

        st.success(
            f"💰 Prediction: ₹ {prediction['prediction']:,.2f}"
        )

        st.markdown(
            "### 🤖 AI Prediction Explanation"
        )

        st.info(
            prediction["explanation"]
        )

    else:

        st.error(
            "Prediction failed."
        )