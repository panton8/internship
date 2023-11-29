from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        ANALYST = "ANALYST", "Analyst"
        USER = "USER", "User"

    first_name = models.CharField(max_lenght=30)
    last_name = models.CharField(max_lenght=30)
    username = models.CharField(unique=True, max_length=20)
    email = models.EmailField(unique=True, max_length=80)
    role = models.CharField(max_length=7, choices=Roles.choices, default=Roles.USER)
    balance = models.FloatField(default=0.0)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return self.username
