# Deployment Runbook

## Purpose
This runbook defines the minimum release safety process, smoke checks, rollback triggers, and on-call actions for ADLM SkillHub backend deployments.

## Pre-deploy checklist
- CI matrix is green for SQLite + PostgreSQL.
- Database migrations reviewed and approved.
- Required production environment variables are present (`SECRET_KEY`, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, email credentials).
- Deployment window and owner are confirmed.

## Deploy procedure
1. Deploy application artifact.
2. Run migrations:
   ```bash
   python manage.py migrate --noinput
   ```
3. Execute smoke checks:
   ```bash
   python manage.py check
   python manage.py smoke_check
   ```
4. Validate critical auth and API routes:
   - `token_obtain_pair`
   - `token_refresh`
   - `schema-json`

## SLO targets and thresholds

### Auth/API reliability
- Login/token endpoints success rate: **>= 99.5%** over 15 minutes.
- 5xx rate across auth endpoints: **< 1%** over 15 minutes.

### Latency targets
- Auth endpoints p95 latency: **< 400ms**.
- Analytics summary p95 latency: **< 800ms**.
- AI endpoints p95 latency: **< 1500ms**.

### AI warning threshold
- `AI_LATENCY_WARN_MS` controls warning logs for AI endpoints.
- Default is `1500` ms.

## Rollback triggers
Initiate rollback if any condition holds for >= 10 minutes after deploy:
- Smoke check failure.
- Auth success rate below 99.5%.
- API 5xx > 2% sustained.
- AI p95 latency > 3000ms sustained.

## Rollback procedure
1. Roll back to previous stable release artifact.
2. Re-run smoke checks:
   ```bash
   python manage.py check
   python manage.py smoke_check
   ```
3. Confirm auth and core API endpoints recover.
4. Post incident note in deployment channel with timeline and root-cause hypothesis.

## Incident ownership
- Release owner: Executes deployment and rollback decisions.
- On-call engineer: Investigates logs (`request` logger, auth/AI logs) and verifies recovery.


## Release completion criteria
- CI matrix green (SQLite + PostgreSQL).
- Migrations and smoke checks pass in deploy target environment.
- Auth and non-auth API response contracts validated against `docs/api/response_contracts.md`.
