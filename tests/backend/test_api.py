import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database.base import Base
from app.database.session import get_db
from app.seed import seed_if_empty

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    seed_if_empty(db)
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["max_alert_event_age_days"] == 14
    assert data["default_alert_radius_km"] == 100.0


def test_regions_danger_endpoint():
    response = client.get("/regions/danger")
    assert response.status_code == 200
    data = response.json()
    assert "regions" in data
    assert len(data["regions"]) > 0


def test_dashboard_endpoint():
    response = client.get("/dashboard?lat=9.03&lon=38.74")
    assert response.status_code == 200
    data = response.json()
    assert "area_name" in data
    assert "nearby_dangers" in data
    assert "recent_alerts" in data


def test_nearby_dangers_endpoint():
    response = client.get("/nearby-dangers?lat=8.9833&lon=40.1667&radius_km=100")
    assert response.status_code == 200
    data = response.json()
    assert "events" in data
    event_ids = [e["event_id"] for e in data["events"]]
    assert "EVT-001" in event_ids


def test_search_endpoint():
    response = client.get("/search?lat=8.9833&lon=40.1667&q=Awash")
    assert response.status_code == 200
    data = response.json()
    assert len(data["events"]) > 0
    assert data["events"][0]["location"]["name"] == "Awash"


def test_get_event_detail_endpoint():
    response = client.get("/events/EVT-001")
    assert response.status_code == 200
    data = response.json()
    assert data["event_id"] == "EVT-001"
    assert data["danger_type"] == "flood"
    assert data["deaths"] == 12
    assert data["displaced"] == 350
    assert "sources" in data
    assert len(data["sources"]) > 0


def test_alert_history_endpoint():
    response = client.get("/alerts/history", headers={"Authorization": "Bearer sample-token"})
    assert response.status_code == 200
    data = response.json()
    assert data["authenticated"] is True
    assert "alerts" in data
