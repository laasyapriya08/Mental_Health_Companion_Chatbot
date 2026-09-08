from google import genai
from config import GOOGLE_API_KEY, GEMINI_MODEL
from prompts import SYSTEM_PROMPT


class GeminiService:

    def __init__(self):
        self.client = genai.Client(
            api_key=GOOGLE_API_KEY
        )

    def generate_response(self, user_message):

        prompt = f"""
{SYSTEM_PROMPT}

User message:
{user_message}

Provide a supportive, empathetic, and safe response.
"""

        try:
            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )

            return response.text

        except Exception as e:
            print(f"Gemini Error: {e}")

            return (
                "I'm having trouble connecting right now. "
                "Please try again in a moment."
            )


gemini_service = GeminiService()