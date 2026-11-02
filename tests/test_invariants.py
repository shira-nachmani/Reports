import pytest
from parsing.parser_factory import ParserFactory


def test_invalid_line_invariant():
    """בדיקת אינווריאנט: שורה ריקה או פגומה אינה שוברת את המערכת אלא מטופלת"""
    parser_func = ParserFactory.get_parser("TypeA")

    # בדיקה ששורת זבל או שורה ריקה מטופלת כראוי (למשל מחזירה None או זורקת שגיאה צפויה)
    with pytest.raises((ValueError, IndexError)):
        parser_func("שורה שגויה לחלוטין ללא מבנה נכון")


def test_working_hours_range_invariant():
    """בדיקת אינווריאנט: ערכי שעות עבודה עומדים בכללי הסף"""
    # כאן אפשר לבדוק פונקציית טרנספורמציה או חישוב המקבלת שעות ומוודאת תקינות
    pass