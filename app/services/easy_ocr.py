import easyocr

reader = easyocr.Reader(['en'])


def extract_text_easyocr(image_path):

    results = reader.readtext(image_path)

    extracted_text = []

    for result in results:

        text = result[1]

        confidence = result[2]

        extracted_text.append({
            "text": text,
            "confidence": float(confidence)
        })

    return extracted_text