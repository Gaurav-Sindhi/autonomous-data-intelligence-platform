from fastapi import APIRouter, UploadFile, File
from backend.app.services.s3_service import upload_file_to_s3

from ml_engine.run_pipeline import run_pipeline

import os
import shutil

router = APIRouter()


@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):

    # Create uploads directory if it doesn't exist
    os.makedirs("uploads", exist_ok=True)

    # Save uploaded file temporarily
    temp_file_path = os.path.join("uploads", file.filename)

    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Upload to S3
    with open(temp_file_path, "rb") as f:
        file_name = upload_file_to_s3(f)

    # Run ML pipeline
    insights = run_pipeline(temp_file_path)

    return {
        "message": "File uploaded successfully",
        "file_name": file_name,
        "insights": insights
    }