from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,  PermissionsMixin
from django.utils import timezone
from .validators.validations import validate_cpf, validate_phone, validate_min_value, validate_max_value


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(
            email=email,
            **kwargs,
        )

        user.set_password(password)
        user.save(using=self._db)

        Subscription.objects.create(user=user, plan_type='BEAR')

        UserProfile.objects.create(user=user)

        return user

    def create_superuser(self, email, password=None, **kwargs):
        
        user = self.create_user(
            email,
            password=password,
            **kwargs
            
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    update_ate = models.DateTimeField(auto_now=True)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_prof(self):
        return hasattr(self, 'subscription') and self.subscription.is_pro

class UserProfile(models.Model):
    def avatar_path(instance, filename):
        return f'avatars/{instance.user.id}/{filename}'
    
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, related_name='profile')
    cpf = models.CharField(max_length=11, unique=True,)
    birth_date = models.DateField(null=True, blank=True)
    age = models.PositiveBigIntegerField(validators=[
        validate_min_value(18),
        validate_max_value(120)
    ],
    null=True,
    blank=True
    )
    gender = models.CharField(
        max_length=20,
        choices=[
            ('M', 'Masculino'),
            ('F', 'Feminino'),
            ('O', 'Outro'),
            ('N', 'Prefiro não informar')
        ],
        null=True,
        blank=True
    )
    avatar = models.ImageField(upload_to=avatar_path, null=True, blank=True)

    #Informações de endereço
    address = models.CharField(max_length=255, blank=True, null=True)
    address_number = models.CharField(max_length=10, blank=True, null=True)
    complement = models.CharField(max_length=100, null=True, blank=True)
    neighborhood = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)

    profession = models.CharField(max_length=30, null=True, blank=True)
    company = models.CharField(max_length=20, null=True, blank=True)

    investiment_experience = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Iniciante'),
            ('Intermediate', 'Intermediário'),
            ('advanced', 'Avançado')
        ],
        default='beginner'
    )

    risk_profile = models.CharField(
        max_length=20,
        choices=[
            ('conservative', 'Conservador'),
            ('moderate', 'Moderador'),
            ('aggressive', 'Agressivo')
        ],
        default='moderate'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Perfil do Usuário'
        verbose_name_plural = 'Perfis dos Usuários'

    def __str__(self):
        return f"Perfil de {self.user.get_full_name()}"
        
    def get_age(self):
        if self.birth_date:
            today = timezone.now().date()
            return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
        return None
    
    def save(self, *args, **kwargs):
        if self.birth_date and not self.age:
            self.age = self.get_age()
        super().save(*args, **kwargs)

class Subscription(models.Model): 
    PLAN_TYPES = [
        ('BEAR', 'Gratuito'),
        ('BULL', 'Profissional'),
        ('WOLF', 'Trader')
    ]

    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, related_name='subscription')
    plan_type = models.CharField(max_length=10, choices=PLAN_TYPES, default='BEAR')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    last_payment_date = models.DateTimeField(null=True, blank=True)
    next_payment_date = models.DateTimeField(null=True, blank=True)

    def is_pro(self):
        return self.plan_type in ['BULL', 'WOLF'] and self.is_active and (self.end_date is None or self.end_date > timezone.now())






    