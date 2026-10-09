from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from functools import wraps
MANAGERS={'Admin','Supervisor'}
def has_role(user,*roles):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name__in=roles).exists())
def roles_required(*roles):
    def outer(view):
        @login_required
        @wraps(view)
        def wrapped(request,*args,**kwargs):
            if not has_role(request.user,*roles):raise PermissionDenied('Insufficient permissions')
            return view(request,*args,**kwargs)
        return wrapped
    return outer
