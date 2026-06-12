import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def explain_prediction(
    prediction,
    input_data
):

    prompt = f"""
    You are an AI Data Scientist.

    Prediction:
    {prediction}

    Input Features:
    {input_data}

    Explain in simple language:

    1. Why this prediction was made.
    2. Which features likely influenced it.
    3. Keep under 60 words.
    """

    try:

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception:

        return (
            "Prediction explanation "
            "temporarily unavailable."
        )