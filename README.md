# 🚀 Autonomous Data Intelligence Platform (ADI)

An AI-powered platform that automatically transforms raw datasets into actionable insights through data cleaning, exploratory data analysis, machine learning, automated reporting, and intelligent predictions.

## 🌟 Overview

Autonomous Data Intelligence (ADI) eliminates the need for manual data preprocessing and model selection by automating the complete machine learning workflow. Users can upload a dataset and instantly receive:

* Automated Data Cleaning
* Exploratory Data Analysis (EDA)
* Interactive Visualizations
* AI-Generated Dataset Insights
* Automated Model Training & Evaluation
* Best Model Selection
* Prediction Interface
* Downloadable PDF Reports
* Cleaned Dataset Export

---

## ✨ Key Features

### 📂 Smart Dataset Upload

* Upload CSV datasets directly through the dashboard
* Automatic dataset profiling
* Dataset health assessment

### 🧹 Automated Data Cleaning

* Missing value handling
* Duplicate record detection
* Data preprocessing pipeline
* Cleaned dataset generation

### 📊 Exploratory Data Analysis

* Target distribution analysis
* Correlation heatmaps
* Feature importance analysis
* Category distributions
* Statistical summaries

### 🤖 AI-Powered Insights

* Dataset quality assessment
* Data cleaning impact analysis
* Pattern discovery
* Risk identification
* Business recommendations

### 🏆 AutoML Engine

Supports automatic training and evaluation of:

#### Classification

* Logistic Regression
* Random Forest Classifier

#### Regression

* Linear Regression
* Random Forest Regressor

The platform automatically selects the best-performing model.

### 🔮 Prediction Center

* Dynamic prediction forms
* Dataset-aware feature inputs
* AI-generated prediction explanations

### 📑 Automated Reporting

Generate downloadable PDF reports containing:

* Dataset summary
* Data quality metrics
* Model performance
* AI-generated insights
* Recommendations

---

## 🏗️ System Architecture

```text
User Upload
     │
     ▼
Dataset Validation
     │
     ▼
Data Cleaning Pipeline
     │
     ▼
EDA & Visualization Engine
     │
     ▼
AutoML Training Engine
     │
     ▼
AI Insight Generation
     │
     ▼
PDF Report Generation
     │
     ▼
Prediction Dashboard
```

---

## 🛠️ Tech Stack

### Backend

* FastAPI
* Python

### Frontend

* Streamlit

### Data Processing

* Pandas
* NumPy

### Machine Learning

* Scikit-Learn
* Random Forest
* Logistic Regression
* Linear Regression

### AI Integration

* Google Gemini API

### Visualization

* Matplotlib

### Reporting

* ReportLab

### Utilities

* Joblib
* JSON
* REST APIs

---

## 📈 Workflow

1. Upload Dataset
2. Automatic Data Cleaning
3. Problem Type Detection
4. Model Training & Evaluation
5. AI Insight Generation
6. Report Generation
7. Prediction Deployment

---

## 📸 Dashboard Modules

### Executive Summary

Quick overview of:

* Dataset statistics
* Best model
* Performance score

### Dataset Health

* Missing values
* Duplicate records
* Dataset dimensions

### AI Analytics Summary

Business-focused interpretation of dataset quality and risks.

### Model Performance

Leaderboard ranking of trained models.

### Advanced Analytics

Automatically generated visualizations and feature insights.

### Prediction Center

Generate predictions using the best trained model.

---

## 🎯 Project Highlights

* Fully automated machine learning workflow
* Dynamic support for multiple datasets
* AI-powered analytical reasoning
* Automated report generation
* Production-ready architecture
* Clean and scalable modular design

---

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/your-username/autonomous-data-intelligence-platform.git
cd autonomous-data-intelligence-platform
```

### Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

### Start Backend

```bash
python -m uvicorn backend.app.main:app --reload
```

### Start Frontend

```bash
streamlit run frontend/app.py
```

---

## 📌 Future Enhancements

* AWS S3 Integration
* Multi-user Authentication
* Model Versioning
* Cloud Deployment
* Advanced AutoML Models
* Real-time Monitoring
* Dataset History Tracking

---

## 👨‍💻 Developer

**Gaurav Sindhi**

B.Tech – Artificial Intelligence & Machine Learning

Passionate about Machine Learning, Data Science, MLOps, and AI-powered automation systems.

---

## 📄 License

Copyright © 2026 Gaurav Sindhi

All Rights Reserved.
