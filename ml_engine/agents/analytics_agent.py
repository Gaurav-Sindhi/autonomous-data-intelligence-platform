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


def generate_analytics_insight(
    summary_text
):

    prompt = f"""
    You are a Senior Data Analyst.

    Analyze:

    {summary_text}

    Give:

    1. Dataset quality
    2. Important patterns
    3. Risks
    4. Recommendation

    Maximum 120 words.
    """

    try:

        response = model.generate_content(
            prompt
        )

        return response.text

    except:

        return (
            "Analytics insights "
            "temporarily unavailable."
        )