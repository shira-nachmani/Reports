from typing import List
from models.attendance_record import AttendanceRecord

def transform_records(records: List[AttendanceRecord]) -> List[AttendanceRecord]:
    # כאן ניתן לבצע עיבוד או חישוב מחדש במידת הצורך
    transformed = []
    for r in records:
        # דוגמה לטרנספורמציה קלה (השארת השדות או עדכון)
        transformed.append(r)
    return transformed