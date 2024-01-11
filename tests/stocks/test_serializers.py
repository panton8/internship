import pytest

from stocks.models import Order
from stocks.serializers import (AddSubscriptionSerializer,
                                CreateOrderSerializer, CryptoSerializer,
                                HistorySerializer, OrderSerializer,
                                SubscriptionSerializer, WalletSerializer)


class TestCryptoSerializer:
    @pytest.mark.django_db
    def test_crypto_serializer(self):
        data = {
            "name": "Bitcoin",
            "code": "BTC",
            "capacity": 8456,
            "exchange_rate": 44798.56,
        }

        serializer = CryptoSerializer(data=data)

        assert serializer.is_valid()
        for key in serializer.validated_data:
            assert serializer.validated_data[key] == data[key]
        assert serializer.data == data
        assert serializer.errors == {}

    @pytest.mark.django_db
    def test_invalid_crypto_serializer(self):
        data = {
            "name": "Bitcoin",
            "code": "BTC",
            "capacity": "crypto_capacity",
            "exchange_rate": 44798.56,
        }

        serializer = CryptoSerializer(data=data)

        assert not serializer.is_valid()


class TestOrderSerializer:
    @pytest.mark.django_db
    def test_order_serializer(self, default_user, default_crypto):
        data = {
            "user": default_user.username,
            "crypto": default_crypto.name,
            "order_type": Order.OrderType.PURCHASE,
            "execution_method": Order.ExecutionMethod.BY_PRICE,
            "total_price": 87542,
            "amount": 12,
        }

        serializer = OrderSerializer(data=data)

        assert serializer.is_valid()

    @pytest.mark.django_db
    def test_invalid_order_serializer(self, default_user, default_crypto):
        data = {
            "user": default_user.username,
            "crypto": default_crypto.name,
            "order_type": "new_type",
            "execution_method": Order.ExecutionMethod.BY_PRICE,
            "total_price": 87542,
            "amount": 12,
        }

        serializer = OrderSerializer(data=data)

        assert not serializer.is_valid()


class TestSubscriptionSerializer:
    @pytest.mark.django_db
    def test_sub_serializer(self):
        data = {"crypto": {"name": "Ethereum", "code": "ETH"}}

        serializer = SubscriptionSerializer(data=data)

        assert serializer.is_valid()
        assert serializer.errors == {}

    @pytest.mark.django_db
    def test_invalid_sub_serializer(self, default_crypto):
        data = {"crypto": {"name": default_crypto.name, "code": default_crypto.name}}

        serializer = SubscriptionSerializer(data=data)

        assert not serializer.is_valid()


class TestHistorySerializer:
    @pytest.mark.django_db
    def test_history_serializer(self):
        data = {
            "username": "test_user",
            "crypto_name": "Bitcoin",
            "total_price": 4615,
            "amount": 0.752,
            "order_type": Order.OrderType.PURCHASE,
            "execution_method": Order.ExecutionMethod.BY_PRICE,
            "exchange_rate": 45865.47,
        }

        serializer = HistorySerializer(data=data)

        assert serializer.is_valid()
        assert serializer.errors == {}


class TestWalletSerializer:
    @pytest.mark.django_db
    def test_wallet_serializer(self, default_crypto):
        data = {"crypto": "Ethereum", "amount": 0.752}

        serializer = WalletSerializer(data=data)

        assert serializer.is_valid()

    @pytest.mark.django_db
    def test_invalid_wallet_serializer(self, default_crypto):
        data = {"crypto": {"name": default_crypto.name, "code": default_crypto.name}}

        serializer = WalletSerializer(data=data)

        assert not serializer.is_valid()


class TestAddSubscriptionSerializer:
    @pytest.mark.django_db
    def test_sub_serializer(self, default_user, default_crypto):
        data = {"user": default_user, "crypto": "Ethereum"}

        serializer = AddSubscriptionSerializer(data=data)

        assert serializer.is_valid()
        assert serializer.validated_data["crypto"]["name"] == data["crypto"]

    @pytest.mark.django_db
    def test_invalid_wallet_serializer(self, default_crypto):
        data = {"user": "user", "crypto": "Ethereum"}

        serializer = WalletSerializer(data=data)

        assert not serializer.is_valid()


class TestCreateOrderSerializer:
    @pytest.mark.django_db
    def test_order_serializer(self, default_user, default_crypto):
        data = {
            "user": default_user,
            "crypto": "Ethereum",
            "order_type": Order.OrderType.PURCHASE,
            "execution_method": Order.ExecutionMethod.BY_PRICE,
            "total_price": 7500,
            "amount": 1,
        }

        serializer = CreateOrderSerializer(data=data)

        assert serializer.is_valid()
        assert serializer.validated_data["order_type"] == data["order_type"]
        assert serializer.validated_data["execution_method"] == data["execution_method"]
        assert serializer.errors == {}

    @pytest.mark.django_db
    def test_invalid_order_serializer(self, default_user, default_crypto):
        data = {
            "user": default_user,
            "crypto": "Ethereum",
            "order_type": "TEST",
            "execution_method": Order.ExecutionMethod.BY_PRICE,
            "total_price": 7500,
            "amount": 1,
        }

        serializer = CreateOrderSerializer(data=data)

        assert not serializer.is_valid()
