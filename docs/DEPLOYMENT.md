# Deployment guide

This is a **development-first MVP**. A public deployment requires a hosting service that runs Python WSGI, HTTPS termination, environment variables and a persistent database.

1. Provision PostgreSQL and a least-privilege database user; back up data before migrations.
2. Set `DJANGO_DEBUG=0`, a strong `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, and PostgreSQL credentials in hosting environment variables (do not commit `.env`).
3. Set `DJANGO_CSRF_TRUSTED_ORIGINS` for your HTTPS origin and enable `DJANGO_SECURE_SSL_REDIRECT=1` if your TLS proxy correctly forwards the scheme. Configure `SECURE_PROXY_SSL_HEADER` only for a trusted proxy with controlled headers.
4. Install requirements, run `python manage.py check --deploy`, `python manage.py migrate`, `python manage.py setup_roles`, and `python manage.py collectstatic --noinput`.
5. Serve static files through a web server or supported static middleware, and configure WSGI using `config.wsgi:application`.
6. Configure password and login brute-force defenses, audit retention, monitoring, log hygiene and backup/recovery testing before production use.

Rollback: restore the previous application release. Database rollback requires a tested migration rollback or a verified backup restore; avoid rolling back destructive migrations without a recovery plan.
