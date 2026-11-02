from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import os


def extract_text_from_pdf(pdf_path: str, poppler_path: str = None) -> str:
    # הגדרת נתיב ברירת מחדל ל-Poppler לפי התיקייה במחשב שלך
    if not poppler_path:
        poppler_path = r'C:\Users\User\Desktop\תוכנות\poppler-26.09.0\Library\bin'

    images = convert_from_path(pdf_path, poppler_path=poppler_path)
    temp_image_path = "temp_page.png"
    images[0].save(temp_image_path)

    custom_config = r'--oem 3 --psm 6'
    raw_text = pytesseract.image_to_string(Image.open(temp_image_path), lang='heb', config=custom_config)

    # ניקוי קובץ זמני
    if os.path.exists(temp_image_path):
        os.remove(temp_image_path)

    return raw_text