"""
Pickup API Test
---------------
Validates pickup creation + tracking ID generation.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_pickup():
    response = client.post(
        "/pickup/",
        json={
            "sender": "Alice",
            "receiver": "Bob",
            "address": "Delhi HQ"
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert data["success"] is True
    assert "PKP-" in data["tracking_id"]
    assert data["sender"] == "Alice"