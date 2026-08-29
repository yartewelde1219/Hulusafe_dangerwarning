"""Extract reported facts only. Missing values stay None / UNKNOWN. Never invent numbers."""

import re
from datetime import datetime
from ai.information_extraction.location_extraction import extract_location
from ai.information_extraction.negation import analyze_context
from ai.information_extraction.time_extraction import extract_event_time


def _extract_deaths(text: str) -> int | None:
    patterns = [
        r"(\d+)\s*(?:ሰው|ሰዎች)?\s*(?:ሞቱ|ተገደሉ|የሞቱ|ሕይወታቸው አለፈ|ህይወታቸው አለፈ|ሞተዋል)",
        r"የ\s*(\d+)\s*(?:ሰዎች|ሰው)?\s*(?:ሕይወት|ህይወት)\s*አለፈ",
        r"(\d+)\s*(?:deaths?|people died|killed|fatalities)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return int(match.group(1))
            except (ValueError, IndexError):
                pass
    return None


def _extract_injuries(text: str) -> int | None:
    patterns = [
        r"(\d+)\s*(?:ሰው|ሰዎች)?\s*(?:ቆሰሉ|የቆሰሉ|ተጎዱ|የተጎዱ|ቁስለኛ)",
        r"(\d+)\s*(?:injuries|injured|people injured|wounded)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return int(match.group(1))
            except (ValueError, IndexError):
                pass
    return None


def _extract_displaced(text: str) -> int | None:
    patterns = [
        r"(\d+)\s*(?:ሰው|ሰዎች|ዜጎች|አባወራዎች)?\s*(?:ተፈናቀሉ|የተፈናቀሉ|ተፈናቅለዋል)",
        r"(\d+)\s*(?:displaced|people displaced|evacuated)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return int(match.group(1))
            except (ValueError, IndexError):
                pass
    return None


def _extract_missing(text: str) -> int | None:
    patterns = [
        r"(\d+)\s*(?:ሰው|ሰዎች)?\s*(?:የጠፉ|ደብዛቸው የጠፋ|የጠፉበት|አልተገኙም)",
        r"(\d+)\s*(?:missing|people missing)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return int(match.group(1))
            except (ValueError, IndexError):
                pass
    return None


def _extract_damage(text: str) -> str | None:
    patterns = [
        r"(?:መኖሪያ\s*)?ቤቶች\s*(?:ወደሙ|ተቃጠሉ|ፈረሱ)",
        r"ንብረት\s*(?:ወደመ|ተቃጠለ|ጉዳት ደረሰ)",
        r"ድልድይ\s*(?:ተሰበረ|ፈረሰ|ተቋረጠ)",
        r"መሰረተ\s*ልማት\s*(?:ወደመ|ተጎዳ|ፈረሰ)",
        r"ከባድ\s*የንብረት\s*ጉዳት",
        r"የሰብል\s*ጉዳት",
        r"homes?\s*destroyed",
        r"property\s*damage",
        r"infrastructure\s*damage",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0).strip()
    return None


def extract(article_text: str, published_at: datetime | None = None, danger_type: str | None = None) -> dict:
    context = analyze_context(article_text)
    location = extract_location(article_text)
    timing = extract_event_time(article_text, published_at)
    status = "active"
    if context["negated"] or context["hypothetical"]:
        status = "not_applicable"
    elif context["historical"]:
        status = "historical"

    return {
        "danger_type": danger_type,
        "location": location,
        "event_time": timing["event_time"],
        "event_time_confidence": timing["event_time_confidence"],
        "deaths": _extract_deaths(article_text),
        "injuries": _extract_injuries(article_text),
        "displaced": _extract_displaced(article_text),
        "missing": _extract_missing(article_text),
        "damage": _extract_damage(article_text),
        "status": status,
        "negated": context["negated"],
        "historical": context["historical"],
        "hypothetical": context["hypothetical"],
    }

