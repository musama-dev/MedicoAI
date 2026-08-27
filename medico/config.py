"""Centralized application configuration.

Settings are read from environment variables so the same codebase can run in
development, testing, and production without modification.
"""

import os
import secrets
from pathlib import Path


def _env_int(name, default):
    try:
        return int(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


def _env_float(name, default):
    try:
        return float(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


class Config:
    """Runtime configuration for the MedicoAI application."""

    BASE_DIR = Path(__file__).resolve().parent.parent

    # Model and data file locations (relative to the project root).
    MODEL_FILE = os.environ.get("MODEL_FILE", "models/data.pth")
    PREDICTION_MODEL_FILE = os.environ.get(
        "PREDICTION_MODEL_FILE", "models/fitted_model.pickle2"
    )
    SYMPTOM_LIST_FILE = os.environ.get(
        "SYMPTOM_LIST_FILE", "data/list_of_symptoms.pickle"
    )
    SYMPTOM_DESCRIPTION_FILE = os.environ.get(
        "SYMPTOM_DESCRIPTION_FILE", "data/symptom_Description.csv"
    )
    SYMPTOM_PRECAUTION_FILE = os.environ.get(
        "SYMPTOM_PRECAUTION_FILE", "data/symptom_precaution.csv"
    )
    SYMPTOM_SEVERITY_FILE = os.environ.get(
        "SYMPTOM_SEVERITY_FILE", "data/Symptom-severity.csv"
    )
    SUGGESTED_SYMPTOMS_FILE = os.environ.get(
        "SUGGESTED_SYMPTOMS_FILE", "static/assets/files/ds_symptoms.txt"
    )

    # Flask
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", secrets.token_hex(32))
    JSON_SORT_KEYS = False

    # Chatbot behavior
    SYMPTOM_CONFIDENCE_THRESHOLD = _env_float("SYMPTOM_CONFIDENCE_THRESHOLD", 0.5)
    MAX_MESSAGE_LENGTH = _env_int("MAX_MESSAGE_LENGTH", 200)
    MAX_SYMPTOMS_PER_SESSION = _env_int("MAX_SYMPTOMS_PER_SESSION", 20)

    # Severity thresholds that trigger the medical-severity warning.
    SEVERITY_MEAN_THRESHOLD = _env_float("SEVERITY_MEAN_THRESHOLD", 4)
    SEVERITY_MAX_THRESHOLD = _env_float("SEVERITY_MAX_THRESHOLD", 5)
