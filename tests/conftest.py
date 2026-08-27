"""Shared pytest fixtures for the MedicoAI application."""

import pytest

from medico import create_app


@pytest.fixture(scope="session")
def app():
    """Build the application once for the whole test session."""
    return create_app()


@pytest.fixture()
def client(app):
    """Provide a fresh test client per test."""
    return app.test_client()
