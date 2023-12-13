# Generated by Django 4.2.7 on 2023-12-07 17:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stocks", "0005_order_desired_exchange_rate"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="execution_method",
            field=models.CharField(
                choices=[("AMOUNT", "By Amount"), ("PRICE", "By Price")],
                default="PRICE",
                max_length=6,
            ),
        ),
    ]