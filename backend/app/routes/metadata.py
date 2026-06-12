from fastapi import APIRouter
import json
import os

router = APIRouter()

@router.get("/metadata")
def get_metadata():

    metadata_file = (
        "ml_engine/models/model_metadata.json"
    )

    if not os.path.exists(metadata_file):
        return {
            "error": "No metadata found"
        }

    with open(metadata_file, "r") as f:
        metadata = json.load(f)

    return metadata