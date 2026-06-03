from fastapi import APIRouter
import json

router = APIRouter()

@router.get("/history")
async def get_history():

    try:
        with open(
            "ml_engine/logs/training_history.json",
            "r"
        ) as f:

            history = json.load(f)

        return history

    except:
        return []