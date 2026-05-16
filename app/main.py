from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import cv2

from services.easy_ocr import extract_text_easyocr
from services.gemini_extract import extract_bill_with_gemini
from services.preprocess import preprocess_image

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

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)


@app.get("/")
def home():
    return {"message": "Bill Extraction Backend Running"}


@app.post("/extract-bill-llm")
async def extract_bill_llm(file: UploadFile = File(...)):
    upload_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    processed_image = preprocess_image(upload_path)

    processed_path = os.path.join(
        PROCESSED_FOLDER,
        f"processed_{file.filename}",
    )

    cv2.imwrite(processed_path, processed_image)

    ocr_data = extract_text_easyocr(processed_path)

    structured_data = extract_bill_with_gemini(ocr_data)

    return {
        "status": "success",
        "ocr_data": ocr_data,
        "structured_data": structured_data,
    }
