import google.generativeai as genai
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(
    api_key=API_KEY
)

print("Testing Gemini Connection...\n")

try:

    print("Available Models:\n")

    for model in genai.list_models():
        print(model.name)

    print("\nTesting Prompt...\n")

    model = genai.GenerativeModel(
        "gemini-flash-latest"
    )

    response = model.generate_content(
        "Say hello in one sentence."
    )

    print("SUCCESS!")
    print(response.text)

except Exception as e:

    print("\nERROR:")
    print(e)