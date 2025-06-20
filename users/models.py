from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name=None, is_superuser=False, phone_number=None, address=None, role='user', password=None):
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            full_name=full_name,
            phone_number=phone_number,
            address=address,
            role=role,
            is_staff=(role == 'admin'),
            is_superuser=is_superuser,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('full_name', '')
        extra_fields.setdefault('phone_number', '')
        extra_fields.setdefault('address', '')
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('role') != 'admin':
            raise ValueError('Superuser must have role="admin"')

        return self.create_user(
            email=email,
            password=password,
            full_name=extra_fields.get('full_name'),
            phone_number=extra_fields.get('phone_number'),
            address=extra_fields.get('address'),
            role=extra_fields.get('role'),
            is_superuser=True
        )

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, unique=True)

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    profile_url = models.CharField(max_length=255, default="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} ({self.role})"

    @property
    def is_admin(self):
        return self.role == 'admin'
    
class Province(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class District(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete= models.CASCADE, related_name="districts")

    def __str__(self):
        return self.name
    

class Municipality(models.Model):
    name = models.CharField(max_length=100)
    ward = models.IntegerField(default=35)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name="municipality")


    def __str__(self):
        return self.name
    

class Place(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

class Volunter(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='volunteers')
    email = models.EmailField(unique=True)
    SKILL_CHOICES = (
        ('transportation', 'Transportation'),
        ('rescue', 'Rescue'),
        ('medical', 'Medical'),
    )
    skill = models.CharField(max_length=100, choices=SKILL_CHOICES, null=True, blank=True)