from fastapi import APIRouter, UploadFile, File
from app.services.s3_service import upload_file_to_s3

router = APIRouter()

@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    file_name = upload_file_to_s3(file)

    return {
        "message": "File uploaded successfully",
        "file_name": file_name
    }