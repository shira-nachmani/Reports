import pytesseract
from parsing.ocr import extract_text_from_pdf
from parsing.classifier import classify_report
from parsing.parser_factory import ParserFactory
from transformation.service import transform_records
from generation.excel_generator import generate_excel

# הגדרת נתיב Tesseract במחשב
pytesseract.pytesseract.tesseract_cmd = r'C:\tessdata\tesseract.exe'


def main():
    # הגדרת נתיבים לקובץ ה-PDF ולתיקיית Poppler
    pdf_path = "n_r_10_n.pdf"
    poppler_path = r'C:\Users\User\Desktop\תוכנות\poppler-26.09.0\Library\bin'

    print("--- מתחיל תהליך חילוץ OCR מהקובץ ---")
    try:
        # שלב 1: OCR
        raw_text = extract_text_from_pdf(pdf_path, poppler_path)
    except Exception as e:
        print(f"שגיאה בשלב ה-OCR: {e}")
        return

    # שלב 2: Classifier (זיהוי סוג הדו"ח)
    report_type = classify_report(raw_text)
    print(f'--- זוהה סוג המסמך בהצלחה: {report_type} ---')

    # שלב 3: Parser באמצעות Factory
    parser_func = ParserFactory.get_parser(report_type)
    lines = raw_text.strip().split('\n')

    records = []
    for line in lines:
        cleaned_line = line.strip()
        if not cleaned_line:
            continue
        if any(char.isdigit() for char in cleaned_line):
            record = parser_func(cleaned_line)
            if record.date:
                records.append(record)

    if not records:
        print("--- אזהרה: לא נמצאו שורות תואמות לחילוץ בקובץ זה ---")
        return

    # שלב 4: Transformer (טרנספורמציה ועיבוד הנתונים)
    transformed_records = transform_records(records)

    # שלב 5: Generator (יצירת קובץ אקסל סופי)
    generate_excel(transformed_records)
    print("--- הצינור הושלם בהצלחה: הנתונים נשמרו לקובץ attendance_report.xlsx! ---")


if __name__ == "__main__":
    main()