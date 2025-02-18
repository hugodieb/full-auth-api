from datetime import date
import re
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile
from .validators.validations import validate_cpf

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'email', 'first_name', 'last_name', 'is_active')
    read_only_fields = ('id', 'is_active')

class UserProfileSerializer(serializers.ModelSerializer):
  user = serializers.PrimaryKeyRelatedField(read_only=True)
  first_name = serializers.CharField(source="user.first_name", required=False)
  last_name = serializers.CharField(source="user.last_name", required=False)
  full_name = serializers.SerializerMethodField()

  class Meta:
    model = UserProfile
    fields = '__all__'
    read_only_fields = ('user', 'created_at', 'update_at')

  def validate_cpf(self, value):       
        
        try:
            is_valid = validate_cpf(value)            
            if not is_valid:
                raise serializers.ValidationError("CPF inválido.")
            return value
        except Exception as e:            
            raise serializers.ValidationError(f"Erro ao validar CPF: {str(e)}")  

  def get_full_name(self, obj):
    return obj.user.get_full_name()
  
  def validate_age(self, value):
    if value and (value < 18 or value > 120):
      raise serializers.ValidationError("A idade deve estar entre 18 e 120 anos de idade.")
    return value
  
  def validate_birth_date(self, value):
    if value:
      today = date.today()
      age = today.year -value.year - ((today.month, today.day) < (value.month, value.day))
      return value
    return None
  
  def update(self, instance, validated_data):     
     user_data = validated_data.pop("user", {})
     
     if user_data:
        for attr, value in user_data.items():           
           setattr(instance.user, attr, value)
        instance.user.save()

     return super().update(instance, validated_data)      
      
class UserProfileUpdateSerializer(UserProfileSerializer):
  class Meta(UserProfileSerializer.Meta):
    read_only_fields = UserProfileSerializer.Meta.read_only_fields + ('avatar',)

class UserAvatarUpdateSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserProfile
    fields = ('avatar',)