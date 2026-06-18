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
You are a Senior Data Analyst.

Raw Dataset Statistics:
{raw_insights}

Cleaned Dataset Statistics:
{cleaned_insights}

Return ONLY in this format:

## Executive Summary
- Point 1
- Point 2
- Point 3

## Key Findings
- Point 1
- Point 2
- Point 3

## Risks
- Point 1
- Point 2

## Recommendations
- Point 1
- Point 2
- Point 3

Maximum 250 words.
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