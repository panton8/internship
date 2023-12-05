from rest_framework import serializers

from stocks.models import Crypto, Order, Subscription, Wallet
from users.models import User
from users.serializers import UserSerializer


class CryptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crypto
        fields = ["name", "capacity", "exchange_rate"]


class WalletSerializer(serializers.ModelSerializer):
    crypto = CryptoSerializer().fields.get("name")

    class Meta:
        model = Wallet
        fields = ["crypto", "amount"]


class SubscriptionSerializer(serializers.ModelSerializer):
    user = UserSerializer().fields.get("username")
    crypto = CryptoSerializer().fields.get("name")

    class Meta:
        model = Subscription
        fields = ["user", "crypto"]


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer().fields.get("username")
    crypto = CryptoSerializer().fields.get("name")

    class Meta:
        model = Order
        fields = ["user", "crypto", "order_type", "total_price", "amount", "is_auto"]

    def to_representation(self, instance):
        representation = super(OrderSerializer, self).to_representation(instance)

        user = self.context["request"].user

        if user.role in [User.Roles.USER]:
            representation.pop("user", None)

        return representation
