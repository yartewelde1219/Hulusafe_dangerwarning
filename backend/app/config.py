from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "HuluSafe API"
    database_url: str = "sqlite:///./hulusafe.db"
    max_alert_event_age_days: int = 14
    default_alert_radius_km: float = 100.0
    alert_severity_threshold: float = 0.5
    alert_confidence_threshold: float = 0.6
    location_confidence_threshold: float = 0.5
    news_poll_minutes: int = 30
    firebase_project_id: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()
