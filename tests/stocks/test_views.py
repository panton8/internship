import pytest
from ddf import G
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework import status

from stocks.models import *


class TestCryptoViews:
    @pytest.mark.django_db
    def test_valid_adding(self, default_admin_api):
        data = {"name": "Bitcoin", "code": "BTC"}

        response = default_admin_api.post(reverse("crypto-list"), data=data)

        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.django_db
    def test_invalid_adding(self, default_user_api):
        data = {"name": "Bitcoin", "code": "BTC"}

        response = default_user_api.post(reverse("crypto-list"), data=data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_crypto_list(self, default_user_api, default_crypto):
        url = reverse("crypto-list")

        response = default_user_api.get(url)

        assert response.status_code == 200
        assert len(response.data) == 1

    @pytest.mark.django_db
    def test_crypto_list(self, default_api, default_crypto):
        url = reverse("crypto-list")

        response = default_api.get(url)

        assert response.status_code == 403
        assert (
            response.data["detail"] == "Authentication credentials were not provided."
        )


class TestSubViews:
    @pytest.mark.django_db
    def test_valid_adding(self, default_admin_api, default_user_api):
        data1 = {"name": "Bitcoin", "code": "BTC"}
        data2 = {"crypto": "Bitcoin"}

        default_admin_api.post(reverse("crypto-list"), data=data1)
        response = default_user_api.post(reverse("subscription-list"), data=data2)

        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.django_db
    def test_invalid_adding(self, default_admin_api, default_user_api):
        data1 = {"name": "Bitcoin", "code": "BTC"}
        data2 = {"crypto": "Bitcoin"}

        default_admin_api.post(reverse("crypto-list"), data=data1)
        default_user_api.post(reverse("subscription-list"), data=data2)
        response = default_user_api.post(reverse("subscription-list"), data=data2)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["Info"] == "You already have such crypto in your subs"

    @pytest.mark.django_db
    def test_unsub(self, default_user_api, default_admin_api, default_user):
        data1 = {"name": "Bitcoin", "code": "BTC"}
        data2 = {"crypto": "Bitcoin"}
        urls = [reverse("crypto-list"), reverse("subscription-list")]

        default_admin_api.post(urls[0], data=data1)
        default_user_api.post(urls[1], data=data2)
        urls.append(
            reverse(
                "subscription-detail", args=(Subscription.objects.all().first().pk,)
            )
        )
        response = default_user_api.delete(urls[2])

        assert response.status_code == 204
        assert Subscription.objects.filter(user=default_user).exists() is False

    @pytest.mark.django_db
    def test_valid_list_len(
        self, default_admin_api, default_user_api, default_api, default_user
    ):
        user = G(
            "users.User",
            username="test2",
            email="tes2t@example.com",
            password=make_password("test2"),
        )
        data1 = [
            {"name": "Bitcoin", "code": "BTC"},
            {"name": "Ethereum", "code": "ETH"},
        ]
        data2 = [{"crypto": "Bitcoin"}, {"crypto": "Ethereum"}]
        default_api.credentials(HTTP_AUTHORIZATION=f"Bearer {user.token}")
        urls = [
            reverse("crypto-list"),
            reverse("crypto-list"),
            reverse("subscription-list"),
        ]

        default_admin_api.post(urls[0], data=data1[0])
        default_admin_api.post(urls[1], data=data1[1])
        default_user_api.post(urls[2], data=data2[0])
        default_user_api.post(urls[2], data=data2[1])
        default_api.post(urls[2], data=data2[0])

        response1 = default_user_api.get(urls[2])
        response2 = default_api.get(urls[2])

        assert response1.status_code == 200
        assert len(response1.data) == 2
        assert response2.status_code == 200
        assert len(response2.data) == 1

    @pytest.mark.django_db
    def test_valid_list_after_unsub(
        self, default_user_api, default_admin_api, default_crypto
    ):
        data = {"crypto": "Bitcoin"}
        urls = [reverse("subscription-list")]

        default_user_api.post(urls[0], data=data)
        urls.append(
            reverse(
                "subscription-detail", args=(Subscription.objects.all().first().pk,)
            )
        )
        default_user_api.delete(urls[1])
        response = default_user_api.get(urls[0])

        assert response.status_code == 200
        assert len(response.data) == 0


class TestOrderViews:
    @pytest.mark.django_db
    def test_order_adding(self, default_user_api, default_crypto):
        urls = [reverse("order-list"), reverse("subscription-list")]
        data = {
            "crypto": "Bitcoin",
            "order_type": Order.OrderType.PURCHASE,
            "execution_method": Order.ExecutionMethod.BY_PRICE,
            "total_price": 1000,
            "amount": 1,
        }

        response = default_user_api.post(urls[0], data=data)

        assert response.status_code == 201
        assert (
            response.data["amount"]
            == response.data["total_price"] / default_crypto.exchange_rate
        )


class TestWalletViews:
    @pytest.mark.django_db
    def test_wallet_list(self, default_user_api):
        url = reverse("wallet-list")
        response = default_user_api.get(url)

        assert response.status_code == 200
        assert len(response.data) == 0

    @pytest.mark.django_db
    def test_invalid_wallet_list(self, default_api):
        url = reverse("wallet-list")
        response = default_api.get(url)

        assert response.status_code == 403
        assert (
            response.data["detail"] == "Authentication credentials were not provided."
        )


class TestHistoryViews:
    @pytest.mark.django_db
    def test_history_list(self, default_user_api):
        url = reverse("history-list")
        response = default_user_api.get(url)

        assert response.status_code == 200
        assert len(response.data) == 0

    @pytest.mark.django_db
    def test_invalid_history_list(self, default_api):
        url = reverse("history-list")
        response = default_api.get(url)

        assert response.status_code == 403
        assert (
            response.data["detail"] == "Authentication credentials were not provided."
        )
