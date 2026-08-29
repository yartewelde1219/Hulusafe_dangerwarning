# API contract

Base URL (local): `http://127.0.0.1:8000`

Shared danger-event JSON:

```json
{
  "event_id": "EVT-001",
  "danger_type": "flood",
  "danger_level": "high",
  "confidence": 0.88,
  "location": {
    "name": "Awash",
    "region": "Afar",
    "latitude": 8.9833,
    "longitude": 40.1667
  },
  "event_time": "2026-08-27T13:50:00",
  "published_at": "2026-08-27T14:30:00",
  "status": "active",
  "deaths": 12,
  "injuries": null,
  "displaced": 350,
  "missing": null,
  "damage": null,
  "distance_km": 78.0,
  "sources": []
}
```

`null` means not reported. `0` means the source stated zero.

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/health` | Service and policy constants |
| GET | `/dashboard?lat=&lon=` | Personalized nearby summary |
| GET | `/nearby-dangers?lat=&lon=&radius_km=100` | Events within radius |
| GET | `/search?lat=&lon=&q=` | Location/type search around selected point |
| GET | `/regions/danger` | Regional scores for the Ethiopia map |
| GET | `/events/{event_id}` | Danger details plus reference media |
| GET | `/alerts/history` | Personalized alert history |

Do not change these shapes without a team discussion. Firebase Authentication tokens will be sent as `Authorization: Bearer <token>`.
