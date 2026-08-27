"""MedicoAI application package."""

import json
import logging

from flask import Flask, jsonify, request

from .config import Config
from .data import SymptomData
from .models import load_models
from .service import ChatService
from . import routes


def create_app(config=None):
    """Application factory: build and configure a MedicoAI Flask app."""
    config = config or Config
    app = Flask(
        __name__,
        template_folder=str(config.BASE_DIR / "templates"),
        static_folder=str(config.BASE_DIR / "static"),
    )
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

    _register_error_handlers(app)
    _configure_logging(app)
    _register_request_logging(app)
    return app


def _register_request_logging(app):
    """Log every request with its duration and status code."""

    @app.before_request
    def _start_timer():
        from time import perf_counter

        request.environ["_request_start"] = perf_counter()

    @app.after_request
    def _log_request(response):
        from time import perf_counter

        started = request.environ.get("_request_start")
        if started is not None:
            duration_ms = (perf_counter() - started) * 1000
            app.logger.info(
                "%s %s -> %s (%.1fms)",
                request.method,
                request.path,
                response.status_code,
                duration_ms,
            )
        return response


def _register_error_handlers(app):
    """Return JSON errors for API-style requests."""

    def _json_error(message, status):
        response = jsonify({"error": message})
        response.status_code = status
        return response

    @app.errorhandler(400)
    def bad_request(error):
        return _json_error("Bad request.", 400)

    @app.errorhandler(404)
    def not_found(error):
        return _json_error("Resource not found.", 404)

    @app.errorhandler(405)
    def method_not_allowed(error):
        return _json_error("Method not allowed.", 405)

    @app.errorhandler(500)
    def internal_error(error):
        return _json_error("Internal server error.", 500)


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
