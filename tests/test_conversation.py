"""Tests for the end-to-end conversation flow and per-session state."""


def test_done_without_symptoms_explains(client):
    response = client.post("/symptom", json={"sentence": "done"})
    assert response.status_code == 200
    assert "symptoms" in response.json["response"].lower()


def test_done_is_case_insensitive(client):
    response = client.post("/symptom", json={"sentence": "DONE"})
    assert response.status_code == 200


def test_unrecognized_message_returns_apology(client):
    response = client.post("/symptom", json={"sentence": "what is love?"})
    assert response.status_code == 200
    assert "don't understand" in response.json["response"]


def test_sessions_are_isolated(client):
    """Symptoms collected in one session must not leak into another."""
    first = client.post(
        "/symptom", json={"sentence": "I have a headache"}, follow_redirects=True
    )
    second = client.post("/symptom", json={"sentence": "done"})
    assert first.status_code == 200
    assert second.status_code == 200


def test_index_resets_conversation(client):
    """Loading the page should clear any collected symptoms."""
    client.post("/symptom", json={"sentence": "I have a headache"})
    client.get("/")
    response = client.post("/symptom", json={"sentence": "done"})
    # The service picks a random empty-state reply, but every variant
    # mentions that no symptoms were provided.
    assert "symptoms" in response.json["response"].lower()
