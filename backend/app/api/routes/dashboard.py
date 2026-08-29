from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database.session import get_db
from app.schemas.events import DangerEventOut
from app.services.events import approximate_area, nearby_events, serialize_event

router = APIRouter()


@router.get("/dashboard")
def dashboard(
    lat: float = Query(...),
    lon: float = Query(...),
    db: Session = Depends(get_db),
) -> dict:
    settings = get_settings()
    nearby = nearby_events(db, lat, lon, settings.default_alert_radius_km)
    serialized = [serialize_event(event, distance).model_dump(by_alias=True) for event, distance in nearby]
    highest = serialized[0] if serialized else None
    return {
        "area_name": approximate_area(db, lat, lon),
        "highest_nearby_danger": highest,
        "nearby_dangers": serialized,
        "recent_alerts": serialized[:5],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
