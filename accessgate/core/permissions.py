from rest_framework.permissions import BasePermission
from accounts.models import UserRole
from roles.models import RolePermission

# -------- API PERMISSION --------
class HasAPIPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        required_permission = getattr(view, "required_permission", None)
        if not required_permission:
            return True

        return user_has_permission(request.user, required_permission)


# -------- SHARED LOGIC --------
def user_has_permission(user, permission_name):
    roles = UserRole.objects.filter(user=user).values_list("role", flat=True)
    return RolePermission.objects.filter(
        role_id__in=roles,
        permission__code=permission_name).exists()


# -------- PAGE (UI) PERMISSION --------
from django.shortcuts import redirect

def require_permission(permission):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("/")
            if not user_has_permission(request.user, permission):
                return redirect("/dashboard/")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
