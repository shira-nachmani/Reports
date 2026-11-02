<<<<<<< HEAD
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
=======
import re
import pandas as pd
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from dataclasses import dataclass


# הגדרת מודל נתונים מורחב התומך בשני סוגי הדו"חות
@dataclass
class AttendanceRecord:
    date: str
    day_of_week: str
    entry_time: str
    exit_time: str
    total_hours: str
    remarks: str
    report_type: str
    raw_line: str


# פונקציה לזיהוי סוג הדו"ח
def detect_report_type(raw_text: str) -> str:
    if "מקומ" in raw_text or "150%" in raw_text or "הפסקה" in raw_text:
        return "Type A"
    else:
        return "Type B"


# פונקציית פירסור עבור סוג B
def parse_type_b_line(cleaned_line: str) -> AttendanceRecord:
    # תמיכה גמישה בתאריכים (נקודה, מקף או קו נטוי)
    date_match = re.search(r'\d{1,2}[./-]\d{1,2}[./-]\d{2,4}', cleaned_line)
    date_str = date_match.group() if date_match else ""

    days_list = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"]
    day_str = ""
    for d in days_list:
        if d in cleaned_line:
            day_str = d
            break

    hours = re.findall(r'\d{1,2}:\d{2}', cleaned_line)
    entry_time = ""
    exit_time = ""

    if len(hours) >= 2:
        def time_to_minutes(t):
            parts = t.split(':')
            return int(parts[0]) * 60 + int(parts[1])

        sorted_hours = sorted(hours, key=time_to_minutes)
        entry_time = sorted_hours[0]
        exit_time = sorted_hours[-1]
    elif len(hours) == 1:
        entry_time = hours[0]

    hours_num_match = re.search(r'\b\d{1,2}\.\d{2}\b', cleaned_line)
    total_hours_str = hours_num_match.group() if hours_num_match else ""

    remarks_str = ""
    if "ערב" in cleaned_line:
        remarks_str += "ערב ראש השנה "
    if "ראש השנה" in cleaned_line:
        remarks_str += "ראש השנה "

    return AttendanceRecord(
        date=date_str,
        day_of_week=day_str,
        entry_time=entry_time,
        exit_time=exit_time,
        total_hours=total_hours_str,
        remarks=remarks_str.strip(),
        report_type="Type B",
        raw_line=cleaned_line
    )


# פונקציית פירסור עבור סוג A
def parse_type_a_line(cleaned_line: str) -> AttendanceRecord:
    date_match = re.search(r'\d{1,2}[./-]\d{1,2}[./-]\d{2,4}', cleaned_line)
    date_str = date_match.group() if date_match else ""

    hours = re.findall(r'\d{1,2}:\d{2}', cleaned_line)
    entry_time = ""
    exit_time = ""

    if len(hours) >= 2:
        def time_to_minutes(t):
            parts = t.split(':')
            return int(parts[0]) * 60 + int(parts[1])

        sorted_hours = sorted(hours, key=time_to_minutes)
        entry_time = sorted_hours[0]
        exit_time = sorted_hours[-1]
    elif len(hours) == 1:
        entry_time = hours[0]

    hours_num_match = re.search(r'\b\d{1,2}\.\d{2}\b', cleaned_line)
    total_hours_str = hours_num_match.group() if hours_num_match else ""

    return AttendanceRecord(
        date=date_str,
        day_of_week="",
        entry_time=entry_time,
        exit_time=exit_time,
        total_hours=total_hours_str,
        remarks="Type A Row",
        report_type="Type A",
        raw_line=cleaned_line
    )


# הגדרת נתיב Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\tessdata\tesseract.exe'

# המרת ה-PDF לתמונה ושמירה זמנית (ודאי ששם הקובץ מעודכן נכון)
pdf_path = "n_r_5_n.pdf"
images = convert_from_path(pdf_path, poppler_path=r'C:\Users\User\Desktop\תוכנות\poppler-26.09.0\Library\bin')
temp_image_path = "temp_page.png"
images[0].save(temp_image_path)

# חילוץ הטקסט באמצעות OCR עם הגדרה מותאמת לטבלאות
custom_config = r'--oem 3 --psm 6'
raw_text = pytesseract.image_to_string(Image.open(temp_image_path), lang='heb', config=custom_config)

# זיהוי סוג המסמך
report_type = detect_report_type(raw_text)
print(f'--- זוהה סוג המסמך בהצלחה: {report_type} ---')

lines = raw_text.strip().split('\n')
records = []

for line in lines:
    cleaned_line = line.strip()
    if not cleaned_line:
        continue

    if re.search(r'\d{1,2}[./-]\d{1,2}[./-]\d{2,4}', cleaned_line):
        if report_type == "Type A":
            record = parse_type_a_line(cleaned_line)
        else:
            record = parse_type_b_line(cleaned_line)
        records.append(record)

# בדיקה האם נמצאו רשומות לפני יצירת הטבלה
if not records:
    print("--- אזהרה: לא נמצאו שורות תואמות לחילוץ בקובץ זה. אנא בדוק את מבנה הקובץ או את פורמט התאריכים ---")
else:
    # הכנת הנתונים לטבלת אקסל סופית
    data_for_df = [
        {
            "תאריך": r.date,
            "יום בשבוע": r.day_of_week,
            "שעת כניסה": r.entry_time,
            "שעת יציאה": r.exit_time,
            "סהכ שעות": r.total_hours,
            "הערות": r.remarks,
            "סוג זיהוי": r.report_type,
            "שורה גולמית": r.raw_line
        } for r in records
    ]

    df = pd.DataFrame(data_for_df)
    df = df[["תאריך", "יום בשבוע", "שעת כניסה", "שעת יציאה", "סהכ שעות", "הערות", "סוג זיהוי", "שורה גולמית"]]

    output_excel = "attendance_report.xlsx"
    df.to_excel(output_excel, index=False)

    print("--- שלב 7 הושלם בהצלחה: הנתונים אוחדו ונשמרו לאקסל הסופי! ---")
>>>>>>> 18c546aa8178b4b63395c16551c74c3a86b18dbb
