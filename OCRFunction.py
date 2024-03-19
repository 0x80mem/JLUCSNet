from Config import ocr
import pytesseract


def image2string(image):
    pytesseract.pytesseract.tesseract_cmd = ocr
    text = pytesseract.image_to_string(image)
    return text
