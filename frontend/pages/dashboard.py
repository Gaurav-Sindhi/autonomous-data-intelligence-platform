import streamlit as st
import pandas as pd
import json
import requests
from utils.api import upload_dataset, predict

BACKEND_URL = "http://127.0.0.1:8000"

# =====================================================
# PAGE CONFIG & TITLE
# =====================================================

st.title("🚀 Autonomous Data Intelligence Platform")
st.caption(
    "Upload datasets, generate AI insights, train models automatically, and make predictions."
)

# =====================================================
# SESSION STATE INITIALIZATION
# =====================================================

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None

if "preview_df_json" not in st.session_state:
    st.session_state.preview_df_json = None

st.markdown("---")

# =====================================================
# DATASET UPLOAD
# =====================================================

st.header("📂 Dataset Upload")

uploaded_file = st.file_uploader("Upload CSV Dataset", type=["csv"])

if uploaded_file is not None:
    preview_df = pd.read_csv(uploaded_file)
    st.subheader("Dataset Preview")
    st.dataframe(preview_df.head(), use_container_width=True)

analyze_btn = st.button("🚀 Analyze Dataset")

# =====================================================
# ANALYZE DATASET (only on button click, only once)
# =====================================================

if analyze_btn:
    if uploaded_file is None:
        st.warning("Please upload a CSV file before analyzing.")
    else:
        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "text/csv",
            )
        }
        with st.spinner("Analyzing dataset and training models..."):
            response = upload_dataset(files)

        if response.status_code == 200:
            st.session_state.analysis_result = response.json()
            st.session_state.uploaded_file_name = uploaded_file.name
            st.success("Dataset analyzed successfully!")
        else:
            st.error(f"Backend Error: {response.text}")

# =====================================================
# CLEAR ANALYSIS BUTTON (top-level, always visible
# when results exist)
# =====================================================

if st.session_state.analysis_result is not None:
    if st.button("🗑 Clear Analysis"):
        st.session_state.analysis_result = None
        st.session_state.uploaded_file_name = None
        st.session_state.preview_df_json = None
        st.rerun()

# =====================================================
# RENDER DASHBOARD FROM CACHED SESSION STATE
# =====================================================

