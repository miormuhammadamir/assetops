# Security Review and Threat Model

## Assets to protect
User credentials, session cookies, asset/work-order records, maintenance schedules and audit history.

## Threats and controls
- **Unauthenticated data disclosure:** session auth and DRF IsAuthenticated / API permission classes.
- **Unauthorized writes:** group-based role checks; no client-supplied role membership; dedicated transition service.
- **Assignment spoofing:** technician work orders automatically assigned to actor.
- **CSRF:** Django CSRF middleware plus DRF SessionAuthentication; regression test provided.
- **Injection:** ORM parameterized queries; templates auto-escape by default.
- **Duplicate maintenance generation:** unique (plan, due date) constraint and transactions; PostgreSQL locking preferred.
- **Sensitive files in Git:** .gitignore excludes `.env`, DB, virtualenv and common secrets; inspect Git history as well.
- **Misconfigured deployment:** DEBUG false, unique secret, HTTPS, ALLOWED_HOSTS, secure cookies.

## Important gaps
- No site/tenant scoping or per-object data isolation.
- Login brute-force protection, complete security logging, immutable audit logs, MFA, production monitoring, backup automation and disaster-recovery drills are not implemented.
- DRF throttling is approximate and should not be considered brute-force protection.
- Server-side role assumptions rely on accurate Group membership administration.
- There is no external security audit or penetration test.

## Preproduction checklist
- Rotate any keys ever committed to Git.
- Set DJANGO_SECRET_KEY with a unique high-entropy value; set DJANGO_DEBUG=0.
- Set DJANGO_ALLOWED_HOSTS and DJANGO_CSRF_TRUSTED_ORIGINS for the deployed hostname.
- Configure TLS termination securely and verify forwarding/proxy headers.
- Use PostgreSQL, regular backups, and test restoration.
- Restrict Django admin access; grant `is_staff` and model permissions only to trusted administrators.
- Define site visibility and least-privilege requirements before real customer data is used.
- Run `python manage.py check --deploy`; review warnings.
- Review dependencies, threat model, and logging retention policies.
