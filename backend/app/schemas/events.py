from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LocationOut(BaseModel):
    name: str
    region: str | None = None
    zone: str | None = None
    woreda: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class SourceOut(BaseModel):
    name: str
    title: str | None = None
    url: str | None = None
    published_at: datetime | None = None
    credibility_score: float | None = None


class DangerEventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    event_id: str
    danger_type: str
    danger_level: str
    confidence: float
    location: LocationOut
    event_time: datetime | None = None
    published_at: datetime | None = None
    updated_at: datetime | None = None
    status: str
    deaths: int | None = None
    injuries: int | None = None
    displaced: int | None = None
    missing: int | None = None
    damage: str | None = None
    trend: str | None = None
    distance_km: float | None = None
    sources: list[SourceOut] = []
