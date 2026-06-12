import os
import json
import joblib
import pandas as pd

from datetime import datetime

from sklearn.model_selection import train_test_split

# Classification
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Regression
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

# XGBoost
from xgboost import XGBClassifier
from xgboost import XGBRegressor


def train_models(df, target_column, problem_type):

    # ==========================
    # Features & Target
    # ==========================

    X = df.drop(columns=[target_column])
    y = df[target_column]

    # Convert categorical features
    original_feature_columns = list(X.columns)
    X = pd.get_dummies(X)

    # ==========================
    # Train Test Split
    # ==========================

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    results = {}
    trained_models = {}

    # ==========================
    # Classification Models
    # ==========================

    if problem_type == "classification":

        models = {

            "Logistic Regression":
                LogisticRegression(
                    max_iter=1000
                ),

            "Random Forest":
                RandomForestClassifier(
                    random_state=42
                ),

            "XGBoost":
                XGBClassifier(
                    n_estimators=100,
                    learning_rate=0.1,
                    max_depth=4,
                    eval_metric="logloss",
                    random_state=42
                )
        }

        for name, model in models.items():

            model.fit(X_train, y_train)

            predictions = model.predict(X_test)

            score = accuracy_score(
                y_test,
                predictions
            )

            results[name] = round(score, 4)

            trained_models[name] = model

    # ==========================
    # Regression Models
    # ==========================

    else:

        models = {

            "Linear Regression":
                LinearRegression(),

            "Random Forest":
                RandomForestRegressor(
                    random_state=42
                ),

            "XGBoost":
                XGBRegressor(
                    n_estimators=100,
                    learning_rate=0.1,
                    max_depth=4,
                    random_state=42
                )
        }

        for name, model in models.items():

            model.fit(X_train, y_train)

            predictions = model.predict(X_test)

            score = r2_score(
                y_test,
                predictions
            )

            results[name] = round(score, 4)

            trained_models[name] = model

    # ==========================
    # Best Model Selection
    # ==========================

    best_model_name = max(
        results,
        key=results.get
    )

    best_model = trained_models[
        best_model_name
    ]

    # ==========================
    # Create Directories
    # ==========================

    os.makedirs(
        "ml_engine/models",
        exist_ok=True
    )

    os.makedirs(
        "ml_engine/logs",
        exist_ok=True
    )

    # ==========================
    # Save Best Model
    # ==========================

    model_path = (
        f"ml_engine/models/"
        f"{best_model_name}.pkl"
    )

    joblib.dump(
        best_model,
        model_path
    )

    # ==========================
    # Save Metadata
    # ==========================

    metadata = {
    "target_column": target_column,

    "original_features":
        original_feature_columns,

    "encoded_features":
        list(X.columns),

    "problem_type":
        problem_type,

    "best_model":
        best_model_name,

    "model_path":
        model_path
}

    with open(
        "ml_engine/models/model_metadata.json",
        "w"
    ) as f:

        json.dump(
            metadata,
            f,
            indent=4
        )

    # ==========================
    # Training History
    # ==========================

    history_record = {

        "timestamp":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "best_model":
            best_model_name,

        "scores":
            results,

        "problem_type":
            problem_type,

        "target_column":
            target_column
    }

    history_file = (
        "ml_engine/logs/"
        "training_history.json"
    )

    try:

        with open(
            history_file,
            "r"
        ) as f:

            history = json.load(f)

    except:

        history = []

    history.append(
        history_record
    )

    with open(
        history_file,
        "w"
    ) as f:

        json.dump(
            history,
            f,
            indent=4
        )

    # ==========================
    # Return Results
    # ==========================

    return {
        "scores": results,
        "best_model": best_model_name,
        "model_path": model_path
    }