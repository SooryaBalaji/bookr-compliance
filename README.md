# Bookr Compliance Command Centre

Regulatory compliance and automated corporate filing tracker for Bookr, Inc.

## Tech Stack
- Backend: FastAPI (Python 3.12)
- Database: PostgreSQL 16
- Auth: Email/password with JWT bearer tokens
- Frontend: Static HTML/JS/CSS served by FastAPI (same UI as the original single-file version)

## Getting Started

1. Copy `.env.example` to `.env` (or just set `SECRET_KEY` in your shell) and pick a real secret:
   ```
   export SECRET_KEY=$(openssl rand -hex 32)
   ```
2. Run `docker-compose up` to start the backend and database.
3. Open `http://localhost:8000`.
4. The **first account you register becomes an admin**; everyone after that registers as a regular member. There's no invite system yet — anyone with access to the login page can create an account. If you're deploying this somewhere reachable outside your team, turn off open registration or put it behind a VPN/allowlist first.

## Data model

- `tasks` — every compliance milestone, both the ~32 built-in federal/state/insurance filings (seeded automatically on first boot) and any custom ones you add. Deleting a task soft-deletes it (`deleted=true`) rather than removing history.
- `compliance_logs` — one row per "mark filed" action, linked to a task and a fiscal year. Powers the History Archive view and per-task filing history.
- `users` — email + bcrypt password hash + role (`admin`/`member`).

## API

Interactive API docs are available at `http://localhost:8000/docs` once the server is running. Every endpoint except `/auth/register`, `/auth/login`, and `/health` requires an `Authorization: Bearer <token>` header.

## Running tests

Playwright/API and load tests are opt-in (they're not part of a normal `docker-compose up`):

```
docker-compose --profile test up playwright
docker-compose --profile test up k6
```

## Local development without Docker

```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="sqlite+aiosqlite:///./dev.db"   # or point at a real Postgres instance
export SECRET_KEY="dev-secret"
uvicorn app.main:app --reload
```
(SQLite needs the `aiosqlite` package if you go this route: `pip install aiosqlite`.)

---
© 2026 Bookr, Inc. All rights reserved.
