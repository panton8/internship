from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.cache import cache
from django.db import models

from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        ANALYST = "ANALYST", "Analyst"
        USER = "USER", "User"

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

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode(
            {"id": self.pk, "exp": int(dt.strftime("%s"))},
            settings.SECRET_KEY,
            algorithm="HS256",
        )
        return token.decode("utf-8")

    def logout(self, token):
        current_time = datetime.now().strftime("%s")
        cache.set(
            token, "blacklisted", timeout=int(self._get_exp(token)) - int(current_time)
        )

    def _get_exp(self, token):
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded.get("exp")

    def is_token_blacklisted(self, token):
        return cache.get(token) == "blacklisted"
