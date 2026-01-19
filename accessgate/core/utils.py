from accounts.models import UserRole
from roles.models import RolePermission
from .models import AuditLog

def log_action(user, action, endpoint):
    AuditLog.objects.create(
        user=user,
        action=action,
        endpoint=endpoint
    )


def user_has_permission(user, permission_code):
    try:
        user_role = UserRole.objects.get(user=user)
    except UserRole.DoesNotExist:
        return False

    return RolePermission.objects.filter(
        role=user_role.role,
        permission__code=permission_code
    ).exists()
