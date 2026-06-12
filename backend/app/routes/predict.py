from fastapi import APIRouter
from pydantic import BaseModel
from ml_engine.agents.prediction_agent import (
    explain_prediction
)
import pandas as pd
import joblib
import json
import os


router = APIRouter()

METADATA_PATH = "ml_engine/models/model_metadata.json"


class PredictionInput(BaseModel):
    age: int
    experience: int


@router.post("/predict")
async def predict(data: PredictionInput):

    if not os.path.exists(METADATA_PATH):
        return {
            "error": "Metadata file not found"
        }

    with open(METADATA_PATH, "r") as f:
        metadata = json.load(f)

    MODEL_PATH = metadata["model_path"]

    if not os.path.exists(MODEL_PATH):
        return {
        "error": "Model file not found"
    }

    model = joblib.load(MODEL_PATH)
    input_df = pd.DataFrame([
    data.model_dump()
    ])

    prediction = model.predict(
    input_df
    )[0]

    explanation = explain_prediction(
    prediction,
    data.model_dump()
    )

    return {
    "prediction": float(prediction),
    "explanation": explanation
}