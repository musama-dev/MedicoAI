"""Tests for the auxiliary API endpoints."""


def test_symptoms_endpoint_lists_symptoms(client):
    response = client.get("/api/symptoms")
    assert response.status_code == 200
    assert isinstance(response.json["symptoms"], list)
    assert len(response.json["symptoms"]) > 0


def test_model_endpoint_reports_metadata(client):
    response = client.get("/api/model")
    assert response.status_code == 200
    assert response.json["input_size"] > 0
    assert response.json["symptom_tags"] > 0


def test_conversation_state_starts_empty(client):
    response = client.get("/api/conversation")
    assert response.status_code == 200
    assert response.json["symptoms"] == []


def test_reset_endpoint_clears_symptoms(client):
    client.post("/symptom", json={"sentence": "I have a headache"})
    response = client.post("/api/reset")
    assert response.status_code == 200
    assert response.json["status"] == "reset"


def test_whitespace_padded_done_is_recognized(client):
    response = client.post("/symptom", json={"sentence": "  done  "})
    assert response.status_code == 200
    assert "symptoms" in response.json["response"].lower()
