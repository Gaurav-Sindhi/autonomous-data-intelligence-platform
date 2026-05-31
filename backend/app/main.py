from fastapi import FastAPI
from backend.app.routes import upload
from backend.app.routes import predict

app = FastAPI()

app.include_router(predict.router)
app.include_router(upload.router)

@app.get("/")
def home():
    return {"message": "API Running 🚀"}