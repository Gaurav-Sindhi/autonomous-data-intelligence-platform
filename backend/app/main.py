from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.app.routes import upload
from backend.app.routes import predict
from backend.app.routes import history
from backend.app.routes import metadata



app = FastAPI()

app.include_router(upload.router)
app.include_router(predict.router)
app.include_router(
    history.router
)
app.include_router(
    metadata.router
)
# Serve chart images
app.mount(
    "/reports",
    StaticFiles(directory="uploads/reports"),
    name="reports"
)