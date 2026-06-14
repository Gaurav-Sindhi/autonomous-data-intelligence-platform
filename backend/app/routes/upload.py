from fastapi import APIRouter, UploadFile, File, HTTPException
from ml_engine.run_pipeline import run_pipeline
import os
import shutil

router = APIRouter()


@router.post("/upload")
async def upload_dataset(
    file: UploadFile = File(...)
):

    try:

        os.makedirs(
            "uploads",
            exist_ok=True
        )

        temp_file_path = os.path.join(
            "uploads",
            file.filename
        )

        with open(
            temp_file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        insights = run_pipeline(
            temp_file_path
        )

        return {
            "message": "File uploaded successfully",
            "file_name": file.filename,
            "insights": insights
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )