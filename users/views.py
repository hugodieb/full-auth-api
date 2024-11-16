from django.conf import settings
from rest_framework_simplejwt.views import (
  TokenObtainPairView,
  TokenRefreshView,
  TokenVerifyView
)

class CustomTokenObtainPairView(TokenObtainPairView):
  def post(self, request, *args, **kwargs):
    response = super().post(request, *args, **kwargs)

    if response.status_code == 200:
      access_token = response.data.get('access')
      refresh_token = response.data.get('refresh')

      response.set_cookie(
        'access',
        access_token,
        max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
        path=settings.AUTH_COOKIE_PATH,
        secure=settings.AUTH_COOKIE_SECURE,
        httponly=settings.AUTH_COOKIE_HTTP_ONLY,
        samesite=settings.AUTH_COOKIE_SAMESITE
      )

      response.set_cookie(
        'refresh',
        refresh_token,
        max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
        path=settings.AUTH_COOKIE_PATH,
        secure=settings.AUTH_COOKIE_SECURE,
        httponly=settings.AUTH_COOKIE_HTTP_ONLY,
        samesite=settings.AUTH_COOKIE_SAMESITE
      )

    return response