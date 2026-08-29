from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.entities import DangerEvent, EventSource, NotificationLog, Region
from app.schemas.events import DangerEventOut, LocationOut, SourceOut
from app.services.geo import haversine_km
from app.services.time_policy import is_within_notification_window


def serialize_event(event: DangerEvent, distance_km: float | None = None) -> DangerEventOut:
    published_at = None
    sources: list[SourceOut] = []
    for link in getattr(event, "source_links", []):
        published_at = published_at or link.published_at
        sources.append(
            SourceOut(
                name=link.source.name,
                title=link.news.title,
                url=link.news.url,
                published_at=link.published_at,
                credibility_score=link.source_credibility,
            )
        )
    return DangerEventOut(
        event_id=event.id,
        danger_type=event.danger_type,
        danger_level=event.danger_level,
        confidence=event.confidence,
        location=LocationOut(
            name=event.location_name,
            region=event.region,
            zone=event.zone,
            woreda=event.woreda,
            latitude=event.latitude,
            longitude=event.longitude,
        ),
        event_time=event.event_time,
        published_at=published_at,
        updated_at=event.updated_at,
        status=event.status,
        deaths=event.deaths,
        injuries=event.injuries,
        displaced=event.displaced,
        missing=event.missing,
        damage=event.damage,
        trend=event.trend,
        distance_km=distance_km,
        sources=sources,
    )


def load_events(db: Session) -> list[DangerEvent]:
    return list(
        db.scalars(
            select(DangerEvent).options(
                selectinload(DangerEvent.source_links).selectinload(EventSource.news),
                selectinload(DangerEvent.source_links).selectinload(EventSource.source),
            )
        )
    )


def with_distance(event: DangerEvent, lat: float, lon: float) -> tuple[DangerEvent, float | None]:
    if event.latitude is None or event.longitude is None:
        return event, None
    return event, haversine_km(lat, lon, event.latitude, event.longitude)


def nearby_events(db: Session, lat: float, lon: float, radius_km: float) -> list[tuple[DangerEvent, float]]:
    results = []
    for event in load_events(db):
        _, distance = with_distance(event, lat, lon)
        if distance is not None and distance <= radius_km:
            results.append((event, distance))
    return sorted(results, key=lambda item: item[1])


def notification_candidates(
    db: Session,
    lat: float,
    lon: float,
    radius_km: float,
    now: datetime,
    max_age_days: int,
) -> list[tuple[DangerEvent, float]]:
    candidates = []
    for event, distance in nearby_events(db, lat, lon, radius_km):
        published_at = event.source_links[0].published_at if event.source_links else event.updated_at
        if event.status != "active":
            continue
        if not is_within_notification_window(now, event.event_time, published_at, max_age_days):
            continue
        candidates.append((event, distance))
    return candidates


def already_notified(db: Session, user_id: str, event_id: str) -> bool:
    row = db.scalar(
        select(NotificationLog).where(
            NotificationLog.user_id == user_id,
            NotificationLog.event_id == event_id,
        )
    )
    return row is not None


def approximate_area(db: Session, lat: float, lon: float) -> str:
    regions = list(db.scalars(select(Region)))
    if not regions:
        return "Ethiopia"
    nearest = min(regions, key=lambda region: haversine_km(lat, lon, region.latitude, region.longitude))
    return nearest.region_name
