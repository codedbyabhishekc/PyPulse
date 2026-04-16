"""
Tracking API Test
-----------------
Validates tracking lookup + status updates.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_tracking_flow():
    # Step 1: create pickup
    pickup = client.post(
        "/pickup/",
        json={
            "sender": "Alice",
            "receiver": "Bob",
            "address": "Delhi"
        }
    ).json()

    tracking_id = pickup["tracking_id"]

    # Step 2: fetch tracking
    response = client.post(
        "/tracking/",
        json={"tracking_id": tracking_id}
    )

    assert response.status_code == 200
    data = response.json()

    assert data["tracking_id"] == tracking_id
    assert data["status"] == "CREATED"