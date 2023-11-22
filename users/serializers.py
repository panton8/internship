from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "password", "role", "balance", "is_active"]


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password", "token"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True)
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        if email is None:
            raise serializers.ValidationError("Email must be set")

        if password is None:
            raise serializers.ValidationError("Password must be set")

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError("Email or password are incorrect")

        if not user.is_active:
            raise serializers.ValidationError("User in blocklist now")

        return {"email": user.email, "username": user.username, "token": user.token}
