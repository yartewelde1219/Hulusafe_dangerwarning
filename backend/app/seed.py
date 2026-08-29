from datetime import datetime, timedelta, timezone
import json
from pathlib import Path

from sqlalchemy.orm import Session

from app.models.entities import DangerEvent, EventSource, News, Region, Source

ROOT = Path(__file__).resolve().parents[2]


def seed_if_empty(db: Session) -> None:
    if db.query(Source).first():
        return

    sources = [
        Source(
            name="Ethiopian News Agency",
            country="Ethiopia",
            language="am",
            source_type="national",
            credibility_score=0.90,
            collection_method="rss",
            url="https://www.ena.et/feed/",
            active=True,
        ),
        Source(
            name="Fana Broadcasting Corporate",
            country="Ethiopia",
            language="am",
            source_type="national",
            credibility_score=0.88,
            collection_method="rss",
            url="https://www.fanabc.com/feed/",
            active=True,
        ),
        Source(
            name="Deutsche Welle Amharic",
            country="Germany",
            language="am",
            source_type="international",
            credibility_score=0.92,
            collection_method="rss",
            url="https://rss.dw.com/rdf/rss-amh-news",
            active=True,
        ),
        Source(
            name="BBC News Amharic",
            country="United Kingdom",
            language="am",
            source_type="international",
            credibility_score=0.94,
            collection_method="rss",
            url="https://feeds.bbci.co.uk/amharic/rss.xml",
            active=True,
        ),
    ]
    db.add_all(sources)
    db.flush()

    geo_path = ROOT / "geographic_data" / "regions" / "ethiopia_regions.json"
    if geo_path.exists():
        regions = json.loads(geo_path.read_text(encoding="utf-8"))
        for item in regions:
            db.add(
                Region(
                    region_name=item["region_name"],
                    latitude=item["latitude"],
                    longitude=item["longitude"],
                    danger_type=item.get("danger_type", "none"),
                    danger_level=item.get("danger_level", "none"),
                    confidence=item.get("confidence", 0.0),
                )
            )

    now = datetime.now(timezone.utc).replace(tzinfo=None)

    # Event 1: Active Flood in Awash (Afar) - 2 days ago
    pub_1 = now - timedelta(days=2, hours=2)
    evt_time_1 = now - timedelta(days=2, hours=3)
    art_1a = News(
        title="በአዋሽ አካባቢ የጎርፍ አደጋ ተከስቶ 12 ሰዎች ሲሞቱ 350 ሰዎች ተፈናቀሉ",
        content="በአዋሽ ወንዝ ሙላት ምክንያት በአካባቢው የጎርፍ አደጋ ተከስቷል። 12 ሰዎች ሲሞቱ 350 ሰዎች ተፈናቅለዋል።",
        source_id=sources[0].id,
        url="https://www.ena.et/sample-flood-awash-1",
        language="am",
        published_at=pub_1,
        raw_location_text="Awash",
    )
    art_1b = News(
        title="Awash flood displaces hundreds and damages property",
        content="Reports from local administration confirm 12 deaths and 350 displaced residents in Awash.",
        source_id=sources[2].id,
        url="https://www.dw.com/am/sample-flood-awash-2",
        language="am",
        published_at=pub_1 + timedelta(minutes=45),
        raw_location_text="Awash",
    )
    db.add_all([art_1a, art_1b])
    db.flush()

    evt_1 = DangerEvent(
        id="EVT-001",
        danger_type="flood",
        danger_level="high",
        confidence=0.88,
        location_name="Awash",
        region="Afar",
        latitude=8.9833,
        longitude=40.1667,
        location_confidence=0.95,
        event_time=evt_time_1,
        event_time_confidence="HIGH",
        status="active",
        deaths=12,
        injuries=None,
        displaced=350,
        missing=None,
        damage="መኖሪያ ቤቶች ፈረሱ",
        trend="increasing",
        severity_score=0.78,
        created_at=pub_1,
        updated_at=pub_1 + timedelta(minutes=45),
    )
    db.add(evt_1)
    db.add_all([
        EventSource(event_id=evt_1.id, news_id=art_1a.id, source_id=sources[0].id, source_credibility=0.90, independent_report=True, published_at=pub_1),
        EventSource(event_id=evt_1.id, news_id=art_1b.id, source_id=sources[2].id, source_credibility=0.92, independent_report=True, published_at=pub_1 + timedelta(minutes=45)),
    ])

    # Event 2: Active Fire in Merkato, Addis Ababa - 1 day ago
    pub_2 = now - timedelta(days=1, hours=5)
    evt_time_2 = now - timedelta(days=1, hours=6)
    art_2 = News(
        title="በአዲስ አበባ መርካቶ ገበያ የእሳት አደጋ ደረሰ",
        content="በመርካቶ በተነሳ እሳት 2 ሰዎች ሲቆስሉ 5 ሱቆች ተቃጥለዋል።",
        source_id=sources[1].id,
        url="https://www.fanabc.com/sample-fire-merkato",
        language="am",
        published_at=pub_2,
        raw_location_text="Addis Ababa",
    )
    db.add(art_2)
    db.flush()

    evt_2 = DangerEvent(
        id="EVT-002",
        danger_type="fire",
        danger_level="moderate",
        confidence=0.84,
        location_name="Addis Ababa",
        region="Addis Ababa",
        latitude=9.03,
        longitude=38.74,
        location_confidence=0.95,
        event_time=evt_time_2,
        event_time_confidence="HIGH",
        status="active",
        deaths=None,
        injuries=2,
        displaced=None,
        missing=None,
        damage="5 ሱቆች ተቃጥለዋል",
        trend="stable",
        severity_score=0.55,
        created_at=pub_2,
        updated_at=pub_2,
    )
    db.add(evt_2)
    db.add(EventSource(event_id=evt_2.id, news_id=art_2.id, source_id=sources[1].id, source_credibility=0.88, independent_report=True, published_at=pub_2))

    # Event 3: Landslide in Gofa (South Ethiopia) - 3 days ago
    pub_3 = now - timedelta(days=3)
    evt_time_3 = now - timedelta(days=3, hours=1)
    art_3 = News(
        title="በደቡብ ኢትዮጵያ በጎፋ ዞን ከባድ የመሬት መንሸራተት አደጋ አጋጠመ",
        content="በደረሰው የመሬት ናዳ 20 ሰዎች ሞተዋል፤ በርካቶች ተቀብረዋል።",
        source_id=sources[3].id,
        url="https://feeds.bbci.co.uk/amharic/sample-landslide-gofa",
        language="am",
        published_at=pub_3,
        raw_location_text="Arba Minch",
    )
    db.add(art_3)
    db.flush()

    evt_3 = DangerEvent(
        id="EVT-003",
        danger_type="landslide",
        danger_level="critical",
        confidence=0.92,
        location_name="Arba Minch",
        region="South Ethiopia",
        latitude=6.0333,
        longitude=37.55,
        location_confidence=0.90,
        event_time=evt_time_3,
        event_time_confidence="HIGH",
        status="active",
        deaths=20,
        injuries=None,
        displaced=None,
        missing=None,
        damage="መንገድ እና ቤቶች ተደረመሱ",
        trend="increasing",
        severity_score=0.88,
        created_at=pub_3,
        updated_at=pub_3,
    )
    db.add(evt_3)
    db.add(EventSource(event_id=evt_3.id, news_id=art_3.id, source_id=sources[3].id, source_credibility=0.94, independent_report=True, published_at=pub_3))

    # Event 4: Historical Event (> 14 days ago) - Prohibited from notifications
    pub_4 = now - timedelta(days=25)
    evt_time_4 = now - timedelta(days=26)
    art_4 = News(
        title="ባለፈው ወር በደብረ ማርቆስ የተከሰተው የጸጥታ ችግር",
        content="ከ25 ቀናት በፊት በደብረ ማርቆስ ግጭት ተከስቶ እንደነበር ይታወሳል።",
        source_id=sources[0].id,
        url="https://www.ena.et/sample-historical-debre-markos",
        language="am",
        published_at=pub_4,
        raw_location_text="Debre Markos",
    )
    db.add(art_4)
    db.flush()

    evt_4 = DangerEvent(
        id="EVT-004",
        danger_type="conflict",
        danger_level="high",
        confidence=0.85,
        location_name="Debre Markos",
        region="Amhara",
        latitude=10.33,
        longitude=37.73,
        location_confidence=0.90,
        event_time=evt_time_4,
        event_time_confidence="HIGH",
        status="historical",
        deaths=4,
        injuries=10,
        displaced=None,
        missing=None,
        damage=None,
        trend="decreasing",
        severity_score=0.72,
        created_at=pub_4,
        updated_at=pub_4,
    )
    db.add(evt_4)
    db.add(EventSource(event_id=evt_4.id, news_id=art_4.id, source_id=sources[0].id, source_credibility=0.90, independent_report=True, published_at=pub_4))

    # Event 5: Active Drought in Gode (Somali) - 5 days ago
    pub_5 = now - timedelta(days=5)
    evt_time_5 = now - timedelta(days=5, hours=4)
    art_5 = News(
        title="በሶማሌ ክልል በጎዴ ዞን ከባድ ድርቅ ተከስቷል",
        content="የዝናብ እጥረት በመከሰቱ ምክንያት የከብቶች ሞት እና የምግብ እጥረት አጋጥሟል።",
        source_id=sources[2].id,
        url="https://www.dw.com/am/sample-drought-gode",
        language="am",
        published_at=pub_5,
        raw_location_text="Gode",
    )
    db.add(art_5)
    db.flush()

    evt_5 = DangerEvent(
        id="EVT-005",
        danger_type="drought",
        danger_level="high",
        confidence=0.82,
        location_name="Gode",
        region="Somali",
        latitude=5.95,
        longitude=43.5833,
        location_confidence=0.90,
        event_time=evt_time_5,
        event_time_confidence="HIGH",
        status="active",
        deaths=None,
        injuries=None,
        displaced=None,
        missing=None,
        damage="የከብቶች ሞት",
        trend="stable",
        severity_score=0.68,
        created_at=pub_5,
        updated_at=pub_5,
    )
    db.add(evt_5)
    db.add(EventSource(event_id=evt_5.id, news_id=art_5.id, source_id=sources[2].id, source_credibility=0.92, independent_report=True, published_at=pub_5))

    db.commit()

