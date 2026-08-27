# Contributing to MedicoAI

Thanks for your interest in improving MedicoAI!

## Getting started

1. Fork the repository and clone your fork.
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   venv/Scripts/activate
   pip install -r requirements.txt
   ```
3. Download the NLTK punkt data:
   ```bash
   python -c "import nltk; nltk.download('punkt')"
   ```
4. Run the test suite to confirm a green baseline:
   ```bash
   pytest
   ```

## Making changes

- Create a branch for your work: `git checkout -b feature/my-change`.
- Keep changes small and focused. One logical change per commit.
- Write commit messages in the conventional style, e.g.
  `feat: add export conversation history` or `fix: handle empty replies`.
- Add or update tests for behavior you change.
- Run the full test suite before opening a pull request.

## Project conventions

- Backend code lives under `medico/` and follows the app-factory pattern.
- Session-scoped state goes through Flask sessions, never module globals.
- User-provided text must be escaped before rendering in the chat UI.
- Model and dataset paths come from `medico/config.py`, never hardcoded.

## Pull requests

- Reference the issue your change addresses, if any.
- Describe what changed and why.
- Note any manual testing you performed.

Thank you for contributing!
