# AssetOps — Industrial Asset & Maintenance Management

AssetOps is a portfolio MVP for registering equipment and managing industrial maintenance workflows.

## Features

- Session login and role-based permissions (Django Groups)
- Asset registry and asset search
- Maintenance work orders and technician assignment
- Controlled workflow: Open → In progress → Review → Completed; with permitted cancellation/rework
- Required resolution notes before review
- Status-change audit events
- Operations dashboard
- Django admin for supervisors and system administrators
- Automated workflow/access tests

## Stack

Python 3.11+, Django 5.2 LTS, server-rendered Django templates, SQLite (development), PostgreSQL (optional production backend).

## Local installation

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
# Copy .env.example to .env and set a unique SECRET KEY
# This repository intentionally does not auto-load .env files.
# For local testing, set the environment variables manually:
# Windows PowerShell: $env:DJANGO_DEBUG='1'
# macOS/Linux: export DJANGO_DEBUG=1
python manage.py migrate
python manage.py setup_roles
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000 and log in as your superuser. Through `/admin/`, create regular user accounts and assign each user to one of the groups: `Admin`, `Supervisor`, `Technician`, or `Viewer`. Groups control application screens; Django's `is_staff` separately controls access to the Django administration interface. Only grant `is_staff` and explicit model permissions to trusted users.

## Permissions

| Action | Admin/Supervisor | Technician | Viewer |
| --- | --- | --- | --- |
| See dashboards, assets, work orders | Yes | Yes | Yes |
| Register assets | Yes | No | No |
| Create work orders | Yes | Yes (self-assigned) | No |
| Work on order | Yes | Assigned orders | No |
| Complete/cancel orders | Yes | No | No |

## Tests

```bash
python manage.py test
python manage.py check
```

## Documentation

See `docs/REQUIREMENTS.md`, `docs/DATABASE.md`, `docs/TESTING.md`, `docs/DEPLOYMENT.md`, and `docs/ROADMAP.md`.

## Security notes

MVP only; not production certified. CSRF, password validation, session cookies and role checks use Django. Configure HTTPS and trusted hosts in production. Use a PostgreSQL-backed deployment and implement backups, login throttling, monitoring, and per-site asset restrictions before handling real company data. Do not commit credentials or production records.

## License

MIT (see LICENSE).
