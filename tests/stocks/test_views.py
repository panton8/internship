import pytest
from ddf import G
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework import status

from stocks.models import Order, Subscription


class TestCryptoViews:
    @pytest.mark.django_db
    def test_valid_adding(self, default_admin_api, crypto_data):
        response = default_admin_api.post(reverse("crypto-list"), data=crypto_data)

        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.django_db
    def test_invalid_adding(self, default_user_api, crypto_data):
        response = default_user_api.post(reverse("crypto-list"), data=crypto_data)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_crypto_list(self, default_user_api, default_crypto):
        url = reverse("crypto-list")

        response = default_user_api.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    @pytest.mark.django_db
    def test_crypto_list(self, default_api, default_crypto):
        url = reverse("crypto-list")

        response = default_api.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            response.data["detail"] == "Authentication credentials were not provided."
        )


class TestSubViews:
    @pytest.mark.django_db
    def test_valid_adding(self, default_admin_api, default_user_api, crypto_data):
        data = {"crypto": "Bitcoin"}

        default_admin_api.post(reverse("crypto-list"), data=crypto_data)
        response = default_user_api.post(reverse("subscription-list"), data=data)

        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.django_db
    def test_invalid_adding(self, default_admin_api, default_user_api, crypto_data):
        data = {"crypto": "Bitcoin"}

        default_admin_api.post(reverse("crypto-list"), data=crypto_data)
        default_user_api.post(reverse("subscription-list"), data=data)
        response = default_user_api.post(reverse("subscription-list"), data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["Info"] == "You already have such crypto in your subs"

    @pytest.mark.django_db
    def test_unsub(
        self, default_user_api, default_admin_api, default_user, crypto_data
    ):
        data = {"crypto": "Bitcoin"}
        urls = [reverse("crypto-list"), reverse("subscription-list")]

        default_admin_api.post(urls[0], data=crypto_data)
        default_user_api.post(urls[1], data=data)
        urls.append(
            reverse(
                "subscription-detail", args=(Subscription.objects.all().first().pk,)
            )
        )
        response = default_user_api.delete(urls[2])

        assert response.status_code == 204
        assert Subscription.objects.filter(user=default_user).exists() is False

    @pytest.fixture
    def create_admin_crypto(self, default_admin_api):
        def _create_admin_crypto(name, code):
            response = default_admin_api.post(
                reverse("crypto-list"), data={"name": name, "code": code}
            )
            return response.json()

        return _create_admin_crypto

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "api, user_data, data, url, expected_len",
        [
            (
                "default_api",
                {
                    "username": "test2",
                    "email": "test2@example.com",
                    "password": "test2",
                },
                [{"crypto": "Bitcoin"}],
                "subscription-list",
                1,
            ),
            (
                "default_user_api",
                {
                    "username": "test2",
                    "email": "test2@example.com",
                    "password": "test2",
                },
                [{"crypto": "Ethereum"}],
                "subscription-list",
                0,
            ),
        ],
    )
    def test_valid_list_len(
        self, api, user_data, data, url, expected_len, create_admin_crypto, request
    ):
        user = G("users.User", **user_data)
        api_client = request.getfixturevalue(api)

        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {user.token}")

        admin_crypto_data = create_admin_crypto("Bitcoin", "BTC")

        assert admin_crypto_data.get("name")
        assert admin_crypto_data.get("code")

        for item_data in data:
            api_client.post(reverse(url), data=item_data)

        response = api_client.get(reverse(url))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == expected_len

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

        assert response.status_code == status.HTTP_200_OK
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

        assert response.status_code == status.HTTP_201_CREATED
        assert (
            response.data["amount"]
            == response.data["total_price"] / default_crypto.exchange_rate
        )


class TestWalletViews:
    @pytest.mark.django_db
    def test_wallet_list(self, default_user_api):
        url = reverse("wallet-list")
        response = default_user_api.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    @pytest.mark.django_db
    def test_invalid_wallet_list(self, default_api):
        url = reverse("wallet-list")
        response = default_api.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            response.data["detail"] == "Authentication credentials were not provided."
        )


class TestHistoryViews:
    @pytest.mark.django_db
    def test_history_list(self, default_user_api):
        url = reverse("history-list")
        response = default_user_api.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    @pytest.mark.django_db
    def test_invalid_history_list(self, default_api):
        url = reverse("history-list")
        response = default_api.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            response.data["detail"] == "Authentication credentials were not provided."
        )
