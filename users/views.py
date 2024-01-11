import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from users.models import User
from users.serializers import (AdminUpdateSerializer, LoginSerializer,
                               PasswordResetSerializer, RegistrationSerializer,
                               UserSerializer)

load_dotenv()


class UserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action == "list":
            if self.request.user.role not in [User.Roles.ADMIN, User.Roles.ANALYST]:
                return User.objects.filter(pk=self.request.user.pk)
        return self.queryset

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[AllowAny],
        serializer_class=RegistrationSerializer,
    )
    def signup(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[AllowAny],
        serializer_class=LoginSerializer,
    )
    def signin(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def logout(self, request):
        token = str(request.auth)
        request.user.logout(token)
        return Response(
            {"detail": "Successfully logged out."}, status=status.HTTP_204_NO_CONTENT
        )

    @action(
        detail=False, methods=["patch", "put"], permission_classes=[IsAuthenticated]
    )
    def update_self(self, request):
        user = self.request.user
        update_data = request.data
        serializer = self.get_serializer(instance=user, data=update_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["patch"],
        permission_classes=[IsAuthenticated, IsAdminUser],
        serializer_class=AdminUpdateSerializer,
    )
    def upd_user(self, request, pk):
        user = self.get_object()
        update_data = request.data
        serializer = self.get_serializer(data=update_data, partial=True)
        serializer.is_valid(raise_exception=True)

        allowed_fields = set(update_data.keys()) - {"balance", "role", "is_active"}
        if allowed_fields:
            return Response(
                {"error": f"Unsupported fields: {', '.join(allowed_fields)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if "balance" in update_data:
            user.balance += serializer.validated_data.get("balance")
        if "role" in update_data:
            user.role = serializer.validated_data.get("role")
        if "is_active" in update_data:
            user.is_active = serializer.validated_data.get("is_active")

        user.save()

        return Response(
            {"message": f"User data for {user.username} updated successfully"},
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[AllowAny],
        serializer_class=PasswordResetSerializer,
    )
    def reset_password(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        try:
            user = User.objects.get(email=email)
            token = user.token
            msg = EmailMessage()
            msg["Subject"] = "Reset Password Invitation"
            msg["From"] = "Crypto Team"
            msg["To"] = email

            msg.set_content(f"Change password with such token: {token}")

            with smtplib.SMTP_SSL(
                os.getenv("EMAIL_HOST"), os.getenv("EMAIL_PORT")
            ) as server:
                server.login(
                    os.getenv("EMAIL_HOST_USER"), os.getenv("EMAIL_HOST_PASSWORD")
                )
                server.send_message(msg)

            return Response(
                {"message": "Email sent successfully"}, status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
