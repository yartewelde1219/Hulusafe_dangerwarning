# HuluSafe --- AI-Powered Danger Warning Application

## Updated Project Plan, Methodology, Five-Student Task Assignment, Tools & GitHub Workflow

------------------------------------------------------------------------

# 1. Project Overview

**HuluSafe** is an AI-powered danger-warning application designed to
monitor credible **Amharic-language news sources** and provide
location-aware danger information and warnings to users in Ethiopia.

The system will extract danger-related information directly from the
news articles, including:

-   Danger type
-   Danger location
-   News publication time
-   Event time when available
-   Deaths
-   Injuries
-   Displaced people
-   Missing people
-   Property/infrastructure damage
-   Affected population
-   Current event status
-   Danger-indicating words and phrases
-   Negation/context
-   Source information
-   Danger severity
-   Confidence

The system will also:

1.  Request the user's location permission.
2.  Collect Amharic news from approved national and international media.
3.  Analyze and classify the news using **Naive Bayes** and Amharic NLP.
4.  Extract event information from the news.
5.  Determine whether the reported event is current, historical, or
    otherwise not suitable for an active warning.
6.  Track danger events across Ethiopian regions.
7.  Calculate danger severity and confidence.
8.  Compare danger locations with the user's location.
9.  Send a warning when an active, sufficiently confident danger is
    approximately **within 100 km** of the user.
10. Clearly show the **news publication time** and relevant event time
    so users can understand how recent the information is.
11. **Never send a notification for a danger event whose relevant
    occurrence is older than two weeks (14 days).**
12. Allow users to search locations and inspect current danger, recent
    danger, and danger progression.
13. Require user authentication for full personalized functionality, including
    personalized dashboard information, alert history, saved locations, and
    notification preferences.

> **Safety principle:** HuluSafe is an information and warning-support
> system, not an official emergency authority. It must show source,
> publication time, event time when available, danger location,
> confidence, and supporting information. The system must never invent
> missing information.

------------------------------------------------------------------------

# 2. Critical Time Policy

Time is a core part of HuluSafe because old news can unnecessarily
frighten users.

The system should maintain at least two separate timestamps:

``` text
NEWS PUBLICATION TIME
When the media outlet published the article.

EVENT TIME
When the danger actually happened or was reported to have started.
```

If the event time is unavailable, the system should explicitly mark it
as:

``` text
Event time: Unknown
```

and use the publication time cautiously according to the project's alert
policy.

## 2.1 Two-Week Notification Rule

HuluSafe must **not notify users about dangers that occurred more than
14 days ago**.

Conceptually:

``` text
Current time
     ↓
Determine event occurrence time
     ↓
How old is the event?
     ↓
> 14 days?
 ┌───────────────┴───────────────┐
 YES                             NO
 ↓                                ↓
NO NOTIFICATION             Continue evaluation
```

This rule applies to **notifications**.

The application may still display older events in historical/search
views if clearly labeled as historical.

## 2.2 Publication Time in Every Warning

Every notification should show when the source published the report.

Example:

``` text
⚠️ HuluSafe Danger Alert

Danger: FLOOD
Danger location: Location X
Distance: 78 km from you
Danger level: HIGH
Confidence: 88%

News published: 27 Aug 2026, 14:30
Event time: 27 Aug 2026, 13:50

Sources: 3 credible reports
```

If the news is older but the danger event itself is still active, the
system should distinguish:

``` text
News published: 20 Aug
Event status: Ongoing
Last updated: 27 Aug
```

The alert engine should use the **event's current status and
occurrence/update information**, not publication date alone, when
determining whether a danger is still active.

------------------------------------------------------------------------

# 3. Main System Architecture

``` text
Approved Amharic News Sources
        ↓
News Collection
(RSS / API / permitted extraction)
        ↓
Amharic Text Processing
(cleaning / normalization / deduplication)
        ↓
AI / NLP
(Naive Bayes + danger features + negation/context)
        ↓
Information Extraction
(type + location + time + deaths + displacement + damage)
        ↓
Event Resolution
(same event? current? historical? ongoing?)
        ↓
Danger Intelligence Engine
(severity + credibility + agreement + confidence + recency)
        ↓
Regional Danger Tracking
        ↓
User Proximity Engine
        ↓
100 km Distance Check
        ↓
14-Day Notification Eligibility Check
        ↓
Alert Threshold Check
        ↓
Push Notification
        ↓
Flutter Mobile Application
```

------------------------------------------------------------------------

# 4. Five-Person Team Assignment

  -----------------------------------------------------------------------
  Member                  Main Responsibility     Secondary
                                                  Responsibility
  ----------------------- ----------------------- -----------------------
  **Student 1**           Frontend --- Dashboard, UI/UX and Flutter
                          User Location &         foundation
                          Settings                

  **Student 2**           Frontend --- Map,       Frontend/backend
                          Search & Notifications  integration

  **Student 3**           Backend --- News        Time filtering and
                          Collection, Database &  proximity service
                          APIs                    

  **Student 4**           AI/NLP --- Amharic      Dataset, preprocessing,
                          Classification &        Naive Bayes
                          Information Extraction  

  **Student 5**           AI/Backend ---          Event resolution and
                          Severity, Confidence,   trend analysis
                          Credibility & Regional  
                          Tracking                
  -----------------------------------------------------------------------

The work is divided so that every student owns a substantial technical
area while all five collaborate through GitHub.

------------------------------------------------------------------------

# STUDENT 1 --- FRONTEND: DASHBOARD, LOCATION & SETTINGS

## Main Responsibility

Build the Flutter application's foundation, dashboard, user location
functionality, and settings.

## Recommended Tools & Languages

  Purpose                Recommended Tool
  ---------------------- -----------------------------------
  Programming language   **Dart**
  Mobile framework       **Flutter**
  IDE                    **VS Code**
  Version control        **Git + GitHub**
  UI design              **Figma** guys keep in mind this is not necessary but it is recommended. 
  API communication      Flutter `http` or `dio`
  State management       **Riverpod** or **Provider**
  Location               `geolocator`
  Testing                Flutter Test

## A. Flutter Foundation

Implement:

-   Flutter project structure.
-   Navigation.
-   Reusable widgets.
-   Theme.
-   API service layer.
-   State management.
-   Loading states.
-   Error states.
-   Empty states.
-   GitHub feature branches.

### Methodology

``` text
Create Flutter Project
        ↓
Define screens
        ↓
Create navigation
        ↓
Create reusable widgets
        ↓
Create API service
        ↓
Connect backend
        ↓
Test on Android
```

