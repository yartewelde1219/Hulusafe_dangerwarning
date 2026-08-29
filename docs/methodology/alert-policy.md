# Time, proximity, and alert methodology

- `NEWS PUBLICATION TIME`: when the outlet published the article.
- `EVENT TIME`: when the danger happened or started. If unknown, store `null` and show `Event time: Unknown`.
- Notification eligibility uses event occurrence, not publication date alone, and never notifies after 14 days (configurable).
- Distance uses the Haversine formula. Default alert radius is 100 km.
- Copied reports cluster into one event; they are not automatically independent confirmations.

```text
ALERT =
  ACTIVE_EVENT
  AND EVENT_AGE <= 14 DAYS
  AND DISTANCE <= 100 KM
  AND SEVERITY >= threshold
  AND CONFIDENCE >= threshold
  AND LOCATION_CONFIDENCE >= threshold
  AND NOT_ALREADY_NOTIFIED
```
