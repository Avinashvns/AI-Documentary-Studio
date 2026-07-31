from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_request_id_header():
    response = client.get("/")

    assert response.status_code == 200
    assert "X-Request-ID" in response.headers


def test_process_time_header():
    response = client.get("/")

    assert response.status_code == 200
    assert "X-Process-Time" in response.headers

    process_time = float(response.headers["X-Process-Time"])

    assert process_time >= 0


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["data"]["status"] == "healthy"


def test_version_endpoint():
    response = client.get("/version")

    assert response.status_code == 200

    body = response.json()

    assert "version" in body["data"]