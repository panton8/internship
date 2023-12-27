import pytest
from ddf import G
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient

from users.models import User


@pytest.fixture
def default_user():
    user = G(
        "users.User",
        username="test",
        email="test@gmail.com",
        password=make_password("test"),
    )
    return user


@pytest.fixture
def default_user_api(default_user):
    client = APIClient()
    client.force_authenticate(user=default_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {default_user.token}")
    return client


@pytest.fixture
def default_admin():
    admin = G(
        "users.User",
        username="admin",
        email="admin@gmail.com",
        password=make_password("admin"),
        is_staff=True,
        is_superuser=True,
        role=User.Roles.ADMIN,
    )
    return admin


@pytest.fixture
def default_admin_api(default_admin):
    client = APIClient()
    client.force_authenticate(user=default_admin)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {default_admin.token}")
    return client


@pytest.fixture
def default_api():
    client = APIClient()
    return client
