from datetime import datetime, timedelta
import re

RELATIVE_DAYS = {
    "ዛሬ": 0,
    "ትናንት": 1,
    "yesterday": 1,
    "today": 0,
}


def extract_event_time(text: str, published_at: datetime | None) -> dict:
    if not published_at:
        return {"event_time": None, "event_time_confidence": "LOW"}

    lowered = text.lower()
    for marker, days_ago in RELATIVE_DAYS.items():
        if marker in text or marker in lowered:
            return {
                "event_time": published_at - timedelta(days=days_ago),
                "event_time_confidence": "MEDIUM",
            }

    match = re.search(r"(20\d{2})[-/.](\d{1,2})[-/.](\d{1,2})", text)
    if match:
        year, month, day = map(int, match.groups())
        try:
            return {
                "event_time": datetime(year, month, day),
                "event_time_confidence": "HIGH",
            }
        except ValueError:
            pass

    return {"event_time": None, "event_time_confidence": "LOW"}
