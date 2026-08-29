# Flutter app (Students 1 and 2)

Riverpod state, Geolocator, Google Maps, and HTTP client against the FastAPI contract.

Set `API_BASE_URL` at build time if the backend is not `http://127.0.0.1:8000`:

```bash
flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000
```

Android emulators should use `10.0.2.2` to reach a backend on the host machine.
