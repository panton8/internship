from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Crypto(models.Model):
    name = models.CharField()
    capacity = models.FloatField()
    exchange_rate = models.FloatField()

    def __str__(self):
        return self.name


class Order(models.Model):
    class Type(models.TextChoices):
        PURCHASE = "PURCHASE", "Purchase"
        SALE = "SALE", "Sale"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto = models.ForeignKey(Crypto, on_delete=models.SET_NULL, null=True)
    order_type = models.CharField(max_length=8, choices=Type.choices)
    total_price = models.FloatField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    is_auto = models.BooleanField()

    def clean(self):
        if self.total_price is not None and self.amount is not None:
            raise ValidationError(
                "Please fill in either total_price or amount, not both."
            )
        elif self.total_price is None and self.amount is None:
            raise ValidationError("Please fill in either total_price or amount.")

        if self.order_type == Order.Type.PURCHASE:
            if self.amount is not None and self.amount > self.crypto.capacity:
                raise ValidationError("Amount exceeds crypto capacity.")
            elif self.total_price is not None and self.total_price > self.user.balance:
                raise ValidationError("Total price exceeds user balance.")


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "crypto")


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)
    amount = models.FloatField(validators=[MinValueValidator(0.0)])
