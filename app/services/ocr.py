from paddleocr import PaddleOCR

# Initialize OCR model
ocr_model = PaddleOCR(
    use_angle_cls=True,
    lang='en',
    use_gpu=False
)


def extract_text(image_path):

    results = ocr_model.ocr(image_path, cls=True)

    extracted_data = []

    for result in results:

        for line in result:

            bbox = line[0]

            text = line[1][0]

            confidence = line[1][1]

            extracted_data.append({
                "text": text,
                "confidence": float(confidence),
                "bbox": bbox
            })

    return extracted_data