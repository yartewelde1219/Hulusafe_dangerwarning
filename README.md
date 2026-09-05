# HuluSafe — AIL-Powered Amharic Danger Warning Application

**HuluSafe** is an AI-powered danger-warning system designed to monitor credible Amharic-language news sources and deliver location-aware warnings to users in Ethiopia. The system analyzes incoming articles, detects danger events via Amharic NLP & Naive Bayes, extracts key facts (type, location, time, casualties, displacement, damage) without fabricating missing values, tracks regional danger progression, and sends warnings when an active, sufficiently confident event occurs approximately **within 100 km** of the user and **not older than 14 days**.

> **Safety Principle**: HuluSafe is an information and warning-support system, not an official emergency authority. Every warning clearly shows the source, news publication time, event time when known, danger location, confidence, and a verification recommendation. The system **never invents missing information**.

---

## Table of Contents
1. [Core Features & Policies](#core-features--policies)
2. [Five-Student Architecture & Responsibilities](#five-student-architecture--responsibilities)
3. [Repository Layout](#repository-layout)
4. [Quick Start Guide](#quick-start-guide)
5. [Running Tests & AI Evaluation](#running-tests--ai-evaluation)
6. [External Configurations & Services (Out of Agent Reach)](#external-configurations--services-out-of-agent-reach)
   - [A. Google Maps API Key Setup](#a-google-maps-api-key-setup)
   - [B. Firebase Authentication Integration](#b-firebase-authentication-integration)
   - [C. Firebase Cloud Messaging (FCM) Push Notifications](#c-firebase-cloud-messaging-fcm-push-notifications)
   - [D. Production PostgreSQL Setup](#d-production-postgresql-setup)
   - [E. Live News Crawling & RSS Feeds](#e-live-news-crawling--rss-feeds)
7. [Git Workflow & Collaboration](#git-workflow--collaboration)

---

## Core Features & Policies

- **Amharic Natural Language Processing**: Custom Amharic text cleaner, unicode NFC normalizer, tokenizer, TF-IDF feature extractor, and Multinomial Naive Bayes classifier supporting 9 danger classes.
- **Negation & Context Verification**: Differentiates active danger from negated statements (*"የጎርፍ አደጋ የለም"*), historical records (*"ከሁለት ዓመት በፊት"*), and hypothetical statements (*"ሊከሰት ይችላል"*).
- **Fact-Faithful Information Extraction**: Extracts reported casualties (`deaths`, `injuries`, `displaced`, `missing`, `damage`) and times (`published_at`, `event_time`). Unreported fields remain `NULL`/`Unknown`, never fabricated.
- **Critical Two-Week (14-Day) Notification Rule**: `MAX_ALERT_EVENT_AGE_DAYS = 14`. Notifications are strictly prohibited for events older than 14 days.
- **100 km User Proximity Engine**: Computes user-to-event distance using the Haversine formula and alerts within `DEFAULT_ALERT_RADIUS_KM = 100`.
- **Source Credibility & Multi-Source Agreement**: Documents source credibility (ENA, FBC, DW Amharic, BBC Amharic) and clusters duplicate coverage into unified events.
- **Regional Danger Tracking**: Aggregates active events across Ethiopian administrative regions to produce real-time regional threat levels and trend direction (*Increasing*, *Stable*, *Decreasing*).
- **Reference Media & User Verification**: Displays original article titles and clickable URLs with explicit advice to cross-verify reports.

---

## Five-Student Architecture & Responsibilities

| Team Member | Primary Responsibility | Directory / Components |
|---|---|---|
| **Student 1** | **Frontend**: Flutter foundation, Dashboard, User Location & Settings, Auth UI | `frontend/lib/screens/dashboard_screen.dart`, `settings_screen.dart`, `login_screen.dart`, `providers/` |
| **Student 2** | **Frontend**: Ethiopia Danger Map, Search (Text & Map selection), Danger Details & Reference Media | `frontend/lib/screens/map_screen.dart`, `search_screen.dart`, `danger_details_screen.dart`, `alert_history_screen.dart` |
| **Student 3** | **Backend**: RSS News Collection, PostgreSQL DB, REST API, Time Policies, Proximity Service | `backend/app/main.py`, `models/`, `api/routes/`, `services/news_collector.py`, `services/time_policy.py`, `services/geo.py` |
| **Student 4** | **AI/NLP**: Amharic Preprocessing, Naive Bayes Classifier, Context/Negation Analyzer, Fact Extraction | `ai/preprocessing/`, `ai/models/`, `ai/information_extraction/`, `ai/dataset/`, `ai/training/`, `ai/evaluation/` |
| **Student 5** | **AI/Backend**: Severity Engine, Multi-factor Confidence, Source Credibility, Event Clustering, Regional Tracking | `backend/app/services/intelligence.py`, `services/alert_eligibility.py`, `services/events.py`, `geographic_data/` |

---

## Repository Layout

```text
HuluSafe/
├── frontend/                     # Flutter mobile application
│   ├── lib/
│   │   ├── models/              # Dart data models (DangerEvent, DashboardData)
│   │   ├── providers/           # Riverpod state management
│   │   ├── screens/             # Dashboard, Map, Search, Details, Settings, Login, History
│   │   ├── services/            # API service, Location service, Auth service
│   │   ├── theme/               # Material 3 HuluSafe theme
│   │   ├── utils/               # Constants and date/percent formatters
│   │   └── widgets/             # Reusable DangerCard, StatusViews, VerificationBanner
│   └── test/                    # Flutter widget and unit tests
├── backend/                      # FastAPI backend service
│   ├── app/
│   │   ├── api/routes/          # /dashboard, /nearby-dangers, /search, /regions/danger, /events, /alerts
│   │   ├── database/            # SQLAlchemy session and Base
│   │   ├── jobs/                # APScheduler background news poller
│   │   ├── models/              # Database entities (News, Source, DangerEvent, Region, User)
│   │   ├── schemas/             # Pydantic schemas for request/response serialization
│   │   ├── services/            # Alert eligibility, Geo proximity, Intelligence scoring, News collector
│   │   ├── config.py            # Pydantic application settings
│   │   ├── main.py              # FastAPI application entrypoint with lifespan
│   │   └── seed.py              # Realistic multi-source seed data
│   └── requirements.txt
├── ai/                           # Amharic NLP & Machine Learning pipeline
│   ├── annotation/              # Label Studio guidelines and schemas
│   ├── dataset/                 # sample_articles.jsonl (Amharic labeled corpus)
│   ├── evaluation/              # Metrics calculation and false-alarm test harness
│   ├── feature_extraction/      # TF-IDF vectorizer configuration
│   ├── information_extraction/  # Casualty, damage, time, and location extractors
│   ├── models/                  # Naive Bayes model builder and joblib serializer
│   ├── preprocessing/           # Amharic Unicode cleaner, normalizer, and tokenizer
│   ├── training/                # Model training script (train.py)
│   └── vocabulary/              # Danger categories, Amharic keywords, and weights
├── geographic_data/              # Ethiopian geographic lookup tables
│   ├── locations/               # Sample cities/zones with Amharic names & coordinates
│   └── regions/                 # Ethiopian regional boundaries and coordinates
├── docs/                         # Architecture, REST API contracts, and methodology
├── tests/                        # Automated Pytest suite
│   ├── ai/                      # NLP, negation, time, extraction, and model tests
│   └── backend/                 # API routes, distance, 14-day policy, and intelligence tests
├── docker/                       # Dockerfile & Docker Compose configurations
└── README.md
```

---

## Quick Start Guide

### 1. Backend Setup (FastAPI)

```bash
# Navigate to backend directory
cd backend

# Create and activate Python virtual environment
python -m venv .venv
.venv\Scripts\activate      # On Windows
# source .venv/bin/activate  # On Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Run the API server with auto-reload
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
- Swagger Interactive Documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Health Check: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

### 2. Frontend Setup (Flutter)

```bash
# Navigate to frontend directory
cd frontend

# Install Flutter dependencies
flutter pub get

# Run on connected device, emulator, or Chrome
flutter run
```

### 3. Docker Compose Setup

```bash
docker compose -f docker/docker-compose.yml up --build
```

### 4. Deploy the Backend to Render

The repository includes `render.yaml` at the repository root. In Render, create a
Blueprint from this repository and select the branch containing that file. It sets
the service root directory to `backend`, installs `backend/requirements.txt`,
starts `app.main:app`, and checks `/health`.

Set `GEMINI_API_KEY` in Render's environment settings. Never commit the key or put
it in the Flutter build. After deployment, use the Render HTTPS URL as the APK API
base URL:

```bash
flutter build apk --release --dart-define=API_BASE_URL=https://your-service.onrender.com
```

---

## Running Tests & AI Evaluation

### Run Full Python Test Suite
```bash
# Run all 24 AI and Backend automated unit tests
pytest
```

### Run Model Training & Evaluation Report
```bash
# Retrain the Naive Bayes classifier
python -m ai.training.train

# Generate classification report and false-alarm validation results
python -m ai.evaluation.metrics
```

### Run Flutter Widget & Unit Tests
```bash
cd frontend
flutter test
```

---

## External Configurations & Services (Out of Agent Reach)

To take HuluSafe from local development to production with real mobile devices and live third-party services, follow these step-by-step instructions.

### A. Google Maps API Key Setup
The interactive Ethiopia Danger Map requires a Google Maps Platform API key.

1. **Obtain API Key**:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project (e.g., `HuluSafe-Maps`).
   - Navigate to **APIs & Services** > **Library** and enable **Maps SDK for Android** and **Maps SDK for iOS**.
   - Go to **APIs & Services** > **Credentials** and click **Create Credentials** > **API Key**.
2. **Configure Android**:
   - Open `frontend/android/app/src/main/AndroidManifest.xml`.
   - Locate the `<meta-data android:name="com.google.android.geo.API_KEY" .../>` tag.
   - Replace `YOUR_GOOGLE_MAPS_API_KEY` with your actual Google Maps API key.
3. **Configure iOS**:
   - Open `frontend/ios/Runner/AppDelegate.swift` and provide your API key in `GMSServices.provideAPIKey("YOUR_KEY")`.

---

### B. Firebase Authentication Integration
Full personalized user features (saved locations, personalized dashboard, user alert history) use Firebase Authentication.

1. **Create Firebase Project**:
   - Visit the [Firebase Console](https://console.firebase.google.com/) and create a project (`HuluSafe`).
   - Navigate to **Build** > **Authentication** and enable **Email/Password** and/or **Phone** sign-in methods.
2. **Add Android App**:
   - In Project Settings, add an Android app with package name `com.hulusafe.hulusafe`.
   - Download the generated `google-services.json` file and place it in `frontend/android/app/`.
3. **Add iOS App**:
   - Add an iOS app with bundle ID `com.hulusafe.hulusafe`.
   - Download `GoogleService-Info.plist` and place it in `frontend/ios/Runner/`.
4. **Backend Token Verification**:
   - In `backend/app/api/routes/alerts.py`, verify incoming Firebase ID Tokens passed in the `Authorization: Bearer <token>` header using the `firebase-admin` Python SDK:
     ```python
     import firebase_admin
     from firebase_admin import auth

     decoded_token = auth.verify_id_token(id_token)
     uid = decoded_token['uid']
     ```

---

### C. Firebase Cloud Messaging (FCM) Push Notifications
To dispatch push notifications to Android & iOS devices when an alert threshold is met:

1. **Generate Service Account Credentials**:
   - In Firebase Console, go to **Project Settings** > **Service Accounts**.
   - Click **Generate New Private Key** to download the JSON credential file (e.g., `serviceAccountKey.json`).
   - Place this file in `backend/` and set its path in your `.env` file:
     ```env
     FIREBASE_SERVICE_ACCOUNT_PATH=./serviceAccountKey.json
     ```
2. **Dispatching Alerts**:
   - When `evaluate_alert()` in `backend/app/services/alert_eligibility.py` returns `eligible=True`, dispatch a targeted FCM message:
     ```python
     from firebase_admin import messaging

     message = messaging.Message(
         notification=messaging.Notification(
             title="⚠️ HuluSafe Danger Alert",
             body=f"{event.danger_type.upper()} reported near {event.location_name} ({distance_km:.0f} km away).",
         ),
         data={"event_id": event.id},
         token=user_fcm_token,
     )
     messaging.send(message)
     ```

---

### D. Production PostgreSQL Setup
For local testing, HuluSafe uses SQLite. For production deployment:

1. **Provision PostgreSQL**:
   - Create a PostgreSQL database on AWS RDS, Supabase, Neon, or your own server.
2. **Update Environment**:
   - Create `.env` in `backend/` from `.env.example`:
     ```env
     DATABASE_URL=postgresql://hulusafe_user:your_password@your_db_host:5432/hulusafe_db
     MAX_ALERT_EVENT_AGE_DAYS=14
     DEFAULT_ALERT_RADIUS_KM=100.0
     ```
3. **Database Migration**:
   - Run the startup script or Alembic migrations to create tables and seed default source records and Ethiopian regions.

---

### E. Live News Crawling & RSS Feeds
HuluSafe comes configured with RSS endpoints for Ethiopian national and international Amharic news sources in `backend/app/seed.py`:
- Ethiopian News Agency (`https://www.ena.et/feed/`)
- Fana Broadcasting Corporate (`https://www.fanabc.com/feed/`)
- Deutsche Welle Amharic (`https://rss.dw.com/rdf/rss-amh-news`)
- BBC News Amharic (`https://feeds.bbci.co.uk/amharic/rss.xml`)

To register additional media:
1. Insert new entries into the `sources` table via SQL or FastAPI admin endpoint.
2. Set `active = True`, specify `credibility_score` (0.0 to 1.0), and provide the RSS/Atom feed URL.
3. Configure the collection frequency in `.env` (default: `NEWS_POLL_MINUTES=30`).

---

## Git Workflow & Collaboration

Follow the branch strategy defined in the project plan:

1. Do not push directly to `main`. All development branches branch from `develop`.
2. Branch naming conventions:
   - `feature/flutter-dashboard`
   - `feature/flutter-map`
   - `feature/flutter-search`
   - `feature/news-ingestion`
   - `feature/amharic-nlp`
   - `feature/danger-scoring`
3. Every pull request must include unit tests and pass `pytest` and `flutter test` before merging.