Suggested structure:

``` text
frontend/
└── lib/
    ├── screens/
    ├── widgets/
    ├── models/
    ├── services/
    ├── providers/
    └── utils/
```

## B. Dashboard

Display:

-   User's current area.
-   Current nearby danger.
-   Highest nearby danger.
-   Danger type.
-   Distance to danger.
-   Danger level.
-   Confidence.
-   Publication time.
-   Event time.
-   Last update.
-   Recent alerts.
-   Map access.
-   Search access.

### Methodology

``` text
GPS location
    ↓
GET /dashboard?lat={lat}&lon={lon}
    ↓
Backend calculates nearby active events
    ↓
Flutter receives JSON
    ↓
Dashboard widgets
```

## C. Location Permission

Implement:

1.  Request location permission.
2.  Explain why location is needed.
3.  Handle denied permission.( if the location permission is denied it should ask for it whenever the user needs information from the App)
4.  Obtain coordinates.
5.  Send location to backend only as needed.
6.  Display approximate area rather than unnecessarily exposing exact
    coordinates.

## D. Settings

Implement:

-   Notification enable/disable.
-   Location permission status.
-   Alert preferences.
-   Privacy information.
-   About HuluSafe.

### Deliverables

-   Flutter foundation.
-   Dashboard.
-   Location permission.
-   Location display.
-   Settings.
-   Navigation.
-   API integration.

------------------------------------------------------------------------

# STUDENT 2 --- FRONTEND: MAP, SEARCH & NOTIFICATIONS

## Main Responsibility

Build the danger visualization, search functionality, and warning
experience.

## Recommended Tools & Languages

  Purpose                Recommended Tool
  ---------------------- ---------------------------------------
  Programming language   **Dart**
  Framework              **Flutter**
  IDE                     VS Code
  Map                    **Google Maps Flutter** or **Mapbox**
  Notifications          **Firebase Cloud Messaging (FCM)**
  UI design              Figma
  API                    `http` / `dio`
  Version control        Git + GitHub

## A. Ethiopia Danger Map

Display:

``` text
🟢 No active danger
🟡 Low
🟠 Moderate
🔴 High
🟣 Critical
```

### Methodology

``` text
GET /regions/danger
        ↓
Backend returns regional danger scores
        ↓
Flutter map
        ↓
Markers / region overlays
        ↓
User selects location
        ↓
Danger details
```

## B. Search

Users can search:

-   Region.
-   Zone.
-   Woreda.
-   City.
-   Danger type.
-   Recent events.

Users must be able to select a location in two ways:

1. **Typing a location name** into the search field.
2. **Interacting with the map and selecting a location** directly.

The selected/typed location becomes the center of the danger search. The same
100 km proximity rule should be used for the selected location when applicable.

### Methodology

``` text
                    LOCATION SEARCH
                          ↓
             ┌────────────┴────────────┐
             ↓                         ↓
      Type location              Select on map
             ↓                         ↓
      Location resolver          Map coordinates
             └────────────┬────────────┘
                          ↓
                 Selected coordinates
                          ↓
                  GET /search
                          ↓
                Backend searches
                          ↓
             Active/recent danger events
                          ↓
                    Display results
```

## C. Danger Details

Display:

``` text
Danger type
Danger location
Distance from user
Danger level
Confidence
News publication time
Event time
Last update
Deaths
Injuries
Displaced
Missing
Damage
Sources
Trend
```

If information was not stated in the news:

``` text
Deaths: Unknown
```

rather than inventing a value.

## D. Push Notifications

Use **Firebase Cloud Messaging**.

### Methodology

``` text
Backend detects alert condition
        ↓
Firebase Cloud Messaging
        ↓
Android device
        ↓
Notification
        ↓
User opens alert
        ↓
Danger details page
```

## E. 100 km Warning Display

Example:

``` text
⚠️ HULUSAFE ALERT

Danger: FLOOD
Danger location: Location X

Distance: 78 km
Danger level: HIGH
Confidence: 88%

News published: 27 Aug 2026, 14:30
Event time: 27 Aug 2026, 13:50
```

### Deliverables

-   Ethiopia danger map.
-   Text-based location search.
-   Interactive map location selection.
-   Danger details.
-   Push notifications.
-   100 km warning UI.
-   Alert history.

------------------------------------------------------------------------

# STUDENT 3 --- BACKEND: NEWS, DATABASE, APIs, TIME & PROXIMITY

## Main Responsibility

Build the backend data infrastructure and services.

## Recommended Tools & Languages

  Purpose                         Recommended Tool
  ------------------------------- ---------------------------
  Programming language            **Python**
  Backend framework               **FastAPI**
  Database                        **PostgreSQL**
  ORM                             **SQLAlchemy**
  API testing                     **Postman**
  Database management             **pgAdmin**
  Scheduled jobs                  **APScheduler** or Celery
  Push notification integration   Firebase Admin SDK
  Version control                 Git + GitHub
  IDE                             VS Code / PyCharm

## A. Amharic News Source Registry

All sources should provide or publish **Amharic-language content**.

Store:

``` text
Source ID
Source Name
Country
Language
Source Type
Credibility Score
Collection Method
URL
Active/Inactive
```

Use a documented source-selection and credibility methodology.

The project should include both suitable:

``` text
National media
+
International media with Amharic reporting
```

## B. News Collection

Use, where permitted:

-   Official APIs.
-   RSS feeds.
-   Public feeds.
-   Permitted web extraction.

Retrieve:

``` text
Title
Content
URL
Publisher
Publication time
Language
```

### Methodology

``` text
Scheduler
    ↓
Approved source list
    ↓
Retrieve new Amharic articles
    ↓
Validate
    ↓
Extract publication timestamp
    ↓
Duplicate check
    ↓
Store raw article
    ↓
Send to AI pipeline
```

Respect source terms, rate limits, robots policies, and applicable laws.

## C. Database

### `news`

``` text
id
title
content
source_id
url
language
published_at
collected_at
raw_location_text
created_at
```

### `sources`

``` text
id
name
country
language
credibility_score
url
collection_method
active
```

### `danger_events`

``` text
id
danger_type
danger_level
confidence
location_name
region
zone
woreda
latitude
longitude
event_time
event_end_time
status
deaths
injuries
displaced
missing
damage
created_at
updated_at
```

## Optional Danger Impact Information

The following danger-event fields are **not mandatory**:

- `deaths`
- `injuries`
- `displaced`
- `missing`
- `damage`
- `created_at`
- `updated_at`

