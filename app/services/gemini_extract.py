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


def extract_bill_with_gemini(ocr_data):

    raw_text = "\n".join(
        [item["text"] for item in ocr_data]
    )

    prompt = f"""
Extract receipt details into JSON.

Return ONLY valid JSON.

Format:
{{
  "vendor": "",
  "total": "",
  "cash": "",
  "change": "",
  "approval_code": ""
}}

OCR TEXT:
{raw_text}
"""

    if not _API_KEY:
        return {
            "error": (
                "GEMINI_API_KEY is not set. Add it to app/services/.env "
                "or set the environment variable, then restart the server."
            )
        }

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
        message = str(e)
        if "API_KEY_INVALID" in message or "API Key not found" in message:
            message = (
                "Invalid GEMINI_API_KEY. Create a new key at "
                "https://aistudio.google.com/apikey and update "
                "app/services/.env, then restart the server."
            )

        return {
            "error": message
        }