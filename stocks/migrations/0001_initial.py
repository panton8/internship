# Generated by Django 4.2.8 on 2023-12-26 08:45

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Crypto",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(unique=True)),
                ("code", models.CharField(unique=True)),
                ("capacity", models.FloatField(blank=True, null=True)),
                ("exchange_rate", models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="History",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField()),
                ("crypto_name", models.CharField()),
                ("total_price", models.FloatField()),
                ("amount", models.FloatField()),
                ("order_type", models.CharField(max_length=8)),
                ("execution_method", models.CharField(max_length=6)),
                ("exchange_rate", models.FloatField()),
                ("date", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "order_type",
                    models.CharField(
                        choices=[("PURCHASE", "Purchase"), ("SALE", "Sale")],
                        max_length=8,
                    ),
                ),
                ("total_price", models.FloatField(blank=True, null=True)),
                ("amount", models.FloatField(blank=True, null=True)),
                (
                    "execution_method",
                    models.CharField(
                        choices=[("AMOUNT", "By Amount"), ("PRICE", "By Price")],
                        default="PRICE",
                        max_length=6,
                    ),
                ),
                ("is_auto", models.BooleanField(default=False)),
                ("desired_exchange_rate", models.FloatField(blank=True, null=True)),
                (
                    "crypto",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="stocks.crypto",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Wallet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "amount",
                    models.FloatField(
                        validators=[django.core.validators.MinValueValidator(0.0)]
                    ),
                ),
                (
                    "crypto",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="stocks.crypto"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "crypto")},
            },
        ),
        migrations.CreateModel(
            name="Subscription",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "crypto",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="stocks.crypto"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "crypto")},
            },
        ),
    ]