They are **highly recommended when explicitly reported in the news article**.
A danger event remains valid even when some or all impact fields are not
reported by the source. Missing information must be stored as `NULL`/`UNKNOWN`,
not as an invented value.

For example, if an article reports a flood but gives no casualty or damage
figures, HuluSafe should still create and process the danger event.

The system must distinguish:

``` text
0       = explicitly reported as zero
NULL    = not reported / unknown
```

The AI must never estimate or fabricate deaths, injuries, displacement,
missing persons, or damage.

### `event_sources`

``` text
event_id
news_id
source_id
source_credibility
independent_report
published_at
```

### `regions`

``` text
id
region_name
latitude
longitude
boundary_data
```

### `user_locations`

``` text
user_id
latitude
longitude
region
updated_at
```

## D. News Deduplication

Compare:

-   URL.
-   Title similarity.
-   Text similarity.
-   Publication time.
-   Event location.
-   Event type.

``` text
Article A ─┐
Article B ─┼→ Same event cluster
Article C ─┘
```

This prevents one event reported by many sources from creating multiple
unrelated alerts.

## E. Publication Time & Event Time

The backend must store both:

``` text
published_at
event_time
```

If the article says the event occurred yesterday, the NLP layer should
attempt to convert the relative date into an actual timestamp using the
article publication date.

If no event time can be reliably extracted:

``` text
event_time = NULL
event_time_confidence = LOW
```

## F. Two-Week Notification Filter

Implement a backend service:

``` text
current_time
      ↓
event_time
      ↓
event_age = current_time - event_time
      ↓
event_age > 14 days?
      ↓
YES → notification prohibited
NO  → continue
```

Important:

``` text
Notification eligibility ≠ historical data deletion
```

Old events can remain in the database for analysis/history but must not
generate new user notifications when outside the two-week notification
window.

## G. 100 km Proximity API

``` text
GET /nearby-dangers?lat={lat}&lon={lon}&radius_km=100
```

The service:

1.  Receives user coordinates.
2.  Finds active events.
3.  Calculates geographical distance.
4.  Filters to approximately 100 km.
5.  Applies time eligibility.
6.  Applies severity/confidence thresholds.
7.  Returns alert candidates.

### Haversine Formula

``` text
a = sin²(Δlat/2)
    + cos(lat1) × cos(lat2) × sin²(Δlon/2)

c = 2 × atan2(√a, √(1-a))

distance = Earth_radius × c
```

## H. Notification Deduplication

Maintain:

``` text
user_id
event_id
notification_sent_at
```

This prevents the same event from repeatedly notifying the same user.

### Deliverables

-   News collector.
-   Source registry.
-   PostgreSQL database.
-   FastAPI backend.
-   REST APIs.
-   Time processing.
-   14-day notification filter.
-   100 km proximity service.
-   Notification backend.
-   Deduplication.

------------------------------------------------------------------------

# STUDENT 4 --- AI/NLP: AMHARIC DANGER DETECTION & INFORMATION EXTRACTION

## Main Responsibility

Build the Amharic NLP pipeline.

## Recommended Tools & Languages

  Purpose                Recommended Tool
  ---------------------- ----------------------------------------
  Programming language   **Python**
  ML                     **scikit-learn**
  Naive Bayes            `MultinomialNB`
  Text features          TF-IDF
  NLP                    **spaCy / custom Python NLP pipeline**
  Data processing        pandas
  Numerical processing   NumPy
  Dataset annotation     Label Studio
  Experiment tracking    Jupyter Notebook
  Model serialization    joblib
  Version control        Git + GitHub

Because the news is in Amharic, the team should not assume that English
NLP tools will work correctly without evaluation. Use custom Amharic
preprocessing and test every component on real Amharic examples.

## A. Dataset Creation

Create an Amharic danger-news dataset.

Each article should be annotated with:

  Field              Example
  ------------------ ---------------------
  Danger             Yes/No
  Danger type        Conflict
  Location           Region/Zone/City
  Event time         Date
  Publication time   Date
  Deaths             Number/Unknown
  Injuries           Number/Unknown
  Displacement       Number/Unknown
  Missing            Number/Unknown
  Damage             Description/Unknown
  Negated            Yes/No
  Historical         Yes/No
  Hypothetical       Yes/No
  Current/Active     Yes/No

## B. Annotation Tool

Recommended:

**Label Studio**

Annotators should mark:

``` text
Danger terms
Location
Time expression
Death information
Injury information
Displacement
Missing persons
Damage
Negation
Event status
```

## C. Amharic Preprocessing

``` text
Raw Amharic news
       ↓
Unicode normalization
       ↓
Cleaning
       ↓
Sentence segmentation
       ↓
Tokenization
       ↓
Normalization
       ↓
Careful stopword handling
       ↓
TF-IDF
```

Stopword removal must be tested because some grammatical words may be
important for negation and context.

## D. Danger Vocabulary

Create categories from the actual corpus:

``` text
CONFLICT
FLOOD
FIRE
LANDSLIDE
DROUGHT
EARTHQUAKE
EXTREME WEATHER
OTHER
```

The project should build a documented Amharic vocabulary for each
category.

## E. Naive Bayes

Initial model:

``` text
Amharic article
       ↓
TF-IDF
       ↓
Multinomial Naive Bayes
       ↓
Danger class
```

Possible output:

``` json
{
  "normal": 0.04,
  "conflict": 0.82,
  "flood": 0.03,
  "fire": 0.02,
  "landslide": 0.01,
  "other": 0.08
}
```

## F. Negation & Context

Keyword detection alone is insufficient.

The system must distinguish:

``` text
Actual danger
No danger
Historical danger
Hypothetical danger
Reported/denied danger
```

### Methodology

``` text
Sentence
   ↓
Find danger term
   ↓
Inspect surrounding context
   ↓
Detect Amharic negation
   ↓
Check temporal context
   ↓
Check event status
   ↓
Modify classification/features
```

Example concept:

``` text
"there is no flood"
        ↓
Flood term detected
        ↓
Negation detected
        ↓
Not automatically an active flood
```

## G. Information Extraction

The NLP system should extract information directly from the article.

``` text
Article
   ↓
Danger type
   ↓
Location
   ↓
Event time
   ↓
Deaths
   ↓
Injuries
   ↓
Displacement
   ↓
Missing
   ↓
Damage
   ↓
Event status
```

If the article does not provide a value:

``` text
NULL / UNKNOWN
```

The model must never invent a number.

## H. Location Extraction

Recommended approach:

