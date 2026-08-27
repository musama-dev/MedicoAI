"""Loading and inference for the NLP and disease-prediction models."""

import pickle
from pathlib import Path

import numpy as np
import torch

from nnet import NeuralNet
from nltk_utils import bag_of_words
from .config import Config


class NlpModel:
    """Thin wrapper around the PyTorch symptom-classification model."""

    def __init__(self, path=None, device=None):
        if path is None:
            path = Config.BASE_DIR / Config.MODEL_FILE
        device = device or torch.device("cpu")
        checkpoint = torch.load(path, map_location=device)

        self.input_size = checkpoint["input_size"]
        self.hidden_size = checkpoint["hidden_size"]
        self.output_size = checkpoint["output_size"]
        self.all_words = checkpoint["all_words"]
        self.tags = checkpoint["tags"]

        self.model = NeuralNet(
            self.input_size, self.hidden_size, self.output_size
        ).to(device)
        self.model.load_state_dict(checkpoint["model_state"])
        self.model.eval()

    def classify(self, sentence):
        """Classify a tokenized sentence into a symptom tag with confidence."""
        tokenized = sentence
        features = bag_of_words(tokenized, self.all_words)
        features = features.reshape(1, features.shape[0])
        tensor = torch.from_numpy(features)

        with torch.no_grad():
            output = self.model(tensor)
            _, predicted = torch.max(output, dim=1)
            probabilities = torch.softmax(output, dim=1)
            confidence = probabilities[0][predicted.item()].item()

        return self.tags[predicted.item()], confidence


class DiseasePredictor:
    """Thin wrapper around the scikit-learn disease predictor."""

    def __init__(self, path=None):
        if path is None:
            path = Config.BASE_DIR / Config.PREDICTION_MODEL_FILE
        with open(path, "rb") as handle:
            self.model = pickle.load(handle)

    def predict(self, symptom_vector):
        """Predict a disease name from a binary symptom vector."""
        vector = np.asarray(symptom_vector).reshape(1, -1)
        return self.model.predict(vector)[0]


def load_models(config=None):
    """Load both models using paths from the given configuration."""
    config = config or Config
    base = config.BASE_DIR
    nlp = NlpModel(base / config.MODEL_FILE)
    predictor = DiseasePredictor(base / config.PREDICTION_MODEL_FILE)
    return nlp, predictor
