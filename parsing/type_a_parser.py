import re
from models.attendance_record import AttendanceRecord

def parse_type_a_line(cleaned_line: str) -> AttendanceRecord:
    date_match = re.search(r'\d{1,2}[./-]\d{1,2}[./-]\d{2,4}', cleaned_line)
    date_str = date_match.group() if date_match else ""

    hours = re.findall(r'\d{1,2}:\d{2}', cleaned_line)
    entry_time = sorted(hours)[0] if hours else ""
    exit_time = sorted(hours)[-1] if len(hours) >= 2 else ""

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