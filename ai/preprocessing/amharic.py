"""Amharic text preprocessing for HuluSafe.

Stopword removal must be validated: some grammatical words carry negation/context.
Never invent missing facts during later extraction stages.
"""

import re
import unicodedata


def normalize_unicode(text: str) -> str:
    return unicodedata.normalize("NFC", text or "")


def clean_text(text: str) -> str:
    text = normalize_unicode(text)
    text = text.replace("\u200b", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text: str) -> list[str]:
    cleaned = clean_text(text)
    return [token for token in re.split(r"\s+", cleaned) if token]


def preprocess(text: str) -> str:
    return " ".join(tokenize(text))
