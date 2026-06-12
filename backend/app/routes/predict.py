from fastapi import APIRouter
from typing import Dict, Any
import pandas as pd
import joblib
import json
import os
from ml_engine.agents.prediction_agent import explain_prediction

router = APIRouter()

METADATA_PATH = "ml_engine/models/model_metadata.json"

@router.post("/predict")
async def predict(
    data: Dict[str, Any]):

    if not os.path.exists(METADATA_PATH):
        return {
            "error": "Metadata file not found"
        }

    with open(METADATA_PATH, "r") as f:
        metadata = json.load(f)

    model_path = metadata["model_path"]

    if not os.path.exists(model_path):
        return {
            "error": "Model file not found"
        }

    model = joblib.load(model_path)

    input_df = pd.DataFrame([data])

    input_df = pd.get_dummies(
    input_df
)

    encoded_columns = metadata[
    "encoded_features"
    ]

    for col in encoded_columns:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[encoded_columns]

    prediction = model.predict(
        input_df
    )[0]

    explanation = explain_prediction(
        prediction,
        data
    )

    return {
        "prediction": float(prediction),
        "explanation": explanation
    }