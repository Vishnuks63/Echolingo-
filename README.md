# EchoLingo – Desi Duolingo

EchoLingo is a language-learning web application inspired by the Duolingo learning experience, focused on helping users learn Indian languages through interactive quizzes and AI-powered translation.

## Features

- User registration and login
- Language and difficulty-based quizzes
- AI-powered English-to-Indian-language translation
- Quiz scoring
- Support for Hindi, Tamil, Telugu, Marathi, and Bengali translation models
- FastAPI backend with SQLite/SQLAlchemy persistence
- Simple browser-based frontend

## Tech Stack

- **Backend:** Python, FastAPI, SQLAlchemy
- **AI/NLP:** Hugging Face Transformers, MarianMT
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript
- **ML runtime:** PyTorch

## Project Structure

```text
.
├── ai_service.py          # Hugging Face translation service
├── database.py            # SQLAlchemy models and database setup
├── main.py                # FastAPI application and API routes
├── seed_questions.py      # Seeds quiz questions into the local database
├── requirements.txt       # Python dependencies
├── .env.example           # Environment configuration template
└── static/                # Frontend pages and assets
```

## Supported Languages

- Hindi
- Tamil
- Telugu
- Marathi
- Bengali

## Getting Started

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd echolingo
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
uvicorn main:app --reload
```

Open the application at:

```text
http://localhost:8000/static/language_selection.html
```

The first translation request for a language may take longer because the corresponding Hugging Face model needs to be downloaded locally.

## Database

EchoLingo uses a local SQLite database named `language_learning.db`. The database is intentionally excluded from Git so local user data and runtime state are never committed to the public repository.

Run the seed script when you want to populate quiz questions:

```bash
python seed_questions.py
```

## Notes

This repository is a portfolio/demo project. Authentication and deployment configuration should be hardened further before using the application with real users or production data.
