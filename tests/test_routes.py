from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home_returns_200() -> None:
    response = client.get("/")
    assert response.status_code == 200


def test_success_demo_returns_200() -> None:
    response = client.get("/success", params={"demo": "true"})
    assert response.status_code == 200


def test_cancel_returns_200() -> None:
    response = client.get("/cancel")
    assert response.status_code == 200
