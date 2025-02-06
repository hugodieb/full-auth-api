from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import UserProfile
from .serializers import (
  UserProfileSerializer,
  UserProfileUpdateSerializer,
  UserAvatarUpdateSerializer
)
from djoser.social.views import ProviderAuthView
from rest_framework_simplejwt.views import (
  TokenObtainPairView,
  TokenRefreshView,
  TokenVerifyView
)

class CustomProviderAuthView(ProviderAuthView):
  def post(self, request, *args, **kwargs):
    response = super().post(request, *args, **kwargs)

    if response.status_code == 201:
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
  
class CustomTokenRefreshView(TokenRefreshView):
  def post(self, request, *args, **kwargs):
    refresh_token = request.COOKIES.get('refresh')

    if refresh_token:
      request.data['refresh'] = refresh_token

    response = super().post(request, *args, **kwargs)

    if response.status_code == 200:
      access_token = response.data.get('access')

      response.set_cookie(
        'access',
        access_token,
        max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
        path=settings.AUTH_COOKIE_PATH,
        secure=settings.AUTH_COOKIE_SECURE,
        httponly=settings.AUTH_COOKIE_HTTP_ONLY,
        samesite=settings.AUTH_COOKIE_SAMESITE
      )

    return response
  
class CustomTokenVerifyView(TokenVerifyView):
  def post(self, request, *args, **kwrgs):
    access_token = request.COOKIES.get('access')

    if access_token:
      request.data['token'] = access_token

    return super().post(request, *args, **kwrgs)

class LogoutView(APIView):
  def post(self, request, *args, **kwargs):
    response = Response(status=status.HTTP_204_NO_CONTENT)
    response.delete_cookie('access')
    response.delete_cookie('refresh')

    return response
  
class UserProfileViewSet(viewsets.ModelViewSet):
  queryset = UserProfile.objects.all()
  serializer_class = UserProfileSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    return UserProfile.objects.filter(user=self.request.user)
  
  def get_serializer_class(self, *args, **kwargs):
    if self.action == 'update' or self.action == 'partial_update':
      return UserProfileUpdateSerializer   
    
    return UserProfileSerializer
  
  def list(self, request, *args, **kwargs):
    profile = get_object_or_404(UserProfile, user=request.user)
    serializer = self.get_serializer(profile)
    return Response(serializer.data)
  
  @action(detail=False, methods=['post'], parser_classes=[MultiPartParser, FormParser] )
  def update_avatar(self, request):    
    profile = get_object_or_404(UserProfile, user=request.user)
    serializer = UserAvatarUpdateSerializer(profile, data=request.data, partial=True, context={"request": request})

    if serializer.is_valid():
      if profile.avatar:
        profile.avatar.delete()

      serializer.save()
      return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  @action(detail=False, methods=['get'])
  def investment_info(self, request):
    profile = get_object_or_404(UserProfile, user=request.user)
    data = {
      'investment_experience': profile.investiment_experience,
      'risk_profile': profile.risk_profile
    }
    
    return Response(data)
  
  @action(detail=False, methods=['patch'])
  def update_notifications(self, request):
    profile = get_object_or_404(UserProfile, user=request.user)

    email_notifications = request.data.get('email_notifications')
    sms_notifications = request.data.get('sms_notificatons')

    if email_notifications is not None:
      profile.email_notifications = email_notifications
    if sms_notifications is not None:
      profile.sms_notifications = sms_notifications

    profile.save()

    return Response({
      'email_notifications': profile.email_notifications,
      'sms_notifications': profile.sms_notifications
    })

    
      

    
