from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from apps.users.views import register

urlpatterns = [
    path("auth/token/", obtain_auth_token, name="auth-token"),
    path("users/", register, name="user-register"),
]
