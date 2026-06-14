from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
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

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return (
            f"Prediction explanation unavailable: "
            f"{str(e)}"
        )