from datetime import datetime, timezone
import time
import logging
import feedparser
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import News, Source

logger = logging.getLogger(__name__)


def _parse_published_time(entry) -> datetime:
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        return datetime.fromtimestamp(time.mktime(entry.published_parsed), tz=timezone.utc).replace(tzinfo=None)
    if hasattr(entry, "updated_parsed") and entry.updated_parsed:
        return datetime.fromtimestamp(time.mktime(entry.updated_parsed), tz=timezone.utc).replace(tzinfo=None)
    return datetime.utcnow()


def collect_from_approved_sources(db: Session) -> int:
    """Collect Amharic articles from approved news source registry.

    Uses official APIs, RSS, or other permitted feeds, extracts publication timestamps,
    skips duplicates, and safely commits new records.
    """
    sources = list(db.scalars(select(Source).where(Source.active.is_(True))))
    new_articles_count = 0

    for source in sources:
        logger.info("Polling Amharic source: %s (%s)", source.name, source.url)
        if source.collection_method != "rss" or not source.url.startswith(("http://", "https://")):
            continue

        try:
            feed = feedparser.parse(source.url)
            for entry in getattr(feed, "entries", []):
                url = getattr(entry, "link", None)
                title = getattr(entry, "title", None)
                if not url or not title:
                    continue

                # Check duplicate by URL
                existing = db.scalar(select(News).where(News.url == url))
                if existing:
                    continue

                content = ""
                if hasattr(entry, "summary"):
                    content = entry.summary
                elif hasattr(entry, "description"):
                    content = entry.description

                published_at = _parse_published_time(entry)

                article = News(
                    title=title.strip(),
                    content=content.strip(),
                    source_id=source.id,
                    url=url.strip(),
                    language=source.language or "am",
                    published_at=published_at,
                    collected_at=datetime.utcnow(),
                    raw_location_text=None,
                )
                db.add(article)
                new_articles_count += 1
        except Exception as exc:
            logger.warning("Failed to collect from source %s: %s", source.name, exc)

    if new_articles_count > 0:
        db.commit()
        logger.info("Collected %d new Amharic news articles.", new_articles_count)

    return new_articles_count

