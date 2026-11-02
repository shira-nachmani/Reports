from dataclasses import dataclass

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