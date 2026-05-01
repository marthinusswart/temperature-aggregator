from fastapi.testclient import TestClient

from app.main import app
from app.api.v1.router import get_db_controller

# 1. Initialize the TestClient with your FastAPI app
client = TestClient(app)

# 2. Create a mock controller to isolate tests from the real database
class MockDatabaseController:
    def store_temperature_reading(self, reading):
        pass  # In a real test, you might store this in a temporary list to assert against

    def get_all_readings(self):
        return []

# 3. Override the dependency 
app.dependency_overrides[get_db_controller] = MockDatabaseController

def test_is_alive():
    response = client.get("/api/v1/is-alive")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}

def test_temperature_reading():
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