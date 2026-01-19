from django.urls import path
from .views import RoleAPI, PermissionAPI, AssignPermissionToRoleAPI

urlpatterns = [
    path('roles/', RoleAPI.as_view()),
    path('permissions/', PermissionAPI.as_view()),
    path('assign-permission/', AssignPermissionToRoleAPI.as_view()),
]
