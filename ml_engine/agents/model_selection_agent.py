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


def explain_model_choice(
    problem_info,
    training_results
):

    prompt = f"""
    You are a Senior Machine Learning Engineer.

    Problem Information:
    {problem_info}

    Training Results:
    {training_results}

    Explain:
    1. Why the selected model won.
    2. Why other models performed worse.
    3. Keep response under 80 words.
    4. Use simple language.
    """

    try:

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        return f"Model explanation unavailable: {str(e)}"