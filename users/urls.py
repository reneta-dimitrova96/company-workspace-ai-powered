from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import OwnerRegisterView

urlpatterns = [
    path("auth/register-owner/", OwnerRegisterView.as_view(), name="register-owner"),
    path("auth/login/", TokenObtainPairView.as_view(), name="login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
