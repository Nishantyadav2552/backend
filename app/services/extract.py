import re


def extract_bill_details(ocr_data):

    extracted = {
        "vendor": None,
        "total": None,
        "cash": None,
        "change": None,
        "approval_code": None
    }

    # =========================================
    # Vendor Name
    # Usually first line
    # =========================================

    if len(ocr_data) > 0:
        extracted["vendor"] = ocr_data[0]["text"]

    # =========================================
    # Loop through OCR text
    # =========================================

    for item in ocr_data:

        text = item["text"].strip()

        lower_text = text.lower()

        # =====================================
        # Total
        # =====================================

        if lower_text == "total":

            extracted["total"] = find_nearest_amount(
                ocr_data,
                item
            )

        # =====================================
        # Cash
        # =====================================

        elif lower_text == "cash":

            extracted["cash"] = find_nearest_amount(
                ocr_data,
                item
            )

        # =====================================
        # Change
        # =====================================

        elif lower_text == "change":

            extracted["change"] = find_nearest_amount(
                ocr_data,
                item
            )

        # =====================================
        # Approval Code
        # =====================================

        elif "approval" in lower_text:

            extracted["approval_code"] = find_nearest_text(
                ocr_data,
                item
            )

    return extracted


# =================================================
# Find nearest numeric value
# =================================================

def find_nearest_amount(ocr_data, current_item):

    current_y = current_item["bbox"][0][1]

    best_match = None

    min_distance = float("inf")

    for item in ocr_data:

        text = item["text"]

        # Check if text is numeric
        if re.match(r'^\d+(\.\d+)?$', text):

            item_y = item["bbox"][0][1]

            distance = abs(item_y - current_y)

            if distance < min_distance:

                min_distance = distance

                best_match = text

    return best_match


# =================================================
# Find nearest text
# =================================================

def find_nearest_text(ocr_data, current_item):

    current_y = current_item["bbox"][0][1]

    best_match = None

    min_distance = float("inf")

    for item in ocr_data:

        text = item["text"]

        if text == current_item["text"]:
            continue

        item_y = item["bbox"][0][1]

        distance = abs(item_y - current_y)

        if distance < min_distance:

            min_distance = distance

            best_match = text

    return best_match