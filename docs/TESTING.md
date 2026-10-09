# Testing guide

Run `python manage.py test` and `python manage.py check` inside the configured environment.

Automated cases cover unauthenticated redirects, viewer authorization, technician transitions, invalid transitions, supervisor approval, POST-only status updates and assignment spoofing.

Manual checks: create groups, create users, register an asset, create an order, assign technician, transition to in-progress, add notes, request review, approve as supervisor, inspect event timeline; verify no edit access as Viewer.

Deployment acceptance should also include CSRF, security headers, HTTPS, PostgreSQL migrations, backup restoration, concurrency and authorization boundary testing.
