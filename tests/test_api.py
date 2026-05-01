import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.api.v1.router import get_db_controller
from app.controller import MemoryDatabaseController

# 1. Initialize the TestClient with your FastAPI app
client = TestClient(app)

# 2. Isolate tests from the main application's database instance 
# by utilizing a dedicated in-memory controller for testing.
test_db_controller = MemoryDatabaseController()

def override_get_db_controller():
    return test_db_controller

# 3. Override the dependency 
app.dependency_overrides[get_db_controller] = override_get_db_controller

@pytest.fixture(autouse=True)
def clear_test_db():
    """Clears the test database before each test to ensure test isolation."""
    test_db_controller.memory_db.readings.clear()
    yield

def test_is_alive():
    response = client.get("/api/v1/is-alive")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}

def test_temperature_reading_with_timestamp():
    payload = {
        "componentId": "sensor-123",
        "temperature": 25.5,
        "timestamp": "1710000000000"
    }
    response = client.post("/api/v1/temperature-reading", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Temperature reading received"
    assert data["data"]["componentId"] == "sensor-123"
    assert data["data"]["timestamp"] == "1710000000000"

def test_temperature_reading_without_timestamp():
    payload = {
        "componentId": "sensor-124",
        "temperature": 26.0
    }
    response = client.post("/api/v1/temperature-reading", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Temperature reading received"
    assert data["data"]["componentId"] == "sensor-124"
    assert "timestamp" in data["data"]
    assert data["data"]["timestamp"] is not None

def test_get_grouped_temperature_readings():
    # Setup initial test data
    client.post("/api/v1/temperature-reading", json={"componentId": "sensor-1", "temperature": 20.0})
    client.post("/api/v1/temperature-reading", json={"componentId": "sensor-1", "temperature": 21.5})
    client.post("/api/v1/temperature-reading", json={"componentId": "sensor-2", "temperature": 22.0})

    response = client.get("/api/v1/temperature-readings")
    assert response.status_code == 200
    data = response.json()
    
    assert "sensor-1" in data
    assert "sensor-2" in data
    assert len(data["sensor-1"]) == 2
    assert len(data["sensor-2"]) == 1

def test_get_temperature_readings_by_component():
    # Setup initial test data
    client.post("/api/v1/temperature-reading", json={"componentId": "sensor-1", "temperature": 20.0})
    client.post("/api/v1/temperature-reading", json={"componentId": "sensor-2", "temperature": 22.0})

    response = client.get("/api/v1/temperature-readings/sensor-1")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 1
    assert data[0]["componentId"] == "sensor-1"

def test_get_latest_temperature_reading_by_component():
    # Insert readings out of chronological order to ensure sorting logic works correctly
    client.post("/api/v1/temperature-reading", json={"componentId": "sensor-1", "temperature": 20.0, "timestamp": "1700000000000"})
    client.post("/api/v1/temperature-reading", json={"componentId": "sensor-1", "temperature": 25.0, "timestamp": "1720000000000"})
    client.post("/api/v1/temperature-reading", json={"componentId": "sensor-1", "temperature": 21.0, "timestamp": "1710000000000"})

    response = client.get("/api/v1/temperature-readings/sensor-1/latest")
    assert response.status_code == 200
    data = response.json()
    
    assert data["componentId"] == "sensor-1"
    assert data["temperature"] == 25.0
    assert data["timestamp"] == "1720000000000"

def test_get_latest_temperature_reading_not_found():
    response = client.get("/api/v1/temperature-readings/unknown-sensor/latest")
    assert response.status_code == 404
    assert response.json() == {"detail": "No readings found for the specified component ID"}