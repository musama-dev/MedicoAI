"""Integration tests that load the real datasets and models from disk."""

import numpy as np

from medico.data import SymptomData
from medico.models import NlpModel, DiseasePredictor


def test_symptom_data_loads_all_datasets():
    data = SymptomData()
    assert len(data.symptoms_list) > 0
    assert len(data.suggested_symptoms) > 0
    assert "Disease" in data.descriptions.columns
    assert "Disease" in data.precautions.columns
    assert "Symptom" in data.severity.columns


def test_nlp_model_classifies_known_symptom():
    model = NlpModel()
    tag, confidence = model.classify("headache")
    assert isinstance(tag, str)
    assert 0.0 <= confidence <= 1.0


def test_disease_predictor_returns_disease_name():
    predictor = DiseasePredictor()
    vector = np.zeros(len(SymptomData().symptoms_list))
    disease = predictor.predict(vector)
    assert isinstance(disease, str)
    assert len(disease) > 0


def test_model_metadata_is_populated():
    model = NlpModel()
    assert model.input_size > 0
    assert model.hidden_size > 0
    assert len(model.tags) > 0
    assert len(model.all_words) == model.input_size
