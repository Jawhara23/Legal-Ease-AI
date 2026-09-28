import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiDocumentGenerator:

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash"
        )

        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is missing in .env"
            )

        self.client = genai.Client(
            api_key=self.api_key
        )

    def generate_document(
        self,
        document_type,
        parties,
        terms,
        dates
    ):

        prompt = f"""
Create a professional legal document draft.

Document Type:
{document_type}

Parties:
{parties}

Key Terms:
{terms}

Effective Date:
{dates}

Instructions:
- Create a complete editable legal document.
- Use clear headings and numbered clauses.
- Include the parties and effective date.
- Include signature sections.
- Do not invent information that was not provided.
- Return only the document content.
"""

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )

        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return response.text.strip()