from pdf2image import convert_from_path
import pytesseract
import os


def extract_text_from_pdf(pdf_path: str, poppler_path: str = None) -> str:
    # הגדרת נתיב ברירת מחדל ל-Poppler לפי התיקייה במחשב שלך
    if not poppler_path:
        poppler_path = r'C:\Users\User\Desktop\תוכנות\poppler-26.09.0\Library\bin'

    # הגדרת נתיב Tesseract (ודאי שהנתיב מדויק אצלך)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Tesseract\tesseract.exe'

    # המרת עמודי ה־PDF לתמונות (מחזיר רשימת אובייקטי תמונה בזיכרון)
    images = convert_from_path(pdf_path, poppler_path=poppler_path)

    if not images:
        return ""

    custom_config = r'--oem 3 --psm 6'

    # שליחת אובייקט התמונה הראשון ישירות ל־OCR ללא שמירת קובץ זמני בתיקייה
    raw_text = pytesseract.image_to_string(images[0], lang='heb', config=custom_config)

    return raw_text