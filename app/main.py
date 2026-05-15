from fastapi import FastAPI, UploadFile, File
import os
import shutil
import cv2
import numpy as np
from paddleocr import PaddleOCR

app = FastAPI()

# Folder where uploaded images will be stored

from services.preprocess import preprocess_image
from services.ocr import extract_text
from services.extract import extract_bill_details

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"

# Create uploads folder if it doesn't exist

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "Bill Extraction Backend Running"
    }


@app.post("/upload-bill")
async def upload_bill(file: UploadFile = File(...)):

    # File path where image will be saved
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Save uploaded image
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "status": "success",
        "filename": file.filename,
        "saved_path": file_path
    }

@app.post("/preprocess-bill")
async def preprocess_bill(file: UploadFile = File(...)):

    # Save uploaded image
    upload_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Preprocess image
    processed_image = preprocess_image(upload_path)

    # Save processed image
    processed_path = os.path.join(
        PROCESSED_FOLDER,
        f"processed_{file.filename}"
    )

    cv2.imwrite(processed_path, processed_image)

    return {
        "status": "success",
        "processed_image_path": processed_path
    }

@app.post("/ocr-bill")
async def ocr_bill(file: UploadFile = File(...)):

    # =========================================
    # Save Uploaded Image
    # =========================================

    upload_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # =========================================
    # Preprocess Image
    # =========================================

    processed_image = preprocess_image(upload_path)

    processed_path = os.path.join(
        PROCESSED_FOLDER,
        f"processed_{file.filename}"
    )

    cv2.imwrite(processed_path, processed_image)

    # =========================================
    # OCR Extraction
    # =========================================

    extracted_text = extract_text(processed_path)

    return {
        "status": "success",
        "ocr_data": extracted_text
    }

@app.post("/extract-bill")
async def extract_bill(
    file: UploadFile = File(...)
):

    # =====================================
    # Save Uploaded Image
    # =====================================

    upload_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(upload_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    # =====================================
    # Preprocess Image
    # =====================================

    processed_image = preprocess_image(
        upload_path
    )

    processed_path = os.path.join(
        PROCESSED_FOLDER,
        f"processed_{file.filename}"
    )

    cv2.imwrite(
        processed_path,
        processed_image
    )

    # =====================================
    # OCR Extraction
    # =====================================

    ocr_data = extract_text(
        processed_path
    )

    # =====================================
    # Structured Data Extraction
    # =====================================

    structured_data = extract_bill_details(
        ocr_data
    )

    # =====================================
    # Final Response
    # =====================================

    return {

        "status": "success",

        "structured_data": structured_data
    }