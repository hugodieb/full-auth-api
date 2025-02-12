from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import (
  CustomProviderAuthView,
  CustomTokenObtainPairView,
  CustomTokenRefreshView,
  CustomTokenVerifyView,
  LogoutView,
  UserProfileViewSet
)

router = DefaultRouter()
router.register('profile', UserProfileViewSet, basename='profile')

urlpatterns = [
  re_path(
    r'^o/(?P<provider>\S+)/$', CustomProviderAuthView.as_view(), name='provider-auth'
  ),
  path('jwt/create/', CustomTokenObtainPairView.as_view()),
  path('jwt/refresh/', CustomTokenRefreshView.as_view()),
  path('jwt/verify/', CustomTokenVerifyView.as_view()),
  path('logout/', LogoutView.as_view()),

  path('', include(router.urls)),
] 