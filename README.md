# Bookr Compliance Command Centre

Regulatory compliance and automated corporate filing tracker for Bookr, Inc.

## Tech Stack
- Backend: FastAPI (Python 3.12)
- Database: PostgreSQL 16
- Auth: Email/password, session via an httponly JWT cookie (`bookr_token`) — not a bearer token
- Frontend: Static HTML/JS/CSS served by FastAPI (same UI as the original single-file version)

## Getting Started

1. Copy `.env.example` to `.env` (or just set `SECRET_KEY` in your shell) and pick a real secret:
   ```
   export SECRET_KEY=$(openssl rand -hex 32)
   ```
2. Run `docker-compose up` to start the backend and database.
3. Open `http://localhost:8000`.
4. The **first account you register becomes a Super Admin**; after that, `/auth/register` is disabled for everyone (`403 Public registration disabled`) — a Super Admin has to create further accounts (as Co-Admin, Editor, or Viewer) from the admin panel or `POST /users/`. There's no invite system yet, and no one owns the Super Admin slot until that first registration happens — if you're deploying this somewhere reachable outside your team, register the first account yourself before making it public, or put it behind a VPN/allowlist until you have.

### Deploying somewhere real

Copy `.env.production.example` to `.env` on the server instead of the dev template, and set `ENVIRONMENT=production`. This enforces a real `SECRET_KEY` (no insecure dev fallback) and marks the auth cookie `Secure`, so the app **must** sit behind TLS (e.g. a reverse proxy terminating HTTPS) — the cookie won't be sent at all over plain HTTP once `ENVIRONMENT=production` is set. Also set `ALLOWED_ORIGINS` to your real domain(s).

## Data model

- `tasks` — every compliance milestone, both the ~32 built-in federal/state/insurance filings (seeded automatically on first boot) and any custom ones you add. Deleting a task soft-deletes it (`deleted=true`) rather than removing history.
- `compliance_logs` — one row per "mark filed" action, linked to a task and a fiscal year. Powers the History Archive view and per-task filing history.
- `users` — email + bcrypt password hash + role (`super_admin`/`co_admin`/`editor`/`viewer`).
- `entity_members` — links a user to the entities (organizations) they're allowed to access. Super Admins see everything; everyone else only sees entities they're a member of.

## API

Interactive API docs are available at `http://localhost:8000/docs` once the server is running. Auth is a `bookr_token` httponly cookie, not a bearer token — `/auth/login` or `/auth/register` sets it, and every route except `/`, `/auth/register`, `/auth/login`, `/auth/logout`, `/auth/is-initialized`, and `/auth/emergency-reset` requires it. On top of that, `/users/*`, `/entities/*`, and `/memberships/` require the `co_admin` or `super_admin` role, and creating/editing/deleting tasks or logs requires any role above `viewer`.

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
