from rest_framework.permissions import BasePermission, SAFE_METHODS
from operations.permissions import has_role

class ManagerWritePermission(BasePermission):
    """All authenticated users can read; only managers can mutate."""
    def has_permission(self, request, view):
        return (request.user.is_authenticated and (
            request.method in SAFE_METHODS or has_role(request.user, 'Admin', 'Supervisor')
        ))

class WorkOrderPermission(BasePermission):
    """Authenticated readers; managers and technicians may create orders."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.method in SAFE_METHODS or has_role(request.user, 'Admin', 'Supervisor', 'Technician')
        )
