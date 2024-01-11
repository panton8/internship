import pytest

from users.models import User
from users.serializers import (AdminUpdateSerializer, LoginSerializer,
                               PasswordResetSerializer, RegistrationSerializer,
                               UserSerializer)


@pytest.fixture
def user_data():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
    }


class TestUserSerializer:
    @pytest.mark.django_db
    def test_user_serializer(self, user_data):
        serializer = UserSerializer(data=user_data)

        assert serializer.is_valid()
        for key in serializer.validated_data:
            assert serializer.validated_data[key] == user_data[key]
        assert serializer.data == user_data
        assert serializer.errors == {}

    def test_invalid_user_serializer(self):
        serializer = UserSerializer(data={"email": "", "username": "", "password": ""})

        assert not serializer.is_valid()


class TestLoginSerializer:
    @pytest.mark.django_db
    def test_login_serializer(self, default_user):
        serializer = LoginSerializer(
            data={"email": "test@gmail.com", "password": "test"}
        )

        assert serializer.is_valid()
        assert serializer.validated_data["email"] == default_user.email
        assert "token" in serializer.validated_data

    @pytest.mark.django_db
    def test_invalid_login_serializer(self, default_user):
        serializer = LoginSerializer(
            data={"email": "test2@gmail.com", "password": "test"}
        )

        assert not serializer.is_valid()


class TestAdminUpdateSerializer:
    def test_admin_update_serializer(self):
        data = {"balance": 200, "role": User.Roles.ADMIN, "is_active": False}

        serializer = AdminUpdateSerializer(data=data)

        assert serializer.is_valid()
        for key in serializer.validated_data:
            assert serializer.validated_data[key] == data[key]
        assert serializer.data == data
        assert serializer.errors == {}

    def test_invalid_admin_update_serializer(self):
        data = {"balance": 200, "role": "Football player", "is_active": False}

        serializer = AdminUpdateSerializer(data=data)

        assert not serializer.is_valid()


class TestResetPasswordSerializer:
    def test_password_reset_serializer(self):
        data = {"email": "test@example.com"}

        serializer = PasswordResetSerializer(data=data)

        assert serializer.is_valid()
        for key in serializer.validated_data:
            assert serializer.validated_data[key] == data[key]
        assert serializer.data == data
        assert serializer.errors == {}

    def test_invalid_password_reset_serializer(self):
        data = {"email": "test"}

        serializer = PasswordResetSerializer(data=data)

        assert not serializer.is_valid()


class TestRegistrationSerializer:
    @pytest.mark.django_db
    def test_registration_serializer(self, user_data):
        serializer = RegistrationSerializer(data=user_data)

        assert serializer.is_valid()
        for key in serializer.validated_data:
            assert serializer.validated_data[key] == user_data[key]
        assert serializer.errors == {}

    def test_invalid_registration_serializer(self):
        data = {"email": "test"}

        serializer = RegistrationSerializer(data=data)

        assert not serializer.is_valid()
