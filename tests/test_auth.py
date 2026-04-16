"""
Auth API Integration Test
-------------------------
Validates user registration flow end-to-end.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_user_registration():
    response = client.post(
        "/auth/register",
        json={
            "name": "Abhishek",
            "email_addr": "test@example.com",
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert data["success"] is True
    assert data["user"]["email"] == "test@example.com"