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
    insights,
    problem_info,
    training_results
):

    prompt = f"""
    You are an expert Data Scientist.

    Dataset Insights:
    {insights}

    Problem Info:
    {problem_info}

    Training Results:
    {training_results}

    Generate:

    1. Dataset Summary
    2. Important Patterns
    3. Model Evaluation
    4. Recommendations

    Keep the response concise.
    """

    try:

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        return f"AI Insight Generation Failed: {str(e)}"