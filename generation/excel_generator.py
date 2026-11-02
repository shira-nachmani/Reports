import pandas as pd
from typing import List
from models.attendance_record import AttendanceRecord

def generate_excel(records: List[AttendanceRecord], output_path: str = "attendance_report.xlsx"):
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
    df.to_excel(output_path, index=False)