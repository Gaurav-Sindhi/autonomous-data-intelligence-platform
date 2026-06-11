import streamlit as st
import requests
import pandas as pd
import json

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Autonomous Data Intelligence Platform",
    page_icon="🚀",
    layout="wide"
)

# ==========================
# SIDEBAR
# ==========================

st.sidebar.title("🚀 ADI Platform")
st.sidebar.success("AI-Powered Dataset Intelligence")

st.sidebar.markdown("---")

st.sidebar.markdown("""
### Features

✅ Dataset Upload

✅ Data Cleaning

✅ Insight Generation

✅ Problem Detection

✅ AutoML Training

✅ Model Selection

✅ Prediction API

✅ Visual Analytics
""")

# ==========================
# HEADER
# ==========================

st.title("🚀 Autonomous Data Intelligence Platform")

st.caption(
    "Upload datasets, generate insights, train models automatically, and make predictions."
)

st.markdown("---")

# ==========================
# DATASET UPLOAD
# ==========================

st.header("📂 Dataset Upload")

uploaded_file = st.file_uploader(
    "Choose CSV File",
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

    with st.spinner("Analyzing dataset and training models..."):

        response = requests.post(
            f"{BACKEND_URL}/upload",
            files=files
        )

    if response.status_code == 200:

        result = response.json()

        st.success("Dataset Processed Successfully")

        insights = result["insights"]

        # ==========================
        # DATASET OVERVIEW
        # ==========================

        st.header("📊 Dataset Overview")

        basic = insights["insights"]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Rows", basic["rows"])
        col2.metric("Columns", basic["columns"])
        col3.metric("Missing Values", basic["missing_values"])
        col4.metric("Duplicate Rows", basic["duplicate_rows"])

        st.markdown("---")

        # ==========================
        # PROBLEM DETECTION
        # ==========================

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

        # ==========================
        # MODEL PERFORMANCE
        # ==========================

        st.header("🤖 Model Leaderboard")

        training = insights["training_results"]

        scores_df = pd.DataFrame(
            list(training["scores"].items()),
            columns=["Model", "Score"]
        )

        scores_df = scores_df.sort_values(
            "Score",
            ascending=False
        )

        st.dataframe(
            scores_df,
            use_container_width=True
        )

        st.success(
            f"🏆 Best Model: {training['best_model']}"
        )

        st.markdown("---")

        # ==========================
        # CHARTS
        # ==========================

        st.header("📈 Visual Analytics")

        chart_cols = st.columns(2)

        charts = insights.get("charts", [])

        for idx, chart in enumerate(charts):

            image_url = (
                BACKEND_URL + "/" +
                chart.replace("uploads/", "")
            )

            chart_cols[idx % 2].image(
                image_url,
                use_container_width=True
            )

        st.markdown("---")

        # ==========================
        # DOWNLOAD REPORT
        # ==========================

        st.header("📥 Download Report")

        st.download_button(
            label="Download Analysis Report",
            data=json.dumps(
                result,
                indent=4
            ),
            file_name="analysis_report.json",
            mime="application/json"
        )

# ==========================
# PREDICTION SECTION
# ==========================

st.markdown("---")

st.header("🔮 Prediction")

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
        "Predict Salary"
    )

if submit:

    payload = {
        "age": age,
        "experience": experience
    }

    response = requests.post(
        f"{BACKEND_URL}/predict",
        json=payload
    )

    if response.status_code == 200:

        prediction = response.json()

        st.success(
            f"💰 Predicted Salary: ₹ {prediction['prediction']:,.2f}"
        )