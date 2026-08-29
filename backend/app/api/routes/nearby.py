from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database.session import get_db
from app.services.events import nearby_events, serialize_event

router = APIRouter()


@router.get("/nearby-dangers")
def nearby_dangers(
    lat: float = Query(...),
    lon: float = Query(...),
    radius_km: float | None = None,
    db: Session = Depends(get_db),
) -> dict:
    settings = get_settings()
    radius = radius_km or settings.default_alert_radius_km
    events = [
        serialize_event(event, distance).model_dump(by_alias=True)
        for event, distance in nearby_events(db, lat, lon, radius)
    ]
    return {"radius_km": radius, "events": events, "as_of": datetime.now(timezone.utc).isoformat()}
