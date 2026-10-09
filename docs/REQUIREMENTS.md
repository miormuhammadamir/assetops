# Requirements — MVP

## User problem
Maintenance teams need a central list of physical equipment and a traceable mechanism to record, assign and approve maintenance tasks.

## Personas
- Supervisor: creates assets and approves completed work
- Technician: records assigned maintenance and resolution notes
- Viewer: monitors work order status

## In scope
Asset registry, work order lifecycle, simple dashboard, Django authentication/groups, audit status events.

## Non-functional requirements
Authenticated requests, CSRF protection, server-side authorization, unique asset codes, referential integrity, transactional transitions, basic automated tests.

## Out of scope (0.1)
Preventive recurrence scheduling, attachments, email notifications, PDF reports, multi-tenant access, public API, inventory parts, mobile application, production SSO.

## Acceptance criteria
1. Supervisors can register assets and assign work orders.
2. Technicians can update assigned work, but cannot approve.
3. Review requires resolution notes and approval is supervisor-only.
4. Each status transition produces an audit event.
5. Viewers cannot create or modify records.
