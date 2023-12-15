from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Crypto(models.Model):
    name = models.CharField(unique=True)
    code = models.CharField(unique=True)
    capacity = models.FloatField(blank=True, null=True)
    exchange_rate = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    class OrderType(models.TextChoices):
        PURCHASE = "PURCHASE", "Purchase"
        SALE = "SALE", "Sale"

    class ExecutionMethod(models.TextChoices):
        BY_AMOUNT = "AMOUNT", "By Amount"
        BY_PRICE = "PRICE", "By Price"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto = models.ForeignKey(Crypto, on_delete=models.SET_NULL, null=True)
    order_type = models.CharField(max_length=8, choices=OrderType.choices)
    total_price = models.FloatField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    execution_method = models.CharField(
        max_length=6, choices=ExecutionMethod.choices, default="PRICE"
    )
    is_auto = models.BooleanField(default=False)
    desired_exchange_rate = models.FloatField(blank=True, null=True)

    def fill_amount_or_price(self):
        if self.execution_method == self.ExecutionMethod.BY_AMOUNT:
            self.total_price = self.crypto.exchange_rate * self.amount
        else:
            self.amount = self.total_price / self.crypto.exchange_rate


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "crypto")


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)
    amount = models.FloatField(validators=[MinValueValidator(0.0)])

    class Meta:
        unique_together = ("user", "crypto")


class History(models.Model):
    username = models.CharField(blank=False)
    crypto_name = models.CharField(blank=False)
    total_price = models.FloatField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
