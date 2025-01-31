from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'email', 'first_name', 'last_name', 'is_active')
    read_only_fields = ('id', 'is_active')

class UserProfileSerializer(serializers.ModelSerializer):
  user = serializers.PrimaryKeyRelatedField(read_only=True)
  first_name = serializers.SerializerMethodField()
  last_name = serializers.SerializerMethodField()
  full_name = serializers.SerializerMethodField()

  class Meta:
    model = UserProfile
    fields = '__all__'
    read_only_fields = ('user', 'created_at', 'updated_ate')

  def get_first_name(self, obj) :
    return obj.user.first_name if obj.user else None
  
  def get_last_name(self, obj) :
    return obj.user.last_name if obj.user else None

  def get_full_name(self, obj):
    return obj.user.get_full_name()
  
  def validate_age(self, value):
    if value and (value < 18 or value > 120):
      raise serializers.ValidationError("A idade deve estar entre 18 e 120 anos de idade.")
    return value
  
  def validate_birth_date(self, value):
    if value:
      age = UserProfile.get_age(value)
      if age < 18:
        raise serializers.ValidationError("O usuário deve ter pelo menos 18 anos de idade.")
      
class UserProfileUpdateSerializer(UserProfileSerializer):
  class Meta(UserProfileSerializer.Meta):
    read_only_fields = UserProfileSerializer.Meta.read_only_fields + ('avatar',)

class UserAvatarUpdateSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserProfile
    fields = ('avatar')