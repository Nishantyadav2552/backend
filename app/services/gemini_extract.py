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
    You are an expert receipt extraction AI.

    You will receive OCR text extracted from a receipt.

    Extract ONLY these fields:

    1. description
    2. total_amount
    3. date
    4. time

    Rules:
    - description should usually be the shop/store/vendor name
    - total_amount should be the FINAL amount paid
    - return ONLY valid JSON
    - no explanation
    - if field missing use empty string

    Return JSON in EXACT format:

    {{
    "description": "",
    "total_amount": "",
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