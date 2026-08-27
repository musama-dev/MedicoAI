"""Tests for input validation on the /symptom endpoint."""


def test_missing_sentence_returns_400(client):
    response = client.post("/symptom", json={})
    assert response.status_code == 400
    assert "sentence" in response.json["error"]


def test_empty_sentence_returns_400(client):
    response = client.post("/symptom", json={"sentence": ""})
    assert response.status_code == 400


def test_whitespace_only_sentence_returns_400(client):
    response = client.post("/symptom", json={"sentence": "   "})
    assert response.status_code == 400


def test_non_string_sentence_returns_400(client):
    response = client.post("/symptom", json={"sentence": 12345})
    assert response.status_code == 400


def test_missing_body_returns_400(client):
    response = client.post("/symptom", data="not json", content_type="text/plain")
    assert response.status_code == 400


def test_get_method_not_allowed(client):
    response = client.get("/symptom")
    assert response.status_code == 405


def test_overlong_sentence_returns_400(client):
    response = client.post("/symptom", json={"sentence": "x" * 500})
    assert response.status_code == 400
    assert "too long" in response.json["error"]
