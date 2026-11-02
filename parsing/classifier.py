def classify_report(raw_text: str) -> str:
    if "מקומ" in raw_text or "150%" in raw_text or "הפסקה" in raw_text:
        return "Type A"
    return "Type B"