``` text
Amharic article
       ↓
Recognize location expression
       ↓
Normalize spelling/name
       ↓
Match against Ethiopian geographic database
       ↓
Region / Zone / Woreda / City
       ↓
Coordinates
```

The NLP model should extract the location name; the backend geographic
database should provide the coordinates.

## I. Time Extraction

The model should recognize:

``` text
Absolute dates
Relative dates
"today"
"yesterday"
"last week"
"earlier"
"since..."
"ongoing"
```

Then normalize them relative to the article publication time.

Example:

``` text
Article published: 27 Aug
"yesterday"
        ↓
Event date ≈ 26 Aug
```

The system should retain an uncertainty indicator when exact timing
cannot be established.

## J. Evaluation

Measure:

-   Accuracy.
-   Precision.
-   Recall.
-   F1-score.
-   Confusion matrix.
-   False-positive rate.
-   False-negative rate.

Create special evaluation sets for:

``` text
Normal
Current danger
Negated danger
Historical danger
Hypothetical danger
Multiple danger types
Relative dates
Unknown locations
```

### Deliverables

-   Amharic dataset.
-   Annotation guidelines.
-   Label Studio project.
-   Preprocessing pipeline.
-   Danger vocabulary.
-   Naive Bayes model.
-   Negation/context module.
-   Information extraction module.
-   Evaluation report.

------------------------------------------------------------------------

# STUDENT 5 --- DANGER INTELLIGENCE: SEVERITY, CONFIDENCE, SOURCES & REGIONAL TRACKING

## Main Responsibility

Convert extracted news information into a structured danger assessment.

## Recommended Tools & Languages

  Purpose                      Recommended Tool
  ---------------------------- ---------------------
  Programming language         **Python**
  ML/data analysis             scikit-learn
  Data processing              pandas + NumPy
  Backend integration          FastAPI
  Visualization/research       Jupyter Notebook
  Database access              SQLAlchemy
  Geospatial processing        GeoPandas / Shapely
  Maps/geographic boundaries   GeoJSON
  Version control              Git + GitHub

## A. Severity Calculation

Do not use keyword count alone.

Combine:

``` text
Extracted impact
+
Danger type
+
Danger-indicating evidence
+
Source credibility
+
Independent-source agreement
+
Recency
+
Location confidence
```

Example initial weighting:

  Factor                           Initial Weight
  ------------------------------ ----------------
  Event/impact severity                       25%
  NLP danger evidence                         20%
  Source credibility                          20%
  Independent-source agreement                20%
  Recency                                     10%
  Location confidence                          5%

These values are starting points and should be validated using project
data.

## B. Danger Word Weighting

Create a documented scoring vocabulary.

Conceptually:

``` text
Minor warning indicator → lower weight
Injury → medium weight
Death → higher weight
Large displacement → higher weight
Major active conflict → very high weight
```

The exact Amharic words and weights must be determined and validated
from the dataset and annotation guidelines.

## C. Source Credibility

Each approved media source receives a documented credibility score.

Consider factors such as:

-   Editorial standards.
-   Transparency.
-   Corrections policy.
-   Reliability history.
-   Primary-source reporting.
-   Reporting consistency.

Example:

``` text
Source A → 0.95
Source B → 0.88
Source C → 0.76
```

The values should be justified in project documentation.

## D. Independent-Source Agreement

Several credible sources reporting the same event can increase
confidence.

``` text
Source A ─┐
Source B ─┼→ Event cluster → Increased confidence
Source C ─┘
```

However:

``` text
A reports original event
B copies A
C copies A
```

must not automatically be treated as three independent confirmations.

Use:

-   Text similarity.
-   Shared referenced source.
-   Location.
-   Event type.
-   Event time.
-   Reporting relationship where identifiable.

## E. Confidence

Conceptual calculation:

``` text
Confidence =
NLP confidence
+
Source credibility
+
Independent agreement
+
Location confidence
+
Recency
```

Example:

``` json
{
  "confidence": 0.87,
  "nlp_confidence": 0.82,
  "source_confidence": 0.91,
  "agreement": 0.86,
  "location_confidence": 0.95,
  "recency_score": 0.89
}
```

## F. Regional Danger Tracking

``` text
News event
    ↓
Extract location
    ↓
Normalize location
    ↓
Map to Ethiopian region
    ↓
Aggregate active events
    ↓
Calculate regional score
    ↓
Store regional snapshot
    ↓
Map + Search
```

Example:

  Region     Danger     Level        Confidence
  ---------- ---------- ---------- ------------
  Region A   Conflict   HIGH                91%
  Region B   Flood      MODERATE            76%
  Region C   Fire       HIGH                84%

## G. Danger Progression

Store historical danger scores:

``` text
Day 1 → LOW
Day 2 → MODERATE
Day 3 → HIGH
Day 4 → CRITICAL

Trend → Increasing
```

or:

``` text
Day 1 → HIGH
Day 2 → MODERATE
Day 3 → LOW

Trend → Decreasing
```

### Methodology

``` text
Current danger score
        +
Previous danger snapshots
        ↓
Time-series comparison
        ↓
Increasing / Stable / Decreasing
```

## H. Active Event Resolution

The same danger can appear in many news articles.

The system should combine reports into an event:

``` text
Article A ─┐
Article B ─┼→ EVENT-001
Article C ─┘
```

Then continuously update:

``` text
EVENT-001
   ↓
New source
   ↓
Updated information
   ↓
Updated confidence
   ↓
Updated severity
   ↓
Updated status
```

## I. Alert Eligibility

Student 5 works with Student 3 to enforce:

``` text
ACTIVE EVENT
+
EVENT AGE ≤ 14 DAYS
+
DISTANCE ≤ 100 KM
+
SEVERITY THRESHOLD
+
CONFIDENCE THRESHOLD
+
NO DUPLICATE ALERT
        ↓
ALERT ELIGIBLE
```

### Deliverables

-   Severity engine.
-   Source credibility model.
-   Confidence model.
-   Multi-source aggregation.
-   Event clustering/resolution.
-   Regional danger tracking.
-   Danger trend analysis.
-   Alert eligibility logic.

------------------------------------------------------------------------











# 5. End-to-End Feature Methodology

## Feature 1 --- User Location

``` text
Flutter
   ↓
Request permission
   ↓
GPS coordinates
   ↓
Backend
   ↓
Nearby danger query
```

Tools:

``` text
Dart
Flutter
geolocator
FastAPI
PostgreSQL
```

------------------------------------------------------------------------

# 6. Feature 2 --- Amharic News Collection

