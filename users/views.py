from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from stocks.serializers import AdditionalBalanceSerializer
from users.models import User
from users.serializers import (LoginSerializer, RegistrationSerializer,
                               UserSerializer)


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
        detail=False,
        methods=["patch"],
        permission_classes=[IsAuthenticated],
        serializer_class=AdditionalBalanceSerializer,
    )
    def fillup(self, request):
        additional_balance = request.data
        serializer = self.serializer_class(data=additional_balance)
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.balance += serializer.data.get("additional_balance")
        user.save()

        return Response(
            {"message": "Balance updated successfully"}, status=status.HTTP_200_OK
        )
