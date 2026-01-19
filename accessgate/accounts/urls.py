from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import *
urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('assign-role/', AssignRoleToUserAPI.as_view()),
    path('forgot-password/', ForgotPasswordAPI.as_view()),
    path('reset-password/', ResetPasswordAPI.as_view()),
    path('register/', RegisterAPI.as_view()),
    path('me/', MeAPI.as_view()),
]
