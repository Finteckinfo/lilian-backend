# Being Lillian — Backend API

FastAPI service for **Being Lillian**: public content, lead capture, studio auth, and admin CRM/content APIs.

## Stack

- Python 3.11+ recommended
- FastAPI + Uvicorn + Pydantic v2
- `python-jose` (JWT) + `bcrypt` (passwords)
- Optional Supabase (Postgres) via service role; otherwise local JSON persistence under `data/`

## Requirements

```bash
python3 -m pip install --user -r requirements.txt
```

## Setup

```bash
cp .env.example .env
# Set AUTH_JWT_SECRET to a long random value (required in production)
PYTHONPATH=. uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Health:

- `GET /health` — liveness
- `GET /health/ready` — counts + mode
- `GET /docs` — OpenAPI (**disabled when `ENVIRONMENT=production`**)

## Environment

| Variable | Required | Description |
|----------|----------|-------------|
| `ENVIRONMENT` | Yes (prod) | `development` or `production` |
| `AUTH_JWT_SECRET` | **Yes in production** | HS256 secret for studio JWTs |
| `AUTH_JWT_HOURS` | No | Token lifetime (default `72`) |
| `AUTH_ALLOW_SIGNUP` | No | After first admin, keep signup closed unless `true` |
| `FRONTEND_ORIGIN` | Yes (prod) | Comma-separated CORS allowlist |
| `DATA_DIR` | No | Local persistence folder (default `data`) |
| `SUPABASE_URL` | Optional | Enables hosted DB mode |
| `SUPABASE_SERVICE_ROLE_KEY` | Optional | Server-only; never expose to browsers |
| `SUPABASE_JWT_SECRET` | Optional | Also accept Supabase Auth JWTs |
| `LEAD_RATE_LIMIT` / `LEAD_RATE_WINDOW_SECONDS` | No | Lead POST throttling |
| `AUTH_RATE_LIMIT` / `AUTH_RATE_WINDOW_SECONDS` | No | Login/signup throttling |

## API surface

### Public

| Method | Path | Notes |
|--------|------|-------|
| GET | `/v1/posts` | Published journal posts |
| GET | `/v1/posts/{slug}` | Single post |
| GET | `/v1/portfolio` | Gallery items |
| GET | `/v1/settings` | Public site settings |
| POST | `/v1/leads` | Create inquiry (rate limited) |
| GET | `/v1/auth/status` | `{ has_users, signup_open }` |

### Auth

| Method | Path | Notes |
|--------|------|-------|
| POST | `/v1/auth/signup` | First admin, or when signup allowed |
| POST | `/v1/auth/login` | Email + password → JWT |
| GET | `/v1/auth/me` | Bearer required |

### Admin (Bearer JWT)

| Method | Path | Notes |
|--------|------|-------|
| GET | `/v1/admin/stats` | Monitor dashboard |
| GET/PATCH | `/v1/admin/settings` | Appearance / capabilities |
| GET/PATCH | `/v1/admin/leads`, `/v1/admin/leads/{id}` | CRM |
| CRUD | `/v1/admin/posts` | Journal |
| CRUD | `/v1/admin/portfolio` | Gallery |

## Project layout

```
app/
  main.py           App, CORS, health
  config.py         Settings
  auth.py           JWT + rate limits
  users.py          Bcrypt users (local JSON)
  store.py          Local content/leads persistence
  seed.py           Seed posts/portfolio
  routers/          auth, posts, portfolio, leads, admin
  schemas/          Pydantic models / enums
data/               Runtime only — gitignored
docs/PRACTICES.md   Engineering rules
supabase/           SQL migrations + seed
```

## Local vs Supabase mode

- **Local (default):** posts, portfolio, settings, leads, and users persist as JSON under `data/`. Ideal for development and demos.
- **Supabase:** set URL + service role; public reads/writes go through the API using the service role. Run `supabase/migrations/001_initial.sql` (and seed if needed).

## Production checklist

1. `ENVIRONMENT=production`
2. Strong unique `AUTH_JWT_SECRET`
3. `FRONTEND_ORIGIN` = exact frontend origin(s)
4. Confirm `/docs` returns 404
5. Create the first admin via `/admin/signup`, then keep `AUTH_ALLOW_SIGNUP=false`
6. Rotate secrets if they ever appeared in logs or tickets
7. Do not deploy `data/users.json` from a developer machine to production without intent

### Railway / Railpack

Root directory must be this package (`lilian-backend`). Start command is defined in `railpack.json`:

```bash
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

Set at least: `ENVIRONMENT`, `AUTH_JWT_SECRET`, `FRONTEND_ORIGIN`.

## Security

See [SECURITY.md](./SECURITY.md) and [docs/PRACTICES.md](./docs/PRACTICES.md).

## Related

- Frontend package: sibling `lilian-frontend` under the workspace `frontend/` directory