``` text
Approved media sources
        ↓
RSS/API/permitted extraction
        ↓
Amharic article
        ↓
Publication timestamp
        ↓
Database
```

Store the original URL and source.

------------------------------------------------------------------------

# 7. Feature 3 --- AI Danger Detection

``` text
Amharic article
       ↓
Preprocessing
       ↓
TF-IDF
       ↓
Naive Bayes
       ↓
Danger probability
       ↓
Danger type
```

------------------------------------------------------------------------

# 8. Feature 4 --- Information Extraction

``` text
Article
   ↓
NLP
   ├── Danger type
   ├── Location
   ├── Event time
   ├── Deaths
   ├── Injuries
   ├── Displacement
   ├── Missing
   ├── Damage
   └── Event status
```

------------------------------------------------------------------------

# 9. Feature 5 --- Negation and Historical Context

``` text
Danger word
     ↓
Context analysis
     ↓
Negation?
     ↓
Historical?
     ↓
Hypothetical?
     ↓
Current/active?
```

Only sufficiently supported active danger events should proceed toward
warning evaluation.

------------------------------------------------------------------------

# 10. Feature 6 --- Source Credibility

``` text
Source
   ↓
Credibility score
   ↓
Event evidence
```

Then combine evidence from multiple sources.

------------------------------------------------------------------------

# 11. Feature 7 --- Confidence

``` text
AI confidence
      +
Source credibility
      +
Independent confirmation
      +
Location confidence
      +
Recency
      ↓
Final confidence
```

------------------------------------------------------------------------

# 12. Feature 8 --- Danger Severity

``` text
Extracted impact
      +
Danger category
      +
Severity indicators
      +
Event status
      ↓
Severity score
```

------------------------------------------------------------------------

# 13. Feature 9 --- Regional Danger Tracking

``` text
Danger location
      ↓
Ethiopian geographic database
      ↓
Region
      ↓
Aggregate active events
      ↓
Regional danger score
      ↓
Map
```

------------------------------------------------------------------------

# 14. Feature 10 --- Danger Progression

``` text
Historical snapshots
       ↓
Compare scores over time
       ↓
Increasing
Stable
Decreasing
```

The application should distinguish:

``` text
Current danger
Recent danger
Historical danger
```

------------------------------------------------------------------------

# 15. Feature 11 --- 100 km Warning

``` text
User coordinates
       +
Danger coordinates
       ↓
Haversine distance
       ↓
Distance ≤ 100 km?
       ↓
YES
       ↓
Continue alert checks
```

The notification must explicitly state the danger location.

------------------------------------------------------------------------

# 16. Feature 12 --- Two-Week Warning Limit

``` text
Danger event
      ↓
Determine occurrence/event time
      ↓
Calculate age
      ↓
Older than 14 days?
    /          \
  YES           NO
   ↓             ↓
No alert     Continue checks
```

The two-week rule should be configurable in the backend:

``` text
MAX_ALERT_EVENT_AGE_DAYS = 14
```

The team can change this configuration later without rewriting the
notification system.

------------------------------------------------------------------------

# 17. Feature 13 --- Warning Notification

Final decision:

``` text
Active danger
      ↓
Reliable location
      ↓
Event age ≤ 14 days
      ↓
Distance ≤ 100 km
      ↓
Severity threshold
      ↓
Confidence threshold
      ↓
No duplicate notification
      ↓
SEND
```

Notification example:

``` text
⚠️ HuluSafe Danger Alert

A HIGH-level flood has been reported near
[Danger Location].

Distance: 78 km from your location
Confidence: 88%

News published:
27 Aug 2026, 14:30

Event time:
27 Aug 2026, 13:50

Reported impacts:
Deaths: 12
Displaced: 350

Sources:
3 credible independent reports

Trend:
Increasing
```

------------------------------------------------------------------------

# 18. Recommended Technology Stack

  Layer                Technology
  -------------------- ------------------------------------
  Mobile frontend      **Flutter**
  Frontend language    **Dart**
  Backend              **Python + FastAPI**
  Database             **PostgreSQL**
  ORM                  SQLAlchemy
  AI/ML                **Python + scikit-learn**
  Classifier           **Multinomial Naive Bayes**
  Text features        **TF-IDF**
  Data processing      pandas + NumPy
  NLP                  Python/custom Amharic NLP pipeline
  Dataset annotation   **Label Studio**
  Model storage        joblib
  Maps                 Google Maps Flutter / Mapbox
  Push notifications   **Firebase Cloud Messaging**
  Authentication       **Firebase Authentication** (recommended) or JWT
  API testing          Postman
  UI/UX                Figma
  IDE                  Android Studio / VS Code
  Version control      **Git + GitHub**
  Documentation        Markdown
  Deployment           Docker + suitable cloud hosting

------------------------------------------------------------------------

# 19. GitHub Collaboration Strategy

Use:

``` text
main
│
└── develop
     │
     ├── feature/flutter-dashboard
     ├── feature/flutter-location
     ├── feature/flutter-map
     ├── feature/flutter-search
     ├── feature/notifications
     ├── feature/news-ingestion
     ├── feature/database
     ├── feature/api
     ├── feature/amharic-nlp
     ├── feature/naive-bayes
     ├── feature/information-extraction
     ├── feature/danger-scoring
     ├── feature/source-credibility
     ├── feature/regional-tracking
     └── feature/event-resolution
```

Do not develop directly on `main`.

------------------------------------------------------------------------

# 20. GitHub Workflow

``` text
GitHub Issue
      ↓
Feature branch
      ↓
Development
      ↓
Testing
      ↓
Commit
      ↓
Push
      ↓
Pull Request
      ↓
Code Review
      ↓
Merge into develop
      ↓
Integration Testing
      ↓
Release into main
```

Example commits:

``` text
feat: add Amharic danger classifier
feat: extract publication and event dates
feat: add 100km proximity service
feat: add 14-day notification filter
feat: add danger location extraction
fix: handle negated flood statements
fix: prevent duplicate danger notifications
feat: add regional danger scoring
```

------------------------------------------------------------------------

# 21. Recommended Repository Structure

