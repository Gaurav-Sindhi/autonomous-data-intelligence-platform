from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_ai_insights(
    raw_insights,
    cleaned_insights,
    problem_info,
    training_results
):

    prompt = f"""
    Original Dataset Statistics:

    {raw_insights}

    Cleaned Dataset Statistics:

    {cleaned_insights}

    Problem Information:

    {problem_info}

    Training Results:

    {training_results}

    Generate:

    1. Dataset Summary
    2. Data Cleaning Impact
    3. Important Patterns
    4. Model Evaluation
    5. Recommendations
    """

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return (
            f"AI Insight Generation Failed: "
            f"{str(e)}"
        )