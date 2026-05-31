import os
import joblib
import pandas as pd

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
            "Logistic Regression":
                LogisticRegression(max_iter=1000),

            "Random Forest":
                RandomForestClassifier()
        }

        for name, model in models.items():

            model.fit(X_train, y_train)

            predictions = model.predict(X_test)

            accuracy = accuracy_score(y_test, predictions)

            results[name] = round(accuracy, 4)

            trained_models[name] = model

    else:

        models = {
            "Linear Regression":
                LinearRegression(),

            "Random Forest":
                RandomForestRegressor()
        }

        for name, model in models.items():

            model.fit(X_train, y_train)

            predictions = model.predict(X_test)

            score = r2_score(y_test, predictions)

            results[name] = round(score, 4)

            trained_models[name] = model

    # Find best model
    best_model_name = max(results, key=results.get)

    best_model = trained_models[best_model_name]

    # Create model directory
    os.makedirs("ml_engine/models", exist_ok=True)

    # Save model
    model_path = f"ml_engine/models/{best_model_name}.pkl"

    joblib.dump(best_model, model_path)

    return {
        "scores": results,
        "best_model": best_model_name,
        "model_path": model_path
    }