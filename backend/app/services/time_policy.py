from datetime import datetime, timedelta, timezone


def event_occurrence_time(event_time: datetime | None, published_at: datetime | None) -> datetime | None:
    return event_time or published_at


def event_age(now: datetime, occurrence: datetime | None) -> timedelta | None:
    if occurrence is None:
        return None
    if occurrence.tzinfo is None:
        occurrence = occurrence.replace(tzinfo=timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    return now - occurrence


def is_within_notification_window(
    now: datetime,
    event_time: datetime | None,
    published_at: datetime | None,
    max_age_days: int,
    unknown_event_time_policy: str = "use_publication_conservatively",
) -> bool:
    """Notifications are prohibited when the relevant occurrence is older than max_age_days.

    If event_time is missing, publication time is used cautiously. Historical events stay
    in the database; this function only gates notifications.
    """
    occurrence = event_occurrence_time(event_time, published_at)
    if occurrence is None:
        return False
    age = event_age(now, occurrence)
    if age is None:
        return False
    if event_time is None and unknown_event_time_policy == "block":
        return False
    return age <= timedelta(days=max_age_days)
