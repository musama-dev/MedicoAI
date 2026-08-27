"""MedicoAI application package."""

import json
import logging

from flask import Flask

from .config import Config
from .data import SymptomData
from .models import load_models
from .service import ChatService
from . import routes


def create_app(config=None):
    """Application factory: build and configure a MedicoAI Flask app."""
    config = config or Config
    app = Flask(__name__)
    app.config.from_object(config)

    # Load datasets and models once so every request reuses them.
    data = SymptomData(config)
    nlp_model, predictor = load_models(config)
    app.extensions["medico_data"] = data
    app.extensions["medico_nlp"] = nlp_model
    app.extensions["medico_predictor"] = predictor

    def _make_service():
        return ChatService(nlp_model, predictor, data, config)

    app.extensions["medico_service_factory"] = _make_service
    app.json.ensure_ascii = False

    app.register_blueprint(routes.bp)

    _configure_logging(app)
    return app


def _configure_logging(app):
    """Set up request-scoped logging for the application."""
    if not app.debug:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s %(name)s: %(message)s"
            )
        )
        app.logger.addHandler(handler)
        app.logger.setLevel(logging.INFO)
