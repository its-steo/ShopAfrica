from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Available stock quantity"
    )
    coupon_code = models.CharField(max_length=50, blank=True, null=True)
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(99.99)],
        help_text="Discount percentage (0 to less than 100%)"
    )
    description = models.TextField()
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    image = models.ImageField(upload_to='product_images')
    manufacturer = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(default=0)
    review_count = models.PositiveIntegerField(default=0)

    def get_discounted_price(self, coupon_code=None):
        if coupon_code and self.coupon_code == coupon_code:
            discount_percent = min(float(self.discount_percentage or 0), 99)
            return self.price * (Decimal('1.0') - Decimal(discount_percent) / Decimal('100'))
        return self.price

    def clean(self):
        if self.discount_percentage is not None:
            if not (0 <= self.discount_percentage < 100):
                raise ValidationError("Discount percentage must be between 0 and less than 100.")

    def save(self, *args, **kwargs):
        self.clean()  # Validation
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(price__gte=0),
                name='price_non_negative'
            ),
            models.CheckConstraint(
                check=models.Q(quantity__gte=0),
                name='quantity_non_negative'
            ),
           # models.CheckConstraint(
           #     check=models.Q(discount_percentage__gte=0, discount_percentage__lt=100),
           #     name='discount_percentage_valid_range'
            #),
        ]



class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variety_images')
    image = models.ImageField(upload_to='product_varieties/')
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.product.name}"


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email