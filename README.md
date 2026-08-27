<div align="center">

# 🩺 MedicoAI

**A conversational medical symptom checker — chat with *Meddy*, describe your symptoms, and get an ML-powered disease prediction with description and precautions.**

*Flask · PyTorch · scikit-learn*

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.x-EE4C2C?style=flat&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.2-F7931E?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Tests](https://img.shields.io/badge/Tests-pytest-6A9F58?style=flat&logo=pytest&logoColor=white)](#-testing)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=flat&logo=docker&logoColor=white)](#-docker)
[![License](https://img.shields.io/badge/License-MIT-1abc9c)](LICENSE)

</div>

---

> ⚠️ **Medical Disclaimer**
>
> MedicoAI is a **machine-learning demonstration**, not a medical device.
> Its predictions are statistical guesses based on a symptom dataset and
> **must never be treated as medical advice or a diagnosis**. Always consult
> a qualified healthcare professional for any health concern.

## ✨ Features

- 💬 **Conversational symptom collection** — describe symptoms in plain English, one message at a time
- 🧠 **Symptom recognition** — a trained PyTorch bag-of-words neural network maps free text to one of **131 known symptoms**, with a confidence score
- 🎯 **Disease prediction** — a scikit-learn classifier turns collected symptoms into a predicted condition
- 📚 **Knowledge lookup** — disease description and four precautions pulled from bundled datasets
- 🚨 **Severity warning** — when symptom severity crosses configured thresholds, Meddy recommends seeing a real doctor
- 🔁 **Per-session state** — conversation state lives in signed Flask sessions, so parallel users never see each other's symptoms
- ⌨️ **Polished chat UI** — autocomplete suggestions, typing indicator, message timestamps, mobile-friendly layout
- 🔌 **JSON API** — every capability is available programmatically, plus a `/health` liveness probe
- ✅ **Tested** — pytest suite covering routes, validation, conversation flow, session isolation, and the model/data layers
- 🐳 **Docker-ready** — ships with a slim, CPU-only Dockerfile

## 🧠 How It Works

```
 User message ("my head hurts")
        │
        ▼
 ┌─────────────────┐   tokenize (NLTK) → bag-of-words
 │  PyTorch NLP    │──────────────────────────────────────┐
 │  model (data.pth)│                                     │
 └─────────────────┘                                      ▼
        │  symptom tag + confidence                  ┌──────────────┐
        ▼                                            │  confidence  │
 [session: collect symptoms]  ◄── threshold ≥ 0.5 ──►│  ≥ 0.5?      │
        │                                            └──────────────┘
        │  user types "done"
        ▼
 ┌──────────────────────┐  binary symptom vector (1 × 131)
 │ scikit-learn         │────────────────────────────────────┐
 │ predictor (.pickle2) │                                    │
 └──────────────────────┘                                    ▼
        │                                            disease name
        ▼
 description + precautions (CSV lookup) + severity check (CSV weights)
        │
        ▼
 Final reply with prediction, description, precautions,
 and a "see a doctor" note when symptoms are severe
```

Two models work in tandem (trained on a dataset of **4,920 symptom records** covering **41 diseases**):

1. **`NlpModel`** (`medico/models.py`) — a 3-layer feed-forward network (`nnet.py`) that classifies a sentence into a symptom tag (e.g. `headache`) and reports its softmax confidence. Sentences below `SYMPTOM_CONFIDENCE_THRESHOLD` are rejected.
2. **`DiseasePredictor`** (`medico/models.py`) — a pickled scikit-learn classifier that maps the binary symptom vector (one slot per symptom in `data/list_of_symptoms.pickle`) to a disease.

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Web framework | Flask 2.x (app-factory pattern, blueprints) |
| Symptom NLP | PyTorch, NLTK (`punkt` tokenizer) |
| Disease prediction | scikit-learn |
| Data handling | pandas, NumPy |
| Frontend | Jinja2 templates, vanilla JS, CSS |
| Testing | pytest |
| Packaging | Docker (python:3.11-slim) |

## 📋 Requirements

- **Python 3.9+** (Docker image uses 3.11)
- pip

## 🚀 Getting Started

### 1. Clone and set up a virtual environment

```bash
git clone <your-repo-url>
cd MedicoAI-upload

python -m venv venv
venv/Scripts/activate           # Windows
# source venv/bin/activate      # Linux / macOS

pip install -r requirements.txt
```

### 2. Download the NLTK tokenizer data

```bash
python -c "import nltk; nltk.download('punkt')"
```

### 3. Configure environment (optional)

Copy the template and adjust values — all settings are read from environment
variables, so the same code runs in dev, test, and production:

```bash
cp .env.example .env
```

Generate a session secret:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Run the app

```bash
flask --app app run
```

Open **http://127.0.0.1:5000/** in your browser and start chatting with Meddy.

<details>
<summary><b>🐳 Docker alternative</b></summary>

```bash
docker build -t medicoai .
docker run --rm -p 5000:5000 -e FLASK_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))") medicoai
```

The image is CPU-only and exposes port `5000`.

</details>

## 💬 Usage

1. Describe **one symptom per message** (e.g. *"I have a headache"*, *"I feel dizzy"*).
   Use the autocomplete suggestions if you're unsure of the phrasing.
2. Keep adding symptoms — each recognized one is echoed back with a confidence
   percentage and stored for your session.
3. When you're finished, type **done** (or press the **Done** button) to receive:
   - the predicted **disease**,
   - a short **description**,
   - **four precautions**,
   - and a **doctor-visit warning** if your symptom severity is high.
4. Start over any time — opening `/` or calling `POST /api/reset` clears the session.

## 🔌 API Reference

| Method | Path | Description |
|:------:|------|-------------|
| `GET` | `/` | Chat interface (resets the conversation) |
| `GET` | `/health` | Liveness probe — `{"status": "ok"}` |
| `GET` | `/api/symptoms` | Symptom list for autocomplete |
| `GET` | `/api/model` | Model metadata (sizes, tag/vocab counts) |
| `GET` | `/api/conversation` | Symptoms collected in this session |
| `POST` | `/api/reset` | Clear the current session's symptoms |
| `POST` | `/symptom` | Send a message; returns the chatbot reply |

### Send a message

```bash
curl -X POST http://127.0.0.1:5000/symptom \
     -H "Content-Type: application/json" \
     -d '{"sentence": "I have a headache"}'
```

```json
{ "response": "Hmm, I'm 95.00% sure this is headache." }
```

Invalid input returns a JSON error with the appropriate status code
(`400` for malformed bodies, oversized messages, or empty sentences).

### Check conversation state

```bash
curl http://127.0.0.1:5000/api/conversation
```

```json
{ "symptoms": ["headache"] }
```

## ⚙️ Configuration

All settings come from environment variables (see `.env.example`). Defaults
live in `medico/config.py` — file paths are never hardcoded in application code.

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_SECRET_KEY` | random per start | Secret for signed session cookies — **set this in production** |
| `SYMPTOM_CONFIDENCE_THRESHOLD` | `0.5` | Minimum confidence to accept a recognized symptom |
| `MAX_MESSAGE_LENGTH` | `200` | Max characters accepted per message |
| `MAX_SYMPTOMS_PER_SESSION` | `20` | Cap on symptoms collected per conversation |
| `SEVERITY_MEAN_THRESHOLD` | `4` | Mean severity above which the doctor warning triggers |
| `SEVERITY_MAX_THRESHOLD` | `5` | Max severity above which the doctor warning triggers |
| `MODEL_FILE` | `models/data.pth` | PyTorch symptom classifier checkpoint |
| `PREDICTION_MODEL_FILE` | `models/fitted_model.pickle2` | Pickled scikit-learn predictor |
| `SYMPTOM_LIST_FILE` | `data/list_of_symptoms.pickle` | Canonical ordered symptom list |
| `SYMPTOM_DESCRIPTION_FILE` | `data/symptom_Description.csv` | Disease → description |
| `SYMPTOM_PRECAUTION_FILE` | `data/symptom_precaution.csv` | Disease → 4 precautions |
| `SYMPTOM_SEVERITY_FILE` | `data/Symptom-severity.csv` | Symptom → severity weight |
| `SUGGESTED_SYMPTOMS_FILE` | `static/assets/files/ds_symptoms.txt` | Autocomplete symptom list |

## 📁 Project Structure

```
MedicoAI-upload/
├── app.py                  # Entry point — builds the Flask app
├── medico/                 # Application package
│   ├── __init__.py         # App factory, security headers, logging, error handlers
│   ├── config.py           # Environment-driven settings
│   ├── data.py             # Dataset loading & normalization (SymptomData)
│   ├── models.py           # PyTorch (NlpModel) & sklearn (DiseasePredictor) wrappers
│   ├── routes.py           # HTTP endpoints (blueprint)
│   └── service.py          # Conversation state & prediction logic (ChatService)
├── nnet.py                 # Neural network architecture (3-layer MLP)
├── nltk_utils.py           # Tokenization & bag-of-words helpers
├── data/                   # Datasets
│   ├── dataset.csv         # Training data — 4,920 rows × 41 diseases (Disease + Symptom_1..17)
│   ├── list_of_symptoms.pickle
│   ├── Symptom-severity.csv
│   ├── symptom_Description.csv
│   └── symptom_precaution.csv
├── models/                 # Trained artifacts
│   ├── data.pth            # PyTorch checkpoint
│   └── fitted_model.pickle2
├── static/                 # css/, js/, assets/ (incl. autocomplete list)
├── templates/
│   └── index.html          # Chat UI
├── tests/                  # pytest suite (routes, service, models, security…)
├── Meddy.ipynb             # Training / exploration notebook
├── intents.json            # Symptom → example sentence patterns
├── Dockerfile              # Slim CPU-only image
├── requirements.txt
├── pytest.ini
├── CONTRIBUTING.md         # Contribution guide
├── SECURITY.md             # Security policy & deployer notes
└── LICENSE                 # MIT
```

## 🧪 Testing

```bash
pytest
```

The suite covers:

- Route handling and JSON error responses
- Input validation (malformed bodies, empty/oversized messages)
- Multi-turn conversation flow and the `done` command
- Session isolation between concurrent users
- Security headers and rendering safety
- The NLP model, predictor, and dataset layers

## 🔒 Security Notes

- **Set a strong `FLASK_SECRET_KEY`** in production — a fresh random key on every
  restart silently invalidates all user sessions.
- Model artifacts are **pickled**: only load model files from a trusted source.
- Run behind a production WSGI server (e.g. **gunicorn**) with TLS.
- Baseline security headers (`nosniff`, CSP, `X-Frame-Options`) are applied to
  every response by the app factory.

See [SECURITY.md](SECURITY.md) for the full policy and vulnerability reporting.

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first —
it covers the branch/commit conventions, testing expectations, and project rules
(session-scoped state, escaped user input, config-driven paths).

## 📄 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

<div align="center">

<sub>Built with Flask, PyTorch & scikit-learn — and a friendly chatbot named Meddy 🤖</sub>

</div>
