from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
import joblib
import os

router = APIRouter()

MODEL_PATH = "ml_engine/models/Linear Regression.pkl"


class PredictionInput(BaseModel):
    age: int
    experience: int


@router.post("/predict")
async def predict(data: PredictionInput):

    if not os.path.exists(MODEL_PATH):
        return {
            "error": "No trained model found"
        }

    model = joblib.load(MODEL_PATH)

    df = pd.DataFrame([data.dict()])

    prediction = model.predict(df)

    return {
        "prediction": float(prediction[0])
    }