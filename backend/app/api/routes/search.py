from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database.session import get_db
from app.services.events import nearby_events, serialize_event

router = APIRouter()


@router.get("/search")
def search(
    lat: float = Query(...),
    lon: float = Query(...),
    q: str | None = None,
    danger_type: str | None = None,
    radius_km: float | None = None,
    db: Session = Depends(get_db),
) -> dict:
    settings = get_settings()
    radius = radius_km or settings.default_alert_radius_km
    query = (q or "").strip().lower()
    results = []
    for event, distance in nearby_events(db, lat, lon, radius):
        blob = " ".join(
            filter(
                None,
                [event.location_name, event.region, event.zone, event.woreda, event.danger_type],
            )
        ).lower()
        if query and query not in blob:
            continue
        if danger_type and event.danger_type.lower() != danger_type.lower():
            continue
        results.append(serialize_event(event, distance).model_dump())
    return {"query": q, "events": results}
