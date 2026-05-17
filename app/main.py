from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from services.gemini_extract import extract_bill_with_gemini
from models.ocr_request import OCRRequest

app = FastAPI()

_allowed_origins = [
    o.strip() for o in os.getenv("ALLOWED_ORIGINS", "*").split(",") if o.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials="*" not in _allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Bill Extraction Backend Running"}


@app.post("/extract-structured-data")
async def extract_structured_data(request: OCRRequest):
    try:
        ocr_text = request.ocr_text

        print("\n========== OCR TEXT RECEIVED ==========\n")
        print(ocr_text)
        print("\n=======================================\n")

        if not ocr_text.strip():
            return {
                "status": "error",
                "message": "OCR text is empty",
            }

        structured_data = extract_bill_with_gemini(ocr_text)

        return {
            "status": "success",
            "structured_data": structured_data,
        }

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return {
            "status": "error",
            "message": str(e),
        }
