import streamlit as st
import requests
import pandas as pd

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Autonomous Data Intelligence Platform",
    layout="wide"
)

st.title("🚀 Autonomous Data Intelligence Platform")

# ==========================
# Upload Dataset
# ==========================

st.header("📂 Upload Dataset")

uploaded_file = st.file_uploader(
    "Choose CSV File",
    type=["csv"]
)

if uploaded_file:

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            "text/csv"
        )
    }

    with st.spinner("Uploading and Training..."):

        response = requests.post(
            f"{BACKEND_URL}/upload",
            files=files
        )

    if response.status_code == 200:

        result = response.json()

        st.success("Dataset Processed Successfully")

        insights = result["insights"]

        # ==========================
        # Insights
        # ==========================

        st.header("📊 Dataset Insights")

        basic = insights["insights"]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Rows", basic["rows"])
        col2.metric("Columns", basic["columns"])
        col3.metric("Missing Values", basic["missing_values"])
        col4.metric("Duplicate Rows", basic["duplicate_rows"])

        # ==========================
        # Problem Info
        # ==========================

        st.header("🧠 Problem Detection")

        problem = insights["problem_info"]

        st.write("Target Column:", problem["target_column"])
        st.write("Problem Type:", problem["problem_type"])

        # ==========================
        # Model Results
        # ==========================

        st.header("🤖 Model Performance")

        training = insights["training_results"]

        st.json(training["scores"])

        st.success(
            f"Best Model: {training['best_model']}"
        )

        # ==========================
        # Charts
        # ==========================

        st.header("📈 Charts")

        for chart in insights["charts"]:

            image_url = (
                BACKEND_URL + "/" +
                chart.replace("uploads/", "")
            )

            st.image(
                image_url,
                use_container_width=True
            )

# ==========================
# Prediction
# ==========================

st.header("🔮 Predict")

age = st.number_input(
    "Age",
    value=30
)

experience = st.number_input(
    "Experience",
    value=5
)

if st.button("Predict"):

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
            f"Prediction: {prediction['prediction']:.2f}"
        )