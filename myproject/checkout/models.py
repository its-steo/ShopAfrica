from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

DELIVERY_CHOICES = [
    ('standard', 'Standard (3-5 Days)'),
    ('express', 'Express (1-2 Days)'),
    ('Cod', 'Cash on delivery (Today)'),
]

PAYMENT_METHODS = [
    ('cod', 'Cash on Delivery'),
    ('card', 'Credit/Debit Card'),
    ('mpesa', 'M-PESA'),
    ('paypal', 'PayPal'),
    ('bank_transfer', 'Bank Transfer'),
    ('crypto', 'Crypto'),
]

ORDER_STATUS = [
    ('pending', 'Pending'),
    ('processing', 'Processing'),
    ('shipping', 'Shipping'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_CHOICES)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    coupon_code = models.CharField(max_length=50, blank=True, null=True)
    discount_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_delivery = models.DateField()
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    timestamp = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"

    def save(self, *args, **kwargs):
        is_update = self.pk is not None
        old_status = None

        if is_update:
            try:
                old_status = Order.objects.get(pk=self.pk).order_status
            except Order.DoesNotExist:
                pass

        super().save(*args, **kwargs)

        # Email notifications on status changes
        if is_update and old_status != self.order_status:
            if self.order_status == 'shipping':
                self.send_shipping_email()
            elif self.order_status == 'delivered':
                self.send_delivered_email()

    def send_shipping_email(self):
        context = {
            'full_name': self.full_name,
            'order_id': self.pk,
            'tracking_url': f"https://yourdomain.com/checkout/track-order/{self.pk}/",
            'year': timezone.now().year
        }

        subject = f"🚚 Your Order #{self.pk} is On the Way!"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient = [self.email]

        html_content = render_to_string('checkout/shipping_email.html', context)
        text_content = f"Hi {self.full_name}, your order #{self.pk} is now shipping. Track it here: {context['tracking_url']}"

        email = EmailMultiAlternatives(subject, text_content, from_email, recipient)
        email.attach_alternative(html_content, "text/html")
        email.send()

    def send_delivered_email(self):
        context = {
            'full_name': self.full_name,
            'order_id': self.pk,
            'year': timezone.now().year
        }

        subject = f"📦 Order #{self.pk} Delivered Successfully"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient = [self.email]

        html_content = render_to_string('checkout/delivered_email.html', context)
        text_content = f"Hi {self.full_name}, your order #{self.pk} has been successfully delivered. We hope you enjoy your purchase!"

        email = EmailMultiAlternatives(subject, text_content, from_email, recipient)
        email.attach_alternative(html_content, "text/html")
        email.send()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    price_at_time = models.DecimalField(max_digits=8, decimal_places=2)

    def get_total(self):
        return self.quantity * self.price_at_time


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('mpesa', 'M-PESA'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('cod', 'Cash on Delivery'),
        ('crypto', 'Crypto'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    screenshot = models.ImageField(upload_to='payments/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order.id} - {self.method.upper()}"
