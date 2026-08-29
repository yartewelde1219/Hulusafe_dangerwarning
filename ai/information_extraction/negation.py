"""Negation and context checks for Amharic danger language.

Keyword presence is never sufficient for an alert.
"""

NEGATION_MARKERS = ("የለም", "አይደለም", "አልተከሰተም", "የለምም")
HISTORICAL_MARKERS = ("በፊት", "ባለፈው", "ከዓመታት በፊት", "ታሪክ")
HYPOTHETICAL_MARKERS = ("ቢሆን", "ሊከሰት ይችላል", "ከተከሰተ")


def analyze_context(sentence: str) -> dict:
    text = sentence or ""
    return {
        "negated": any(marker in text for marker in NEGATION_MARKERS),
        "historical": any(marker in text for marker in HISTORICAL_MARKERS),
        "hypothetical": any(marker in text for marker in HYPOTHETICAL_MARKERS),
        "active_candidate": True,
    }


def is_active_danger_language(sentence: str) -> bool:
    context = analyze_context(sentence)
    if context["negated"] or context["historical"] or context["hypothetical"]:
        return False
    return True
