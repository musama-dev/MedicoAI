"""Tests for baseline security headers and session handling."""


def test_security_headers_present(client):
    response = client.get("/health")
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "SAMEORIGIN"
    assert "Content-Security-Policy" in response.headers


def test_session_cookie_is_set(client):
    client.post("/symptom", json={"sentence": "done"})
    assert "session" in client.cookie_jar


def test_symptoms_are_stored_in_session(client):
    client.post("/symptom", json={"sentence": "I have a headache"})
    assert "session" in client.cookie_jar
