from parsing.classifier import classify_report

def test_classify_report_type_a():
    text = "דוח נוכחות הכולל 150% שעות נוספות"
    assert classify_report(text) == "Type A"

def test_classify_report_type_b():
    text = "דוח נוכחות חודשי רגיל"
    assert classify_report(text) == "Type B"

def test_classify_report_unknown():
    text = "טקסט כללי כלשהו שאינו דוח מוכר"
    result = classify_report(text)
    # ודאי שהתוצאה מטופלת נכון לפי הלוגיקה שבקוד שלך
    assert result is not None