from apscheduler.schedulers.background import BackgroundScheduler

from app.config import get_settings
from app.database.session import SessionLocal
from app.services.news_collector import collect_from_approved_sources

scheduler = BackgroundScheduler()


def _collect_job() -> None:
    db = SessionLocal()
    try:
        collect_from_approved_sources(db)
    finally:
        db.close()


def start_scheduler() -> None:
    settings = get_settings()
    if not scheduler.running:
        scheduler.add_job(_collect_job, "interval", minutes=settings.news_poll_minutes, id="news-collect")
        scheduler.start()
