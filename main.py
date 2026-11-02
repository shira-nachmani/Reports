import os
import pandas as pd
from parsing.ocr import extract_text_from_pdf
from parsing.classifier import classify_report
from parsing.parser_factory import ParserFactory
from generation.pdf_generator import generate_pdf


def main():
    print("--- מתחיל תהליך חילוץ OCR מהקובץ ---")

    # הגדרת נתיב לקובץ הקלט
    input_pdf = "a_r_25_NEW.pdf"

    if not os.path.exists(input_pdf):
        print(f"שגיאה: קובץ הקלט {input_pdf} לא נמצא בתיקייה.")
        return

    # שלב 1: חילוץ טקסט בעזרת OCR מה-PDF
    raw_text = extract_text_from_pdf(input_pdf)

    # שלב 2: זיהוי אוטומטי של סוג המסמך (Type A או Type B)
    doc_type = classify_report(raw_text)
    print(f"--- זוהה סוג המסמך בהצלחה: {doc_type} ---")

    # שלב 3: שליפת הפארסר המתאים דרך ה־Factory
    parser_func = ParserFactory.get_parser(doc_type)

    # שלב 4: פיצול הטקסט לשורות והפעלת הניתוח על כל שורה
    lines = raw_text.splitlines()
    records = []
    for line in lines:
        if line.strip():
            record = parser_func(line)
            records.append(record)

    # שלב 5: המרת הרשומות ל־DataFrame של Pandas
    df_final = pd.DataFrame([vars(r) for r in records])

    print("--- שלב יצירת קובץ ה־PDF הסופי ---")

    # שלב 6: הפקת קובץ ה־PDF המעוצב
    generate_pdf(df_final, output_path="attendance_report.pdf")

    print("--- התהליך הושלם בהצלחה! קובץ ה־PDF נוצר ונשמר ---")


if __name__ == "__main__":
    main()