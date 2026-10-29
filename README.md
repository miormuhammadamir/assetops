# AssetOps — Industrial Asset & Maintenance Management

<img width="1847" height="937" alt="image" src="https://github.com/user-attachments/assets/4f247cb4-87b7-4807-8bcf-1e6c34134706" />


Portfolio-grade **Django maintenance management application** with server-rendered web UI and a Django REST Framework API. Supports registered equipment, controlled maintenance work orders, recurring preventive plans and auditable status events.

> **Status:** demonstrable application / portfolio release. Not certified or hardened for live industrial operations. Runtime verification must be performed in your deployment environment.

## Implemented features
- Login/logout and Group-based roles: Admin, Supervisor, Technician, Viewer.
- Asset registration, search, status and criticality.
- Work orders with technician assignment and guarded state changes.
- Resolution notes, supervisor approval and work order status audit events.
- Recurring preventive maintenance plans with generation management command.
- DRF `/api/v1/` endpoints with session authentication, CSRF and role-based writes.
- Pagination, filters and automated tests.

## Quick start (Windows PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:DJANGO_DEBUG="1"
python manage.py migrate
python manage.py setup_roles
python manage.py createsuperuser
python manage.py test
python manage.py runserver
```
Visit http://127.0.0.1:8000/ ; admin is at `/admin/`, API at `/api/v1/`. For maintenance orders run `python manage.py generate_maintenance` manually or from a scheduler.

## Documentation
- [Installation](docs/INSTALLATION.md)
- [User Guide](docs/USER_GUIDE.md)
- [Requirements](docs/REQUIREMENTS.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Database / ERD](docs/DATABASE.md)
- [API Reference](docs/API.md)
- [Security](docs/SECURITY.md)
- [Testing](docs/TESTING.md)
- [Deployment / Operations](docs/DEPLOYMENT.md)
- [Roadmap](docs/ROADMAP.md)

## License
MIT. See LICENSE.
