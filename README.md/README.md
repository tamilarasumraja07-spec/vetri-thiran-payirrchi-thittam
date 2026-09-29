# PocketSmart AI

PocketSmart AI is a Generative AI-powered budget and recommendation assistant.

It provides three planning modules:

1. Home Interior Planning
2. Party/Event Budget Planning
3. Jewelry Recommendation

The project uses FastAPI, SQLite, SQLAlchemy, Jinja2 and Google Gemini.

---

## Technology Stack

Frontend:

- HTML
- CSS
- JavaScript
- Jinja2

Backend:

- Python
- FastAPI
- Uvicorn

Database:

- SQLite
- SQLAlchemy

AI:

- Google Gemini
- google-genai SDK

Authentication:

- JWT
- bcrypt password hashing

Testing:

- pytest

---

## Project Structure

```text
PocketSmart_AI/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   │
│   ├── models/
│   ├── routes/
│   └── services/
│
├── templates/
├── static/
├── tests/
│
├── scripts_test_gemini.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md