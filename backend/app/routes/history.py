from fastapi import APIRouter
import json
import os

router = APIRouter()

@router.get("/history")
def get_history():

    history_file = "ml_engine/logs/training_history.json"

    if not os.path.exists(history_file):
        return []

    with open(history_file, "r") as f:
        history = json.load(f)

    return history