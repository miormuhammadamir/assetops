# Deployment and Operations Guide

## Local Windows installation
```powershell
cd C:\Projectsssetops
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:DJANGO_DEBUG="1"
python manage.py migrate
python manage.py setup_roles
python manage.py createsuperuser
python manage.py test
python manage.py runserver
```
Open `http://127.0.0.1:8000/`. Local DEBUG mode is for a private development computer only.

## Environment variables
`DJANGO_SECRET_KEY` (required for DEBUG=0), `DJANGO_DEBUG` (0 or 1), `DJANGO_ALLOWED_HOSTS`, `DJANGO_CSRF_TRUSTED_ORIGINS`, `DJANGO_TIME_ZONE`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`, `DJANGO_SECURE_SSL_REDIRECT`, `DJANGO_HSTS_SECONDS`.

This project **does not automatically load `.env` files**. Configure environment variables in the process manager or terminal; do not commit secrets. `.env.example` documents the names.

## Scheduler
Run manually:
```powershell
python manage.py generate_maintenance
```
Production scheduling requires a process manager (cron, Windows Task Scheduler or equivalent) launching a configured Django environment. Use one scheduler on SQLite. Prefer PostgreSQL in multi-worker deployments. Verify idempotency of a single due date; each subsequent run may process the next overdue interval.

## Production readiness
Use a supported WSGI/ASGI server behind HTTPS reverse proxy; configure static file serving, secure headers, host restrictions, PostgreSQL, monitoring and backups. Django `runserver` is not suitable for production. `python manage.py check --deploy` provides a checklist, not certification.

## Migration procedure
1. Announce maintenance window where appropriate and back up database.
2. Deploy tested source and install dependencies.
3. Run `python manage.py migrate` once.
4. Run smoke tests; verify login, asset read, work-order status and scheduler.
5. Roll back application code only if compatible with migrated schema; restore from tested database backup if necessary. Do not casually reverse destructive migrations.
