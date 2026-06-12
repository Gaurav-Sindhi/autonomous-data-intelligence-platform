import streamlit as st
import pandas as pd
import json
import requests

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

        raw = result["raw_insights"]

        cleaned = result["cleaned_insights"]

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
        st.header("📊 Data Quality Report")

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Before Cleaning")

            st.metric(
                "Missing Values",
                raw["missing_values"]
            )

            st.metric(
                "Duplicates",
                raw["duplicate_rows"]
            )

        with col2:

            st.subheader("After Cleaning")

            st.metric(
                "Missing Values",
                cleaned["missing_values"]
            )

            st.metric(
                "Duplicates",
                cleaned["duplicate_rows"]
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
        st.header("📈 Advanced Analytics"
        )

        charts = insights.get(
            "charts",
            []
        )

        if not charts:

            st.info(
                "No meaningful visualizations available."
            )

        else:

            for chart in charts:

                st.subheader(
                    chart["title"]
                )

                image_url = (
                    BACKEND_URL + "/" +
                    chart["path"]
                    .replace(
                        "uploads/",
                        ""
                    )
                )

                st.image(
                    image_url,
                    use_container_width=True
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

        st.header("📥 Download Reports")

        col1, col2 = st.columns(2)

        # ==========================
        # JSON REPORT
        # ==========================

        with col1:

            st.download_button(
                label="📊 Download JSON Report",
                data=json.dumps(
                    result,
                    indent=4
                ),
                file_name="analysis_report.json",
                mime="application/json"
            )

        # ==========================
        # PDF REPORT
        # ==========================

        with col2:

            pdf_path = insights.get(
                "pdf_report"
            )

            if pdf_path:

                try:

                    with open(
                        pdf_path,
                        "rb"
                    ) as pdf_file:

                        st.download_button(
                            label="📄 Download PDF Report",
                            data=pdf_file,
                            file_name="analysis_report.pdf",
                            mime="application/pdf"
                        )

                except Exception as e:

                    st.warning(
                        "PDF report not available."
                    )

            else:

                st.info(
                    "Generate a dataset report first."
                )

# =====================================================
# PREDICTION CENTER
# =====================================================

        st.markdown("---")

        metadata_response = requests.get(
            f"{BACKEND_URL}/metadata"
        )

        metadata = metadata_response.json()

        st.header("🔮 Prediction Center")

        if "feature_columns" in metadata:

            feature_columns = metadata["feature_columns"]

            prediction_payload = {}

            with st.form("prediction_form"):

                for feature in feature_columns:

                    value = st.text_input(
                        feature,
                        ""
                    )

                    prediction_payload[
                        feature
                    ] = value

                submit = st.form_submit_button(
                    "Predict"
                )

            if submit:

                response = requests.post(
                    f"{BACKEND_URL}/predict",
                    json=prediction_payload
                )

                if response.status_code == 200:

                    prediction = response.json()

                    st.success(
                        f"Prediction: {prediction['prediction']}"
                    )

                    st.info(
                        prediction["explanation"]
                    )

                else:

                    st.error(
                        "Prediction failed"
                    )