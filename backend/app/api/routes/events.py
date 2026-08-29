from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.entities import Region
from app.services.events import load_events, serialize_event

router = APIRouter()


@router.get("/regions/danger")
def regional_danger(db: Session = Depends(get_db)) -> dict:
    regions = list(db.scalars(select(Region)))
    return {
        "regions": [
            {
                "region_name": region.region_name,
                "danger_type": region.danger_type,
                "level": region.danger_level,
                "confidence": region.confidence,
                "latitude": region.latitude,
                "longitude": region.longitude,
            }
            for region in regions
        ]
    }


@router.get("/events/{event_id}")
def get_event(event_id: str, db: Session = Depends(get_db)) -> dict:
    events = {event.id: event for event in load_events(db)}
    event = events.get(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return serialize_event(event).model_dump(by_alias=True)
