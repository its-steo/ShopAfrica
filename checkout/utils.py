# checkout/utils.py
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_order_email(order, status_template):
    subject = f"Order #{order.id} - {order.order_status.capitalize()}"
    html_message = render_to_string(f'emails/{status_template}.html', {'order': order})
    send_mail(
        subject,
        '',
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
        html_message=html_message,
    )

