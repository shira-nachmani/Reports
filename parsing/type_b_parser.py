import re
from models.attendance_record import AttendanceRecord

def parse_type_b_line(cleaned_line: str) -> AttendanceRecord:
    date_match = re.search(r'\d{1,2}[./-]\d{1,2}[./-]\d{2,4}', cleaned_line)
    date_str = date_match.group() if date_match else ""

    days_list = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"]
    day_str = next((d for d in days_list if d in cleaned_line), "")

    hours = re.findall(r'\d{1,2}:\d{2}', cleaned_line)
    entry_time = sorted(hours)[0] if hours else ""
    exit_time = sorted(hours)[-1] if len(hours) >= 2 else ""

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