from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
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

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return (
            f"Model explanation unavailable: "
            f"{str(e)}"
        )