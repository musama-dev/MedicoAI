"""Core chatbot logic: symptom recognition and disease prediction."""

import random

import numpy as np

from .config import Config


class ChatService:
    """Holds the conversation state and prediction logic for one session."""

    DONE_COMMAND = "done"

    NO_SYMPTOM_RESPONSES = [
        "I can't know what disease you may have if you don't enter any symptoms :)",
        "Meddy can't know the disease if there are no symptoms...",
        "You first have to enter some symptoms!",
    ]

    UNRECOGNIZED_RESPONSE = "I'm sorry, but I don't understand you."

    def __init__(self, nlp_model, predictor, data, config=None):
        self.nlp_model = nlp_model
        self.predictor = predictor
        self.data = data
        self.config = config or Config
        self.user_symptoms = set()

    def reset(self):
        """Clear all symptoms collected in this conversation."""
        self.user_symptoms.clear()

    def is_done_command(self, sentence):
        """Return True when the user asked to finish entering symptoms."""
        cleaned = sentence.replace(".", "").replace("!", "").lower().strip()
        return cleaned == self.DONE_COMMAND

    def recognize_symptom(self, sentence):
        """Classify a sentence into a symptom; returns (symptom, confidence)."""
        return self.nlp_model.classify(sentence)

    def add_symptom(self, symptom):
        """Record a recognized symptom, ignoring duplicates."""
        self.user_symptoms.add(symptom)

    def symptom_vector(self):
        """Build the binary feature vector expected by the predictor."""
        return [
            1 if symptom in self.user_symptoms else 0
            for symptom in self.data.symptoms_list
        ]

    def _severity_scores(self):
        scores = []
        for symptom in self.user_symptoms:
            normalized = symptom.lower().strip().replace(" ", "")
            matches = self.data.severity.loc[
                self.data.severity["Symptom"] == normalized, "weight"
            ]
            if not matches.empty:
                scores.append(matches.iloc[0])
        return scores

    def is_severe(self):
        """Return True when symptom severity warrants a doctor warning."""
        scores = self._severity_scores()
        if not scores:
            return False
        return (
            np.mean(scores) > self.config.SEVERITY_MEAN_THRESHOLD
            or np.max(scores) > self.config.SEVERITY_MAX_THRESHOLD
        )

    def diagnose(self):
        """Predict a disease from collected symptoms and build the reply."""
        if not self.user_symptoms:
            return random.choice(self.NO_SYMPTOM_RESPONSES)

        vector = np.asarray(self.symptom_vector())
        disease = self.predictor.predict(vector)

        description = self.data.descriptions.loc[
            self.data.descriptions["Disease"] == disease.lower().strip(),
            "Description",
        ].iloc[0]

        precautions = self.data.precautions.loc[
            self.data.precautions["Disease"] == disease.lower().strip()
        ]
        precaution_text = ", ".join(
            [
                precautions.Precaution_1.iloc[0],
                precautions.Precaution_2.iloc[0],
                precautions.Precaution_3.iloc[0],
                precautions.Precaution_4.iloc[0],
            ]
        )

        reply = (
            f"It looks to me like you have {disease}. <br><br>"
            f"<i>Description: {description}</i><br><br>"
            f"<b>Precautions: {precaution_text}</b>"
        )

        if self.is_severe():
            reply += (
                "<br><br>Considering your symptoms are severe, and Meddy isn't "
                "a real doctor, you should consider talking to one. :)"
            )

        self.reset()
        return reply
