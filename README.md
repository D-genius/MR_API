# MR_API

A FastAPI backend REST API. This README describes how to set up, run, test and containerize the project.

## Features
- FastAPI application with auto-generated OpenAPI docs (/docs, /redoc)
- Development server with hot reload
- Example health and CRUD endpoints
- Optional database support (Postgres) with Alembic migrations
- Docker and docker-compose support
- Tests with pytest

## Prerequisites
- Python 3.10+ (adjust if project uses another minor version)
- pip
- (optional) Docker & docker-compose
- (optional) PostgreSQL (or another DB supported by SQLAlchemy)

## Setup (local development)
1. Clone the repository
    - git clone <repo-url>
    - cd <repo-dir>

2. Create and activate a virtual environment
    - python -m venv .venv
    - source .venv/bin/activate  # macOS / Linux
    - .venv\Scripts\activate     # Windows (Powershell)

3. Install dependencies
    - pip install --upgrade pip
    - pip install -r requirements.txt

4. Environment variables
    - Copy `.env.example` to `.env` and update values (e.g. DATABASE_URL, SECRET_KEY, DEBUG)
    - Example DATABASE_URL for Postgres:
      - postgres://user:password@localhost:5432/mr_api_db

5. Database (optional)
    - Create database in Postgres
    - Run Alembic migrations:
      - alembic upgrade head
    - Or use a management script if provided:
      - python app/db/init_db.py

## Run the app
- Development server (hot reload)
  - uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

- Production (example using gunicorn + uvicorn workers)
  - gunicorn -k uvicorn.workers.UvicornWorker app.main:app --workers 4 --bind 0.0.0.0:8000

## Docker
- Build:
  - docker build -t mr_api:latest .
- Run:
  - docker run -p 8000:8000 --env-file .env mr_api:latest
- With docker-compose:
  - docker-compose up --build

## Tests
- Run tests:
  - pytest -q
- Add test coverage:
  - pytest --cov=app --cov-report=term-missing

## Linting & Formatting
- Black:
  - black .
- Isort:
  - isort .
- Flake8:
  - flake8

## API docs
- Interactive Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health check: GET /health or similar (adjust to your route)

## Example requests
- Health check:
  - curl -v http://localhost:8000/health
- Example GET:
  - curl -v http://localhost:8000/users/me
- Example POST:
  - curl -X POST http://localhost:8000/register -H "Content-Type: application/json" -d '{"name":"example","value":123}'

Adjust routes/payloads to match your implementation.

## Migrations (Alembic)
- Generate migration:
  - alembic revision --autogenerate -m "describe changes"
- Apply migration:
  - alembic upgrade head
