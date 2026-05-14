# 🚀 Autonomous Data Intelligence Platform

An AI-powered cloud platform that automates the complete data analysis workflow — from raw dataset upload to intelligent insights, machine learning model generation, and prediction APIs.

This project simulates a real-world autonomous data scientist system inspired by modern AutoML platforms like DataRobot and Google AutoML.

---

# 🔥 Key Features

## 📂 Smart Dataset Upload
- Upload CSV/Excel datasets
- Secure cloud storage using AWS S3
- Automatic dataset tracking with Job IDs

---

## 🧹 Automated Data Cleaning Engine
The system automatically:
- Handles missing values
- Detects and removes outliers
- Encodes categorical features
- Prepares datasets for ML training

---

## 🤖 Auto ML Pipeline
Automatically detects:
- Classification problems
- Regression problems

Then trains multiple ML models:
- Linear Regression
- Logistic Regression
- Random Forest
- XGBoost

Selects the best-performing model automatically.

---

## 📊 Intelligent Insight Generator
The platform generates automated insights such as:
- Feature correlations
- Statistical trends
- Pattern detection
- Important feature identification

Example:
> “Sales increase significantly during weekends.”

---

## 📈 Visualization Dashboard
Interactive dashboard for:
- Dataset preview
- Charts and trends
- Model performance
- Feature importance
- Prediction outputs

---

## 🔮 Prediction API
Users can submit new data and receive:
- Real-time predictions
- Confidence scores
- Model-generated outputs

---

# 🏗️ System Architecture

```text
Frontend (Streamlit)
        ↓
FastAPI Backend
        ↓
Upload API
        ↓
AWS S3 Bucket
        ↓
Lambda Trigger
        ↓
EC2 ML Processing Engine
        ↓
Model + Insights Storage
        ↓
Prediction API + Dashboard
