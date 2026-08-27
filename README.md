# MedicoAI

A Flask-based medical chatbot ("Meddy") that collects symptoms through a
conversational interface and predicts a possible disease using a PyTorch NLP
model and a scikit-learn classifier.

> **Disclaimer:** This application is a machine-learning demonstration only.
> It is not a medical device and its predictions are not medical advice.
> Always consult a qualified healthcare professional.

## Features

- Conversational symptom collection with autocomplete suggestions
- Symptom recognition via a trained PyTorch bag-of-words model
- Disease prediction from a scikit-learn classifier
- Per-session conversation state (no shared global state)
- Disease description and precaution lookup from bundled datasets
- Severity-based warning suggesting a doctor visit for severe symptoms
- Typing indicator, message timestamps, and mobile-friendly layout
- JSON API plus a browsable chat interface
- Automated test suite

## Requirements

- Python 3.9+
- Flask, PyTorch, NLTK, NumPy, scikit-learn, pandas, matplotlib

## Setup

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv venv
venv/Scripts/activate          # Windows
# source venv/bin/activate     # Linux/macOS

pip install -r requirements.txt
```

The NLTK tokenizer needs the `punkt` data package:

```bash
python -c "import nltk; nltk.download('punkt')"
```

## Running

```bash
flask --app app run
```

Open http://127.0.0.1:5000/ in your browser.

## Usage

1. Describe one symptom at a time (e.g., "I have a headache").
2. Keep adding symptoms until you are done.
3. Type **done** or click the **Done** button to receive a prediction,
   description, and precautions.

## API

| Method | Path              | Description                                  |
| ------ | ----------------- | -------------------------------------------- |
| GET    | `/`               | Chat interface (resets conversation)         |
| GET    | `/health`         | Liveness probe                               |
| GET    | `/api/symptoms`   | List of symptoms for autocomplete            |
| GET    | `/api/model`      | Model metadata                               |
| GET    | `/api/conversation` | Symptoms collected in this session         |
| POST   | `/api/reset`      | Clear the current session's symptoms         |
| POST   | `/symptom`        | Send a message; returns the chatbot reply    |

`POST /symptom` accepts a JSON body:

```json
{ "sentence": "I have a headache" }
```

and responds with:

```json
{ "response": "Hmm, I'm 95.00% sure this is headache." }
```

## Configuration

Configuration is read from environment variables; see `.env.example` for the
full list. Notable settings:

- `FLASK_SECRET_KEY` - secret used for signed session cookies
- `SYMPTOM_CONFIDENCE_THRESHOLD` - minimum confidence to accept a symptom
- `MAX_SYMPTOMS_PER_SESSION` - cap on collected symptoms

## Testing

```bash
pytest
```

The suite covers route handling, input validation, conversation flow,
session isolation, and the model/data layers.

## Project structure

```
app.py               # entry point
medico/              # application package
  __init__.py        # app factory, error handlers, logging
  config.py          # environment-driven settings
  data.py            # dataset loading
  models.py          # PyTorch and scikit-learn wrappers
  routes.py          # HTTP endpoints
  service.py         # conversation and prediction logic
nnet.py              # neural network architecture
nltk_utils.py        # tokenization helpers
data/                # symptom and disease datasets
models/              # trained model artifacts
static/              # CSS, JS, images
templates/           # HTML templates
tests/               # pytest suite
```
