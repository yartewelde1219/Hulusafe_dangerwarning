import json
from pathlib import Path

GEO_PATH = Path(__file__).resolve().parents[2] / "geographic_data" / "locations" / "sample_locations.json"


def extract_location(text: str) -> dict:
    if not text:
        return {
            "name": None,
            "region": None,
            "latitude": None,
            "longitude": None,
            "location_confidence": 0.0,
        }

    try:
        locations = json.loads(GEO_PATH.read_text(encoding="utf-8"))
    except Exception:
        locations = []

    text_lower = text.lower()
    for place in locations:
        name_en = place.get("name")
        name_am = place.get("name_am")

        matched = False
        if name_am and name_am in text:
            matched = True
        elif name_en and name_en.lower() in text_lower:
            matched = True

        if matched:
            return {
                "name": place["name"],
                "region": place["region"],
                "latitude": place["latitude"],
                "longitude": place["longitude"],
                "location_confidence": 0.95 if name_am and name_am in text else 0.90,
            }

    return {
        "name": None,
        "region": None,
        "latitude": None,
        "longitude": None,
        "location_confidence": 0.0,
    }

