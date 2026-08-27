"""Shared pytest fixtures for the MedicoAI application."""

# Import torch before anything that pulls in sklearn/nltk. On Windows
# their bundled runtime DLLs conflict with torch's and break the import.
import torch  # noqa: F401

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
