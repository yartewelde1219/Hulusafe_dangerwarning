from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database.base import Base
from app.database.session import SessionLocal, engine
from app.models import entities  # noqa: F401
from app.api.routes import alerts, dashboard, events, nearby, search
from app.jobs.scheduler import start_scheduler
from app.seed import seed_if_empty

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_if_empty(db)
    finally:
        db.close()
    start_scheduler()
    yield


app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(dashboard.router)
app.include_router(nearby.router)
app.include_router(search.router)
app.include_router(events.router)
app.include_router(alerts.router)


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "max_alert_event_age_days": settings.max_alert_event_age_days,
        "default_alert_radius_km": settings.default_alert_radius_km,
    }

