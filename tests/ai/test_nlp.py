from datetime import datetime
from ai.information_extraction.extractor import extract
from ai.information_extraction.location_extraction import extract_location
from ai.information_extraction.negation import analyze_context, is_active_danger_language
from ai.information_extraction.time_extraction import extract_event_time
from ai.models.naive_bayes import load_model, predict_proba
from ai.preprocessing.amharic import clean_text, normalize_unicode, preprocess, tokenize
from ai.training.train import MODEL_PATH


def test_preprocess_collapses_whitespace():
    assert preprocess("  ሰላም   አለ  ") == "ሰላም አለ"
    assert clean_text("አዲስ\u200bአበባ") == "አዲስ አበባ"
    assert normalize_unicode("ሐዋሳ") == "ሐዋሳ"


def test_tokenize_amharic_words():
    tokens = tokenize("በአዋሽ አካባቢ የጎርፍ አደጋ ተከስቷል")
    assert "በአዋሽ" in tokens
    assert "የጎርፍ" in tokens
    assert len(tokens) == 5



def test_negated_flood_is_not_active():
    assert is_active_danger_language("በአዋሽ የጎርፍ አደጋ የለም።") is False
    assert is_active_danger_language("በሰመራ ምንም ዓይነት አደጋ አልተከሰተም") is False


def test_historical_and_hypothetical_context():
    hist_ctx = analyze_context("ከሁለት ዓመት በፊት የጎርፍ አደጋ ነበር")
    assert hist_ctx["historical"] is True
    assert is_active_danger_language("ከሁለት ዓመት በፊት የጎርፍ አደጋ ነበር") is False

    hypo_ctx = analyze_context("ዝናቡ ከቀጠለ ጎርፍ ሊከሰት ይችላል")
    assert hypo_ctx["hypothetical"] is True
    assert is_active_danger_language("ዝናቡ ከቀጠለ ጎርፍ ሊከሰት ይችላል") is False


def test_location_extraction_amharic_and_english():
    loc_am = extract_location("በአዋሽ ወንዝ ሙላት ምክንያት")
    assert loc_am["name"] == "Awash"
    assert loc_am["region"] == "Afar"
    assert loc_am["latitude"] is not None

    loc_en = extract_location("Heavy rain near Bahir Dar yesterday")
    assert loc_en["name"] == "Bahir Dar"
    assert loc_en["region"] == "Amhara"

    loc_unknown = extract_location("በአንድ ያልታወቀ አካባቢ አደጋ ደረሰ")
    assert loc_unknown["name"] is None
    assert loc_unknown["location_confidence"] == 0.0


def test_casualty_and_damage_extraction():
    text = "በአዋሽ አካባቢ የጎርፍ አደጋ ተከስቶ 12 ሰዎች ሞተዋል፤ 350 ሰዎች ተፈናቅለዋል፤ መኖሪያ ቤቶች ወደሙ።"
    res = extract(text, published_at=datetime(2026, 8, 27, 14, 30), danger_type="flood")

    assert res["deaths"] == 12
    assert res["displaced"] == 350
    assert res["injuries"] is None  # Never fabricated when not in text
    assert res["missing"] is None   # Never fabricated when not in text
    assert res["damage"] is not None
    assert res["location"]["name"] == "Awash"
    assert res["status"] == "active"


def test_time_extraction_relative():
    pub = datetime(2026, 8, 27, 12, 0)
    res_today = extract_event_time("ዛሬ የተከሰተ አደጋ", pub)
    assert res_today["event_time"].day == 27
    assert res_today["event_time_confidence"] == "MEDIUM"

    res_yesterday = extract_event_time("ትናንት የተከሰተ አደጋ", pub)
    assert res_yesterday["event_time"].day == 26

    res_none = extract_event_time("አደጋ ተከስቷል", None)
    assert res_none["event_time"] is None
    assert res_none["event_time_confidence"] == "LOW"


def test_naive_bayes_model_inference():
    if MODEL_PATH.exists():
        model = load_model(MODEL_PATH)
        probas = predict_proba(model, "በአዋሽ አካባቢ ከባድ የጎርፍ አደጋ ተከስቷል")
        assert "flood" in probas
        assert probas["flood"] > 0.5

