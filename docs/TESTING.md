# Test Plan

## Setup
```powershell
$env:DJANGO_DEBUG="1"
python -m pip install -r requirements.txt
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test -v 2
```

## Automated suites
- `operations.tests`: login, read/write roles, work order transitions, impersonation resistance.
- `operations.test_maintenance`: recurring scheduling and plan permission behavior.
- `operations.test_api`: GET/POST/PATCH validation, group enforcement, assignment protection, workflow transitions, basic CSRF check, pagination.

## Manual integration scenarios
1. Create Admin and Technician users; assign groups via Django admin.
2. Register asset and find it in the equipment list.
3. Create work order and verify Technician sees assignment.
4. Technician starts work, adds notes, requests review.
5. Supervisor completes order and audit history records transition.
6. Supervisor schedules a plan due today; run `generate_maintenance`; verify one new work order and occurrence.
7. Run command again; confirm prior plan/date occurrence is not duplicated.
8. Log into browser and navigate to `/api/v1/`; test read responses.
9. Verify a Viewer/Technician cannot POST an asset.
10. Verify invalid criticality and duplicate code yield 400 from API.

## Limitations
CI only proves behavior under the configured test runtime/database; production HTTPS, backup restoration, deployment, multi-worker concurrency and object-level security require additional tests.
