import cv2
import numpy as np


def preprocess_image(image_path):

    # Read image
    image = cv2.imread(image_path)

    # Check if image loaded properly
    if image is None:
        raise ValueError("Image not found or unable to read image")

    # =========================================
    # 1. Resize Image
    # =========================================

    height, width = image.shape[:2]

    # Resize only if image is too large
    if width > 1200:
        scale = 1200 / width
        new_width = int(width * scale)
        new_height = int(height * scale)

        image = cv2.resize(
            image,
            (new_width, new_height),
            interpolation=cv2.INTER_AREA
        )

    # =========================================
    # 2. Convert to Grayscale
    # =========================================

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # =========================================
    # 3. Denoising
    # =========================================

    denoised = cv2.fastNlMeansDenoising(
        gray,
        None,
        h=10
    )

    # =========================================
    # 4. Thresholding (Binarization)
    # =========================================

    threshold = cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    # =========================================
    # 5. Deskewing
    # =========================================

    coords = np.column_stack(np.where(threshold > 0))

    angle = cv2.minAreaRect(coords)[-1]

    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = threshold.shape[:2]

    center = (w // 2, h // 2)

    rotation_matrix = cv2.getRotationMatrix2D(
        center,
        angle,
        1.0
    )

    deskewed = cv2.warpAffine(
        threshold,
        rotation_matrix,
        (w, h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE
    )

    return deskewed