# REST API Reference — v1

Base: `/api/v1/` — Django REST Framework, session authentication and CSRF protection for unsafe methods. Responses use JSON by default; the browsable API is enabled. No public token issuance endpoint is included.

## Resource endpoints
| Method | URL | Access | Notes |
|---|---|---|---|
| GET | `/api/v1/assets/` | Signed-in | Paginated; `?search=` and `?status=` |
| GET | `/api/v1/assets/{id}/` | Signed-in | 404 if missing |
| POST | `/api/v1/assets/` | Admin, Supervisor | Register asset |
| PATCH | `/api/v1/assets/{id}/` | Admin, Supervisor | Partial edit |
| GET | `/api/v1/work-orders/` | Signed-in | Paginated; `?status=` and `?priority=` |
| GET | `/api/v1/work-orders/{id}/` | Signed-in | Read order |
| POST | `/api/v1/work-orders/` | Admin, Supervisor, Technician | Technician is auto-assigned self |
| POST | `/api/v1/work-orders/{id}/resolution/` | Manager or assigned technician | `resolution_notes` required field |
| POST | `/api/v1/work-orders/{id}/transition/` | Manager or assigned technician | Valid target status and business rules |
| GET | `/api/v1/maintenance-plans/` | Signed-in | Paginated; `?active=true/false` |
| GET | `/api/v1/maintenance-plans/{id}/` | Signed-in | Plan details |
| POST | `/api/v1/maintenance-plans/` | Admin, Supervisor | Create plan |
| PATCH | `/api/v1/maintenance-plans/{id}/` | Admin, Supervisor | Modify or pause plan |

DELETE and PUT are intentionally not exposed by the current API. No bulk-write endpoint.

## Example payloads
Create asset:
```json
{"code":"PMP-200","name":"Cooling Pump","location":"Plant A","status":"operational","criticality":"high"}
```
Create maintenance plan:
```json
{"asset":1,"title":"Monthly inspection","instructions":"Check seals and vibration","interval_days":30,"next_due":"2026-11-15","is_active":true,"priority":"medium","assigned_to":null}
```
Transition work order:
```json
{"status":"in_progress","note":"Inspection started"}
```
Resolution:
```json
{"resolution_notes":"Inspected seals and verified vibration"}
```

## HTTP codes
- `200`: successful read, edit or transition.
- `201`: created.
- `400`: invalid data or invalid transition.
- `401/403`: unauthenticated or forbidden, depending on authentication scheme; session-only DRF often returns 403.
- `404`: unknown resource.
- `405`: unsupported HTTP method.
- `429`: throttle exceeded (throttling is best-effort, not a security rate limiter).

## Pagination
DRF page-number pagination returns `count`, `next`, `previous`, and `results`, with 25 records per page. `?page=2` accesses subsequent pages.

## Authentication and CSRF
Log in at `/accounts/login/` using a browser session. `POST` and `PATCH` with SessionAuthentication need the `csrftoken` cookie and `X-CSRFToken` header when used from a browser. For production integrations, design a separate reviewed machine-to-machine authentication mechanism; do not disable CSRF or embed passwords in source.

## Security caveat
Read access is currently broad for signed-in users. Site-level filtering and object-level authorization are not yet implemented, so do not deploy for segregated customers or confidential facilities.