``` text
HuluSafe/
│
├── frontend/
│   └── lib/
│       ├── screens/
│       ├── widgets/
│       ├── models/
│       ├── services/
│       ├── providers/
│       └── utils/
│
├── backend/
│   └── app/
│       ├── api/
│       ├── models/
│       ├── schemas/
│       ├── services/
│       ├── database/
│       ├── jobs/
│       └── main.py
│
├── ai/
│   ├── dataset/
│   ├── annotation/
│   ├── preprocessing/
│   ├── feature_extraction/
│   ├── models/
│   ├── training/
│   ├── information_extraction/
│   └── evaluation/
│
├── geographic_data/
│   ├── regions/
│   └── locations/
│
├── docs/
│   ├── architecture/
│   ├── api/
│   ├── methodology/
│   └── research/
│
├── tests/
│
├── docker/
│
└── README.md
```

------------------------------------------------------------------------

# 22. Development Timeline

## Phase 1 --- Requirements & Architecture



**All students**

-   Finalize requirements.
-   Define danger categories.
-   Define 100 km policy.
-   Define 14-day notification policy.
-   Define severity thresholds.
-   Define confidence thresholds.
-   Define publication/event time rules.
-   Design database.
-   Design UI.
-   Define API.
-   Define AI pipeline.
-   Identify candidate Amharic sources.
-   Define source credibility methodology.
-   Create GitHub repository.

### Deliverable

**System Requirements + Architecture Document**

------------------------------------------------------------------------

# 23. Phase 2 --- Foundation


### Student 1

-   Flutter foundation.
-   Dashboard.
-   Authentication screens.
-   Personalized user profile UI.
-   Location permission.
-   Settings.

### Student 2

-   Map.
-   Search.
-   Danger details UI.

### Student 3

-   PostgreSQL.
-   FastAPI.
-   Authentication integration.
-   User/profile data.
-   News ingestion.
-   Source registry.
-   Timestamp storage.

### Student 4

-   Amharic dataset.
-   Annotation.
-   Preprocessing.
-   Danger vocabulary.

### Student 5

-   Severity methodology.
-   Confidence methodology.
-   Source weighting.
-   Event clustering design.
-   Regional aggregation design.

------------------------------------------------------------------------

# 24. Phase 3 --- MVP



Build a working system before advanced AI.

``` text
Amharic News
     ↓
Basic AI danger detection
     ↓
Danger location
     ↓
Event time
     ↓
Database
     ↓
User location
     ↓
100 km calculation
     ↓
14-day filter
     ↓
Notification
```

### MVP Goal

A user should be able to receive a basic location-aware danger warning
from a recent Amharic news report and see:

``` text
Danger type
Danger location
Distance
News publication time
Event time
Danger level
Confidence
Source
```

------------------------------------------------------------------------

# 25. Phase 4 --- AI Integration



### Student 4

``` text
Dataset
 ↓
Amharic preprocessing
 ↓
TF-IDF
 ↓
Naive Bayes
 ↓
Negation/context
 ↓
Information extraction
 ↓
Evaluation
```

### Student 5

``` text
AI output
 ↓
Severity
 ↓
Credibility
 ↓
Multi-source confidence
 ↓
Event resolution
 ↓
Regional aggregation
 ↓
Trend
```

------------------------------------------------------------------------

# 26. Phase 5 --- Full Integration



``` text
News
 ↓
Backend
 ↓
Amharic AI
 ↓
Information extraction
 ↓
Event resolution
 ↓
Danger intelligence
 ↓
Database
 ↓
API
 ↓
Flutter
 ↓
100 km
 ↓
14-day filter
 ↓
Notification
```

------------------------------------------------------------------------

# 27. Phase 6 --- Testing



## AI Testing

Test:

-   Accuracy.
-   Precision.
-   Recall.
-   F1-score.
-   Confusion matrix.
-   False positives.
-   False negatives.
-   Negation.
-   Historical articles.
-   Hypothetical articles.
-   Relative dates.
-   Multiple danger types.
-   Unknown information.

## Backend Testing

Test:

-   News collection.
-   Duplicate articles.
-   Database.
-   API.
-   Publication time.
-   Event time.
-   14-day filtering.
-   Location extraction.
-   Distance calculation.
-   100 km filtering.
-   Notification deduplication.
-   Source aggregation.

## Frontend Testing

Test:

-   Location permission.
-   Dashboard.
-   Map.
-   Search.
-   Notifications.
-   Alert details.
-   Time display.
-   Offline/error states.

------------------------------------------------------------------------

# 28. Critical False-Alarm Tests

## Test 1 --- Current Danger

``` text
Article reports an active flood.
→ Danger = TRUE
→ Type = FLOOD
→ Current/active = TRUE
→ Eligible for further alert checks
```

## Test 2 --- Negation

``` text
Article states that there is no flood.
→ Flood term detected
→ Negation detected
→ No active flood alert
```

## Test 3 --- Historical Event

``` text
Article discusses a flood from 20 days ago.
→ Historical
→ No notification
```

## Test 4 --- Recent Historical Event

``` text
Article discusses a flood from 5 days ago,
but the article clearly indicates the event has ended.
→ No active warning
```

## Test 5 --- Ongoing Event

``` text
Article published several days ago
but states that the danger is still ongoing.
→ Evaluate current event status
→ Continue alert evaluation if event remains within policy
```

## Test 6 --- Old Event

``` text
Event occurred 15 days ago.
→ Notification prohibited
```

## Test 7 --- Unknown Event Time

``` text
Article reports danger but event time cannot be reliably established.
→ Mark event time as unknown
→ Apply documented conservative notification policy
```

## Test 8 --- Unknown Location

``` text
Danger detected but location cannot be reliably identified.
→ Do not invent coordinates
→ No location-specific 100 km alert
```

## Test 9 --- Copied Reports

``` text
Three websites repeat the same original report.
→ Cluster as one event
→ Do not automatically count as three independent confirmations
```

------------------------------------------------------------------------

# 29. Responsible Alert Logic

The final system should NOT use:

``` text
Danger keyword found
        ↓
SEND ALERT
```

Instead:

``` text
Danger evidence
      ↓
Naive Bayes classification
      ↓
Negation/context verification
      ↓
Event information extraction
      ↓
Danger location
      ↓
Event-time verification
      ↓
Current/active status
      ↓
Source credibility
      ↓
Independent-source confirmation
      ↓
Severity
      ↓
Confidence
      ↓
Event age ≤ 14 days?
      ↓
User distance ≤ 100 km?
      ↓
Alert threshold?
      ↓
Duplicate alert?
      ↓
SEND NOTIFICATION
```

------------------------------------------------------------------------

# 30. Final Alert Decision Formula

Conceptually:

