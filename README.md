# Bookr Compliance Command Centre

Regulatory compliance and automated corporate filing tracker for Bookr, Inc.

## Tech Stack
- Backend: FastAPI (Python 3.12)
- Database: PostgreSQL 16 via SQLAlchemy's async ORM
- Auth: Email/password, session via an httponly JWT cookie (`bookr_token`) — not a bearer token
- Frontend: Static HTML/JS/CSS served by FastAPI (same UI as the original single-file version)
- Redis (`cache` service in `docker-compose.yml`) is provisioned but not wired into the app yet — the `/auth/emergency-reset` rate limiter is in-memory only today and won't share state across multiple instances (see the comment in `app/main.py`)

## Getting Started

1. Copy `.env.example` to `.env` and pick a real secret:
   ```
   openssl rand -hex 32   # paste the result in as SECRET_KEY
   ```
2. Run `docker-compose up` to start the backend, Postgres, and Redis.
3. Open `http://localhost:8000`.
4. The **first account you register becomes a Super Admin**; after that, `/auth/register` is disabled for everyone (`403 Public registration disabled`) — a Super Admin has to create further accounts (as Co-Admin, Editor, or Viewer) from the admin panel or `POST /users/`. There's no invite system yet, and no one owns the Super Admin slot until that first registration happens — if you're deploying this somewhere reachable outside your team, register the first account yourself before making it public, or put it behind a VPN/allowlist until you have.

### Deploying somewhere real

Copy `.env.production.example` to `.env` on the server instead of the dev template, and set `ENVIRONMENT=production`. This enforces a real `SECRET_KEY` (no insecure dev fallback) and marks the auth cookie `Secure`, so the app **must** sit behind TLS (e.g. a reverse proxy terminating HTTPS) — the cookie won't be sent at all over plain HTTP once `ENVIRONMENT=production` is set. Also set `ALLOWED_ORIGINS` to your real domain(s).

## Data model

- `entities` — the organizations being tracked (name, org type, incorporation state, HQ, NAICS code). Creating one seeds its compliance task list automatically (see below).
- `entity_members` — links a user to the entities they're allowed to access. Super Admins see every entity regardless of membership; everyone else only sees entities they're a member of.
- `tasks` — every compliance milestone for an entity, both the ones seeded from a template and any custom ones you add. Deleting a task soft-deletes it (`deleted=true`) rather than removing history.
- `compliance_logs` — one row per "mark filed" action, linked to a task and a fiscal year. Powers the History Archive view and per-task filing history.
- `users` — email + bcrypt password hash + role (`super_admin`/`co_admin`/`editor`/`viewer`).

### Compliance task templates

New entities are seeded from one of seven task lists in `app/seed_data.py`, chosen automatically by org type + incorporation state:

| Org type | Incorporation state | Template |
|---|---|---|
| C-Corp / S-Corp | Delaware | `DELAWARE_CCORP_TASKS` |
| C-Corp / S-Corp | California | `CA_FOR_PROFIT_TASKS` |
| C-Corp / S-Corp | anywhere else | `GENERAL_CORP_TASKS` |
| LLC | any | `GENERAL_LLC_TASKS` |
| Non-profit | any | `NON_PROFIT_TASKS` |

`CORE_TASKS` and `PEBBLE_TASKS` are named templates (`"bookr"` / `"pebble"`) you can pick explicitly instead, bypassing the org-type/state logic above. Whichever template applies, `STATE_TASKS_MAP` also layers on a state-specific annual-report/franchise-tax task, covering all 50 states plus DC.

## Roles & permissions

- **Super Admin** — full access to every entity and every user; the only role that can grant or revoke Super Admin.
- **Co-Admin** — same admin capabilities as Super Admin (`/users/*`, `/entities/*`, `/memberships/`), but scoped to the entities they're a member of — can't see or touch users/entities outside their own orgs, and can't grant or revoke Super Admin.
- **Editor** — can create, edit, and delete tasks and compliance logs, scoped to their assigned entities.
- **Viewer** — read-only, scoped to their assigned entities.

## API

Interactive API docs are available at `http://localhost:8000/docs` once the server is running. Auth is the `bookr_token` httponly cookie, not a bearer token — `/auth/login` or `/auth/register` sets it, and every route except `/`, `/auth/register`, `/auth/login`, `/auth/logout`, `/auth/is-initialized`, and `/auth/emergency-reset` requires it. On top of that, `/users/*`, `/entities/*`, and `/memberships/` require the Co-Admin or Super Admin role, and creating/editing/deleting tasks or logs requires any role above Viewer.

## Running tests

- **API tests** (`tests/api.spec.js`, Playwright) — there's no docker-compose profile for this; run the official Playwright image on the same Docker network as the app:
  ```
  docker-compose up -d
  docker run --rm --network bookr-compliance_default \
    -v "$(pwd)/tests:/tests" -w /tests \
    mcr.microsoft.com/playwright:v1.44.0-jammy \
    bash -c "npm install && npx playwright test api.spec.js"
  ```
  Against a fresh database it bootstraps the first Super Admin itself. Against an already-initialized one, pass `-e TEST_ADMIN_EMAIL=... -e TEST_ADMIN_PASSWORD=...` for a real account.

- **Load test** (`tests/load.js`, k6) — currently stale: it posts to `/tasks/` with no auth cookie and a schema (`title`/`description`/`status`) that predates the current `Task` model, so it fails against this version of the API as-is. Needs updating before it's useful again.

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
