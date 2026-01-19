from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import UserRole
from .serializers import UserRoleSerializer
from roles.models import *
from django.contrib.auth.models import User

import uuid
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response

class AssignRoleToUserAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserRoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Role assigned to user"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

password_reset_tokens= {}
class ForgotPasswordAPI(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()

        if not user:
            return Response({"message": "If email exists, link will be sent"})

        token = str(uuid.uuid4())
        password_reset_tokens[token] = user.id

        reset_link = f"http://127.0.0.1:8000/reset/?token={token}"
  
        send_mail(
            "Reset your password",
            f"Click to reset password: {reset_link}",
            "noreply@accessgate.com",
            [email]
        )

        return Response({"message": "Reset link sent"})
    
class ResetPasswordAPI(APIView):
    permission_classes = []

    def post(self, request):
        token = request.data.get("token")
        new_password = request.data.get("password")

        user_id = password_reset_tokens.get(token)
        if not user_id:
            return Response({"error": "Invalid or expired token"}, status=400)

        user = User.objects.get(id=user_id)
        user.set_password(new_password)
        user.save()

        del password_reset_tokens[token]

        return Response({"message": "Password reset successful"})


class RegisterAPI(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password required"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Assign default role
        viewer_role, _ = Role.objects.get_or_create(name="Viewer")
        UserRole.objects.create(user=user, role=viewer_role)

        return Response({"message": "User registered successfully"})
    

class MeAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            role = UserRole.objects.get(user=request.user).role.name
        except:
            role = "No Role"

        return Response({
            "username": request.user.username,
            "role": role
        })
