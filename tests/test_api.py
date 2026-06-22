import os
import tempfile
from fastapi.testclient import TestClient

os.environ["TICKET_DATA_FILE"] = tempfile.NamedTemporaryFile(delete=False).name

from app.main import app  # noqa: E402

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "AI-Powered" in response.json()["message"]


def test_create_ticket():
    payload = {"title": "Login issue", "description": "Production users are unable to login urgently", "created_by": "Pratik"}
    response = client.post("/tickets", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "Login Issue"
    assert data["priority"] == "High"
    assert data["status"] == "Open"
