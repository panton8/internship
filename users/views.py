from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from users.models import User
from users.serializers import (AdminUpdateSerializer, LoginSerializer,
                               RegistrationSerializer, UserSerializer)


class UserViewSet(
    mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

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
        detail=True,
        methods=["patch"],
        permission_classes=[IsAuthenticated, IsAdminUser],
        serializer_class=AdminUpdateSerializer,
    )
    def update_user(self, request, pk):
        user = self.get_object()
        update_data = request.data
        serializer = self.serializer_class(data=update_data, partial=True)
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
