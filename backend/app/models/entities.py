from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    country: Mapped[str] = mapped_column(String(128))
    language: Mapped[str] = mapped_column(String(32), default="am")
    source_type: Mapped[str] = mapped_column(String(64), default="national")
    credibility_score: Mapped[float] = mapped_column(Float)
    collection_method: Mapped[str] = mapped_column(String(64), default="rss")
    url: Mapped[str] = mapped_column(String(1024))
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class News(Base):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(512))
    content: Mapped[str] = mapped_column(Text)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"))
    url: Mapped[str] = mapped_column(String(1024), unique=True)
    language: Mapped[str] = mapped_column(String(16), default="am")
    published_at: Mapped[datetime] = mapped_column(DateTime)
    collected_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    raw_location_text: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    source: Mapped[Source] = relationship()


class DangerEvent(Base):
    __tablename__ = "danger_events"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    danger_type: Mapped[str] = mapped_column(String(64))
    danger_level: Mapped[str] = mapped_column(String(32))
    confidence: Mapped[float] = mapped_column(Float)
    location_name: Mapped[str] = mapped_column(String(255))
    region: Mapped[str | None] = mapped_column(String(128), nullable=True)
    zone: Mapped[str | None] = mapped_column(String(128), nullable=True)
    woreda: Mapped[str | None] = mapped_column(String(128), nullable=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    location_confidence: Mapped[float] = mapped_column(Float, default=0.0)
    event_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    event_end_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    event_time_confidence: Mapped[str] = mapped_column(String(16), default="LOW")
    status: Mapped[str] = mapped_column(String(32), default="active")
    deaths: Mapped[int | None] = mapped_column(Integer, nullable=True)
    injuries: Mapped[int | None] = mapped_column(Integer, nullable=True)
    displaced: Mapped[int | None] = mapped_column(Integer, nullable=True)
    missing: Mapped[int | None] = mapped_column(Integer, nullable=True)
    damage: Mapped[str | None] = mapped_column(Text, nullable=True)
    trend: Mapped[str | None] = mapped_column(String(32), nullable=True)
    severity_score: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, default=datetime.utcnow, nullable=True)

    source_links: Mapped[list["EventSource"]] = relationship(back_populates="event")


class EventSource(Base):
    __tablename__ = "event_sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[str] = mapped_column(ForeignKey("danger_events.id"))
    news_id: Mapped[int] = mapped_column(ForeignKey("news.id"))
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"))
    source_credibility: Mapped[float] = mapped_column(Float)
    independent_report: Mapped[bool] = mapped_column(Boolean, default=True)
    published_at: Mapped[datetime] = mapped_column(DateTime)

    news: Mapped[News] = relationship()
    source: Mapped[Source] = relationship()
    event: Mapped["DangerEvent"] = relationship(back_populates="source_links")


class Region(Base):
    __tablename__ = "regions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    region_name: Mapped[str] = mapped_column(String(128), unique=True)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    boundary_data: Mapped[str | None] = mapped_column(Text, nullable=True)
    danger_type: Mapped[str] = mapped_column(String(64), default="none")
    danger_level: Mapped[str] = mapped_column(String(32), default="none")
    confidence: Mapped[float] = mapped_column(Float, default=0.0)


class UserRecord(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(128), primary_key=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    notifications_enabled: Mapped[bool] = mapped_column(Boolean, default=True)


class UserLocation(Base):
    __tablename__ = "user_locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    region: Mapped[str | None] = mapped_column(String(128), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class NotificationLog(Base):
    __tablename__ = "notification_log"
    __table_args__ = (UniqueConstraint("user_id", "event_id", name="uq_user_event_notification"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(String(128))
    event_id: Mapped[str] = mapped_column(String(64))
    notification_sent_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class RegionalSnapshot(Base):
    __tablename__ = "regional_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    region_name: Mapped[str] = mapped_column(String(128))
    score: Mapped[float] = mapped_column(Float)
    level: Mapped[str] = mapped_column(String(32))
    captured_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
