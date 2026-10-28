# Functional and Nonfunctional Requirements

## Actors
- Admin and Supervisor: register assets, manage preventive plans, create and approve/cancel work orders.
- Technician: see equipment and orders, create self-assigned orders, update assigned work, supply resolution notes.
- Viewer: read-only access to operational data.
- Anonymous visitor: must log in.

## Functional requirements
FR-01: sign in and out using Django session authentication.
FR-02: register assets with unique equipment codes, location, status and criticality.
FR-03: search assets and view operational dashboard.
FR-04: create work orders and assign only active Technician-group users.
FR-05: enforce transitions Open -> In progress -> Review -> Completed, with permitted rework/cancellation.
FR-06: require resolution notes before review.
FR-07: restrict completion and cancellation to manager roles.
FR-08: store status-change events.
FR-09: create/pause maintenance plans using interval days and next due date.
FR-10: generate due work orders via management command; prevent duplicate occurrences for the same plan/date.
FR-11: serve asset, work-order and plan data at `/api/v1/`.
FR-12: enforce authentication and role-based write restrictions in API and HTML.

## Nonfunctional requirements
NFR-01: secrets supplied via environment variables; never commit production credentials.
NFR-02: request inputs validated server-side.
NFR-03: migrations and automated tests checked in CI.
NFR-04: development uses SQLite; PostgreSQL recommended for multi-user deployment.
NFR-05: database backups and an operator-run restoration procedure required before production.
NFR-06: use HTTPS in production; harden hosts, proxies, cookies and CSRF settings.
NFR-07: monitoring, login throttling and access scopes are future production requirements.

## Acceptance criteria
- Full test suite passes on developer machine and GitHub Actions.
- Unauthenticated API request is denied.
- Technician cannot create/update asset or assign a work order to another user.
- Technician cannot approve completed work; manager can.
- Re-running scheduler does not duplicate a plan/date work order.
- API POST/PATCH validates model constraints.
