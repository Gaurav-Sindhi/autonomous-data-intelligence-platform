import google.generativeai as genai

from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(
    api_key=API_KEY
)

model = genai.GenerativeModel(
    "gemini-flash-latest"
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

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        return f"AI Insight Generation Failed: {str(e)}"