from pydantic import BaseModel


class OCRRequest(BaseModel):

    ocr_text: str