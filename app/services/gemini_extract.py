import google.generativeai as genai
import json
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env", override=True)

_API_KEY = os.getenv("GEMINI_API_KEY")
if _API_KEY:
    genai.configure(api_key=_API_KEY)

model = genai.GenerativeModel(
    "gemini-3-flash-preview"
)


def extract_bill_with_gemini(ocr_text):

    prompt = f"""
    You are an AI receipt extraction system.

    Extract receipt information from OCR text.

    Return ONLY valid JSON.

    Extract ONLY these fields:

    1. vendor
    2. total
    3. date
    4. time

    Rules:
    - Do not explain anything
    - Return valid JSON only
    - If a field is missing use empty string
    - total must contain decimal value if present

    JSON FORMAT:

    {{
    "vendor": "",
    "total": "",
    "date": "",
    "time": ""
    }}

    OCR TEXT:
    {ocr_text}
    """

    try:

        response = model.generate_content(
            prompt
        )

        response_text = response.text.strip()

        response_text = response_text.replace(
            "```json",
            ""
        ).replace(
            "```",
            ""
        ).strip()

        return json.loads(response_text)

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }