# Product Roadmap

## Included in this source package
V0.1: asset registry, work orders, RBAC, basic dashboard and audit events.
V0.2: recurring maintenance plans, plan controls, scheduled work order generation.
V0.3: session-authenticated DRF API with read/write role restrictions, pagination and tests.

## Future enhancements (not implemented)
- Per-site scopes and object-level access control.
- User management UI and approval delegation.
- Better downtime and failure metrics with event timestamps.
- File attachments with malware scanning and access enforcement.
- Reporting exports, analytics and equipment-hour recurrence.
- Token/OAuth integrations and OpenAPI schema.
- Multi-worker scheduling hardening, production monitoring and backup automation.

## Quality gates
Test locally, verify migration consistency, push feature branch, obtain CI pass, review diff, merge via Pull Request.
