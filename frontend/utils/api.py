import requests

BACKEND_URL = "http://127.0.0.1:8000"


def upload_dataset(files):
    return requests.post(
        f"{BACKEND_URL}/upload",
        files=files
    )


def predict(data):
    return requests.post(
        f"{BACKEND_URL}/predict",
        json=data
    )


def get_history():
    return requests.get(
        f"{BACKEND_URL}/history"
    )


def get_metadata():

    return requests.get(
        f"{BACKEND_URL}/metadata"
    )