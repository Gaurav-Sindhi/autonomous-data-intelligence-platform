from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_analytics_insight(
    raw_insights,
    cleaned_insights
):

    prompt = f"""
    Raw Dataset:
    {raw_insights}

    Cleaned Dataset:
    {cleaned_insights}

    Analyze dataset quality,
    risks, patterns and recommendations.
    """

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return (
            f"Analytics Agent Error: {str(e)}"
        )