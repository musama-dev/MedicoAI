"""Loading and normalization of the medical datasets used by the chatbot."""

import pickle
from pathlib import Path

import pandas as pd

from .config import Config


def _normalize(value):
    """Lowercase and strip whitespace from a string value."""
    if isinstance(value, str):
        return value.lower().strip()
    return value


class SymptomData:
    """Bundle of symptom and disease metadata loaded from disk."""

    def __init__(self, config=None):
        config = config or Config
        base = config.BASE_DIR

        self.symptoms_list = self._load_pickle(base / config.SYMPTOM_LIST_FILE)

        self.descriptions = pd.read_csv(base / config.SYMPTOM_DESCRIPTION_FILE)
        self.descriptions["Disease"] = self.descriptions["Disease"].apply(
            _normalize
        )

        self.precautions = pd.read_csv(base / config.SYMPTOM_PRECAUTION_FILE)
        self.precautions["Disease"] = self.precautions["Disease"].apply(
            _normalize
        )

        severity = pd.read_csv(base / config.SYMPTOM_SEVERITY_FILE)
        severity = severity.map(
            lambda value: value.lower().strip().replace(" ", "")
            if isinstance(value, str)
            else value
        )
        self.severity = severity

        self.suggested_symptoms = self._load_suggested_symptoms(
            base / config.SUGGESTED_SYMPTOMS_FILE
        )

    @staticmethod
    def _load_pickle(path):
        with open(path, "rb") as handle:
            return pickle.load(handle)

    @staticmethod
    def _load_suggested_symptoms(path):
        """Read the autocomplete symptom list, cleaning raw lines."""
        with open(path, "r", encoding="utf-8") as handle:
            lines = handle.readlines()
        return [
            line.replace("'", "").replace("_", " ").replace(",\n", "")
            for line in lines
        ]
