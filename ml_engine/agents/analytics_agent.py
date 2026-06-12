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
    raw_insights,
    cleaned_insights
):

    prompt = f"""
    You are a Senior Data Analyst.

    Original Dataset Statistics:

    {raw_insights}

    Cleaned Dataset Statistics:

    {cleaned_insights}

    Analyze:

    1. Data quality before cleaning
    2. Cleaning improvements made
    3. Important patterns
    4. Risks
    5. Recommendations

    Maximum 150 words.
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