``` text
ALERT =
    ACTIVE_EVENT
    AND
    EVENT_AGE <= 14 DAYS
    AND
    DISTANCE <= 100 KM
    AND
    SEVERITY >= ALERT_THRESHOLD
    AND
    CONFIDENCE >= CONFIDENCE_THRESHOLD
    AND
    LOCATION_CONFIDENCE >= LOCATION_THRESHOLD
    AND
    NOT_ALREADY_NOTIFIED
```

All thresholds should be configurable.

------------------------------------------------------------------------

# 31. Fair Workload Distribution

## Student 1 --- Flutter Dashboard

Owns:

-   Flutter architecture.
-   Dashboard.
-   Location permission.
-   Settings.
-   Navigation.
-   Dashboard testing.

## Student 2 --- Flutter Map & Alerts

Owns:

-   Ethiopia danger map.
-   Text-based location search.
-   Interactive map location selection.
-   Danger details.
-   Push notifications.
-   Alert history.
-   Frontend integration.

## Student 3 --- Backend & Data

Owns:

-   News collection.
-   Database.
-   Source registry.
-   REST API.
-   Publication/event time.
-   14-day filter.
-   Location matching.
-   100 km service.
-   Notification backend.

## Student 4 --- Amharic AI/NLP

Owns:

-   Dataset.
-   Annotation.
-   Amharic preprocessing.
-   Danger vocabulary.
-   Naive Bayes.
-   Negation/context.
-   Information extraction.
-   Time/location extraction.
-   Model evaluation.

## Student 5 --- Danger Intelligence

Owns:

-   Severity.
-   Source credibility.
-   Confidence.
-   Multi-source aggregation.
-   Event clustering.
-   Regional tracking.
-   Danger trends.
-   Alert eligibility.

------------------------------------------------------------------------

# 32. Shared Responsibilities

All five students should participate in:

-   Requirements analysis.
-   GitHub issue management.
-   Code review.
-   Documentation.
-   Testing.
-   Final integration.
-   Presentation.
-   Demonstration.

Weekly meeting:

``` text
1. What did I complete?
2. What am I working on?
3. What is blocked?
4. What do I need from another member?
5. What will I complete next?
```

------------------------------------------------------------------------

# 33. Definition of Done

A feature is complete only when:

``` text
Code written
   ↓
Unit tested
   ↓
Documented
   ↓
Pushed to GitHub
   ↓
Pull request
   ↓
Code review
   ↓
Merged
   ↓
Integrated
   ↓
End-to-end tested
```

------------------------------------------------------------------------

# 34. Final Demonstration Scenario

Demonstrate one complete workflow:

``` text
1. User opens HuluSafe
        ↓
2. User grants location permission
        ↓
3. App obtains user location
        ↓
4. Backend collects recent Amharic news
        ↓
5. AI preprocesses the article
        ↓
6. Naive Bayes detects danger
        ↓
7. Negation/context is checked
        ↓
8. Danger type is extracted
        ↓
9. Danger location is extracted
        ↓
10. Event time is extracted
        ↓
11. Deaths/displacement/injuries/damage are extracted
        ↓
12. Publication time is stored
        ↓
13. Related articles are clustered
        ↓
14. Source credibility is evaluated
        ↓
15. Severity + confidence calculated
        ↓
16. Regional danger updated
        ↓
17. User-to-danger distance calculated
        ↓
18. Example distance = 78 km
        ↓
19. Event age = 2 days
        ↓
20. 2 days ≤ 14 days
        ↓
21. Alert thresholds satisfied
        ↓
22. User has not already been notified
        ↓
23. Push notification sent
        ↓
24. User opens notification
        ↓
25. App shows:

Danger: FLOOD
Danger location: Location X
Distance: 78 km
Level: HIGH
Confidence: 88%

News published:
27 Aug 2026, 14:30

Event time:
27 Aug 2026, 13:50

Deaths: XX
Displaced: XX
Sources: 3 credible independent reports
Trend: ↑ Increasing
        ↓
26. User views event on map
```

------------------------------------------------------------------------

# 36. Reference Media & User Verification

Whenever HuluSafe reports a danger event, it must identify the **reference
media/source(s)** from which the information was obtained. The danger report
should show, where available:

- Media/source name.
- Original article title.
- Original article URL.
- News publication date and time.
- Event time when available.
- Source credibility score/category.
- Number of credible independent sources reporting the event.
- Last update time when available.

### Methodology

``` text
Danger event
     ↓
Reference source(s) identified
     ↓
Display source information
     ↓
User can open original report
     ↓
User is encouraged to further investigate
```

HuluSafe should explicitly recommend that users review the referenced media
and other reliable information, especially for high-impact, rapidly changing,
or lower-confidence situations.

Example: 

``` text
⚠️ Verification Recommendation

This warning is based on reports from 3 credible independent media sources.
Please review the referenced reports and other reliable information to
further investigate the situation before making important decisions.

[View Reference Sources]
```

The user's independent investigation must **not** be treated as a replacement
for the system's confidence calculation. System confidence should be based on
NLP evidence, source credibility, independent-source agreement, location
confidence, and recency.

### Student Responsibilities

**Student 3** stores source/article metadata and exposes it through the API.

**Student 5** evaluates source credibility, independent-source agreement, and
confidence.

**Student 2** displays the references and verification recommendation in the
frontend.

------------------------------------------------------------------------

# 37. Authentication & Personalized Information

Authentication is a **core HuluSafe feature** because it enables personalized
information and user-specific functionality.

Recommended authentication: **Firebase Authentication**.

An authenticated user can have: 

- Personalized dashboard information.
- Current location association when permission is granted.
- Saved/favorite locations.
- Notification preferences.
- Alert history.
- Previously viewed danger events.
- User-specific notification status.

Location permission and authentication are separate. A device may provide GPS
location after permission is granted, but authentication allows HuluSafe to
associate preferences and personalized information with the correct user.

### Authentication Flow

``` text
User
 ↓
Sign up / Sign in
 ↓
Firebase Authentication
 ↓
Authenticated user ID
 ↓
User profile + preferences
 ↓
Location permission
 ↓
Personalized dashboard
 ↓
Personalized danger information
 ↓
Personalized notifications
```

Guest access may be considered for limited public information, but **full
personalized HuluSafe functionality requires authentication**.

### Student Responsibilities

- **Student 1:** Login, registration, logout, profile and personalized UI.
- **Student 3:** Authentication integration, user records, authorization and
  user-specific APIs.
- **Student 2:** Personalized map/search/alert presentation and alert history.

No student should implement a separate authentication mechanism.

------------------------------------------------------------------------

# 38. Search & Map Location Selection

HuluSafe must support both **text-based location search** and **interactive map
selection**.

