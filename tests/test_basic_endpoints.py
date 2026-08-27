"""Tests for the index and health endpoints."""


def test_index_serves_chat_interface(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Medical Chatbot" in response.data


def test_index_includes_suggested_symptoms(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"symptoms" in response.data


def test_health_returns_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_unknown_route_returns_json_404(client):
    response = client.get("/does-not-exist")
    assert response.status_code == 404
    assert response.json["error"] == "Resource not found."
