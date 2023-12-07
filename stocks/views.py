from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from stocks.models import Crypto, Order, Subscription, Wallet
from stocks.serializers import (CryptoSerializer, OrderSerializer,
                                SubscriptionSerializer, WalletSerializer)
from users.models import User


class WalletViewSet(
    mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action == "list":
            if self.request.user.role not in [User.Roles.ADMIN, User.Roles.ANALYST]:
                return Wallet.objects.filter(user=self.request.user)
        return self.queryset


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action == "list":
            if self.request.user.role not in [User.Roles.ADMIN, User.Roles.ANALYST]:
                return Order.objects.filter(user=self.request.user)
        return self.queryset

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        serializer_class=OrderSerializer,
    )
    def add(self, request):
        new_order = request.data
        serializer = self.serializer_class(
            data=new_order, context={"request": request}, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CryptoViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Crypto.objects.all()
    serializer_class = CryptoSerializer
    permission_classes = [AllowAny]

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        serializer_class=CryptoSerializer,
    )
    def add(self, request):
        if request.user.is_superuser:
            new_crypto = request.data
            serializer = self.serializer_class(data=new_crypto)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_403_FORBIDDEN)


class SubscriptionViewSet(
    mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        serializer_class=...,
    )
    def add(self, request):
        pass
