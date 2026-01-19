from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Role, Permission, RolePermission
from .serializers import (
    RoleSerializer,
    PermissionSerializer,
    RolePermissionSerializer
)

from core.permissions import HasAPIPermission


# ----------------- ROLES -----------------

class RoleAPI(APIView):
    permission_classes = [HasAPIPermission]
    required_permission = "MANAGE_ROLES"

    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------- PERMISSIONS -----------------

class PermissionAPI(APIView):
    permission_classes = [HasAPIPermission]
    required_permission = "MANAGE_ROLES"

    def get(self, request):
        permissions = Permission.objects.all()
        serializer = PermissionSerializer(permissions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------- ROLE ↔ PERMISSION -----------------

class AssignPermissionToRoleAPI(APIView):
    permission_classes = [HasAPIPermission]
    required_permission = "MANAGE_ROLES"

    def post(self, request):
        serializer = RolePermissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Permission assigned to role"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
