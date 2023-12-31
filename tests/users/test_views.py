import pytest
from ddf import G
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework import status

from users.models import User


class TestSignup:
    @pytest.mark.django_db
    def test_valid_signup(self, default_api):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
        }
        url = reverse("user-signup")

        response = default_api.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert "token" in response.data

    def test_invalid_signup(self, default_api):
        data = {
            "username": "",
            "email": "test2@example.com",
            "password": "test2password",
        }
        url = reverse("user-signup")

        response = default_api.post(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestSignin:
    @pytest.mark.django_db
    def test_valid_signin(self, default_api, default_user):
        data = {"email": "test@gmail.com", "password": "test"}
        url = reverse("user-signin")

        response = default_api.post(url, data=data)

        assert response.status_code == status.HTTP_200_OK
        assert "token" in response.data

    @pytest.mark.django_db
    def test_invalid_signin(self, default_api, default_user):
        data = {"email": "test2@gmail.com", "password": "test"}
        url = reverse("user-signin")

        response = default_api.post(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "token" not in response.data


class TestLogout:
    @pytest.mark.django_db
    def test_valid_logout(self, default_api):
        user = G(
            "users.User",
            username="test",
            email="test@example.com",
            password=make_password("testpassword"),
        )
        default_api.credentials(HTTP_AUTHORIZATION=f"Bearer {user.token}")

        response = default_api.post(reverse("user-logout"))

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data["detail"] == "Successfully logged out."

    @pytest.mark.django_db
    def test_invalid_logout(self, default_api):
        response = default_api.post(reverse("user-logout"))

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "detail" in response.data
        assert (
            response.data["detail"] == "Authentication credentials were not provided."
        )


class TestUpdateUserByAdmin:
    @pytest.mark.django_db
    def test_valid_update(self, default_admin_api, default_user):
        data = {"balance": 1000, "role": User.Roles.ANALYST}
        url = reverse("user-upd-user", args=(default_user.pk,))

        response = default_admin_api.patch(url, data=data)

        assert response.status_code == status.HTTP_200_OK
        default_user.refresh_from_db()
        assert (
            default_user.balance == data["balance"]
            and default_user.role == data["role"]
        )

    @pytest.mark.django_db
    def test_invalid_update(self, default_user_api, default_user):
        data = {"balance": 1000, "role": User.Roles.ANALYST}
        url = reverse("user-upd-user", args=(default_user.pk,))

        response = default_user_api.patch(url, data=data)

        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestUserList:
    @pytest.mark.django_db
    def test_user_list(self, default_admin_api, default_user_api, default_api):
        user = G(
            "users.User",
            username="user",
            email="user@gmail.com",
            password=make_password("user"),
        )
        url = reverse("user-list")
        default_api.credentials(HTTP_AUTHORIZATION=f"Bearer {user.token}")

        admin_response = default_admin_api.get(url)
        user1_response = default_user_api.get(url)
        user2_response = default_api.get(url)

        assert len(admin_response.data) == 3
        assert len(user1_response.data) == 1
        assert len(user2_response.data) == 1


class TestUpdateUser:
    @pytest.mark.django_db
    def test_update(self, default_user_api, default_user):
        data = {"username": "test2", "balance": 1000, "role": User.Roles.ANALYST}
        url = reverse("user-update-self")

        response = default_user_api.patch(url, data=data)

        assert response.status_code == status.HTTP_200_OK
        default_user.refresh_from_db()
        assert default_user.balance == 0
        assert default_user.role == User.Roles.USER
        assert default_user.username == "test2"
