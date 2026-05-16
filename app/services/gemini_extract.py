import google.generativeai as genai
import json

genai.configure(
    api_key="AIzaSyDhTxDXHjTryG78frt309J223lX2GIBhWY"
)

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
            "error": str(e)
        }