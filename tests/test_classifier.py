from parsing.classifier import classify_report

def test_classify_report_type_a():
    text = "דוח נוכחות הכולל 150% שעות נוספות"
    assert classify_report(text) == "Type A"

def test_classify_report_type_b():
    text = "דוח נוכחות חודשי רגיל"
    assert classify_report(text) == "Type B"