# HuluSafe system architecture

HuluSafe monitors approved Amharic news, extracts reported danger events, scores them, and warns authenticated users when an eligible active event is within about 100 km.

```text
Approved Amharic sources
  → news collection (Student 3)
  → Amharic NLP / Naive Bayes / extraction (Student 4)
  → severity, confidence, event resolution, regional tracking (Student 5)
  → FastAPI + PostgreSQL (Student 3)
  → Flutter dashboard, map, search, notifications (Students 1–2)
```

## Safety

HuluSafe is not an official emergency authority. Every warning must show source, publication time, event time when known, location, confidence, and a verification recommendation. Missing optional impact fields stay `null` / Unknown.

## Time

Store `published_at` and `event_time` separately. Notifications are prohibited when the relevant occurrence is older than `MAX_ALERT_EVENT_AGE_DAYS` (default 14). Historical data may remain searchable.

## Ownership

| Area | Owner |
| --- | --- |
| Flutter foundation, dashboard, location, settings, auth UI | Student 1 |
| Map, search, danger details, FCM, alert history | Student 2 |
| News, database, APIs, time filter, 100 km service | Student 3 |
| Dataset, preprocessing, Naive Bayes, extraction | Student 4 |
| Severity, credibility, clustering, regional scores | Student 5 |
