from datetime import datetime, timedelta, timezone

from app.services.alert_eligibility import evaluate_alert
from app.services.geo import haversine_km
from app.services.time_policy import is_within_notification_window
from app.services.intelligence import (
    impact_score,
    severity_score,
    confidence_score,
    score_to_level,
    independent_agreement,
)


def test_haversine_addis_to_awash_under_250km():
    distance = haversine_km(9.03, 38.74, 8.9833, 40.1667)
    assert 100 < distance < 250


def test_same_point_is_zero():
    assert haversine_km(9.0, 38.7, 9.0, 38.7) == 0


def test_14_day_window_blocks_old_events():
    now = datetime(2026, 8, 27, tzinfo=timezone.utc)
    old = now - timedelta(days=15)
    assert is_within_notification_window(now, old, old, 14) is False


def test_14_day_window_allows_recent_events():
    now = datetime(2026, 8, 27, tzinfo=timezone.utc)
    recent = now - timedelta(days=2)
    assert is_within_notification_window(now, recent, recent, 14) is True


def test_alert_formula_requires_active_nearby_recent_event():
    now = datetime(2026, 8, 27, tzinfo=timezone.utc)
    recent = now - timedelta(days=1)
    decision = evaluate_alert(
        status="active",
        now=now,
        event_time=recent,
        published_at=recent,
        max_age_days=14,
        distance_km=78,
        radius_km=100,
        severity_score=0.8,
        severity_threshold=0.5,
        confidence=0.88,
        confidence_threshold=0.6,
        location_confidence=0.95,
        location_threshold=0.5,
        already_notified=False,
    )
    assert decision.eligible is True
    assert len(decision.reasons) == 0


def test_alert_formula_blocks_duplicate_and_unknown_location():
    now = datetime(2026, 8, 27, tzinfo=timezone.utc)
    recent = now - timedelta(days=1)
    unknown = evaluate_alert(
        status="active",
        now=now,
        event_time=recent,
        published_at=recent,
        max_age_days=14,
        distance_km=None,
        radius_km=100,
        severity_score=0.8,
        severity_threshold=0.5,
        confidence=0.88,
        confidence_threshold=0.6,
        location_confidence=0.95,
        location_threshold=0.5,
        already_notified=False,
    )
    assert unknown.eligible is False
    assert "unknown_location" in unknown.reasons

    dupe = evaluate_alert(
        status="active",
        now=now,
        event_time=recent,
        published_at=recent,
        max_age_days=14,
        distance_km=78,
        radius_km=100,
        severity_score=0.8,
        severity_threshold=0.5,
        confidence=0.88,
        confidence_threshold=0.6,
        location_confidence=0.95,
        location_threshold=0.5,
        already_notified=True,
    )
    assert dupe.eligible is False
    assert "already_notified" in dupe.reasons


def test_alert_formula_blocks_outside_radius():
    now = datetime(2026, 8, 27, tzinfo=timezone.utc)
    recent = now - timedelta(days=1)
    faraway = evaluate_alert(
        status="active",
        now=now,
        event_time=recent,
        published_at=recent,
        max_age_days=14,
        distance_km=125,
        radius_km=100,
        severity_score=0.8,
        severity_threshold=0.5,
        confidence=0.88,
        confidence_threshold=0.6,
        location_confidence=0.95,
        location_threshold=0.5,
        already_notified=False,
    )
    assert faraway.eligible is False
    assert "outside_radius" in faraway.reasons


def test_severity_and_impact_scoring():
    imp = impact_score(deaths=12, injuries=None, displaced=350, missing=None, damage="houses destroyed")
    assert 0.4 < imp <= 1.0

    sev = severity_score(
        impact=imp,
        nlp_evidence=0.85,
        source_credibility=0.90,
        agreement=0.90,
        recency=0.95,
        location_confidence=0.95,
    )
    assert 0.7 <= sev <= 1.0
    assert score_to_level(sev) in ("high", "critical")


def test_confidence_and_agreement():
    conf = confidence_score(
        nlp_confidence=0.85,
        source_confidence=0.90,
        agreement=0.80,
        location_confidence=0.95,
        recency_score=0.90,
    )
    assert 0.8 <= conf <= 1.0

    assert independent_agreement(3, 3) == 1.0
    assert independent_agreement(1, 3) == (1 / 3)
    assert independent_agreement(0, 0) == 0.0