if st.session_state.analysis_result is not None:

    api_response = st.session_state.analysis_result
    result = api_response["insights"]

    raw = result["raw_insights"]
    cleaned = result["cleaned_insights"]
    problem = result["problem_info"]
    training = result["training_results"]
    charts = result["charts"]
    ai_insights = result["ai_insights"]
    model_reasoning = result["model_reasoning"]
    analytics_insight = result["analytics_insight"]
    pdf_report = result.get("pdf_report")
    model_file = result.get("model_file")
    cleaned_dataset = result.get("cleaned_dataset")

    st.success("✅ Analysis Loaded From Cache")

    # =====================================================
    # EXECUTIVE SUMMARY
    # =====================================================

    st.markdown("---")
    st.header("📋 Executive Summary")

    best_score = max(training["scores"].values())

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Problem Type", problem["problem_type"])
    c2.metric("Target Column", problem["target_column"])
    c3.metric("Best Model", training["best_model"])
    c4.metric("Best Score", round(best_score, 4))

    # =====================================================
    # DATA QUALITY REPORT
    # =====================================================

    st.markdown("---")
    st.header("📊 Data Quality Report")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Before Cleaning")
        st.metric("Missing Values", raw["missing_values"])
        st.metric("Duplicates", raw["duplicate_rows"])

    with col2:
        st.subheader("After Cleaning")
        st.metric("Missing Values", cleaned["missing_values"])
        st.metric("Duplicates", cleaned["duplicate_rows"])

    if cleaned_dataset:
        try:
            with open(cleaned_dataset, "rb") as f:
                cleaned_bytes = f.read()
            st.download_button(
                label="📥 Download Cleaned Dataset",
                data=cleaned_bytes,
                file_name="cleaned_dataset.csv",
                mime="text/csv",
            )
        except Exception:
            st.warning("Cleaned dataset file not available.")

    # =====================================================
    # AI ANALYTICS SUMMARY
    # =====================================================

    st.markdown("---")
    st.header("🤖 AI Analytics Summary")
    st.info(result.get("analytics_insight", "No analytics summary available."))

    # =====================================================
    # MODEL PERFORMANCE
    # =====================================================

    st.markdown("---")
    st.header("🏆 Model Performance")

    scores_df = pd.DataFrame(
        list(training["scores"].items()),
        columns=["Model", "Score"],
    )
    scores_df = scores_df.sort_values("Score", ascending=False)

    left, right = st.columns(2)

    with left:
        st.subheader("Model Leaderboard")
        st.dataframe(scores_df, use_container_width=True)

    with right:
        st.subheader("Performance Comparison")
        st.bar_chart(scores_df.set_index("Model"))

    # =====================================================
    # ADVANCED ANALYTICS CHARTS
    # =====================================================

    st.markdown("---")
    st.header("📈 Advanced Analytics")

    if not charts:
        st.info("No meaningful visualizations available.")
    else:
        for chart in charts:
            st.subheader(chart["title"])
            image_url = (
                BACKEND_URL + "/" + chart["path"].replace("uploads/", "")
            )
            st.image(image_url, use_container_width=True)

    # =====================================================
    # AI DATASET INSIGHTS
    # =====================================================

    st.markdown("---")
    st.header("🧠 AI Dataset Insights")
    st.success(result.get("ai_insights", "No AI insights generated."))

    # =====================================================
    # MODEL SELECTION REASONING
    # =====================================================

    st.markdown("---")
    st.header("🎯 Model Selection Reasoning")
    st.info(result.get("model_reasoning", "No model reasoning available."))

    # =====================================================
    # DOWNLOAD REPORTS
    # =====================================================

    st.markdown("---")
    st.header("📥 Download Reports")

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="📊 Download JSON Report",
            data=json.dumps(result, indent=4),
            file_name="analysis_report.json",
            mime="application/json",
        )

    with col2:
        if pdf_report:
            try:
                with open(pdf_report, "rb") as pdf_file:
                    pdf_bytes = pdf_file.read()
                st.download_button(
                    label="📄 Download PDF Report",
                    data=pdf_bytes,
                    file_name="analysis_report.pdf",
                    mime="application/pdf",
                )
            except Exception:
                st.warning("PDF report not available.")
        else:
            st.info("Generate a dataset report first.")

    # =====================================================
    # TRAINED MODEL DOWNLOAD
    # =====================================================

    if model_file:
        try:
            with open(model_file, "rb") as mf:
                model_bytes = mf.read()
            st.download_button(
                label="🤖 Download Trained Model",
                data=model_bytes,
                file_name="best_model.pkl",
                mime="application/octet-stream",
            )
        except Exception:
            st.warning("Trained model file not available.")

    # =====================================================
    # PREDICTION CENTER
    # =====================================================

    st.markdown("---")
    st.header("🔮 Prediction Center")

    try:
        metadata_response = requests.get(f"{BACKEND_URL}/metadata")
        metadata = metadata_response.json()
    except Exception:
        metadata = {}
        st.warning("Could not load model metadata from backend.")

    if "feature_columns" in metadata:
        feature_columns = metadata["feature_columns"]
        prediction_payload = {}

        with st.form("prediction_form"):
            for feature in feature_columns:
                value = st.text_input(feature, "")
                prediction_payload[feature] = value

            submit = st.form_submit_button("Predict")

        if submit:
            try:
                response = requests.post(
                    f"{BACKEND_URL}/predict",
                    json=prediction_payload,
                )
                if response.status_code == 200:
                    prediction = response.json()
                    st.success(f"Prediction: {prediction['prediction']}")
                    st.info(prediction["explanation"])
                else:
                    st.error("Prediction failed.")
            except Exception as e:
                st.error(f"Prediction request error: {e}")
    else:
        st.info("No feature columns available for prediction.")