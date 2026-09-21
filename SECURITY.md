# Security — Being Lillian API

## Trust boundary

| Secret | Where it may live |
|--------|-------------------|
| `AUTH_JWT_SECRET` | API host env only |
| `SUPABASE_SERVICE_ROLE_KEY` | API host env only |
| `SUPABASE_JWT_SECRET` | API host env only |
| Admin password hashes | `data/users.json` (local) or IdP (Supabase Auth) — never in git |
| Browser | Access token only, after login |

The frontend must **not** receive service-role keys or JWT signing secrets.

## Authentication

- Passwords hashed with **bcrypt** (cost factor 12).
- Studio JWTs: HS256, issuer `being-lillian`, expiring per `AUTH_JWT_HOURS`.
- Admin routes fail closed (`401`) on missing/invalid tokens.
- Signup is open only until the first admin exists, unless `AUTH_ALLOW_SIGNUP=true`.
- Auth and lead endpoints are IP rate-limited.

## Data handling

- Lead PII (name, phone, email, notes) is sensitive. Prefer hosted DB with RLS in production.
- Local `data/` files are for development; exclude from VCS and from audit zip files unless redacted.
- Do not log JWTs, full phone numbers, or password material.

## CORS

`FRONTEND_ORIGIN` is an allowlist. Misconfiguration can enable browser-based abuse of cookie-less APIs; keep it tight in production.

## Production hardening

- Set `ENVIRONMENT=production` (disables OpenAPI UI).
- Require a non-default `AUTH_JWT_SECRET` (startup fails closed if missing in production).
- Prefer HTTPS everywhere; terminate TLS at the edge.

## Reporting

Report vulnerabilities privately to the repository owner. Avoid public disclosure before a fix is available.
