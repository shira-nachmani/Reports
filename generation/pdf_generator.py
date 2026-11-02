import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def generate_pdf(df, output_path="attendance_report.pdf"):
    """
    מייצר קובץ PDF מעוצב מתוך נתוני ה־DataFrame של הדוח.
    """
    # הגדרת מסמך PDF בגודל A4
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=30, leftMargin=30,
        topMargin=30, bottomMargin=30
    )

    elements = []
    styles = getSampleStyleSheet()

    # כותרת ראשית לדוח
    title_style = ParagraphStyle(
        name='ReportTitle',
        parent=styles['Heading1'],
        fontSize=16,
        alignment=1,  # מרכוז
        spaceAfter=15
    )
    elements.append(Paragraph("דוח נוכחות מרוכז - Type B", title_style))
    elements.append(Spacer(1, 10))

    # המרת נתוני ה־DataFrame למבנה טבלה עבור ReportLab
    # המרת העמודות והשורות למחרוזות
    table_data = [list(df.columns)]
    for _, row in df.iterrows():
        table_data.append([str(val) if pd_notna(val) else "" for val in row.values])

    # יצירת הטבלה והגדרת עיצוב (צבעים, קווים ויישור)
    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2C3E50")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F8F9F9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#BDC3C7")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F4F4")])
    ]))

    elements.append(table)

    # בניית והפקת הקובץ
    doc.build(elements)
    print(f"קובץ ה־PDF נוצר בהצלחה בנתיב: {output_path}")


def pd_notna(val):
    import pandas as pd
    return pd.notna(val)