from dataclasses import dataclass

from app.services.time_policy import is_within_notification_window


@dataclass
class AlertDecision:
    eligible: bool
    reasons: list[str]


def evaluate_alert(
    *,
    status: str,
    now,
    event_time,
    published_at,
    max_age_days: int,
    distance_km: float | None,
    radius_km: float,
    severity_score: float,
    severity_threshold: float,
    confidence: float,
    confidence_threshold: float,
    location_confidence: float,
    location_threshold: float,
    already_notified: bool,
) -> AlertDecision:
    reasons: list[str] = []
    if status.lower() != "active":
        reasons.append("not_active")
    if not is_within_notification_window(now, event_time, published_at, max_age_days):
        reasons.append("older_than_notification_window")
    if distance_km is None:
        reasons.append("unknown_location")
    elif distance_km > radius_km:
        reasons.append("outside_radius")
    if severity_score < severity_threshold:
        reasons.append("below_severity_threshold")
    if confidence < confidence_threshold:
        reasons.append("below_confidence_threshold")
    if location_confidence < location_threshold:
        reasons.append("below_location_confidence")
    if already_notified:
        reasons.append("already_notified")
    return AlertDecision(eligible=not reasons, reasons=reasons)
