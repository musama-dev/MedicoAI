"""Unit tests for the ChatService using lightweight fakes."""

import numpy as np
import pytest

from medico.service import ChatService


class FakeNlp:
    def classify(self, sentence):
        return ("headache", 0.95)


class FakePredictor:
    def predict(self, vector):
        return "Migraine"


class FakeData:
    symptoms_list = ["headache", "fever", "cough"]
    severity = None


def make_service(**kwargs):
    defaults = dict(nlp_model=FakeNlp(), predictor=FakePredictor(), data=FakeData())
    defaults.update(kwargs)
    return ChatService(**defaults)


def test_done_command_detection():
    service = make_service()
    assert service.is_done_command("done")
    assert service.is_done_command("  Done.  ")
    assert not service.is_done_command("headache")


def test_recognize_symptom_returns_tag_and_confidence():
    service = make_service()
    tag, confidence = service.recognize_symptom("I have a headache")
    assert tag == "headache"
    assert confidence == 0.95


def test_add_symptom_ignores_duplicates():
    service = make_service()
    service.add_symptom("headache")
    service.add_symptom("headache")
    assert service.user_symptoms == {"headache"}


def test_symptom_vector_marks_present_symptoms():
    service = make_service()
    service.add_symptom("fever")
    vector = service.symptom_vector()
    assert vector == [0, 1, 0]


def test_diagnose_without_symptoms_returns_hint():
    service = make_service()
    reply = service.diagnose()
    assert "symptoms" in reply.lower()


def test_reset_clears_symptoms():
    service = make_service()
    service.add_symptom("cough")
    service.reset()
    assert service.user_symptoms == set()


@pytest.mark.parametrize(
    "scores,expected",
    [
        ([1, 2], False),
        ([5, 5], True),
        ([3, 3, 3], False),
    ],
)
def test_severity_thresholds(scores, expected):
    class FakeSeverity:
        pass

    data = FakeData()
    data.severity = None

    class FakeService(ChatService):
        def _severity_scores(self):
            return scores

    service = FakeService(nlp_model=FakeNlp(), predictor=FakePredictor(), data=data)
    assert service.is_severe() == expected