### Method 1 --- Type a Location

``` text
User types: Mekelle
        ↓
Location resolver
        ↓
Mekelle coordinates
        ↓
Danger events around selected location
```

### Method 2 --- Select on Map

``` text
User opens Ethiopia map
        ↓
Moves/interacts with map
        ↓
Selects a location
        ↓
Coordinates obtained
        ↓
Danger events around selected location
```

The selected location should be clearly marked on the map. Search/map queries
may be used to investigate a location even when it is not the user's current
location.

The 100 km proximity analysis should use the selected location as the center
for search results when appropriate.

------------------------------------------------------------------------

# 39. Optional Information Policy

HuluSafe must not require every news article to contain every possible danger
impact field. Real news reports vary in the amount of information they provide.

### Core information

The danger event should attempt to contain:

- Danger type.
- Danger location.
- Source.
- Publication time.
- Event time when available.
- Event status.
- Danger level.
- Confidence.

### Optional but highly recommended when reported

- Deaths.
- Injuries.
- Displaced people.
- Missing people.
- Damage.
- `created_at`.
- `updated_at`.

``` text
Information explicitly stated in article?
              ↓
            YES → Extract and store
              ↓
             NO → NULL / UNKNOWN
```

Missing information must never prevent an otherwise valid danger event from
being processed.

------------------------------------------------------------------------

# 40. Cross-Team Alignment & Merge-Conflict Prevention

Every student's task must remain aligned with the overall HuluSafe architecture
and with the other four students' tasks. The team must work as **one integrated
system**, not five independent projects merged at the end.

Before major implementation, all five students must jointly agree on:

- System architecture.
- Technology stack.
- Database schema.
- API endpoints and JSON formats.
- AI input/output format.
- Authentication method.
- Location and coordinate format.
- Time definitions.
- Danger categories.
- Severity levels.
- Confidence calculation.
- Source credibility methodology.
- Shared naming conventions.
- Repository structure.

These decisions should be documented in `docs/architecture/` and `docs/api/`.

### Shared Data Contract

All components should use the same danger-event structure. For example:

``` json
{
  "event_id": "EVT-001",
  "danger_type": "flood",
  "danger_level": "high",
  "confidence": 0.88,
  "location": {
    "name": "Example Location",
    "region": "Example Region",
    "latitude": 0.0,
    "longitude": 0.0
  },
  "event_time": "2026-08-27T13:50:00",
  "published_at": "2026-08-27T14:30:00",
  "status": "active",
  "deaths": 12,
  "injuries": null,
  "displaced": 350,
  "missing": null,
  "damage": null,
  "sources": []
}
```

The exact schema must be finalized jointly before integration.

### Dependency Alignment

``` text
Student 4: Amharic NLP
        ↓
Agreed AI output
        ↓
Student 5: Danger Intelligence
        ↓
Agreed danger assessment
        ↓
Student 3: Backend/API/Database
        ↓
Agreed API response
        ↓
Students 1 & 2: Flutter
```

Students must not independently change shared interfaces without discussing the
change with affected teammates.

### File Ownership

Where possible, students should work in separate areas of the repository:

``` text
Student 1 → frontend/dashboard and shared Flutter foundation
Student 2 → frontend/map, search and notifications
Student 3 → backend and database
Student 4 → ai/preprocessing, models and information extraction
Student 5 → danger intelligence, scoring and regional tracking
```

Shared files should be changed only through team coordination.

### Pull Request Checklist

Before merging any branch:

``` text
□ Follows agreed architecture
□ Uses agreed technology
□ Uses shared data model
□ Follows API contract
□ Does not unnecessarily modify another student's files
□ Unit tested
□ Existing features still work
□ Reviewed by another team member
□ Integration tested
```

### Integration Rule

No student's feature is considered complete merely because it works on their
branch. It is complete only after it has been successfully integrated and tested
with the components it depends on.

### Weekly Integration Meeting

All students should report:

1. What was completed.
2. What is currently being developed.
3. What is blocked.
4. Which teammate dependencies are required.
5. Which shared interfaces changed.
6. What will be integrated next.

------------------------------------------------------------------------

# 41. Updated End-to-End Personalized Warning Flow

``` text
Authenticated User
        ↓
Personal preferences + location permission
        ↓
Approved Amharic news sources
        ↓
News collection
        ↓
Amharic preprocessing
        ↓
Naive Bayes danger classification
        ↓
Negation/context analysis
        ↓
Information extraction
        ↓
Location + time + optional impact information
        ↓
Event resolution
        ↓
Source credibility + independent-source agreement
        ↓
Severity + confidence
        ↓
Regional danger tracking
        ↓
User/search-selected location
        ↓
100 km distance check
        ↓
14-day event eligibility check
        ↓
Alert threshold + duplicate check
        ↓
Personalized notification
        ↓
Danger details + reference media
        ↓
User verification recommendation
```

------------------------------------------------------------------------

# 35. Final Project Objective

HuluSafe transforms:

``` text
Amharic News
      ↓
AI Understanding
      ↓
Danger Detection
      ↓
Negation / Context Analysis
      ↓
Information Extraction
      ↓
Location + Time Identification
      ↓
Impact Extraction
      ↓
Source Credibility
      ↓
Multi-source Confirmation
      ↓
Severity + Confidence
      ↓
Regional Danger Tracking
      ↓
100 km Proximity Analysis
      ↓
14-Day Notification Filter
      ↓
Personalized User Evaluation
      ↓
Reference Media + Verification Recommendation
      ↓
Personalized Warning
```

## Core Principle

> **HuluSafe should not simply search for dangerous words. It should
> extract reported danger events and their associated information directly
> from Amharic news, determine whether the information refers to a current
> or relevant event, evaluate source credibility and independent evidence,
> calculate danger severity and confidence, track the event geographically
> and over time, and provide a personalized location-aware warning when an
> eligible danger is approximately within 100 km of the user. Every warning
> should identify its reference media and encourage the user to further
> investigate the situation. Missing optional information must never be
> invented or treated as a reason to reject a valid danger event.**

## Important Time Principle

> **Every warning must show the news publication time and, when
> available, the actual event time. HuluSafe must not send a
> notification for a danger whose occurrence is more than 14 days old.
> Historical information may remain available for search and analysis,
> but it must be clearly labeled and must not create an old-danger
> notification.**

## Recommended Development Principle

> **Build the simple MVP first, validate it with real Amharic news, then
> progressively add more advanced NLP, information extraction, source
> aggregation, severity scoring, and regional intelligence.**
