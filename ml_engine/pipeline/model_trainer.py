import os
import joblib
import pandas as pd
import json
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


def train_models(df, target_column, problem_type):

    X = df.drop(columns=[target_column])

    y = df[target_column]

    X = pd.get_dummies(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    results = {}
    trained_models = {}

    if problem_type == "classification":

        models = {
            "Logistic Regression": LogisticRegression(max_iter=1000),
            "Random Forest": RandomForestClassifier()
        }

        for name, model in models.items():

            model.fit(X_train, y_train)

            predictions = model.predict(X_test)

            accuracy = accuracy_score(y_test, predictions)

            results[name] = round(accuracy, 4)

            trained_models[name] = model

    else:

        models = {
            "Linear Regression": LinearRegression(),
            "Random Forest": RandomForestRegressor()
        }

        for name, model in models.items():

            model.fit(X_train, y_train)

            predictions = model.predict(X_test)

            score = r2_score(y_test, predictions)

            results[name] = round(score, 4)

            trained_models[name] = model

    # Best model
    best_model_name = max(results, key=results.get)

    best_model = trained_models[best_model_name]

    # Create folders
    os.makedirs("ml_engine/models", exist_ok=True)
    os.makedirs("ml_engine/logs", exist_ok=True)

    # Save model
    model_path = f"ml_engine/models/{best_model_name}.pkl"

    joblib.dump(best_model, model_path)

    # Save metadata
    metadata = {
        "target_column": target_column,
        "feature_columns": list(X.columns),
        "problem_type": problem_type,
        "best_model": best_model_name,
        "model_path": model_path
    }

    with open(
        "ml_engine/models/model_metadata.json",
        "w"
    ) as f:

        json.dump(metadata, f, indent=4)

    # Save training history
    history_record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "best_model": best_model_name,
        "scores": results,
        "problem_type": problem_type,
        "target_column": target_column
    }

    history_file = "ml_engine/logs/training_history.json"

    try:
        with open(history_file, "r") as f:
            history = json.load(f)

    except:
        history = []

    history.append(history_record)

    with open(history_file, "w") as f:
        json.dump(history, f, indent=4)

    return {
        "scores": results,
        "best_model": best_model_name,
        "model_path": model_path
    }