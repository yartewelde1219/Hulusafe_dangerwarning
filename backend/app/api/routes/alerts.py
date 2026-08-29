from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.events import load_events, serialize_event

router = APIRouter()


@router.get("/alerts/history")
def alert_history(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> dict:
    # Personalized history will use Firebase UID once Student 3 finishes auth integration.
    events = [serialize_event(event).model_dump(by_alias=True) for event in load_events(db)]
    return {"alerts": events, "authenticated": bool(authorization)}
