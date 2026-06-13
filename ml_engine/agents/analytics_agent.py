import google as genai
from dotenv import load_dotenv
import os

# ==========================================
# Load Environment Variables
# ==========================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("WARNING: GEMINI_API_KEY not found.")

genai.configure(
    api_key=API_KEY
)

# ==========================================
# Gemini Model
# ==========================================

try:
    model = genai.GenerativeModel(
    "gemini-2.5-flash"
)
except Exception as e:
    print(f"Gemini Initialization Error: {e}")
    model = None


# ==========================================
# Analytics Agent
# ==========================================

def generate_analytics_insight(
    raw_insights,
    cleaned_insights
):
    """
    Generates a short executive analytics summary
    comparing raw dataset vs cleaned dataset.
    """

    if model is None:
        return (
            "Analytics Agent Error: "
            "Gemini model could not be initialized."
        )

    prompt = f"""
    You are a Senior Data Analyst.

    Analyze the dataset below.

    ===================================
    BEFORE CLEANING
    ===================================

    {raw_insights}

    ===================================
    AFTER CLEANING
    ===================================

    {cleaned_insights}

    ===================================
    TASK
    ===================================

    Provide:

    1. Dataset Quality
       - Missing values
       - Duplicates
       - Dataset size

    2. Cleaning Improvements
       - What was improved

    3. Important Patterns
       - Potential observations

    4. Risks
       - Data quality risks
       - Dataset size risks

    5. Recommendations
       - What user should do next

    Rules:

    - Maximum 150 words
    - Professional tone
    - Easy to understand
    - Use bullet points
    - Do not use markdown tables
    """

    try:

        response = model.generate_content(
            prompt
        )

        if not response:
            return (
                "Analytics Agent Error: "
                "Empty response received."
            )

        if not hasattr(response, "text"):
            return (
                "Analytics Agent Error: "
                "No text generated."
            )

        return response.text

    except Exception as e:

        print(
            f"ANALYTICS AGENT ERROR: {str(e)}"
        )

        return (
            f"Analytics Agent Error: "
            f"{str(e)}"
        )