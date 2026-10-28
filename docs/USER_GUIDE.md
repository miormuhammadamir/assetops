# User Guide

## Starting AssetOps
Run the server and open `/`. Sign in with a Django user account assigned an appropriate Group. Superusers can manage everything; Django admin (`/admin/`) requires `is_staff`.

## Asset registry
Open **Assets**, search equipment by code/name/location, or select **Register asset** as a Supervisor/Admin. Record a unique code, location, criticality and current status. Use consistent equipment identifiers.

## Work orders
Open **Work orders** and create a request. Supervisors can assign active technicians; technician-created requests are self-assigned. From an order detail page, authorized users can start work, enter resolution notes, request review, and supervisors can complete or cancel according to allowed transitions.

## Preventive maintenance
Open **Maintenance**. Admin/Supervisor can create a plan with an asset, title, instructions, interval in days and next due date. To generate due orders, run `python manage.py generate_maintenance`; it does not run automatically just because the web server is running. Pause schedules before planned shutdowns if needed.

## API browsing
With an authenticated browser session, visit `/api/v1/`. APIs use JSON and page-number pagination. See API.md for request examples and security rules.

## Troubleshooting
- `Set DJANGO_SECRET_KEY when DEBUG=0`: configure secret for non-debug environment or set `DJANGO_DEBUG=1` locally.
- `No such table`: run `python manage.py migrate`.
- `No changes detected` expected from `python manage.py makemigrations --check --dry-run`.
- HTTP 403: check login and Django Groups; session POST/PATCH requires CSRF token.
- Missing maintenance orders: run the management command and verify plan active/due.
