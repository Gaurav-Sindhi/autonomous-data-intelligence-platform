from ml_engine.agents.model_selection_agent import (
    explain_model_choice
)

problem_info = {
    "target_column": "salary",
    "problem_type": "regression"
}

training_results = {
    "scores": {
        "Linear Regression": 0.9853,
        "Random Forest": 0.9757
    },
    "best_model": "Linear Regression"
}

result = explain_model_choice(
    problem_info,
    training_results
)

print(result)