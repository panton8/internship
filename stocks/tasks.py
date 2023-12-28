import os
import smtplib
from email.message import EmailMessage

from celery import shared_task
from celery.utils.log import get_task_logger
from dotenv import load_dotenv

from crypto_project.celery import app
from stocks.models import Crypto, History, Order, Wallet
from stocks.utils import order_possible_complete_check
from users.models import User

load_dotenv()

logger = get_task_logger(__name__)


@app.task
def close_order(order, user, possible_wallet):
    if order_possible_complete_check(user, order, possible_wallet):
        if order.order_type == Order.OrderType.PURCHASE:
            if possible_wallet:
                possible_wallet.amount += order.amount
                possible_wallet.save()
            else:
                Wallet.objects.create(
                    user=order.user, crypto=order.crypto, amount=order.amount
                )
            user.balance -= order.total_price
            user.save()
        else:
            user.balance += order.total_price
            user.save()
            possible_wallet.amount -= order.amount
            possible_wallet.save()

        History.objects.create(
            username=order.user.username,
            crypto_name=order.crypto.name,
            total_price=order.total_price,
            amount=order.amount,
            order_type=order.order_type,
            execution_method=order.execution_method,
            exchange_rate=order.crypto.exchange_rate,
        )
        confirm_order(order.pk, user.pk)
        Order.objects.get(pk=order.pk).delete()


@shared_task
def complete_order(order_pk):
    order = Order.objects.get(pk=order_pk)
    user = order.user
    possible_wallet = Wallet.objects.filter(crypto=order.crypto, user=user).first()
    close_order(order, user, possible_wallet)


@shared_task
def complete_auto_order(crypto_pk=None, new_ex_rate=None):
    if crypto_pk and new_ex_rate:
        crypto = Crypto.objects.get(pk=crypto_pk)
        crypto.exchange_rate = new_ex_rate
        crypto.save()
    orders = Order.objects.all()
    for order in orders:
        order.fill_amount_or_price()
        order.save()
        if order.crypto.exchange_rate <= order.desired_exchange_rate:
            user = order.user
            possible_wallet = Wallet.objects.filter(
                crypto=order.crypto, user=user
            ).first()
            close_order(order, user, possible_wallet)


@shared_task
def confirm_order(order_pk, user_pk):
    user = User.objects.get(pk=user_pk)
    order = Order.objects.get(pk=order_pk)
    msg = EmailMessage()
    email = user.email
    msg["Subject"] = "Order Confirmation"
    msg["From"] = "Crypto Team"
    msg["To"] = email

    msg.set_content(
        f"Ordered was closed successfully  with such parameters: \n"
        f"Crypto: {order.crypto.name}\n"
        f"Total Price: {order.total_price}\n"
        f"Amount : {order.amount}\n"
        f"Order Type: {order.order_type}\n"
        f"Execution method: {order.execution_method}\n"
        f"Exchange Rate: {order.crypto.exchange_rate}\n"
    )

    with smtplib.SMTP_SSL(os.getenv("EMAIL_HOST"), os.getenv("EMAIL_PORT")) as server:
        server.login(os.getenv("EMAIL_HOST_USER"), os.getenv("EMAIL_HOST_PASSWORD"))
        server.send_message(msg)
