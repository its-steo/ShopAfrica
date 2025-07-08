from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=32, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} for {'user ' + str(self.user) if self.user else 'session ' + self.session_key}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    selected_image_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart {self.cart.id}"

    @property
    def unit_price(self):
        """Return the discounted price of the product."""
        # Assume coupon_code is stored in session; this is a simplification
        # In practice, you may need to access the request.session
        return float(self.product.get_discounted_price())

    @property
    def total_price(self):
        """Return the total price for this item (unit_price * quantity)."""
        return self.unit_price * self.quantity

class SavedItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variety = models.CharField(max_length=100, blank=True, null=True)  # Optional: If product has variety
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
   