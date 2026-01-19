from django.urls import path
from .views import TestProtectedAPI
from .views import CreateUserAPI


urlpatterns = [
    path('test/', TestProtectedAPI.as_view()),
    path('create-user/', CreateUserAPI.as_view()),
]
