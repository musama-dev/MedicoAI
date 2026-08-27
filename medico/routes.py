"""HTTP routes for the MedicoAI application."""

import json

from flask import Blueprint, jsonify, render_template, request, session

from .config import Config

bp = Blueprint("medico", __name__)


@bp.route("/")
def index():
    """Serve the chat interface and reset the conversation state."""
    service = _current_service()
    service.reset()
    data = _current_data()
    return render_template("index.html", data=json.dumps(data.suggested_symptoms))


@bp.route("/health")
def health():
    """Simple liveness probe for uptime monitors and load balancers."""
    return jsonify({"status": "ok"})


@bp.route("/api/model")
def model_info():
    """Expose model metadata for debugging and health checks."""
    from flask import current_app

    nlp = current_app.extensions["medico_nlp"]
    return jsonify(
        {
            "input_size": nlp.input_size,
            "hidden_size": nlp.hidden_size,
            "symptom_tags": len(nlp.tags),
            "vocabulary_size": len(nlp.all_words),
        }
    )


@bp.route("/api/conversation")
def conversation_state():
    """Return the symptoms collected so far in this session."""
    service = _current_service()
    return jsonify({"symptoms": sorted(service.user_symptoms)})


@bp.route("/api/reset", methods=["POST"])
def reset_conversation():
    """Clear all symptoms collected in this session."""
    service = _current_service()
    service.reset()
    _persist_service(service)
    return jsonify({"status": "reset"})


@bp.route("/api/symptoms")
def list_symptoms():
    """Return the full list of symptoms used for autocomplete."""
    data = _current_data()
    return jsonify({"symptoms": data.suggested_symptoms})


@bp.route("/symptom", methods=["POST"])
def predict_symptom():
    """Handle a single user message and return the chatbot reply."""
    payload = request.get_json(silent=True)
    if payload is None or not isinstance(payload, dict):
        return jsonify({"error": "Request body must be valid JSON."}), 400

    sentence = payload.get("sentence")
    if not isinstance(sentence, str) or not sentence.strip():
        return jsonify({"error": "The 'sentence' field must be a non-empty string."}), 400

    if len(sentence) > Config.MAX_MESSAGE_LENGTH:
        return (
            jsonify(
                {
                    "error": (
                        f"Message is too long. Maximum length is "
                        f"{Config.MAX_MESSAGE_LENGTH} characters."
                    )
                }
            ),
            400,
        )

    service = _current_service()
    response_text = _handle_message(service, sentence.strip())
    _persist_service(service)
    return jsonify({"response": response_text})


def _current_service():
    """Build a service whose symptoms are restored from the session."""
    from flask import current_app

    service = current_app.extensions["medico_service_factory"]()
    service.user_symptoms = set(session.get("symptoms", []))
    return service


def _persist_service(service):
    """Store the conversation's symptoms back into the session."""
    session["symptoms"] = sorted(service.user_symptoms)


def _current_data():
    from flask import current_app

    return current_app.extensions["medico_data"]


def _handle_message(service, sentence):
    """Route a user message through recognition or diagnosis."""
    if service.is_done_command(sentence):
        return service.diagnose()

    symptom, confidence = service.recognize_symptom(sentence)
    threshold = Config.SYMPTOM_CONFIDENCE_THRESHOLD
    if confidence > threshold:
        if len(service.user_symptoms) >= Config.MAX_SYMPTOMS_PER_SESSION:
            return (
                "You've already entered the maximum number of symptoms. "
                "Write 'done' to get your prediction."
            )
        service.add_symptom(symptom)
        return f"Hmm, I'm {confidence * 100:.2f}% sure this is {symptom}."
    return service.UNRECOGNIZED_RESPONSE
