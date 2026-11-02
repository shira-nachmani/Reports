from parsing.type_b_parser import parse_type_b_line

def test_parse_type_b_line():
    line = "12/01/2026 ראשון 08:00 17:00 8.00"
    record = parse_type_b_line(line)
    assert record.date == "12/01/2026"
    assert record.day_of_week == "ראשון"
    assert record.entry_time == "08:00"
    assert record.exit_time == "17:00"
    assert record.total_hours == "8.00"