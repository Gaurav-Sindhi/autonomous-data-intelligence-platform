"""
utils/api.py — ADI Platform
All backend HTTP calls in one place.
Never import requests directly in page files — use this module.
"""

import requests

BACKEND_URL = "http://127.0.0.1:8000"

_TIMEOUT = 300  # seconds — AutoML training can be slow


def upload_dataset(files: dict) -> requests.Response:
    """POST a CSV file to the backend for analysis and training."""
    return requests.post(
        f"{BACKEND_URL}/upload",
        files=files,
        timeout=_TIMEOUT,
    )


def predict(data: dict) -> requests.Response:
    """POST feature values and receive a prediction."""
    return requests.post(
        f"{BACKEND_URL}/predict",
        json=data,
        timeout=15,
    )


def get_history() -> requests.Response:
    """GET the list of past training runs."""
    return requests.get(
        f"{BACKEND_URL}/history",
        timeout=10,
    )


def get_metadata() -> requests.Response:
    """GET model metadata (feature columns, types, etc.)."""
    return requests.get(
        f"{BACKEND_URL}/metadata",
        timeout=10,
    )
