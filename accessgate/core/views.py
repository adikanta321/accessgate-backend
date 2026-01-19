from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .permissions import HasAPIPermission
from django.shortcuts import render
from .utils import log_action
from .permissions import require_permission, HasAPIPermission

class CreateUserAPI(APIView):
    permission_classes = [IsAuthenticated, HasAPIPermission]
    required_permission = "CREATE_USER"

    def post(self, request):
        log_action(request.user, "CREATE_USER", request.path)
        return Response({"message": "User created (fake API)"})


class TestProtectedAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "message": "JWT is working",
            "user": request.user.username
        })
    
def home(request):
    return render(request, "login.html")

def dashboard(request):
    return render(request, "dashboard.html")

@require_permission("MANAGE_ROLES")
def roles_page(request):
    return render(request, "roles.html")

@require_permission("MANAGE_ROLES")
def permissions_page(request):
    return render(request, "permissions.html")

def forgot_page(request):
    return render(request, "forgot.html")

def reset_page(request):
    return render(request, "reset.html")

def register_page(request):
    return render(request, "register.html")
