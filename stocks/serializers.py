from rest_framework import serializers

from stocks.models import Crypto, Order, Subscription, Wallet
from stocks.utils import order_params_check
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
    user = serializers.CharField(source="user.username")
    crypto = serializers.CharField(source="crypto.name")

    class Meta:
        model = Order
        fields = [
            "user",
            "crypto",
            "order_type",
            "execution_method",
            "total_price",
            "amount",
            "is_auto",
            "desired_exchange_rate",
        ]

    def to_representation(self, instance):
        representation = super(OrderSerializer, self).to_representation(instance)

        user = self.context["request"].user

        if user.role in [User.Roles.USER]:
            representation.pop("user", None)

        return representation


class CreateOrderSerializer(OrderSerializer):
    user = serializers.CharField(allow_null=True, read_only=True)

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        crypto_name = validated_data["crypto"]
        validated_data["crypto"] = Crypto.objects.get(name=crypto_name["name"])
        order_params_check(validated_data)
        new_order = Order.objects.create(**validated_data)
        return new_order
