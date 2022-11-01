from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.text import slugify
from django.contrib.auth.hashers import make_password
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

# from .validators import UnicodeUsernameValidators

# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, gender, password=None):
        if not username:
            raise ValueError("User must have a username")
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(username=username, first_name=first_name,
                          last_name=last_name, gender=gender, email=self.normalize_email(email))
        # user.password = make_password(password)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(first_name=first_name, last_name=last_name,
                                username=username, email=self.normalize_email(email), password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superadmin = True
        user.is_active = True
        user.save(using=self._db)

        return user


class ApplicantManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_applicant=True)


class AdminManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_admin=True)


class Account(AbstractBaseUser):
    GENDER_CHOICES = (
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE'),
        # ('NON-BINARY', 'NON-BINARY')
    )
    # username_validator = UnicodeUsernameValidators
    first_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True, db_index=True)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(
        max_length=100, choices=GENDER_CHOICES, default="MALE")
    email = models.EmailField(max_length=100, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=True)
    # is_superadmin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # is_applicant = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name", "username", ]
    objects = MyAccountManager()
    admin_objects = AdminManager()
    applicant_objects = ApplicantManager()
