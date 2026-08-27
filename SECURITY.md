# Security Policy

## Medical disclaimer

MedicoAI is a machine-learning demonstration. It does not provide medical
diagnoses or treatment advice. Outputs from the chatbot must never be used as
a substitute for professional medical care.

## Reporting a vulnerability

If you discover a security issue, please do not open a public issue. Instead,
email the maintainers with a description of the problem, the affected
version, and reproduction steps. Please include the word "SECURITY" in the
subject line.

We ask that you allow a reasonable disclosure window before publishing
details publicly.

## Security notes for deployers

- Set a strong, random `FLASK_SECRET_KEY` in production.
- The bundled model artifacts are pickled; only load models from a trusted
  source and never accept model files from untrusted users.
- Run behind a production WSGI server (e.g., gunicorn) with TLS.
- User messages are escaped before rendering; keep escaping in place when
  modifying the frontend.
